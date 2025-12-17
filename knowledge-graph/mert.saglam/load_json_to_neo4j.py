# -*- coding: utf-8 -*-
"""
Load ner_ensemble_sgk_llm.json into Neo4j (Aura-friendly)

- Expects JSON produced by your SGK extractor:
  {
    "entities": [...],
    "relations": [...],
    "entities_by_type": {...},
    "relations_by_predicate": {...},
    "statistics": {...}
  }

- Creates (:Entity) nodes + also adds a label equal to entity 'type' via APOC
  (fallback: still stores type as property even if APOC unavailable)

- Creates relationships with dynamic type = predicate via APOC
  (fallback: creates :RELATED with property predicate)

ENV (.env supported):
NEO4J_URI=neo4j+ssc://xxxx.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=...
NEO4J_DATABASE=neo4j
"""

import os
import json
import time
import hashlib
import logging
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("json2neo4j")

load_dotenv()


def _norm_text(s: str) -> str:
    return (s or "").strip()


def _entity_id(entity_type: str, text: str) -> str:
    """
    Stable ID. Must match how we resolve relation endpoints.
    We do not rely on Neo4j internal ids.
    """
    content = f"{_norm_text(entity_type).lower()}::{_norm_text(text).lower()}"
    return hashlib.md5(content.encode("utf-8")).hexdigest()[:16]


def _safe_json_dumps(obj: Any) -> str:
    try:
        return json.dumps(obj, ensure_ascii=False)
    except Exception:
        return json.dumps(str(obj), ensure_ascii=False)


