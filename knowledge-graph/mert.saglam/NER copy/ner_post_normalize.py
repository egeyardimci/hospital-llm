# -*- coding: utf-8 -*-
"""
Post-ensemble normalizer for SGK NER + Relation Extraction.

Takes an ensemble JSON (from ner_ensemble.py) and:
  - Canonicalizes & merges duplicate entities:
      * Normalizes labels (e.g. drops trailing 'birimleri', 'hizmeti', 'merkezleri')
      * Normalizes some types (e.g. GSS -> InsuranceSystem)
      * Unions aliases, attributes, providers, contexts
      * Recomputes vote_count as number of distinct providers
  - Rewrites relations to point to canonical entity text/type
  - Deduplicates relations after rewrite
  - Rebuilds entities_by_type, relations_by_predicate, statistics

USAGE:
    python ner_post_normalize.py

CONFIG:
    INPUT_FILE  = "ner_ensemble_sgk_rule.json"   # or llm
    OUTPUT_FILE = "ner_ensemble_sgk_normalized.json"
"""

import json
import logging
import os
import re
from collections import defaultdict
from typing import Any, Dict, List, Tuple

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

INPUT_FILE = os.getenv("POST_NORMALIZE_INPUT", "ner_ensemble_sgk_rule.json")
OUTPUT_FILE = os.getenv("POST_NORMALIZE_OUTPUT", "ner_ensemble_sgk_normalized.json")


# ---------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------

def _norm_space(s: str) -> str:
    """Collapse whitespace and strip."""
    return " ".join((s or "").split()).strip()


def normalize_label_for_key(text: str) -> str:
    """
    Normalize an entity label into a canonical *lowercase* key used for grouping.

    - Lowercase
    - Collapse whitespace
    - Remove some generic trailing words like:
        birimi, birimleri, hizmeti, hizmetleri, merkezi, merkezleri, birimler
    - Remove trailing commas/periods
    """
    t = _norm_space(text).lower()

    # Remove trailing punctuation
    t = re.sub(r"[.,;:]+$", "", t).strip()

    # Generic trailing words we want to drop (Turkish institution tails)
    tail_pattern = re.compile(
        r"\b(birim(leri|i)?|birimler|hizmet(leri|i)?|merkez(leri|i)?|kuruluş(ları)?|tesis(leri)?)\b$",
        re.IGNORECASE,
    )

    # Remove multiple times if needed
    while True:
        new_t = tail_pattern.sub("", t).strip()
        new_t = _norm_space(new_t)
        if new_t == t:
            break
        t = new_t

    return t


def normalize_entity_type(text: str, etype: str) -> str:
    """
    Normalize some entity types heuristically.

    Examples:
      - 'genel sağlık sigortası' -> InsuranceSystem
      - '... yararlandırılan kişiler' as HealthCondition -> BeneficiaryGroup
    """
    t = (text or "").lower()
    e = (etype or "").strip() or "Unknown"

    # GSS: Genel Sağlık Sigortası
    if "genel sağlık sigortası" in t:
        return "InsuranceSystem"

    # Beneficiary group phrasing
    if "yararlandırılan kişiler" in t or "yararlanan kişiler" in t:
        if e == "HealthCondition":
            return "BeneficiaryGroup"

    return e


def canonical_entity_key(raw_text: str, normalized_form: str, etype: str) -> Tuple[str, str]:
    """
    Build a canonical key for grouping entities:

      key_text   = normalized_label_for_key(normalized_form or raw_text)
      key_type   = normalize_entity_type(key_text, etype)

    We return (key_text_lower, key_type).
    """
    base_label = normalized_form or raw_text
    key_text = normalize_label_for_key(base_label)
    key_type = normalize_entity_type(key_text, etype)
    return key_text, key_type


def unique_preserve_order(seq):
    seen = set()
    out = []
    for x in seq:
        if not x:
            continue
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def canonical_relation_key(subject: str, predicate: str, obj: str) -> str:
    return f"{subject.strip().lower()}||{predicate.strip().upper()}||{obj.strip().lower()}"


# ---------------------------------------------------------------------------
# ENTITY NORMALIZATION & MERGE
# ---------------------------------------------------------------------------

