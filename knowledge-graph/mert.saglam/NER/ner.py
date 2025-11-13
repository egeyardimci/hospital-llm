"""
Named Entity Recognition (NER) for Turkish Healthcare Documents
Extracts entities dynamically without predefined categories using Groq LLM
"""

import os
import json
import re
from typing import List, Dict, Any, Set
from dataclasses import dataclass, asdict
from dotenv import load_dotenv
from groq import Groq
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


@dataclass
class NamedEntity:
    """Represents a named entity extracted from text"""
    text: str  # The actual text of the entity
    type: str  # Dynamic type (discovered from text)
    start_pos: int  # Start position in original text
    end_pos: int  # End position in original text
    context: str  # Surrounding context
    properties: Dict[str, Any]  # Additional properties
    
    def to_dict(self):
        return asdict(self)


@dataclass
class EntityRelation:
    """Represents a relationship between two entities"""
    entity1: str  # First entity text
    entity2: str  # Second entity text
    relation_type: str  # Type of relationship
    context: str  # Context where relation appears
    properties: Dict[str, Any]
    
    def to_dict(self):
        return asdict(self)


class TurkishNERExtractor:
    """
    Named Entity Recognition for Turkish legal/healthcare documents
    Uses LLM to dynamically discover entity types instead of predefined categories
    """
    
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.model = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
        self.entity_cache: Dict[str, NamedEntity] = {}
        self.discovered_types: Set[str] = set()
        
    def extract_entities_from_chunk(self, text: str, chunk_index: int = 0) -> List[NamedEntity]:
        """
        Extract named entities from a text chunk using LLM
        Discovers entity types dynamically from the content
        """
        
        prompt = f"""You are an expert in Turkish Named Entity Recognition for healthcare and legal documents.

TASK: Extract ALL named entities from this text. DO NOT use predefined categories. Instead, identify what each entity actually represents in the context. In this project what SGK with what context is extremely important so pay attetion to that.

For each entity, determine:
1. The exact text span
2. What type of thing it is (be specific: e.g., "İlaç Sistemi", "Sosyal Güvenlik Kanunu", "Tıbbi Prosedür", etc.)
3. Its role/function in the document
4. Any relevant attributes (numbers, dates, descriptions)

TEXT:
{text}

Return JSON in this EXACT format:
{{
  "entities": [
    {{
      "text": "MEDULA",
      "type": "Sağlık Bilgi Sistemi",
      "start_pos": 245,
      "end_pos": 251,
      "context": "Kurum bilgi işlem sistemi (MEDULA-Hastane, MEDULA-Optik)",
      "properties": {{
        "description": "Provizyon ve hasta takip sistemi",
        "subsystems": ["MEDULA-Hastane", "MEDULA-Optik", "MEDULA-Eczane"]
      }}
    }},
    {{
      "text": "T.C. Kimlik Numarası",
      "type": "Kimlik Belgesi",
      "start_pos": 520,
      "end_pos": 541,
      "context": "üzerinden T.C. Kimlik Numarası veya YUPASS numarası",
      "properties": {{
        "usage": "Hasta tanımlama ve provizyon",
        "mandatory": true
      }}
    }}
  ]
}}

CRITICAL RULES:
1. Extract ACTUAL entities from the text (organizations, systems, documents, laws, procedures, conditions, etc.)
2. DO NOT invent generic categories - use specific types that describe what the entity IS
3. Include proper Turkish characters (ı, ş, ğ, ü, ö, ç, İ, Ş, Ğ, Ü, Ö, Ç)
4. Position indices should be approximate (we'll find exact positions later)
5. Provide meaningful context (the sentence or phrase containing the entity)
6. Add relevant properties based on the text
7. Confidence should reflect how certain you are this is a distinct entity
8. Return ONLY valid JSON, no markdown or explanations"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Clean JSON if wrapped in markdown
            if content.startswith('```'):
                content = re.sub(r'^```json?\n?|\n?```$', '', content, flags=re.MULTILINE)
            
            result = json.loads(content)
            
            # Convert to NamedEntity objects
            entities = []
            for ent_data in result.get('entities', []):
                # Find actual position in text
                entity_text = ent_data['text']
                actual_start = text.lower().find(entity_text.lower())
                
                if actual_start == -1:
                    # Try to find partial match
                    words = entity_text.split()
                    if words:
                        actual_start = text.lower().find(words[0].lower())
                
                actual_end = actual_start + len(entity_text) if actual_start != -1 else -1
                
                entity = NamedEntity(
                    text=ent_data['text'],
                    type=ent_data['type'],
                    start_pos=actual_start if actual_start != -1 else ent_data.get('start_pos', 0),
                    end_pos=actual_end if actual_end != -1 else ent_data.get('end_pos', 0),
                    context=ent_data.get('context', ''),
                    properties=ent_data.get('properties', {}),
                )
                
                entities.append(entity)
                self.discovered_types.add(entity.type)
            
            logger.info(f"Chunk {chunk_index}: Extracted {len(entities)} entities with {len(self.discovered_types)} unique types")
            return entities
            
        except Exception as e:
            logger.error(f"Error extracting entities from chunk {chunk_index}: {e}")
            return []
    
    def extract_relations_from_chunk(self, text: str, entities: List[NamedEntity], chunk_index: int = 0) -> List[EntityRelation]:
        """
        Extract relationships between entities in a chunk
        Discovers relationship types dynamically
        """
        
        if len(entities) < 2:
            return []
        
        # Create entity context for the prompt
        entity_list = "\n".join([f"- {e.text} ({e.type})" for e in entities[:20]])  # Limit to first 20
        
        prompt = f"""You are an expert in relationship extraction for Turkish healthcare documents.