class JsonToNeo4jLoader:
    def __init__(self) -> None:
        self.uri = os.getenv("NEO4J_URI", "").strip()
        self.user = os.getenv("NEO4J_USERNAME", "").strip()
        self.password = os.getenv("NEO4J_PASSWORD", "").strip()
        self.database = os.getenv("NEO4J_DATABASE", "neo4j").strip()

        if not (self.uri and self.user and self.password):
            raise ValueError(
                "Missing NEO4J_URI / NEO4J_USERNAME / NEO4J_PASSWORD env vars. "
                "Put them in a .env file in the same folder or set system env vars."
            )

        # Aura often uses neo4j+s://. You have neo4j+ssc://; we try a few variants.
        uri_options = [
            self.uri,
            self.uri.replace("neo4j+ssc://", "neo4j+s://"),
            self.uri.replace("neo4j+ssc://", "neo4j://"),
        ]

        self.driver = None
        last_err = None
        for u in uri_options:
            if not u:
                continue
            try:
                self.driver = GraphDatabase.driver(
                    u,
                    auth=(self.user, self.password),
                    connection_timeout=30,
                )
                with self.driver.session(database=self.database) as s:
                    s.run("RETURN 1").consume()
                self.uri = u
                logger.info("Connected to Neo4j: %s (db=%s)", self.uri, self.database)
                break
            except Exception as e:
                last_err = e
                logger.warning("Failed connecting with %s: %s", u, str(e)[:120])
                try:
                    if self.driver:
                        self.driver.close()
                except Exception:
                    pass
                self.driver = None

        if not self.driver:
            raise RuntimeError(f"Could not connect to Neo4j. Last error: {last_err}")

        self.has_apoc = self._check_apoc()

    def _check_apoc(self) -> bool:
        try:
            with self.driver.session(database=self.database) as s:
                res = s.run("RETURN apoc.version() AS v").single()
                v = res["v"] if res else None
            logger.info("APOC available: %s (version=%s)", bool(v), v)
            return bool(v)
        except Exception:
            logger.warning("APOC not available. Falling back to generic labels/relationships.")
            return False

    def close(self) -> None:
        if self.driver:
            self.driver.close()

    # ------------------------ loading helpers ------------------------

    @staticmethod
    def _sanitize_entity_props(e: Dict[str, Any]) -> Dict[str, Any]:
        props = dict(e)
        attrs = props.pop("attributes", None)
        if attrs is not None:
            props["attributes_json"] = _safe_json_dumps(attrs)

        # ensure some normalized keys exist
        props["text"] = _norm_text(props.get("text", ""))
        props["type"] = _norm_text(props.get("type", ""))
        props["subtype"] = props.get("subtype", None)
        props["normalized_form"] = props.get("normalized_form", None)
        props["context"] = (props.get("context", "") or "")[:500]

        aliases = props.get("aliases", [])
        if aliases is None:
            aliases = []
        props["aliases"] = aliases

        props["id"] = _entity_id(props["type"], props["text"])
        return props

    @staticmethod
    def _sanitize_relation_props(r: Dict[str, Any]) -> Dict[str, Any]:
        props = dict(r)
        attrs = props.pop("attributes", None)
        if attrs is not None:
            props["attributes_json"] = _safe_json_dumps(attrs)

        props["subject"] = _norm_text(props.get("subject", ""))
        props["object"] = _norm_text(props.get("object", ""))
        props["predicate"] = _norm_text(props.get("predicate", ""))

        props["subject_type"] = _norm_text(props.get("subject_type", "")) or "Unknown"
        props["object_type"] = _norm_text(props.get("object_type", "")) or "Unknown"

        # lists safe
        props["conditions"] = (props.get("conditions") or [])[:20]
        props["exceptions"] = (props.get("exceptions") or [])[:20]
        props["temporal"] = props.get("temporal", None)
        props["context"] = (props.get("context", "") or "")[:800]

        props["subject_id"] = _entity_id(props["subject_type"], props["subject"])
        props["object_id"] = _entity_id(props["object_type"], props["object"])
        props["id"] = hashlib.md5(
            f"{props['subject_id']}::{props['predicate']}::{props['object_id']}".encode("utf-8")
        ).hexdigest()[:16]

        return props

    # ------------------------ main load ------------------------

    def load_json_file(self, json_path: str, clean_first: bool = True) -> None:
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"JSON file not found: {json_path}")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        entities: List[Dict[str, Any]] = data.get("entities", []) or []
        relations: List[Dict[str, Any]] = data.get("relations", []) or []

        logger.info("Loaded JSON: %s entities, %s relations", len(entities), len(relations))

        with self.driver.session(database=self.database) as s:
            if clean_first:
                logger.info("Cleaning graph (delete all rels then nodes)...")
                s.run("MATCH ()-[r]->() DELETE r").consume()
                s.run("MATCH (n) DELETE n").consume()
                logger.info("Cleanup done.")

            logger.info("Creating indexes/constraints...")
            # Unique constraint on Entity.id
            s.run("CREATE CONSTRAINT entity_id_unique IF NOT EXISTS FOR (e:Entity) REQUIRE e.id IS UNIQUE").consume()
            s.run("CREATE INDEX entity_text IF NOT EXISTS FOR (e:Entity) ON (e.text)").consume()
            s.run("CREATE INDEX entity_type IF NOT EXISTS FOR (e:Entity) ON (e.type)").consume()
            logger.info("Indexes ready.")

            # --- Nodes ---
            logger.info("Upserting Entity nodes...")
            batch_size = 500
            for i in range(0, len(entities), batch_size):
                batch = entities[i:i + batch_size]
                safe_batch = [self._sanitize_entity_props(e) for e in batch]

                if self.has_apoc:
                    cypher = """
                    UNWIND $rows AS row
                    MERGE (e:Entity {id: row.id})
                    SET e += row
                    WITH e, row
                    CALL apoc.create.addLabels(e, [row.type]) YIELD node
                    RETURN count(node) AS c
                    """
                else:
                    # No dynamic label. We keep :Entity and property e.type
                    cypher = """
                    UNWIND $rows AS row
                    MERGE (e:Entity {id: row.id})
                    SET e += row
                    RETURN count(e) AS c
                    """

                s.run(cypher, rows=safe_batch).consume()
                logger.info("  nodes: %s/%s", min(i + batch_size, len(entities)), len(entities))

            # --- Relationships ---
            logger.info("Creating relationships...")
            for i in range(0, len(relations), batch_size):
                batch = relations[i:i + batch_size]
                safe_batch = [self._sanitize_relation_props(r) for r in batch]

                if self.has_apoc:
                    cypher = """
                    UNWIND $rows AS row
                    MATCH (s:Entity {id: row.subject_id})
                    MATCH (o:Entity {id: row.object_id})
                    CALL apoc.create.relationship(s, row.predicate, row, o) YIELD rel
                    SET rel.id = row.id
                    RETURN count(rel) AS c
                    """
                else:
                    # Fallback relationship type
                    cypher = """
                    UNWIND $rows AS row
                    MATCH (s:Entity {id: row.subject_id})
                    MATCH (o:Entity {id: row.object_id})
                    MERGE (s)-[rel:RELATED {id: row.id}]->(o)
                    SET rel += row
                    RETURN count(rel) AS c
                    """

                s.run(cypher, rows=safe_batch).consume()
                logger.info("  rels: %s/%s", min(i + batch_size, len(relations)), len(relations))

        logger.info("✅ Load finished successfully.")


def main() -> None:
    JSON_FILE = "ner_ensemble_sgk_llm.json"  # <- your specific file
    CLEAN_FIRST = True  # set False if you want to append

    loader = JsonToNeo4jLoader()
    try:
        loader.load_json_file(JSON_FILE, clean_first=CLEAN_FIRST)
    finally:
        loader.close()


if __name__ == "__main__":
    main()
