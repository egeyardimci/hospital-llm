import json
import hashlib
import re

def clean_text(text):
    """Escapes characters that would break Cypher strings."""
    if text:
        # Escape single quotes and remove newlines
        return str(text).replace("'", "\\'").replace("\n", " ").strip()
    return ""

def sanitize_var(text):
    """
    Creates a valid Cypher variable name by removing illegal characters.
    """
    if not text:
        return "var_unknown"
    # Replace non-alphanumeric chars with underscore
    clean = re.sub(r'[^a-zA-Z0-9_]', '_', str(text))
    # Ensure it doesn't start with a number
    if clean[0].isdigit():
        clean = "_" + clean
    # Remove consecutive underscores for readability
    return re.sub(r'_+', '_', clean).strip('_')

def generate_uid(item):
    """Generates a consistent unique ID."""
    unique_str = f"{item.get('extraction_index', 0)}_{item.get('group_index', 0)}_{item.get('extraction_text', '')[:20]}"
    return hashlib.md5(unique_str.encode()).hexdigest()

def generate_cypher(data):
    cypher_lines = []
    
    # 1. PRE-SEED BASE NODES
    # We use distinct variables here just in case this runs in the same transaction
    cypher_lines.append("// --- BASE SETUP ---")
    cypher_lines.append("MERGE (p1_base:ProviderType {level: 'birinci basamak'});")
    cypher_lines.append("MERGE (p2_base:ProviderType {level: 'ikinci basamak'});")
    cypher_lines.append("MERGE (p3_base:ProviderType {level: 'üçüncü basamak'});")
    cypher_lines.append("")

    # 2. ITERATE THROUGH ALL EXTRACTIONS
    for item in data['extractions']:
        e_class = item.get('extraction_class')
        attrs = item.get('attributes', {})
        uid = generate_uid(item)
        
        # Map JSON 'extraction_class' to Neo4j Labels
        label_map = {
            'section': 'Section',
            'billing_rule': 'Rule:BillingRule',
            'coverage_rule': 'Rule:CoverageRule',
            'payment_rule': 'Rule:PaymentRule',
            'medical_service': 'MedicalService',
            'medical_procedure': 'MedicalProcedure',
            'list_reference': 'RegulatoryList',
            'limit': 'Limit',
            'amendment': 'Amendment',
            'referral_rule': 'Rule:ReferralRule',
            'scope': 'Scope',
            'quota_rule': 'Rule:QuotaRule'
        }
        labels = label_map.get(e_class, 'Entity')
        
        # Build Properties
        props = [f"uid: '{uid}'"]
        
        if 'extraction_text' in item:
            props.append(f"text: '{clean_text(item['extraction_text'])}'")
            
        for k, v in attrs.items():
            if v is not None and not isinstance(v, (list, dict)):
                props.append(f"{k}: '{clean_text(v)}'")
            elif isinstance(v, list):
                props.append(f"{k}: '{clean_text(','.join(map(str, v)))}'")

        # VARIABLE UNIQUENESS FIX:
        # We append the UID to the main node variable to ensure it doesn't conflict globally
        node_var = f"n_{uid}"

        # 3. CREATE/MERGE THE NODE
        if e_class == 'section' and 'identifier' in attrs:
             identifier = clean_text(attrs['identifier'])
             cypher_lines.append(f"MERGE ({node_var}:{labels} {{identifier: '{identifier}'}})")
        elif e_class == 'list_reference':
             code_raw = attrs.get('list_code') or attrs.get('list_name') or uid
             codes = [x.strip() for x in str(code_raw).split(',')]
             primary_code = codes[0]
             cypher_lines.append(f"MERGE ({node_var}:{labels} {{code: '{clean_text(primary_code)}'}})")
        else:
             cypher_lines.append(f"MERGE ({node_var}:{labels} {{uid: '{uid}'}})")
        
        cypher_lines.append(f"SET {node_var} += {{{', '.join(props)}}}")

        # 4. CREATE RELATIONSHIPS (With Scoped Variables)
        
        # Parent Section
        parent = attrs.get('parent_section')
        if parent and parent != 'UNKNOWN':
            p_id = clean_text(parent)
            # FIX: Append _{uid} to parent variable so it is unique to THIS block
            # This prevents "Variable already declared" because every block declares its own local reference
            p_var = f"s_{sanitize_var(p_id)}_{uid}"
            
            cypher_lines.append(f"MERGE ({p_var}:Section {{identifier: '{p_id}'}})")
            cypher_lines.append(f"MERGE ({p_var})-[:CONTAINS]->({node_var})")

        # List References
        ref_raw = attrs.get('list_reference') or attrs.get('list_code')
        ref_list = []
        if ref_raw:
            if isinstance(ref_raw, str):
                ref_list = [x.strip() for x in ref_raw.split(',')]
            elif isinstance(ref_raw, list):
                for x in ref_raw:
                    if isinstance(x, str):
                        ref_list.extend([sub.strip() for sub in x.split(',')])
                    else:
                        ref_list.append(str(x))

        for i, ref in enumerate(ref_list):
            if not ref: continue
            ref_clean = clean_text(ref)
            # FIX: Append _{uid}_{i} to make list reference variable unique to this block
            ref_var = f"l_{sanitize_var(ref_clean)}_{uid}_{i}"
            
            if e_class == 'list_reference' and ref_clean == attrs.get('list_code'):
                continue
                
            cypher_lines.append(f"MERGE ({ref_var}:RegulatoryList {{code: '{ref_clean}'}})")
            cypher_lines.append(f"MERGE ({node_var})-[:REFERENCES_LIST]->({ref_var})")

        # Applicability Levels
        levels_raw = attrs.get('healthcare_level') or attrs.get('applicable_level')
        level_list = []
        if levels_raw:
            if isinstance(levels_raw, str):
                level_list = [x.strip() for x in levels_raw.split(',')]
            elif isinstance(levels_raw, list):
                level_list = levels_raw
                
        for i, lvl in enumerate(level_list):
            if not lvl: continue
            lvl_clean = clean_text(lvl)
            # FIX: Append _{uid}_{i} for unique variable scope
            lvl_var = f"p_{sanitize_var(lvl_clean)}_{uid}_{i}"
            
            cypher_lines.append(f"MERGE ({lvl_var}:ProviderType {{level: '{lvl_clean}'}})")
            cypher_lines.append(f"MERGE ({node_var})-[:APPLIES_TO]->({lvl_var})")

        # Medical Codes
        code = attrs.get('code')
        if code:
             c_val = clean_text(code)
             # FIX: Append _{uid} for unique variable scope
             c_var = f"c_{sanitize_var(c_val)}_{uid}"
             
             cypher_lines.append(f"MERGE ({c_var}:Code {{value: '{c_val}'}})")
             cypher_lines.append(f"MERGE ({node_var})-[:HAS_CODE]->({c_var})")

        # Add a semicolon to strictly separate statements if your tool requires it
        cypher_lines.append(";") 
        cypher_lines.append("")

    return "\n".join(cypher_lines)

# Execution block
if __name__ == "__main__":
    try:
        with open('pdf_extractions.jsonl', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        full_script = generate_cypher(data)
        
        with open('output_script.cypher', 'w', encoding='utf-8') as f:
            f.write(full_script)
            
        print("Success! 'output_script.cypher' created.")
        
    except FileNotFoundError:
        print("Error: 'pdf_extractions.jsonl' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")