TASK: Identify relationships between these entities found in the text.

ENTITIES FOUND:
{entity_list}

TEXT:
{text}

For each meaningful relationship, determine:
1. Which two entities are related
2. What type of relationship connects them (be specific and natural, e.g., "yönetir", "gerektirir", "düzenler", "kullanılır")
3. The context showing this relationship
4. Any properties of the relationship

Return JSON in this EXACT format:
{{
  "relations": [
    {{
      "entity1": "MEDULA",
      "entity2": "SGK",
      "relation_type": "tarafından yönetilir",
      "context": "Kurum bilgi işlem sistemi (MEDULA)",
      "properties": {{
        "direction": "managed_by",
        "domain": "sağlık hizmetleri"
      }}
    }},
    {{
      "entity1": "Provizyon işlemi",
      "entity2": "T.C. Kimlik Numarası",
      "relation_type": "gerektirir",
      "context": "T.C. Kimlik Numarası ile hasta takip numarası/provizyon alacaklardır",
      "properties": {{
        "requirement_type": "mandatory",
        "purpose": "kimlik doğrulama"
      }}
    }}
  ]
}}

RULES:
1. Only extract relationships explicitly stated or strongly implied in the text
2. Use natural Turkish relationship descriptions
3. Both entities must be from the entity list above
4. Include meaningful context
5. Confidence reflects how clearly the relationship is stated
6. Return ONLY valid JSON"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=3000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Clean JSON
            if content.startswith('```'):
                content = re.sub(r'^```json?\n?|\n?```$', '', content, flags=re.MULTILINE)
            
            result = json.loads(content)
            
            # Convert to EntityRelation objects
            relations = []
            for rel_data in result.get('relations', []):
                relation = EntityRelation(
                    entity1=rel_data['entity1'],
                    entity2=rel_data['entity2'],
                    relation_type=rel_data['relation_type'],
                    context=rel_data.get('context', ''),
                    properties=rel_data.get('properties', {})
                )
                relations.append(relation)
            
            logger.info(f"Chunk {chunk_index}: Extracted {len(relations)} relations")
            return relations
            
        except Exception as e:
            logger.error(f"Error extracting relations from chunk {chunk_index}: {e}")
            return []
    
    def chunk_text(self, text: str, chunk_size: int = 3000, overlap: int = 400) -> List[Dict[str, Any]]:
        """Split text into overlapping chunks with metadata - FIXED"""
        chunks = []
        text_length = len(text)
        
        # Quick estimate of number of chunks
        estimated_chunks = (text_length // (chunk_size - overlap)) + 1
        logger.info(f"Document size: {text_length} chars, estimated chunks: {estimated_chunks}")
        
        start = 0
        chunk_index = 0
        
        while start < text_length:
            # CRITICAL FIX: Make sure we always move forward
            end = min(start + chunk_size, text_length)
            
            # Only try sentence boundary if not at end
            if end < text_length:
                # Look in last 200 chars for sentence boundary
                search_start = max(end - 200, start)
                substring = text[search_start:end]
                
                # Find last period or newline
                last_period = substring.rfind('. ')
                last_newline = substring.rfind('\n')
                last_delim = max(last_period, last_newline)
                
                if last_delim != -1:
                    end = search_start + last_delim + 1
            
            chunk_text = text[start:end]
            
            chunks.append({
                'index': chunk_index,
                'text': chunk_text,
                'start_pos': start,
                'end_pos': end,
                'length': len(chunk_text)
            })
            
            chunk_index += 1
            
            # CRITICAL FIX: Always move forward by at least (chunk_size - overlap)
            # This prevents infinite loops
            next_start = end - overlap
            if next_start <= start:
                # If overlap is too large, force move forward
                next_start = start + (chunk_size - overlap)
            start = next_start
            
            # Progress logging every 100 chunks
            if chunk_index % 100 == 0:
                logger.info(f"Created {chunk_index} chunks... ({(start/text_length)*100:.1f}% complete)")
        
        logger.info(f"Split text into {len(chunks)} chunks")
        return chunks
    
    def extract_from_document(self, text: str, max_chunks: int = None) -> Dict[str, Any]:
        """
        Extract all entities and relations from a complete document
        max_chunks: Limit number of chunks to process (for testing)
        """
        logger.info(f"Starting NER extraction from document (length: {len(text)} chars)...")
        
        # Reset discovered types for this document
        self.discovered_types = set()
        
        # Chunk the document
        logger.info("Chunking document...")
        chunks = self.chunk_text(text)
        
        # Limit chunks if specified (for testing)
        if max_chunks and max_chunks < len(chunks):
            logger.info(f"Limiting to first {max_chunks} chunks for testing")
            chunks = chunks[:max_chunks]
        
        all_entities = []
        all_relations = []
        entity_texts_seen = set()  # For deduplication
        
        # Process chunks with progress updates
        total_chunks = len(chunks)
        for chunk_info in chunks:
            chunk_idx = chunk_info['index']
            chunk_text = chunk_info['text']
            chunk_start = chunk_info['start_pos']
            
            # Progress update
            progress = ((chunk_idx + 1) / total_chunks) * 100
            logger.info(f"Processing chunk {chunk_idx + 1}/{total_chunks} ({progress:.1f}%)")
            
            # Extract entities
            entities = self.extract_entities_from_chunk(chunk_text, chunk_idx)
            
            # Adjust positions to document coordinates and deduplicate
            for entity in entities:
                entity.start_pos += chunk_start
                entity.end_pos += chunk_start
                
                # Deduplicate by text and type
                entity_key = (entity.text.lower(), entity.type)
                if entity_key not in entity_texts_seen:
                    entity_texts_seen.add(entity_key)
                    all_entities.append(entity)
            
            # Extract relations (only if we have entities)
            if len(entities) >= 2:
                relations = self.extract_relations_from_chunk(chunk_text, entities, chunk_idx)
                all_relations.extend(relations)
            
            # Periodic summary every 5 chunks
            if (chunk_idx + 1) % 5 == 0:
                logger.info(f"Progress: {len(all_entities)} entities, {len(all_relations)} relations so far")
        
        # Deduplicate relations
        unique_relations = []
        seen_relations = set()
        for rel in all_relations:
            rel_key = (rel.entity1.lower(), rel.entity2.lower(), rel.relation_type.lower())
            if rel_key not in seen_relations:
                seen_relations.add(rel_key)
                unique_relations.append(rel)
        
        # Group entities by type
        entities_by_type = {}
        for entity in all_entities:
            if entity.type not in entities_by_type:
                entities_by_type[entity.type] = []
            entities_by_type[entity.type].append(entity)
        
        result = {
            'entities': [e.to_dict() for e in all_entities],
            'relations': [r.to_dict() for r in unique_relations],
            'entities_by_type': {k: [e.to_dict() for e in v] for k, v in entities_by_type.items()},
            'statistics': {
                'total_entities': len(all_entities),
                'total_relations': len(unique_relations),
                'unique_entity_types': len(self.discovered_types),
                'entity_types': sorted(list(self.discovered_types))
            }
        }
        
        logger.info(f"Extraction complete: {result['statistics']['total_entities']} entities, "
                   f"{result['statistics']['total_relations']} relations, "
                   f"{result['statistics']['unique_entity_types']} entity types")
        
        return result
    
    def save_extraction_results(self, results: Dict[str, Any], output_file: str = 'ner_extraction.json'):
        """Save extraction results to JSON file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        logger.info(f"Results saved to {output_file}")
    
    def print_summary(self, results: Dict[str, Any]):
        """Print a summary of extraction results"""
        stats = results['statistics']
        
        print("\n" + "="*80)
        print("  NER EXTRACTION SUMMARY")
        print("="*80)
        print(f"\n📊 Statistics:")
        print(f"   Total Entities: {stats['total_entities']}")
        print(f"   Total Relations: {stats['total_relations']}")
        print(f"   Unique Entity Types: {stats['unique_entity_types']}")
        
        print(f"\n🏷️  Discovered Entity Types:")
        for entity_type in stats['entity_types']:
            count = len(results['entities_by_type'][entity_type])
            print(f"   • {entity_type}: {count} entities")
        
        print(f"\n📝 Sample Entities (first 5):")
        for i, entity in enumerate(results['entities'][:5], 1):
            print(f"   {i}. {entity['text']} ({entity['type']})")
            print(f"      Context: {entity['context'][:80]}...")
           
        
        print(f"\n🔗 Sample Relations (first 5):")
        for i, relation in enumerate(results['relations'][:5], 1):
            print(f"   {i}. {relation['entity1']} → [{relation['relation_type']}] → {relation['entity2']}")
           


def main():
    """Main function for testing NER extraction"""
    
    # Load document
    try:
        with open('sgk_document.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        logger.info(f"Loaded document: {len(text)} characters")
    except FileNotFoundError:
        logger.error("sgk_document.txt not found. Please provide the document.")
        return
    
    # For testing: process only first N chunks (remove limit for full extraction)
    TEST_MODE = False  # Set to False for full extraction
    MAX_CHUNKS = 10 if TEST_MODE else None
    
    if TEST_MODE:
        logger.warning(f"TESTING MODE: Processing only first {MAX_CHUNKS} chunks")
        logger.warning("Set TEST_MODE = False in main() for full extraction")
    
    # Initialize NER extractor
    ner_extractor = TurkishNERExtractor()
    
    # Extract entities and relations
    results = ner_extractor.extract_from_document(text, max_chunks=MAX_CHUNKS)
    
    # Print summary
    ner_extractor.print_summary(results)
    
    # Save results
    output_file = 'ner_extraction_test.json' if TEST_MODE else 'ner_extraction.json'
    ner_extractor.save_extraction_results(results, output_file)
    
    print(f"\n✅ NER extraction complete!")
    print(f"   Results saved to: {output_file}")
    print("   Use these results with the knowledge graph system.")
    
    if TEST_MODE:
        print("\n⚠️  NOTE: This was a test run with limited chunks.")
        print("   Set TEST_MODE = False in main() for full document extraction.")


if __name__ == "__main__":
    main()