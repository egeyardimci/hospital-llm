# -*- coding: utf-8 -*-
"""
SGK NER + Relation Extraction with Neo4j Integration

- Flexible entity types (can invent new ones)
- Focus on meaningful coverage relations + conditions
- Better relation extraction prompts
- Neo4j loader that serializes dict attributes safely
"""

import os
import json
import re
import time
import hashlib
import logging
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any, Optional, Set
from collections import defaultdict

from dotenv import load_dotenv
from groq import Groq
from neo4j import GraphDatabase

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
load_dotenv()

# ============================================================================
# EXAMPLE ENTITIES (for guidance only - not enforced)
# ============================================================================

EXAMPLE_ENTITIES = {
    "Institution": ["SGK", "Sağlık Bakanlığı", "özel hastane", "kamu hastanesi"],
    "MedicalProcedure": ["gastroskopi", "kolonoskopi", "anjiyografi", "ameliyat"],
    "Medicine": ["ilaç", "aşı", "protez", "tıbbi malzeme"],
    "Document": ["sevk belgesi", "rapor", "reçete", "T.C. Kimlik Numarası"],
    "Regulation": ["5510 sayılı Kanun", "Tebliğ", "Genelge", "Yönetmelik"],
    "HealthCondition": ["acil hal", "kronik hastalık", "kanser", "diyabet"],
    "Professional": ["hekim", "uzman doktor", "diş hekimi", "sigortalı"],
    "FinancialTerm": ["ödeme", "katkı payı", "fatura", "tedavi bedeli"],
    "TimeConstraint": ["24 saat", "3 ay içinde", "yıllık", "ikinci ve üçüncü basamak"],
    "System": ["MEDULA", "e-Nabız", "provizyon sistemi"],
}

# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Entity:
    text: str
    type: str
    subtype: Optional[str] = None
    normalized_form: Optional[str] = None
    aliases: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)
    context: str = ""

    def __hash__(self) -> int:
        return hash((self.text.lower().strip(), self.type))

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @property
    def unique_id(self) -> str:
        content = f"{self.type}:{self.text.lower().strip()}"
        return hashlib.md5(content.encode("utf-8")).hexdigest()[:16]


@dataclass
class Relation:
    subject: str
    subject_type: str
    predicate: str
    object: str
    object_type: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    conditions: List[str] = field(default_factory=list)
    exceptions: List[str] = field(default_factory=list)
    temporal: Optional[str] = None
    context: str = ""

    def __hash__(self) -> int:
        return hash((self.subject.lower().strip(), self.predicate, self.object.lower().strip()))

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @property
    def unique_id(self) -> str:
        content = f"{self.subject}:{self.predicate}:{self.object}"
        return hashlib.md5(content.encode("utf-8")).hexdigest()[:16]


# ============================================================================
# PROMPT BUILDER
# ============================================================================

