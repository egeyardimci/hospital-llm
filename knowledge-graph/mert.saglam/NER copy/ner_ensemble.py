# -*- coding: utf-8 -*-
"""
Ensemble + Neo4j loader for SGK NER & Relation Extraction

Two ensemble methods:

1) Rule-based:
   - Combine Groq/OpenAI/Anthropic outputs by canonical keys
   - Merge aliases, attributes, conditions, etc.
   - Count votes & track which providers agreed

2) LLM-based (OpenAI):
   - For each relation key, give all provider candidates to OpenAI
   - OpenAI returns the "best" merged relation or null (discard)
   - Entities are still merged rule-based

Both methods then load the ensemble into Neo4j.

USAGE:
  1) Make sure you have these JSONs (or adjust paths below):
       ner_test_sgk_groq.json
       ner_test_sgk_openai.json
       ner_test_sgk_anthropic.json

  2) Set ENSEMBLE_METHOD below ("rule" or "llm")

  3) Make sure you have Neo4j env vars set:
       NEO4J_URI
       NEO4J_USERNAME
       NEO4J_PASSWORD
       (optional) NEO4J_DATABASE

  4) For LLM-based method, also set:
       OPENAI_API_KEY
       (optional) OPENAI_ENSEMBLE_MODEL  (default: gpt-4.1-mini)

  5) Run:
       python ner_ensemble.py
"""

import json
import os
import logging
from typing import Dict, Any, List, Tuple, Optional
from collections import defaultdict

from neo4j import GraphDatabase
from dotenv import load_dotenv
from openai import OpenAI  # <-- NEW: OpenAI client for LLM ensemble

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

INPUT_FILES = {
    "groq": "ner_test_sgk_groq.json",
    "openai": "ner_test_sgk_openai.json",
    "anthropic": "ner_test_sgk_anthropic.json",
}

# "rule"  -> pure rule-based ensemble
# "llm"   -> OpenAI LLM decides & merges relations
ENSEMBLE_METHOD = os.getenv("ENSEMBLE_METHOD", "rule").lower()

# Output JSON file
OUTPUT_FILE_RULE = "ner_ensemble_sgk_rule.json"
OUTPUT_FILE_LLM = "ner_ensemble_sgk_llm.json"


# ---------------------------------------------------------------------------
# BASIC UTILS
# ---------------------------------------------------------------------------

def _canonical_entity_key(e: Dict[str, Any]) -> str:
    """
    Stable key for entity deduplication.

    Priority:
      1) normalized_form (lowercased, stripped)
      2) text (lowercased, stripped)

    Also includes type, so same text with different types stays separate.
    """
    norm = (e.get("normalized_form") or "").strip().lower()
    text = (e.get("text") or "").strip().lower()
    etype = (e.get("type") or "").strip()
    base = norm if norm else text
    return f"{base}||{etype}"


def _canonical_string(s: str) -> str:
    return (s or "").strip().lower()


def _canonical_relation_key(r: Dict[str, Any]) -> str:
    """
    Stable key for relation deduplication:
      (subject_norm, predicate_upper, object_norm)
    """
    subj = _canonical_string(r.get("subject", ""))
    obj = _canonical_string(r.get("object", ""))
    pred = (r.get("predicate") or "").strip().upper()
    return f"{subj}||{pred}||{obj}"


def _merge_dict_shallow(base: Dict[str, Any], other: Dict[str, Any]) -> Dict[str, Any]:
    """
    Shallow merge two dicts:
      - prefer keys from base if conflict
      - merge dictionaries on a key using base as truth
    """
    result = dict(base)
    for k, v in other.items():
        if k not in result:
            result[k] = v
        else:
            if isinstance(result[k], dict) and isinstance(v, dict):
                # Could recursively merge; we keep base for simplicity.
                continue
            else:
                continue
    return result