def normalize_and_merge_entities(
    entities: List[Dict[str, Any]]
) -> Tuple[List[Dict[str, Any]], Dict[Tuple[str, str], Tuple[str, str]]]:
    """
    Takes the 'entities' list from ensemble JSON and returns:

      merged_entities: List[Dict]
          - text: canonical display label
          - normalized_form: canonical lowercase label
          - type: normalized type
          - aliases: union of all textual variants
          - attributes: shallow merged attributes
          - contexts: up to 3 distinct contexts
          - providers: union of providers from all clustered entities
          - vote_count: number of distinct providers

      redirect_map: Dict[(orig_text_lower, orig_type) -> (new_text, new_type)]
          A mapping from original (text, type) pairs to canonical (text, type),
          used later to rewrite relations.
    """
    merged_by_key: Dict[Tuple[str, str], Dict[str, Any]] = {}
    redirect: Dict[Tuple[str, str], Tuple[str, str]] = {}

    for e in entities:
        raw_text = e.get("text") or ""
        etype_original = e.get("type") or "Unknown"
        norm_form = e.get("normalized_form") or ""

        # Compute canonical key
        key_text, key_type = canonical_entity_key(raw_text, norm_form, etype_original)
        if not key_text:
            # Skip truly broken entries
            continue

        key = (key_text, key_type)

        # Pick a canonical display text:
        # prefer normalized_form if non-empty, otherwise original text,
        # otherwise key_text (already lowercase).
        canonical_display_text = e.get("normalized_form") or raw_text or key_text

        aliases = e.get("aliases") or []
        if not isinstance(aliases, list):
            aliases = [str(aliases)]

        # We will recalc providers & vote_count globally; ignore incoming vote_count
        providers = e.get("providers") or []
        if not isinstance(providers, list):
            providers = [str(providers)]

        attributes = e.get("attributes") or {}
        if not isinstance(attributes, dict):
            attributes = {}

        contexts = e.get("contexts") or []
        if isinstance(contexts, str):
            contexts = [contexts]

        if key not in merged_by_key:
            merged_by_key[key] = {
                "text": canonical_display_text,
                "type": key_type,
                "subtype": e.get("subtype"),
                # canonical lowercase form stored as normalized_form
                "normalized_form": key_text,
                "aliases": [],
                "attributes": {},
                "contexts": [],
                "providers": set(),  # temp as set
            }

        agg = merged_by_key[key]

        # Collect aliases: include raw_text if different from canonical display text
        if raw_text and raw_text != agg["text"]:
            agg["aliases"].append(raw_text)
        # incoming aliases
        agg["aliases"].extend(aliases)

        # contexts
        agg["contexts"].extend(contexts)

        # attributes (shallow merge: keep existing on conflict)
        for k_attr, v_attr in attributes.items():
            if k_attr not in agg["attributes"]:
                agg["attributes"][k_attr] = v_attr

        # providers
        for p in providers:
            agg["providers"].add(p)

        # redirect mapping for this original entity text/type
        orig_key = (raw_text.strip().lower(), etype_original)
        redirect[orig_key] = (agg["text"], agg["type"])

    # Build final list & finalize providers / vote_count / contexts / aliases
    merged_entities: List[Dict[str, Any]] = []
    for (key_text, key_type), agg in merged_by_key.items():
        # Deduplicate lists and sort contexts
        agg["aliases"] = unique_preserve_order(agg["aliases"])
        contexts = unique_preserve_order(agg["contexts"])
        agg["contexts"] = contexts[:3]

        providers_list = sorted(list(agg["providers"]))
        agg["providers"] = providers_list
        agg["vote_count"] = len(providers_list)

        merged_entities.append(agg)

    merged_entities.sort(
        key=lambda x: (-x.get("vote_count", 0), x.get("type") or "", x.get("text") or "")
    )

    logger.info("Post-normalization: %s entities -> %s canonical entities",
                len(entities), len(merged_entities))
    return merged_entities, redirect


# ---------------------------------------------------------------------------
# RELATION REWRITE & DEDUP
# ---------------------------------------------------------------------------