class PromptBuilder:
    """Prompts for NER and relation extraction, tuned for SGK coverage logic."""

    @staticmethod
    def build_entity_extraction_prompt(text: str) -> str:
        # Build example entities string
        examples = []
        for etype, items in list(EXAMPLE_ENTITIES.items())[:6]:  # Show first 6 types
            examples.append(f"  - {etype}: {', '.join(items[:3])}")
        example_str = "\n".join(examples)

        json_template = '''{
  "entities": [
    {
      "text": "exact phrase from text",
      "type": "descriptive type label",
      "subtype": "more specific classification or null",
      "normalized_form": "canonical Turkish form or null",
      "aliases": ["alternative names, abbreviations"],
      "attributes": {"key": "value pairs about the entity"},
      "context": "short excerpt around the entity"
    }
  ]
}'''

        prompt = f'''You are extracting entities from Turkish SGK (social security) healthcare regulations.

EXAMPLE ENTITY TYPES (you can use these OR invent your own descriptive labels):
{example_str}
  ... and any other types you find relevant

GUIDELINES:
- Extract medically/administratively meaningful phrases (institutions, procedures, medicines, documents, conditions, systems, financial terms, time limits)
- Use descriptive type labels that make sense (you can invent new types like "CoverageRule", "Requirement", "Exception", etc.)
- Prefer full phrases over partial words (e.g. "sözleşmeli özel sağlık kuruluşları" not just "kuruluşları")
- Extract 5-15 entities per chunk if the text is dense with information
- If you find no relevant entities, return: {{"entities": []}}

For each entity:
- 'text': exact substring from the text (preserve Turkish characters)
- 'type': descriptive label (use examples above or create your own)
- 'subtype': optional classification (e.g. 'emergency', 'diagnostic', 'referral') or null
- 'normalized_form': canonical/base form if possible, otherwise null
- 'aliases': alternative phrases (e.g. 'Kurum' for SGK)
- 'attributes': simple key-value pairs (role, sector, urgency, etc.)
- 'context': 5-15 words of surrounding text

TEXT TO ANALYZE:
{text[:2500]}

OUTPUT (JSON only):
{json_template}
'''
        return prompt

    @staticmethod
    def build_relation_extraction_prompt(text: str, entities: List[Entity]) -> str:
        # Format entity list
        entity_list = "\n".join([f"  - {e.text} ({e.type})" for e in entities[:40]])

        json_template = '''{
  "relations": [
    {
      "subject": "entity text from the list above",
      "subject_type": "entity type",
      "predicate": "relationship type (see examples below)",
      "object": "entity text from the list above",
      "object_type": "entity type",
      "attributes": {"key": "value"},
      "conditions": ["conditions from the text"],
      "exceptions": ["exceptions from the text"],
      "temporal": "time constraint or null",
      "context": "excerpt justifying this relation"
    }
  ]
}'''

        prompt = f'''You are extracting relationships between entities in Turkish SGK healthcare regulations.

ENTITIES AVAILABLE TO CONNECT:
{entity_list}

COMMON RELATIONSHIP TYPES (use these or invent descriptive ones):
- COVERS: An institution/regulation covers/pays for a procedure, medicine, or cost
- REQUIRES: Something requires a prerequisite (document, condition, approval, etc.)
- APPLIES_TO: A rule/policy applies to specific entities or situations
- EXCLUDES: Something is explicitly excluded from coverage or rules
- PERFORMED_AT: A procedure is performed at an institution
- ADMINISTERED_BY: A system/institution manages something
- APPROVED_BY: Something must be approved by an actor
- REQUIRES_DOCUMENTATION: Documentation needed for a process
- MUST_BE_SUBMITTED_WITHIN: Time limit for submission
- RECORDED_IN: Information stored in a system (e.g., MEDULA)
- TRIGGERS: A condition triggers a process
- EXEMPT_FROM: Exemption from requirements/payments
- CREATES: An actor creates/issues something

IMPORTANT FOR COVERS RELATIONS:
- When extracting COVERS relations, capture conditions like:
  • "acil hallerde" (in emergencies)
  • "ikinci ve üçüncü basamak sağlık tesislerinde" (in secondary/tertiary facilities)
  • "sözleşmeli sağlık hizmeti sunucularında" (at contracted providers)
  • Time limits: "24 saat içinde", "3 ay içinde", "yıllık"
- Put these phrases in the 'conditions' array EXACTLY as they appear in text

GUIDELINES:
- Extract 3-10 relations per chunk if the text contains rules/policies
- Only create relations clearly stated in the text
- For COVERS: subject is usually Institution/Regulation, object is usually Procedure/Medicine/Cost
- Include all relevant conditions and exceptions
- If no clear relations exist, return: {{"relations": []}}

TEXT TO ANALYZE:
{text[:2500]}

OUTPUT (JSON only):
{json_template}
'''
        return prompt


# ============================================================================
# EXTRACTOR
# ============================================================================

