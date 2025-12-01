#!/usr/bin/env python3
"""
Healthcare Regulations Knowledge Graph Generator
Generates Cypher queries from JSONL extraction data for Neo4j visualization

Usage:
    python generate_kg_cypher.py input.jsonl output.cypher
"""

import json
import re
from collections import defaultdict
from typing import Dict, List, Any, Set

def sanitize_string(s: str) -> str:
    """Escape special characters for Cypher strings"""
    if not s:
        return ""
    return s.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"').replace("\n", " ").strip()

def generate_node_id(prefix: str, value: str) -> str:
    """Generate a valid Neo4j node variable name"""
    # Remove special chars and spaces, convert to camelCase
    clean = re.sub(r'[^a-zA-Z0-9_]', '_', value)
    clean = re.sub(r'_+', '_', clean).strip('_')
    return f"{prefix}_{clean[:30]}"

class KnowledgeGraphGenerator:
    def __init__(self, data: Dict):
        self.data = data
        self.extractions = data.get('extractions', [])
        
        # Node collections
        self.payment_methods: Set[str] = set()
        self.care_settings: Set[str] = set()
        self.institutions: Dict[str, Dict] = {}
        self.medical_services: Dict[str, Dict] = {}
        self.medical_procedures: Dict[str, Dict] = {}
        self.billing_rules: List[Dict] = []
        self.sections: Dict[str, Dict] = {}
        self.regulation_lists: Dict[str, Dict] = {}
        self.amendments: List[Dict] = []
        self.professional_roles: Dict[str, Dict] = {}
        
        # Relationship collections
        self.relationships: List[Dict] = []
        
    def extract_entities(self):
        """Extract all entities from the extractions"""
        for ext in self.extractions:
            cls = ext.get('extraction_class')
            attrs = ext.get('attributes') or {}
            text = ext.get('extraction_text', '')
            
            # Extract payment methods
            pm = attrs.get('payment_method') or attrs.get('payment_model')
            if pm and isinstance(pm, str):
                self.payment_methods.add(pm)
            
            # Extract care settings
            cs = attrs.get('care_setting')
            if cs and isinstance(cs, str):
                self.care_settings.add(cs)
            
            # Process by class
            if cls == 'regulation':
                self._process_regulation(ext, attrs, text)
            elif cls == 'institution':
                self._process_institution(ext, attrs, text)
            elif cls == 'medical_service':
                self._process_medical_service(ext, attrs, text)
            elif cls == 'medical_procedure':
                self._process_medical_procedure(ext, attrs, text)
            elif cls in ['billing_rule', 'billing_prohibition']:
                self._process_billing_rule(ext, attrs, text)
            elif cls == 'list' or cls == 'regulation_annex':
                self._process_regulation_list(ext, attrs, text)
            elif cls == 'amendment':
                self._process_amendment(ext, attrs, text)
            elif cls == 'professional_role':
                self._process_professional_role(ext, attrs, text)
    
    def _process_regulation(self, ext, attrs, text):
        topic = attrs.get('topic')
        identifier = attrs.get('identifier')
        if topic or identifier:
            key = identifier or topic[:50]
            self.sections[key] = {
                'identifier': identifier,
                'topic': topic,
                'payment_model': attrs.get('payment_model'),
                'care_setting': attrs.get('care_setting'),
                'parent_section': attrs.get('parent_section'),
                'text': text[:100]
            }
    
    def _process_institution(self, ext, attrs, text):
        inst_type = attrs.get('type')
        if inst_type:
            key = text[:50] if text else inst_type
            self.institutions[key] = {
                'name': text[:100] if text else '',
                'type': inst_type,
                'supervising_authority': attrs.get('supervising_authority'),
                'funding_model': attrs.get('funding_model'),
                'role': attrs.get('role'),
                'ownership': attrs.get('ownership')
            }
    
    def _process_medical_service(self, ext, attrs, text):
        svc_type = attrs.get('type')
        if svc_type:
            self.medical_services[svc_type] = {
                'type': svc_type,
                'name': text[:100] if text else '',
                'payment_method': attrs.get('payment_method'),
                'legal_context': attrs.get('legal_context'),
                'coverage_status': attrs.get('coverage_status'),
                'provider': attrs.get('provider'),
                'specialty': attrs.get('specialty')
            }
    
    def _process_medical_procedure(self, ext, attrs, text):
        name = text[:50] if text else attrs.get('name', 'Unknown')
        code = attrs.get('code')
        key = code or name
        self.medical_procedures[key] = {
            'name': name,
            'code': code,
            'type': attrs.get('type'),
            'body_system': attrs.get('body_system'),
            'category': attrs.get('category'),
            'specialty': attrs.get('specialty'),
            'technique': attrs.get('technique')
        }
    
    def _process_billing_rule(self, ext, attrs, text):
        self.billing_rules.append({
            'class': ext.get('extraction_class'),
            'text': text[:100] if text else '',
            'action': attrs.get('action') or attrs.get('prohibited_action'),
            'responsible_party': attrs.get('responsible_party'),
            'requirement_type': attrs.get('requirement_type'),
            'items': attrs.get('items'),
            'context': attrs.get('context'),
            'payer': attrs.get('payer'),
            'condition': attrs.get('condition')
        })
    
    def _process_regulation_list(self, ext, attrs, text):
        code = attrs.get('annex_code') or attrs.get('code')
        if code:
            # Handle list type codes
            if isinstance(code, list):
                for c in code:
                    self._add_regulation_list(c, attrs, text)
            else:
                self._add_regulation_list(code, attrs, text)
    
    def _add_regulation_list(self, code, attrs, text):
        self.regulation_lists[code] = {
            'code': code,
            'name': text[:100] if text else '',
            'function': attrs.get('function'),
            'scope': attrs.get('scope'),
            'type': attrs.get('type')
        }
    
    def _process_amendment(self, ext, attrs, text):
        self.amendments.append({
            'text': text[:100] if text else '',
            'official_gazette_date': attrs.get('official_gazette_date'),
            'official_gazette_number': attrs.get('official_gazette_number'),
            'article_reference': attrs.get('article_reference'),
            'effective_date': attrs.get('effective_date'),
            'type': attrs.get('type'),
            'scope': attrs.get('scope')
        })
    
    def _process_professional_role(self, ext, attrs, text):
        role_type = attrs.get('type')
        if role_type:
            self.professional_roles[role_type] = {
                'type': role_type,
                'name': text[:50] if text else '',
                'sector': attrs.get('sector'),
                'regulatory_status': attrs.get('regulatory_status')
            }
    
    def generate_cypher(self) -> str:
        """Generate complete Cypher script"""
        lines = []
        
        # Header
        lines.append("// " + "=" * 76)
        lines.append("// AUTO-GENERATED HEALTHCARE REGULATIONS KNOWLEDGE GRAPH")
        lines.append("// Generated from JSONL extraction data")
        lines.append("// " + "=" * 76)
        lines.append("")
        
        # Constraints
        lines.extend(self._generate_constraints())
        
        # Payment Method nodes (central hubs)
        lines.extend(self._generate_payment_method_nodes())
        
        # Care Setting nodes
        lines.extend(self._generate_care_setting_nodes())
        
        # Section nodes
        lines.extend(self._generate_section_nodes())
        
        # Institution nodes
        lines.extend(self._generate_institution_nodes())
        
        # Medical Service nodes
        lines.extend(self._generate_medical_service_nodes())
        
        # Medical Procedure nodes
        lines.extend(self._generate_medical_procedure_nodes())
        
        # Regulation List nodes
        lines.extend(self._generate_regulation_list_nodes())
        
        # Billing Rule nodes
        lines.extend(self._generate_billing_rule_nodes())
        
        # Amendment nodes
        lines.extend(self._generate_amendment_nodes())
        
        # Professional Role nodes
        lines.extend(self._generate_professional_role_nodes())
        
        # Relationships
        lines.extend(self._generate_relationships())
        
        return "\n".join(lines)
    
    def _generate_constraints(self) -> List[str]:
        lines = [
            "",
            "// " + "=" * 76,
            "// CONSTRAINTS",
            "// " + "=" * 76,
            "",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (p:PaymentMethod) REQUIRE p.name IS UNIQUE;",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:CareSetting) REQUIRE c.name IS UNIQUE;",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (s:Section) REQUIRE s.identifier IS UNIQUE;",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (i:Institution) REQUIRE i.name IS UNIQUE;",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (m:MedicalService) REQUIRE m.type IS UNIQUE;",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (p:MedicalProcedure) REQUIRE p.name IS UNIQUE;",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (l:RegulationList) REQUIRE l.code IS UNIQUE;",
            ""
        ]
        return lines
    
    def _generate_payment_method_nodes(self) -> List[str]:
        lines = [
            "",
            "// " + "=" * 76,
            "// PAYMENT METHOD NODES (Central Hub Nodes)",
            "// " + "=" * 76,
            ""
        ]
        
        for pm in sorted(self.payment_methods):
            pm_safe = sanitize_string(pm)
            pm_type = "fee_for_service" if "hizmet başına" in pm.lower() else "diagnosis_based" if "tanıya" in pm.lower() else "other"
            lines.append(f"MERGE (pm:PaymentMethod {{name: '{pm_safe}', type: '{pm_type}'}});")
        
        lines.append("")
        return lines
    
    def _generate_care_setting_nodes(self) -> List[str]:
        lines = [
            "",
            "// " + "=" * 76,
            "// CARE SETTING NODES",
            "// " + "=" * 76,
            ""
        ]
        
        for cs in sorted(self.care_settings):
            cs_safe = sanitize_string(cs)
            cs_type = "outpatient" if "ayak" in cs.lower() else "inpatient" if "yatak" in cs.lower() else "emergency" if "acil" in cs.lower() else "other"
            lines.append(f"MERGE (cs:CareSetting {{name: '{cs_safe}', type: '{cs_type}'}});")
        
        lines.append("")
        return lines
    
    def _generate_section_nodes(self) -> List[str]:
        lines = [
            "",
            "// " + "=" * 76,
            "// SECTION/TOPIC NODES",
            "// " + "=" * 76,
            ""
        ]
        
        for key, sec in self.sections.items():
            identifier = sanitize_string(sec.get('identifier') or key)
            topic = sanitize_string(sec.get('topic') or '')
            payment_model = sanitize_string(sec.get('payment_model') or '')
            care_setting = sanitize_string(sec.get('care_setting') or '')
            
            props = [f"identifier: '{identifier}'"]
            if topic:
                props.append(f"topic: '{topic}'")
            if payment_model:
                props.append(f"payment_model: '{payment_model}'")
            if care_setting:
                props.append(f"care_setting: '{care_setting}'")
            
            lines.append(f"MERGE (sec:Section {{{', '.join(props)}}});")
        
        lines.append("")
        return lines
    
    def _generate_institution_nodes(self) -> List[str]:
        lines = [
            "",
            "// " + "=" * 76,
            "// INSTITUTION NODES",
            "// " + "=" * 76,
            ""
        ]
        
        for key, inst in self.institutions.items():
            name = sanitize_string(inst.get('name') or key)
            inst_type = sanitize_string(inst.get('type') or '')
            
            props = [f"name: '{name}'"]
            if inst_type:
                props.append(f"type: '{inst_type}'")
            
            for attr in ['supervising_authority', 'funding_model', 'role', 'ownership']:
                val = inst.get(attr)
                if val:
                    props.append(f"{attr}: '{sanitize_string(str(val))}'")
            
            lines.append(f"MERGE (inst:Institution {{{', '.join(props)}}});")
        
        lines.append("")
        return lines
    
    def _generate_medical_service_nodes(self) -> List[str]:
        lines = [
            "",
            "// " + "=" * 76,
            "// MEDICAL SERVICE NODES (Surrounding Payment Method Hub)",
            "// " + "=" * 76,
            ""
        ]
        
        for svc_type, svc in self.medical_services.items():
            svc_type_safe = sanitize_string(svc_type)
            name = sanitize_string(svc.get('name') or '')
            
            props = [f"type: '{svc_type_safe}'"]
            if name:
                props.append(f"name: '{name}'")
            
            for attr in ['payment_method', 'legal_context', 'coverage_status', 'provider', 'specialty']:
                val = svc.get(attr)
                if val:
                    props.append(f"{attr}: '{sanitize_string(str(val))}'")
            
            lines.append(f"MERGE (ms:MedicalService {{{', '.join(props)}}});")
        
        lines.append("")
        return lines
    
    def _generate_medical_procedure_nodes(self) -> List[str]:
        lines = [
            "",
            "// " + "=" * 76,
            "// MEDICAL PROCEDURE NODES",
            "// " + "=" * 76,
            ""
        ]
        
        for key, proc in self.medical_procedures.items():
            name = sanitize_string(proc.get('name') or key)
            
            props = [f"name: '{name}'"]
            
            for attr in ['code', 'type', 'body_system', 'category', 'specialty', 'technique']:
                val = proc.get(attr)
                if val:
                    props.append(f"{attr}: '{sanitize_string(str(val))}'")
            
            lines.append(f"MERGE (proc:MedicalProcedure {{{', '.join(props)}}});")
        
        lines.append("")
        return lines
    
    def _generate_regulation_list_nodes(self) -> List[str]:
        lines = [
            "",
            "// " + "=" * 76,
            "// REGULATION LIST/ANNEX NODES",
            "// " + "=" * 76,
            ""
        ]
        
        for code, lst in self.regulation_lists.items():
            code_safe = sanitize_string(code)
            name = sanitize_string(lst.get('name') or '')
            
            props = [f"code: '{code_safe}'"]
            if name:
                props.append(f"name: '{name}'")
            
            for attr in ['function', 'scope', 'type']:
                val = lst.get(attr)
                if val:
                    props.append(f"{attr}: '{sanitize_string(str(val))}'")
            
            lines.append(f"MERGE (list:RegulationList {{{', '.join(props)}}});")
        
        lines.append("")
        return lines
    
    def _generate_billing_rule_nodes(self) -> List[str]:
        lines = [
            "",
            "// " + "=" * 76,
            "// BILLING RULE NODES",
            "// " + "=" * 76,
            ""
        ]
        
        for i, br in enumerate(self.billing_rules[:50]):  # Limit to 50 rules
            rule_id = f"BR-{i+1:03d}"
            
            props = [f"identifier: '{rule_id}'"]
            
            for attr in ['action', 'responsible_party', 'requirement_type', 'payer', 'context']:
                val = br.get(attr)
                if val:
                    props.append(f"{attr}: '{sanitize_string(str(val)[:100])}'")
            
            lines.append(f"MERGE (br:BillingRule {{{', '.join(props)}}});")
        
        lines.append("")
        return lines
    
    def _generate_amendment_nodes(self) -> List[str]:
        lines = [
            "",
            "// " + "=" * 76,
            "// AMENDMENT NODES",
            "// " + "=" * 76,
            ""
        ]
        
        seen = set()
        for amd in self.amendments:
            og_num = amd.get('official_gazette_number')
            if og_num and og_num not in seen:
                seen.add(og_num)
                
                props = [f"official_gazette_number: '{sanitize_string(og_num)}'"]
                
                for attr in ['official_gazette_date', 'article_reference', 'effective_date', 'type', 'scope']:
                    val = amd.get(attr)
                    if val:
                        props.append(f"{attr}: '{sanitize_string(str(val))}'")
                
                lines.append(f"MERGE (amd:Amendment {{{', '.join(props)}}});")
        
        lines.append("")
        return lines
    
    def _generate_professional_role_nodes(self) -> List[str]:
        lines = [
            "",
            "// " + "=" * 76,
            "// PROFESSIONAL ROLE NODES",
            "// " + "=" * 76,
            ""
        ]
        
        for role_type, role in self.professional_roles.items():
            role_type_safe = sanitize_string(role_type)
            name = sanitize_string(role.get('name') or '')
            
            props = [f"type: '{role_type_safe}'"]
            if name:
                props.append(f"name: '{name}'")
            
            for attr in ['sector', 'regulatory_status']:
                val = role.get(attr)
                if val:
                    props.append(f"{attr}: '{sanitize_string(str(val))}'")
            
            lines.append(f"MERGE (role:ProfessionalRole {{{', '.join(props)}}});")
        
        lines.append("")
        return lines
    
    def _generate_relationships(self) -> List[str]:
        lines = [
            "",
            "// " + "=" * 76,
            "// RELATIONSHIPS",
            "// " + "=" * 76,
            "",
            "// Connect Medical Services to Payment Methods",
        ]
        
        # Medical Services to Payment Methods
        for svc_type, svc in self.medical_services.items():
            pm = svc.get('payment_method')
            if pm:
                svc_safe = sanitize_string(svc_type)
                pm_safe = sanitize_string(pm)
                lines.append(f"""
MATCH (ms:MedicalService {{type: '{svc_safe}'}})
MATCH (pm:PaymentMethod {{name: '{pm_safe}'}})
MERGE (ms)-[:BILLED_VIA]->(pm);""")
        
        # Sections to Payment Methods
        lines.append("")
        lines.append("// Connect Sections to Payment Methods")
        for key, sec in self.sections.items():
            pm = sec.get('payment_model')
            identifier = sec.get('identifier') or key
            if pm:
                id_safe = sanitize_string(identifier)
                pm_safe = sanitize_string(pm)
                lines.append(f"""
MATCH (sec:Section {{identifier: '{id_safe}'}})
MATCH (pm:PaymentMethod) WHERE pm.name CONTAINS '{pm_safe[:20]}'
MERGE (sec)-[:USES_PAYMENT_METHOD]->(pm);""")
        
        # Sections to Care Settings
        lines.append("")
        lines.append("// Connect Sections to Care Settings")
        for key, sec in self.sections.items():
            cs = sec.get('care_setting')
            identifier = sec.get('identifier') or key
            if cs:
                id_safe = sanitize_string(identifier)
                cs_safe = sanitize_string(cs)
                lines.append(f"""
MATCH (sec:Section {{identifier: '{id_safe}'}})
MATCH (cs:CareSetting {{name: '{cs_safe}'}})
MERGE (sec)-[:APPLIES_TO_SETTING]->(cs);""")
        
        # Sections to Medical Services
        lines.append("")
        lines.append("// Connect Sections to Medical Services")
        lines.append("""
MATCH (sec:Section)
WHERE sec.payment_model IS NOT NULL
MATCH (ms:MedicalService)
WHERE ms.payment_method CONTAINS sec.payment_model OR sec.payment_model CONTAINS ms.payment_method
MERGE (sec)-[:INCLUDES_SERVICE]->(ms);""")
        
        # Medical Services to Institutions
        lines.append("")
        lines.append("// Connect Medical Services to Institutions")
        for svc_type, svc in self.medical_services.items():
            provider = svc.get('provider')
            if provider:
                svc_safe = sanitize_string(svc_type)
                provider_safe = sanitize_string(provider)
                lines.append(f"""
MATCH (ms:MedicalService {{type: '{svc_safe}'}})
MATCH (inst:Institution) WHERE inst.name CONTAINS '{provider_safe[:30]}'
MERGE (ms)-[:PROVIDED_BY]->(inst);""")
        
        lines.append("")
        return lines