def rewrite_relations_to_canonical(
    relations: List[Dict[str, Any]],
    redirect: Dict[Tuple[str, str], Tuple[str, str]],
) -> List[Dict[str, Any]]:
    """
    Rewrites relations so that subject/object text + type match the canonical
    entity text/type from the redirect map.

    After rewrite, deduplicates relations based on:
        (canonical subject, predicate, canonical object)
    and merges metadata (conditions, exceptions, providers, contexts).
    """
    # First, rewrite
    rewritten: List[Dict[str, Any]] = []
    for r in relations:
        subj = r.get("subject")
        obj = r.get("object")
        pred = r.get("predicate")
        if not subj or not obj or not pred:
            continue

        stype = r.get("subject_type") or "Unknown"
        otype = r.get("object_type") or "Unknown"

        # Lookup canonical subject
        subj_key = (subj.strip().lower(), stype)
        if subj_key in redirect:
            new_subj_text, new_stype = redirect[subj_key]
        else:
            new_subj_text, new_stype = subj, stype

        # Lookup canonical object
        obj_key = (obj.strip().lower(), otype)
        if obj_key in redirect:
            new_obj_text, new_otype = redirect[obj_key]
        else:
            new_obj_text, new_otype = obj, otype

        new_r = dict(r)
        new_r["subject"] = new_subj_text
        new_r["subject_type"] = new_stype
        new_r["object"] = new_obj_text
        new_r["object_type"] = new_otype

        rewritten.append(new_r)

    logger.info("Rewrote %s relations to canonical entities", len(relations))

    # Then deduplicate + merge metadata
    merged_by_key: Dict[str, Dict[str, Any]] = {}
    for r in rewritten:
        subj = r["subject"]
        obj = r["object"]
        pred = r.get("predicate") or "RELATED_TO"

        key = canonical_relation_key(subj, pred, obj)

        conditions = r.get("conditions") or []
        if isinstance(conditions, str):
            conditions = [conditions]

        exceptions = r.get("exceptions") or []
        if isinstance(exceptions, str):
            exceptions = [exceptions]

        contexts = r.get("contexts") or []
        if isinstance(contexts, str):
            contexts = [contexts]

        providers = r.get("providers") or []
        if isinstance(providers, str):
            providers = [providers]

        attributes = r.get("attributes") or {}
        if not isinstance(attributes, dict):
            attributes = {}

        temporal = r.get("temporal")

        if key not in merged_by_key:
            merged_by_key[key] = {
                "subject": subj,
                "subject_type": r.get("subject_type") or "Unknown",
                "predicate": pred,
                "object": obj,
                "object_type": r.get("object_type") or "Unknown",
                "attributes": {},
                "conditions": [],
                "exceptions": [],
                "temporal": temporal,
                "contexts": [],
                "providers": set(),
            }

        agg = merged_by_key[key]

        # Merge attributes (shallow)
        for k_attr, v_attr in attributes.items():
            if k_attr not in agg["attributes"]:
                agg["attributes"][k_attr] = v_attr

        agg["conditions"].extend(conditions)
        agg["exceptions"].extend(exceptions)
        agg["contexts"].extend(contexts)
        for p in providers:
            agg["providers"].add(p)

        # temporal: prefer first non-empty
        if not agg["temporal"] and temporal:
            agg["temporal"] = temporal

    # Finalize
    merged_relations: List[Dict[str, Any]] = []
    for key, agg in merged_by_key.items():
        agg["conditions"] = unique_preserve_order(agg["conditions"])
        agg["exceptions"] = unique_preserve_order(agg["exceptions"])
        contexts = unique_preserve_order(agg["contexts"])
        agg["contexts"] = contexts[:3]

        providers_list = sorted(list(agg["providers"]))
        agg["providers"] = providers_list
        agg["vote_count"] = len(providers_list)

        merged_relations.append(agg)

    merged_relations.sort(
        key=lambda x: (-x.get("vote_count", 0), x.get("predicate") or "", x.get("subject") or "")
    )
    logger.info("After rewrite+dedup: %s relations -> %s canonical relations",
                len(relations), len(merged_relations))

    return merged_relations


# ---------------------------------------------------------------------------
# REBUILD BY-TYPE / BY-PREDICATE + STATS
# ---------------------------------------------------------------------------

def rebuild_index_structures(
    entities: List[Dict[str, Any]],
    relations: List[Dict[str, Any]],
) -> Dict[str, Any]:
    entities_by_type: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for e in entities:
        t = e.get("type") or "Unknown"
        entities_by_type[t].append(e)

    relations_by_predicate: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for r in relations:
        p = r.get("predicate") or "UNKNOWN"
        relations_by_predicate[p].append(r)

    result = {
        "entities": entities,
        "relations": relations,
        "entities_by_type": entities_by_type,
        "relations_by_predicate": relations_by_predicate,
        "statistics": {
            "total_entities": len(entities),
            "total_relations": len(relations),
            "entity_types": len(entities_by_type),
            "relation_types": len(relations_by_predicate),
        },
    }
    return result


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main() -> None:
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    logger.info("Loading ensemble JSON from %s", INPUT_FILE)
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    entities = data.get("entities", [])
    relations = data.get("relations", [])

    logger.info("Original: %s entities, %s relations", len(entities), len(relations))

    # 1) Normalize + merge entities
    merged_entities, redirect = normalize_and_merge_entities(entities)

    # 2) Rewrite + dedup relations
    merged_relations = rewrite_relations_to_canonical(relations, redirect)

    # 3) Rebuild by-type/predicate + stats
    normalized = rebuild_index_structures(merged_entities, merged_relations)

    # 4) Save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(normalized, f, ensure_ascii=False, indent=2)

    logger.info("Saved normalized ensemble to %s", OUTPUT_FILE)
    logger.info(
        "FINAL COUNTS: %s entities, %s relations, %s entity types, %s relation types",
        normalized["statistics"]["total_entities"],
        normalized["statistics"]["total_relations"],
        normalized["statistics"]["entity_types"],
        normalized["statistics"]["relation_types"],
    )

    print(f"\n✓ Post-normalization completed.\n"
          f"  Input : {INPUT_FILE}\n"
          f"  Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