def _unique_preserve_order(items: List[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for x in items:
        if not x:
            continue
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


# ---------------------------------------------------------------------------
# LOADING PROVIDER RESULTS
# ---------------------------------------------------------------------------

def load_results() -> Dict[str, Dict[str, Any]]:
    """
    Load all provider JSON results into a dict:
        { "groq": {...}, "openai": {...}, "anthropic": {...} }
    """
    results: Dict[str, Dict[str, Any]] = {}
    for provider, path in INPUT_FILES.items():
        if not os.path.exists(path):
            logger.warning("File for provider %s not found: %s (skipping)", provider, path)
            continue
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        results[provider] = data
        logger.info(
            "Loaded %s entities, %s relations from %s (%s)",
            len(data.get("entities", [])),
            len(data.get("relations", [])),
            path,
            provider,
        )
    if not results:
        raise RuntimeError("No input files found. Check INPUT_FILES config.")
    return results


# ---------------------------------------------------------------------------
# RULE-BASED ENSEMBLE: ENTITIES
# ---------------------------------------------------------------------------

def merge_entities_rule_based(all_results: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Rule-based entity ensemble:
      - group by canonical key
      - union aliases
      - shallow merge attributes
      - collect up to 3 context snippets
      - track vote_count & providers
    """
    merged: Dict[str, Dict[str, Any]] = {}

    for provider, data in all_results.items():
        for e in data.get("entities", []):
            key = _canonical_entity_key(e)
            if not key.strip("||"):
                continue

            aliases = e.get("aliases") or []
            if not isinstance(aliases, list):
                aliases = [str(aliases)]
            context = e.get("context") or ""

            if key not in merged:
                merged[key] = {
                    "text": e.get("text"),
                    "type": e.get("type"),
                    "subtype": e.get("subtype"),
                    "normalized_form": e.get("normalized_form"),
                    "aliases": list(aliases),
                    "attributes": e.get("attributes") or {},
                    "contexts": [context] if context else [],
                    "providers": [provider],
                    "vote_count": 1,
                }
            else:
                m = merged[key]
                m["vote_count"] += 1
                m["providers"].append(provider)

                m["aliases"].extend(aliases)
                base_attrs = m.get("attributes") or {}
                other_attrs = e.get("attributes") or {}
                m["attributes"] = _merge_dict_shallow(base_attrs, other_attrs)
                if context:
                    m["contexts"].append(context)

    final_entities: List[Dict[str, Any]] = []
    for key, e in merged.items():
        e["aliases"] = _unique_preserve_order(e.get("aliases", []))
        e["providers"] = _unique_preserve_order(e.get("providers", []))
        contexts = _unique_preserve_order(e.get("contexts", []))
        e["contexts"] = contexts[:3]
        final_entities.append(e)

    final_entities.sort(
        key=lambda x: (-x.get("vote_count", 0), str(x.get("type") or ""), str(x.get("text") or ""))
    )

    logger.info("Merged entities (rule-based): %s", len(final_entities))
    return final_entities


# ---------------------------------------------------------------------------
# RULE-BASED ENSEMBLE: RELATIONS
# ---------------------------------------------------------------------------

def merge_relations_rule_based(
    all_results: Dict[str, Dict[str, Any]]
) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    """
    Rule-based relation ensemble:
      - group by canonical relation key
      - union conditions/exceptions
      - shallow merge attributes
      - collect up to 3 context snippets
      - track vote_count & providers

    Returns:
      (final_relations, merged_by_key)
    """
    merged: Dict[str, Dict[str, Any]] = {}

    for provider, data in all_results.items():
        for r in data.get("relations", []):
            subj = r.get("subject")
            obj = r.get("object")
            pred = r.get("predicate")
            if not subj or not obj or not pred:
                continue

            key = _canonical_relation_key(r)
            if not key.strip("||"):
                continue

            conditions = r.get("conditions") or []
            if not isinstance(conditions, list):
                conditions = [str(conditions)]
            exceptions = r.get("exceptions") or []
            if not isinstance(exceptions, list):
                exceptions = [str(exceptions)]
            context = r.get("context") or ""

            if key not in merged:
                merged[key] = {
                    "subject": subj,
                    "subject_type": r.get("subject_type"),
                    "predicate": pred,
                    "object": obj,
                    "object_type": r.get("object_type"),
                    "attributes": r.get("attributes") or {},
                    "conditions": list(conditions),
                    "exceptions": list(exceptions),
                    "temporal": r.get("temporal"),
                    "contexts": [context] if context else [],
                    "providers": [provider],
                    "vote_count": 1,
                }
            else:
                m = merged[key]
                m["vote_count"] += 1
                m["providers"].append(provider)

                base_attrs = m.get("attributes") or {}
                other_attrs = r.get("attributes") or {}
                m["attributes"] = _merge_dict_shallow(base_attrs, other_attrs)

                m["conditions"].extend(conditions)
                m["exceptions"].extend(exceptions)

                if not m.get("temporal") and r.get("temporal"):
                    m["temporal"] = r["temporal"]

                if context:
                    m["contexts"].append(context)

    final_relations: List[Dict[str, Any]] = []
    for key, r in merged.items():
        r["providers"] = _unique_preserve_order(r.get("providers", []))
        r["conditions"] = _unique_preserve_order(r.get("conditions", []))
        r["exceptions"] = _unique_preserve_order(r.get("exceptions", []))
        contexts = _unique_preserve_order(r.get("contexts", []))
        r["contexts"] = contexts[:3]
        final_relations.append(r)

    final_relations.sort(
        key=lambda x: (-x.get("vote_count", 0), x.get("predicate") or "", x.get("subject") or "")
    )

    logger.info("Merged relations (rule-based): %s", len(final_relations))
    return final_relations, merged


# ---------------------------------------------------------------------------
# LLM CLIENT (OPENAI) FOR LLM-BASED ENSEMBLE
# ---------------------------------------------------------------------------

class OpenAILLM:
    """Minimal OpenAI client for LLM-based relation ensemble"""

    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set for LLM-based ensemble")

        # Uses the new OpenAI Python SDK
        self.client = OpenAI(api_key=api_key)
        # Use a dedicated model for ensemble if you want; falls back to gpt-4.1-mini
        self.model = os.getenv("OPENAI_ENSEMBLE_MODEL", "gpt-4.1-mini")

    @staticmethod
    def _clean_json_text(raw: str) -> str:
        text = raw.strip()
        import re
        text = re.sub(r"```json\s*|```", "", text, flags=re.IGNORECASE)
        if "{" in text and "}" in text:
            start = text.find("{")
            end = text.rfind("}") + 1
            text = text[start:end]
        return text.strip()

    def call_json(self, prompt: str, max_tokens: int = 600) -> Optional[Dict[str, Any]]:
        """
        Call OpenAI and parse JSON output.
        Returns dict or None if parsing fails.
        """
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=max_tokens,
            )
            content = (resp.choices[0].message.content or "").strip()
            cleaned = self._clean_json_text(content)
            return json.loads(cleaned)
        except Exception as exc:
            logger.warning("LLM JSON parse error: %s", str(exc)[:200])
            return None


# ---------------------------------------------------------------------------
# LLM-BASED ENSEMBLE FOR RELATIONS
# ---------------------------------------------------------------------------

def build_relation_groups(
    all_results: Dict[str, Dict[str, Any]]
) -> Dict[str, Dict[str, Any]]:
    """
    Build relation groups per canonical key:

    {
      key: {
        "subject": ...,
        "object": ...,
        "predicate": ...,
        "candidates": [
          {"provider": "groq", "relation": {...}},
          {"provider": "openai", "relation": {...}},
          ...
        ]
      },
      ...
    }
    """
    groups: Dict[str, Dict[str, Any]] = {}
    for provider, data in all_results.items():
        for r in data.get("relations", []):
            subj = r.get("subject")
            obj = r.get("object")
            pred = r.get("predicate")
            if not subj or not obj or not pred:
                continue

            key = _canonical_relation_key(r)
            if not key.strip("||"):
                continue

            if key not in groups:
                groups[key] = {
                    "subject": subj,
                    "object": obj,
                    "predicate": pred,
                    "candidates": [],
                }
            groups[key]["candidates"].append(
                {"provider": provider, "relation": r}
            )
    return groups


def merge_relations_llm_based(
    all_results: Dict[str, Dict[str, Any]],
    rule_based_by_key: Dict[str, Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Use OpenAI to decide the final merged relation per key.

    For each canonical key, we:
      - Show LLM the subject, object, predicate and all candidates
      - LLM returns:
          {"relation": {...}} or {"relation": null}
      - If parsing fails, fall back to rule-based merged relation if available.
    """
    llm = OpenAILLM()
    groups = build_relation_groups(all_results)

    merged_relations: List[Dict[str, Any]] = []
    total = len(groups)
    logger.info("Starting LLM-based ensemble for %s relation keys", total)

    for i, (key, info) in enumerate(groups.items(), start=1):
        subject = info["subject"]
        obj = info["object"]
        predicate = info["predicate"]
        candidates = info["candidates"]

        logger.info("LLM ensemble [%s/%s] %s --%s--> %s", i, total, subject, predicate, obj)

        # Build prompt
        prompt = (
            "You are merging relation candidates extracted from a legal/healthcare regulation.\n"
            "Each candidate has the same logical key (subject, predicate, object) but may differ\n"
            "in types, conditions, exceptions, attributes, or may be spurious.\n\n"
            "Your job: decide if there is a valid relation and, if yes, produce a single merged\n"
            "relation object that best reflects the text.\n\n"
            "Subject: " + repr(subject) + "\n"
            "Object: " + repr(obj) + "\n"
            "Predicate: " + repr(predicate) + "\n\n"
            "Here are the candidates (JSON list):\n"
            + json.dumps(candidates, ensure_ascii=False, indent=2)
            + "\n\n"
              "Return ONLY JSON in this form:\n"
              "{\n"
              '  "relation": {\n'
              '    "subject": "string",\n'
              '    "subject_type": "string or null",\n'
              '    "predicate": "string",\n'
              '    "object": "string",\n'
              '    "object_type": "string or null",\n'
              '    "attributes": { "key": "value", ... },\n'
              '    "conditions": ["condition1", ...],\n'
              '    "exceptions": ["exception1", ...],\n'
              '    "temporal": "string or null",\n'
              '    "context": "short justification snippet"\n'
              "  }\n"
              "}\n"
              "If you think all candidates are unreliable and no relation should be kept, return:\n"
              '{"relation": null}\n'
              "JSON only, no extra commentary."
        )

        resp = llm.call_json(prompt)
        final_rel: Optional[Dict[str, Any]] = None

        if resp and isinstance(resp, dict):
            maybe_rel = resp.get("relation", None)
            if isinstance(maybe_rel, dict):
                final_rel = maybe_rel

        if not final_rel:
            # fallback: rule-based merged relation (if it exists)
            rb = rule_based_by_key.get(key)
            if rb:
                logger.info("  -> LLM returned null/invalid, using rule-based relation")
                merged_relations.append(rb)
            else:
                logger.info("  -> No relation kept for this key (LLM + no rule-based)")
            continue

        # Clean up + add providers/votes info from candidates
        attributes = final_rel.get("attributes") or {}
        if not isinstance(attributes, dict):
            attributes = {}

        conditions = final_rel.get("conditions") or []
        if not isinstance(conditions, list):
            conditions = [str(conditions)]

        exceptions = final_rel.get("exceptions") or []
        if not isinstance(exceptions, list):
            exceptions = [str(exceptions)]

        # compute providers + vote_count
        providers = [c["provider"] for c in candidates]
        providers = _unique_preserve_order(providers)
        vote_count = len(providers)

        merged_relations.append(
            {
                "subject": final_rel.get("subject") or subject,
                "subject_type": final_rel.get("subject_type"),
                "predicate": final_rel.get("predicate") or predicate,
                "object": final_rel.get("object") or obj,
                "object_type": final_rel.get("object_type"),
                "attributes": attributes,
                "conditions": _unique_preserve_order(conditions),
                "exceptions": _unique_preserve_order(exceptions),
                "temporal": final_rel.get("temporal"),
                "contexts": [final_rel.get("context") or ""],
                "providers": providers,
                "vote_count": vote_count,
            }
        )

    merged_relations.sort(
        key=lambda x: (-x.get("vote_count", 0), x.get("predicate") or "", x.get("subject") or "")
    )
    logger.info("Merged relations (LLM-based): %s", len(merged_relations))
    return merged_relations


# ---------------------------------------------------------------------------
# BUILD RESULT STRUCTURE (LIKE ner.py)
# ---------------------------------------------------------------------------

def build_result_structure(
    merged_entities: List[Dict[str, Any]],
    merged_relations: List[Dict[str, Any]],
) -> Dict[str, Any]:
    entities_by_type: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for e in merged_entities:
        et = e.get("type") or "Unknown"
        entities_by_type[et].append(e)

    relations_by_predicate: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for r in merged_relations:
        p = r.get("predicate") or "UNKNOWN"
        relations_by_predicate[p].append(r)

    result = {
        "entities": merged_entities,
        "relations": merged_relations,
        "entities_by_type": entities_by_type,
        "relations_by_predicate": relations_by_predicate,
        "statistics": {
            "total_entities": len(merged_entities),
            "total_relations": len(merged_relations),
            "entity_types": len(entities_by_type),
            "relation_types": len(relations_by_predicate),
        },
    }
    return result


# ---------------------------------------------------------------------------
# NEO4J LOADER FOR ENSEMBLE
# ---------------------------------------------------------------------------

class Neo4jEnsembleLoader:
    """
    Simple Neo4j loader for ensemble results.

    - Nodes: (:Entity {id, text, type, normalized_form, aliases, providers, vote_count, attributes_json, ...})
    - Edges: (s)-[:PREDICATE {conditions, exceptions, temporal, providers, vote_count, attributes_json, ...}]->(o)
    """

    def __init__(self) -> None:
        uri_env = os.getenv("NEO4J_URI", "")
        self.driver = None

        if not uri_env:
            logger.error("NEO4J_URI is not set; skipping Neo4j load")
            return

        uri_options = [
            uri_env,
            uri_env.replace("neo4j+ssc://", "neo4j+s://"),
            uri_env.replace("neo4j+ssc://", "neo4j://"),
        ]

        for uri in uri_options:
            try:
                self.driver = GraphDatabase.driver(
                    uri,
                    auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD")),
                    connection_timeout=30,
                )
                with self.driver.session(
                    database=os.getenv("NEO4J_DATABASE", "neo4j")
                ) as session:
                    session.run("RETURN 1")
                logger.info("Connected to Neo4j at %s", uri)
                break
            except Exception as exc:
                logger.warning("Failed to connect to %s: %s", uri, str(exc)[:100])
                if self.driver:
                    self.driver.close()
                    self.driver = None

        if not self.driver:
            logger.error("Neo4j connection could not be established")

    def close(self) -> None:
        if self.driver:
            self.driver.close()

    def clean_graph(self) -> None:
        if not self.driver:
            return
        with self.driver.session(
            database=os.getenv("NEO4J_DATABASE", "neo4j")
        ) as session:
            logger.info("Cleaning existing nodes and relationships...")
            session.run("MATCH ()-[r]->() DELETE r")
            session.run("MATCH (n) DELETE n")
            logger.info("Graph cleaned")

    def load(self, results: Dict[str, Any]) -> None:
        if not self.driver:
            logger.error("No Neo4j driver available, skip loading.")
            return

        with self.driver.session(
            database=os.getenv("NEO4J_DATABASE", "neo4j")
        ) as session:
            # Create index on Entity id
            session.run("CREATE INDEX IF NOT EXISTS FOR (e:Entity) ON (e.id)")

            entities = results.get("entities", [])
            relations = results.get("relations", [])

            logger.info("Loading %s entities into Neo4j...", len(entities))
            for e in entities:
                node_id = (e.get("normalized_form") or e.get("text") or "").strip().lower() + "_" + (
                    e.get("type") or "Unknown"
                )

                # serialize attributes dict to JSON string, Neo4j can't store maps directly
                attributes = e.get("attributes") or {}
                attributes_json = json.dumps(attributes, ensure_ascii=False)

                session.run(
                    """
                    MERGE (ent:Entity {id: $id})
                    SET ent.text = $text,
                        ent.type = $type,
                        ent.subtype = $subtype,
                        ent.normalized_form = $normalized_form,
                        ent.aliases = $aliases,
                        ent.providers = $providers,
                        ent.vote_count = $vote_count,
                        ent.attributes_json = $attributes_json,
                        ent.contexts = $contexts
                    """,
                    id=node_id,
                    text=e.get("text"),
                    type=e.get("type"),
                    subtype=e.get("subtype"),
                    normalized_form=e.get("normalized_form"),
                    aliases=e.get("aliases") or [],
                    providers=e.get("providers") or [],
                    vote_count=e.get("vote_count") or 1,
                    attributes_json=attributes_json,
                    contexts=e.get("contexts") or [],
                )

            logger.info("Loading %s relations into Neo4j...", len(relations))
            for r in relations:
                subj_text = r.get("subject")
                subj_type = r.get("subject_type") or "Unknown"
                obj_text = r.get("object")
                obj_type = r.get("object_type") or "Unknown"
                predicate = (r.get("predicate") or "RELATED_TO").upper()

                if not subj_text or not obj_text:
                    continue

                subj_id = subj_text.strip().lower() + "_" + subj_type
                obj_id = obj_text.strip().lower() + "_" + obj_type

                attributes = r.get("attributes") or {}
                attributes_json = json.dumps(attributes, ensure_ascii=False)

                session.run(
                    f"""
                    MATCH (s:Entity {{id: $subj_id}})
                    MATCH (o:Entity {{id: $obj_id}})
                    MERGE (s)-[rel:`{predicate}`]->(o)
                    SET rel.attributes_json = $attributes_json,
                        rel.conditions = $conditions,
                        rel.exceptions = $exceptions,
                        rel.temporal = $temporal,
                        rel.providers = $providers,
                        rel.vote_count = $vote_count,
                        rel.contexts = $contexts
                    """,
                    subj_id=subj_id,
                    obj_id=obj_id,
                    attributes_json=attributes_json,
                    conditions=r.get("conditions") or [],
                    exceptions=r.get("exceptions") or [],
                    temporal=r.get("temporal"),
                    providers=r.get("providers") or [],
                    vote_count=r.get("vote_count") or 1,
                    contexts=r.get("contexts") or [],
                )

        logger.info("Neo4j ensemble load finished")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main() -> None:
    logger.info("ENSEMBLE_METHOD = %s", ENSEMBLE_METHOD)
    all_results = load_results()

    # Entities are always merged rule-based (first step)
    merged_entities = merge_entities_rule_based(all_results)

    # Relations: either rule-based or LLM-based
    if ENSEMBLE_METHOD == "rule":
        merged_relations, _rb_by_key = merge_relations_rule_based(all_results)
        results = build_result_structure(merged_entities, merged_relations)
        out_path = OUTPUT_FILE_RULE

    elif ENSEMBLE_METHOD == "llm":
        # first get rule-based (used as fallback per key)
        _, rb_by_key = merge_relations_rule_based(all_results)
        merged_relations = merge_relations_llm_based(all_results, rb_by_key)
        results = build_result_structure(merged_entities, merged_relations)
        out_path = OUTPUT_FILE_LLM

    else:
        raise ValueError("ENSEMBLE_METHOD must be 'rule' or 'llm'")

    # Save ensemble JSON
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    logger.info("Ensemble results saved to %s", out_path)

    # Load into Neo4j
    loader = Neo4jEnsembleLoader()
    if loader.driver:
        # Optional: clean previous graph; comment out if you want to append
        loader.clean_graph()
        loader.load(results)
        loader.close()
        print(f"\n✓ Ensemble ({ENSEMBLE_METHOD}) loaded into Neo4j and saved to {out_path}")
    else:
        print(f"\nNeo4j not configured; ensemble JSON saved to {out_path} only")


if __name__ == "__main__":
    main()