def main():
    import sys
    
    if len(sys.argv) < 2:
        input_file = '/mnt/user-data/uploads/pdf_extractions_100k_115k.jsonl'
        output_file = '/home/claude/generated_kg.cypher'
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else 'output.cypher'
    
    print(f"Reading from: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Found {len(data.get('extractions', []))} extractions")
    
    generator = KnowledgeGraphGenerator(data)
    generator.extract_entities()
    
    print(f"Extracted entities:")
    print(f"  - Payment Methods: {len(generator.payment_methods)}")
    print(f"  - Care Settings: {len(generator.care_settings)}")
    print(f"  - Sections: {len(generator.sections)}")
    print(f"  - Institutions: {len(generator.institutions)}")
    print(f"  - Medical Services: {len(generator.medical_services)}")
    print(f"  - Medical Procedures: {len(generator.medical_procedures)}")
    print(f"  - Regulation Lists: {len(generator.regulation_lists)}")
    print(f"  - Billing Rules: {len(generator.billing_rules)}")
    print(f"  - Amendments: {len(generator.amendments)}")
    print(f"  - Professional Roles: {len(generator.professional_roles)}")
    
    cypher = generator.generate_cypher()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cypher)
    
    print(f"\nCypher queries written to: {output_file}")


if __name__ == '__main__':
    main()