class EnhancedSGKExtractor:
    """End-to-end SGK NER + relation extraction."""

    def __init__(self) -> None:
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.entity_cache: Dict[str, Entity] = {}
        self.relation_cache: Set[Relation] = set()
        self.prompt_builder = PromptBuilder()

    # ---------- helpers ----------

    @staticmethod
    def _clean_json_text(raw: str) -> str:
        """Strip ``` fences and keep only the JSON-looking part."""
        text = raw.strip()
        text = re.sub(r"```json\s*|```", "", text, flags=re.IGNORECASE)
        if "{" in text and "}" in text:
            start = text.find("{")
            end = text.rfind("}") + 1
            text = text[start:end]
        return text.strip()

    # ---------- entity extraction ----------

    def extract_entities(self, text: str, chunk_id: int) -> List[Entity]:
        prompt = self.prompt_builder.build_entity_extraction_prompt(text)

        for attempt in range(3):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    max_tokens=2500,
                )
                content = response.choices[0].message.content or ""
                cleaned = self._clean_json_text(content)

                try:
                    data = json.loads(cleaned)
                except json.JSONDecodeError as exc:
                    logger.error(
                        "Chunk %s entity JSON error (attempt %s): %s",
                        chunk_id,
                        attempt + 1,
                        str(exc)[:120],
                    )
                    if attempt == 2:
                        return []
                    time.sleep(1.0)
                    continue

                entities: List[Entity] = []
                for e in data.get("entities", []):
                    if not e.get("text") or not e.get("type"):
                        continue
                    entity = Entity(
                        text=e["text"].strip(),
                        type=e["type"],
                        subtype=e.get("subtype"),
                        normalized_form=e.get("normalized_form"),
                        aliases=e.get("aliases", []) or [],
                        attributes=e.get("attributes", {}) or {},
                        context=e.get("context", "")[:200],
                    )
                    entities.append(entity)

                    key = f"{entity.type}:{entity.text.lower().strip()}"
                    if key not in self.entity_cache:
                        self.entity_cache[key] = entity

                logger.info("Chunk %s: extracted %s entities", chunk_id, len(entities))
                time.sleep(0.3)
                return entities

            except Exception as exc:  # noqa: BLE001
                logger.error(
                    "Chunk %s entity request error (attempt %s): %s",
                    chunk_id,
                    attempt + 1,
                    str(exc)[:120],
                )
                if attempt == 2:
                    return []
                time.sleep(1.0)

        return []

    # ---------- relation extraction ----------

    def extract_relations(self, text: str, entities: List[Entity], chunk_id: int) -> List[Relation]:
        if len(entities) < 2:
            logger.info("Chunk %s: skipping relations (only %s entities)", chunk_id, len(entities))
            return []

        prompt = self.prompt_builder.build_relation_extraction_prompt(text, entities)
        
        # Create lookup maps for entities (case-insensitive)
        entity_map = {e.text.lower().strip(): e for e in entities}

        for attempt in range(3):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    max_tokens=3000,
                )
                content = response.choices[0].message.content or ""
                cleaned = self._clean_json_text(content)

                try:
                    data = json.loads(cleaned)
                except json.JSONDecodeError as exc:
                    logger.error(
                        "Chunk %s relation JSON error (attempt %s): %s",
                        chunk_id,
                        attempt + 1,
                        str(exc)[:120],
                    )
                    if attempt == 2:
                        return []
                    time.sleep(1.0)
                    continue

                relations: List[Relation] = []
                for r in data.get("relations", []):
                    if not r.get("subject") or not r.get("object") or not r.get("predicate"):
                        continue

                    subj_text = r["subject"].strip()
                    obj_text = r["object"].strip()

                    # Try to match entities (case-insensitive)
                    subj_ent = entity_map.get(subj_text.lower().strip())
                    obj_ent = entity_map.get(obj_text.lower().strip())
                    
                    # Use provided types or fall back to entity types
                    subj_type = r.get("subject_type") or (subj_ent.type if subj_ent else "Unknown")
                    obj_type = r.get("object_type") or (obj_ent.type if obj_ent else "Unknown")

                    # Basic validation: subject and object should be different
                    if subj_text.lower().strip() == obj_text.lower().strip():
                        continue

                    relation = Relation(
                        subject=subj_text,
                        subject_type=subj_type,
                        predicate=r["predicate"],
                        object=obj_text,
                        object_type=obj_type,
                        attributes=r.get("attributes", {}) or {},
                        conditions=(r.get("conditions", []) or [])[:8],
                        exceptions=(r.get("exceptions", []) or [])[:8],
                        temporal=r.get("temporal"),
                        context=r.get("context", "")[:250],
                    )
                    relations.append(relation)
                    self.relation_cache.add(relation)

                logger.info("Chunk %s: extracted %s relations", chunk_id, len(relations))
                time.sleep(0.3)
                return relations

            except Exception as exc:  # noqa: BLE001
                logger.error(
                    "Chunk %s relation request error (attempt %s): %s",
                    chunk_id,
                    attempt + 1,
                    str(exc)[:120],
                )
                if attempt == 2:
                    return []
                time.sleep(1.0)

        return []

    # ---------- chunking / orchestration ----------

    def chunk_text(self, text: str, chunk_size: int = 2500) -> List[Dict[str, Any]]:
        """Chunk by characters, nudging to sentence boundaries."""
        chunks: List[Dict[str, Any]] = []
        start = 0
        idx = 0
        n = len(text)
        overlap = 400

        logger.info("Chunking %s characters...", f"{n:,}")

        while start < n:
            end = min(start + chunk_size, n)
            if end < n and end - start > 1200:
                window = text[end - 200 : end]
                for punct in [". ", ".\n", "! ", "? "]:
                    pos = window.rfind(punct)
                    if pos != -1:
                        end = end - 200 + pos + len(punct)
                        break

            chunks.append({"id": idx, "text": text[start:end], "start": start, "end": end})
            idx += 1
            next_start = end - overlap
            if next_start <= start:
                next_start = end
            start = next_start

        logger.info("Created %s chunks", len(chunks))
        return chunks

    def process(self, text: str, max_chunks: Optional[int] = None) -> Dict[str, Any]:
        logger.info("=" * 70)
        logger.info("SGK NER + RELATION EXTRACTION - START")
        logger.info("=" * 70)

        chunks = self.chunk_text(text)
        if max_chunks is not None:
            chunks = chunks[:max_chunks]
            logger.info("Processing only first %s chunks (test mode)", max_chunks)

        all_entities: List[Entity] = []
        all_relations: List[Relation] = []
        total = len(chunks)
        t0 = time.time()

        for i, chunk in enumerate(chunks, start=1):
            cid = chunk["id"]
            elapsed = time.time() - t0
            avg = elapsed / i if i > 0 else 0
            eta = avg * (total - i)

            logger.info("\n[%s/%s] Chunk %s | ETA ~ %.1f min", i, total, cid, eta / 60.0)

            entities = self.extract_entities(chunk["text"], cid)
            all_entities.extend(entities)
            logger.info("  + %s entities (cumulative: %s)", len(entities), len(all_entities))

            if len(entities) >= 2:
                relations = self.extract_relations(chunk["text"], entities, cid)
                all_relations.extend(relations)
                logger.info("  + %s relations (cumulative: %s)", len(relations), len(all_relations))
            else:
                logger.info("  + 0 relations (not enough entities)")

        # Deduplicate
        unique_entities = list({hash(e): e for e in all_entities}.values())
        unique_relations = list({hash(r): r for r in all_relations}.values())

        # Group by type
        entities_by_type: Dict[str, List[Entity]] = defaultdict(list)
        for e in unique_entities:
            entities_by_type[e.type].append(e)

        relations_by_predicate: Dict[str, List[Relation]] = defaultdict(list)
        for r in unique_relations:
            relations_by_predicate[r.predicate].append(r)

        minutes = (time.time() - t0) / 60.0

        result: Dict[str, Any] = {
            "entities": [e.to_dict() for e in unique_entities],
            "relations": [r.to_dict() for r in unique_relations],
            "entities_by_type": {
                k: [e.to_dict() for e in v] for k, v in entities_by_type.items()
            },
            "relations_by_predicate": {
                k: [r.to_dict() for r in v] for k, v in relations_by_predicate.items()
            },
            "statistics": {
                "total_entities": len(unique_entities),
                "total_relations": len(unique_relations),
                "entity_types": len(entities_by_type),
                "relation_types": len(relations_by_predicate),
                "chunks_processed": len(chunks),
                "processing_time_minutes": minutes,
            },
        }

        logger.info("\n" + "=" * 70)
        logger.info(
            "DONE: %s entities, %s relations in %.1f minutes",
            len(unique_entities),
            len(unique_relations),
            minutes,
        )
        logger.info("=" * 70)

        return result

    def save(self, results: Dict[str, Any], filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        logger.info("Saved results to %s", filename)

    def print_summary(self, results: Dict[str, Any]) -> None:
        stats = results["statistics"]
        print("\n" + "=" * 70)
        print("  EXTRACTION SUMMARY")
        print("=" * 70)
        print(f"Total entities:   {stats['total_entities']}")
        print(f"Total relations:  {stats['total_relations']}")
        print(f"Processing time:  {stats['processing_time_minutes']:.1f} minutes")
        print(f"Entity types:     {stats['entity_types']}")
        print(f"Relation types:   {stats['relation_types']}")

        print("\nEntity counts by type:")
        for etype, items in sorted(
            results["entities_by_type"].items(), key=lambda x: -len(x[1])
        ):
            print(f"  - {etype}: {len(items)}")

        print("\nRelation counts by predicate:")
        for pred, items in sorted(
            results["relations_by_predicate"].items(), key=lambda x: -len(x[1])
        ):
            print(f"  - {pred}: {len(items)}")

        print("\nSample entities:")
        for e in results["entities"][:10]:
            alias_part = f" (aliases: {', '.join(e.get('aliases', [])[:2])})" if e.get("aliases") else ""
            print(f"  • {e['text']} [{e['type']}]{alias_part}")

        print("\nSample relations (with conditions):")
        for r in results["relations"][:15]:
            cond = f" | CONDITIONS: {', '.join(r['conditions'][:2])}" if r.get("conditions") else ""
            exc = f" | EXCEPT: {r['exceptions'][0]}" if r.get("exceptions") else ""
            print(f"  • {r['subject']} --[{r['predicate']}]--> {r['object']}{cond}{exc}")


# ============================================================================
# NEO4J LOADER (with attributes_json)
# ============================================================================

class Neo4jLoader:
    def __init__(self) -> None:
        uri_env = os.getenv("NEO4J_URI", "")
        uri_options = [
            uri_env,
            uri_env.replace("neo4j+ssc://", "neo4j+s://") if uri_env else "",
            uri_env.replace("neo4j+ssc://", "neo4j://") if uri_env else "",
        ]

        self.driver = None
        for uri in uri_options:
            if not uri:
                continue
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
            except Exception as exc:  # noqa: BLE001
                logger.warning("Failed to connect to %s: %s", uri, str(exc)[:100])
                if self.driver:
                    self.driver.close()
                    self.driver = None

        if not self.driver:
            logger.error("Neo4j connection could not be established")

    @staticmethod
    def _sanitize_entity_props(e: Dict[str, Any]) -> Dict[str, Any]:
        """Convert entity dict to Neo4j-safe properties."""
        props = dict(e)
        attrs = props.pop("attributes", None)
        if attrs is not None:
            props["attributes_json"] = json.dumps(attrs, ensure_ascii=False)
        return props

    @staticmethod
    def _sanitize_relation_props(r: Dict[str, Any]) -> Dict[str, Any]:
        """Convert relation dict to Neo4j-safe properties."""
        props = dict(r)
        attrs = props.pop("attributes", None)
        if attrs is not None:
            props["attributes_json"] = json.dumps(attrs, ensure_ascii=False)
        return props

    def load_data(self, results: Dict[str, Any], clean_first: bool = True) -> None:
        if not self.driver:
            logger.error("No Neo4j driver available")
            return

        with self.driver.session(
            database=os.getenv("NEO4J_DATABASE", "neo4j")
        ) as session:
            # Clean up previous graph if requested
            if clean_first:
                logger.info("Cleaning up previous graph data...")
                try:
                    # Delete all relationships first
                    result = session.run("MATCH ()-[r]->() DELETE r")
                    logger.info("Deleted all relationships")
                    
                    # Then delete all nodes
                    result = session.run("MATCH (n) DELETE n")
                    logger.info("Deleted all nodes")
                    
                    # Drop all indexes
                    logger.info("Dropping existing indexes...")
                    indexes_result = session.run("SHOW INDEXES")
                    for record in indexes_result:
                        index_name = record.get("name")
                        if index_name:
                            try:
                                session.run(f"DROP INDEX {index_name} IF EXISTS")
                                logger.info(f"Dropped index: {index_name}")
                            except Exception as e:
                                logger.warning(f"Could not drop index {index_name}: {e}")
                    
                    logger.info("Graph cleanup completed successfully")
                except Exception as exc:
                    logger.error(f"Error during graph cleanup: {exc}")
                    raise
            
            logger.info("Creating indexes (if not exist)...")
            for entity_type in results["entities_by_type"].keys():
                cypher = f"CREATE INDEX IF NOT EXISTS FOR (n:{entity_type}) ON (n.id)"
                session.run(cypher)

            logger.info("Loading %s entities into Neo4j...", len(results["entities"]))
            for e in results["entities"]:
                safe_props = self._sanitize_entity_props(e)
                node_id = e["text"].lower().strip() + "_" + e["type"]
                session.run(
                    """
                    MERGE (ent:Entity {id: $id})
                    SET ent += $props
                    WITH ent
                    CALL apoc.create.addLabels(ent, [$type]) YIELD node
                    RETURN node
                    """,
                    id=node_id,
                    type=e["type"],
                    props=safe_props,
                )

            logger.info("Loading %s relations into Neo4j...", len(results["relations"]))
            for r in results["relations"]:
                safe_props = self._sanitize_relation_props(r)
                session.run(
                    """
                    MATCH (s:Entity {text: $subject})
                    MATCH (o:Entity {text: $object})
                    CALL apoc.create.relationship(s, $predicate, $props, o) YIELD rel
                    RETURN rel
                    """,
                    subject=r["subject"],
                    object=r["object"],
                    predicate=r["predicate"],
                    props=safe_props,
                )

        logger.info("Neo4j load finished")

    def close(self) -> None:
        if self.driver:
            self.driver.close()


# ============================================================================
# MAIN
# ============================================================================

def main() -> None:
    try:
        with open("sgk_document.txt", "r", encoding="utf-8") as f:
            text = f.read()
        logger.info("Loaded sgk_document.txt (%s characters)", f"{len(text):,}")
    except FileNotFoundError:
        logger.error("File 'sgk_document.txt' not found")
        return

    TEST_MODE = False
    MAX_CHUNKS = 3 if TEST_MODE else None

    print("\n" + "=" * 70)
    print("  SGK NER + RELATION EXTRACTION (FLEXIBLE TYPES)")
    print("=" * 70)
    print(f"Document size : {len(text):,} characters")
    print(f"Mode          : {'TEST' if TEST_MODE else 'FULL'} ({MAX_CHUNKS or 'all'} chunks)")
    print(f"Model         : {os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')}")
    print("=" * 70)

    extractor = EnhancedSGKExtractor()
    results = extractor.process(text, max_chunks=MAX_CHUNKS)

    extractor.print_summary(results)

    out_name = "ner_test_sgk.json" if TEST_MODE else "ner_full_sgk.json"
    extractor.save(results, out_name)

    if os.getenv("NEO4J_URI"):
        print("\n" + "=" * 70)
        ans = input("Load results into Neo4j? (y/n): ").strip().lower()
        if ans == "y":
            clean = input("Clean previous graph data first? (y/n, default=y): ").strip().lower()
            clean_first = clean != "n"  # Default to yes unless explicitly "n"
            
            loader = Neo4jLoader()
            loader.load_data(results, clean_first=clean_first)
            loader.close()
            
            if clean_first:
                print("✓ Previous graph data cleaned and new data loaded")
            else:
                print("✓ New data added to existing graph")

    print(f"\nDone. Results saved to: {out_name}")
    if TEST_MODE:
        print("NOTE: TEST_MODE=True – set to False for full document processing.")


if __name__ == "__main__":
    main()