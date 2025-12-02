import json

def json_to_chatbot_graph(json_data, output_file="CHATBOT_GRAPH.cypher"):
    """
    Yasal sorgu motoru (chatbot) için optimize edilmiş graph
    """
    
    extractions = json_data.get("extractions", [])
    queries = []
    
    # Utility
    def clean(text):
        if not isinstance(text, str):
            return str(text)
        return text.replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ")
    
    def to_label(snake_case):
        components = snake_case.split('_')
        # Özel durumlar için mapping
        label_map = {
            'reference_document': 'ReferenceDoc',
            'regulation_id': 'Regulation',
            'regulation_clause': 'Regulation',
            'legal_amendment': 'Amendment'
        }
        if snake_case in label_map:
            return label_map[snake_case]
        return ''.join(word.capitalize() for word in components)
    
    # Index'ler için extraction'ları grupla
    by_class = {}
    by_group = {}
    
    for ex in extractions:
        cls = ex.get("extraction_class")
        grp = ex.get("group_index")
        
        if cls not in by_class:
            by_class[cls] = []
        by_class[cls].append(ex)
        
        if grp not in by_group:
            by_group[grp] = []
        by_group[grp].append(ex)
    
    # 1. NODE OLUŞTURMA - Full-text search için optimize
    for extraction in extractions:
        ex_class = extraction.get("extraction_class", "Unknown")
        ex_text = clean(extraction.get("extraction_text", ""))
        ex_idx = extraction.get("extraction_index", 0)
        group_idx = extraction.get("group_index", 0)
        attrs = extraction.get("attributes", {})
        
        label = to_label(ex_class)
        
        # Ana properties
        props = [
            f"id: {ex_idx}",
            f"text: '{ex_text}'",
            f"group_id: {group_idx}",
            f"extraction_class: '{ex_class}'"
        ]
        
        # Chatbot için önemli: searchable keywords
        keywords = ex_text.lower().split()[:20]  # İlk 20 kelime
        keywords_str = ', '.join([f"'{w}'" for w in keywords if len(w) > 2])
        props.append(f"keywords: [{keywords_str}]")
        
        # Attributes'ları ekle
        for key, val in attrs.items():
            if val is not None:
                if isinstance(val, str):
                    props.append(f"{key}: '{clean(val)}'")
                elif isinstance(val, (int, float)):
                    props.append(f"{key}: {val}")
        
        props_str = ",\n    ".join(props)
        
        queries.append(f"""
CREATE (n:{label} {{
    {props_str}
}})
""")
    
    # 2. SEMANTIC İLİŞKİLER
    
    # A. REGULATION → Rules (Madde içeriğini tanımlar)
    regulations = by_class.get("regulation", []) + by_class.get("regulation_clause", []) + by_class.get("regulation_id", [])
    
    for reg in regulations:
        reg_id = reg.get("extraction_index")
        reg_group = reg.get("group_index")
        
        # Aynı gruptaki tüm rule'lar bu madde tarafından tanımlanır
        for ex in by_group.get(reg_group, []):
            if ex.get("extraction_index") != reg_id:
                ex_label = to_label(ex.get("extraction_class"))
                ex_id = ex.get("extraction_index")
                
                if any(keyword in ex.get("extraction_class", "") for keyword in ["rule", "prohibition", "obligation"]):
                    queries.append(f"""
MATCH (reg:Regulation {{id: {reg_id}}}),
      (rule:{ex_label} {{id: {ex_id}}})
CREATE (reg)-[:DEFINES {{group: {reg_group}}}]->(rule)
""")
    
    # B. CONDITION → PROHIBITION/OBLIGATION (Şart sonucu tetikler)
    conditions = by_class.get("condition", [])
    prohibitions = by_class.get("prohibition", [])
    obligations = by_class.get("obligation", [])
    
    for cond in conditions:
        cond_id = cond.get("extraction_index")
        cond_group = cond.get("group_index")
        
        # Aynı gruptaki yasaklar
        for prob in prohibitions:
            if prob.get("group_index") == cond_group:
                prob_id = prob.get("extraction_index")
                queries.append(f"""
MATCH (c:Condition {{id: {cond_id}}}),
      (p:Prohibition {{id: {prob_id}}})
CREATE (c)-[:TRIGGERS {{type: 'prohibition'}}]->(p)
""")
        
        # Aynı gruptaki yükümlülükler
        for obl in obligations:
            if obl.get("group_index") == cond_group:
                obl_id = obl.get("extraction_index")
                queries.append(f"""
MATCH (c:Condition {{id: {cond_id}}}),
      (o:Obligation {{id: {obl_id}}})
CREATE (c)-[:REQUIRES {{type: 'obligation'}}]->(o)
""")
    
    # C. RULES → ENTITY (Kurallar varlıklara uygulanır)
    entities = by_class.get("entity", []) + by_class.get("institution", [])
    all_rules = []
    for rule_type in ["payment_rule", "billing_rule", "financial_rule", "deduction_rule"]:
        all_rules.extend(by_class.get(rule_type, []))
    
    for rule in all_rules:
        rule_id = rule.get("extraction_index")
        rule_group = rule.get("group_index")
        rule_label = to_label(rule.get("extraction_class"))
        rule_attrs = rule.get("attributes", {})
        
        # Attributes'larda entity bilgisi var mı?
        target_entity = rule_attrs.get("target_entity") or rule_attrs.get("recipient") or rule_attrs.get("responsible_party")
        
        # Aynı veya yakın gruptaki entity'leri bul
        for entity in entities:
            entity_group = entity.get("group_index")
            entity_id = entity.get("extraction_index")
            entity_text = entity.get("extraction_text", "").lower()
            
            # Entity yakın grupta VE rule'da bahsediliyorsa
            if abs(entity_group - rule_group) <= 2:
                if target_entity and any(word in entity_text for word in target_entity.lower().split()):
                    queries.append(f"""
MATCH (r:{rule_label} {{id: {rule_id}}}),
      (e:Entity {{id: {entity_id}}})
CREATE (r)-[:APPLIES_TO {{target: '{clean(target_entity)}'}}]->(e)
""")
    
    # D. PROHIBITION → ENTITY (Yasaklar varlıkları kısıtlar)
    for prob in prohibitions:
        prob_id = prob.get("extraction_index")
        prob_group = prob.get("group_index")
        prob_attrs = prob.get("attributes", {})
        
        subject = prob_attrs.get("subject") or prob_attrs.get("responsible_party")
        
        if subject:
            for entity in entities:
                entity_group = entity.get("group_index")
                entity_id = entity.get("extraction_index")
                entity_text = entity.get("extraction_text", "").lower()
                
                if abs(entity_group - prob_group) <= 1 and subject.lower() in entity_text:
                    queries.append(f"""
MATCH (p:Prohibition {{id: {prob_id}}}),
      (e:Entity {{id: {entity_id}}})
CREATE (p)-[:PROHIBITS {{subject: '{clean(subject)}'}}]->(e)
""")
    
    # E. RULES → REFERENCE_DOCUMENT (Kurallar belgelere atıfta bulunur)
    ref_docs = by_class.get("reference_document", [])
    
    for ref in ref_docs:
        ref_id = ref.get("extraction_index")
        ref_group = ref.get("group_index")
        
        for rule in all_rules:
            if abs(rule.get("group_index") - ref_group) <= 2:
                rule_id = rule.get("extraction_index")
                rule_label = to_label(rule.get("extraction_class"))
                
                queries.append(f"""
MATCH (rule:{rule_label} {{id: {rule_id}}}),
      (ref:ReferenceDoc {{id: {ref_id}}})
CREATE (rule)-[:REFERENCES]->(ref)
""")
    
    # F. PROCESS → REQUIREMENT (Süreçler gereklilik içerir)
    processes = by_class.get("process", []) + by_class.get("procedure", [])
    requirements = by_class.get("requirement", [])
    
    for proc in processes:
        proc_id = proc.get("extraction_index")
        proc_group = proc.get("group_index")
        proc_label = to_label(proc.get("extraction_class"))
        
        for req in requirements:
            if req.get("group_index") == proc_group:
                req_id = req.get("extraction_index")
                queries.append(f"""
MATCH (p:{proc_label} {{id: {proc_id}}}),
      (r:Requirement {{id: {req_id}}})
CREATE (p)-[:HAS_REQUIREMENT]->(r)
""")
    
    # G. EXCEPTION ilişkileri
    exceptions = by_class.get("exception", [])
    
    for exc in exceptions:
        exc_id = exc.get("extraction_index")
        exc_group = exc.get("group_index")
        
        # Aynı gruptaki regulation'ı bul
        for reg in regulations:
            if reg.get("group_index") == exc_group:
                reg_id = reg.get("extraction_index")
                queries.append(f"""
MATCH (reg:Regulation {{id: {reg_id}}}),
      (exc:Exception {{id: {exc_id}}})
CREATE (reg)-[:HAS_EXCEPTION]->(exc)
""")
    
    # H. GROUP içinde sıralı ilişkiler (bağlam için)
    for group_id, items in by_group.items():
        if len(items) > 1:
            # Group içinde sıralı bağlantı
            sorted_items = sorted(items, key=lambda x: x.get("extraction_index"))
            
            for i in range(len(sorted_items) - 1):
                curr = sorted_items[i]
                next_item = sorted_items[i + 1]
                
                curr_label = to_label(curr.get("extraction_class"))
                next_label = to_label(next_item.get("extraction_class"))
                
                queries.append(f"""
MATCH (curr:{curr_label} {{id: {curr.get("extraction_index")}}}),
      (next:{next_label} {{id: {next_item.get("extraction_index")}}})
CREATE (curr)-[:IN_CONTEXT {{group: {group_id}, order: {i}}}]->(next)
""")
    
    # 3. CHATBOT HELPER QUERIES (dosyanın sonuna ekle)
    helper_queries = [
        """
// ═══════════════════════════════════════════════════════
// CHATBOT YARDIMCI İNDEXLER
// ═══════════════════════════════════════════════════════

// Full-text search için index
CREATE INDEX text_search IF NOT EXISTS FOR (n:PaymentRule) ON (n.text);
CREATE INDEX text_search IF NOT EXISTS FOR (n:Prohibition) ON (n.text);
CREATE INDEX text_search IF NOT EXISTS FOR (n:Obligation) ON (n.text);
CREATE INDEX text_search IF NOT EXISTS FOR (n:Condition) ON (n.text);
CREATE INDEX text_search IF NOT EXISTS FOR (n:Entity) ON (n.text);

// Keyword search için index
CREATE INDEX keyword_search IF NOT EXISTS FOR (n:PaymentRule) ON (n.keywords);
CREATE INDEX keyword_search IF NOT EXISTS FOR (n:Prohibition) ON (n.keywords);
CREATE INDEX keyword_search IF NOT EXISTS FOR (n:Obligation) ON (n.keywords);
""",
        """
// ═══════════════════════════════════════════════════════
// ÖRNEK CHATBOT SORGULARI
// ═══════════════════════════════════════════════════════

// 1. "Laboratuvar hizmeti alındığında ne olur?"
// MATCH (c:Condition)
// WHERE toLower(c.text) CONTAINS 'laboratuvar'
// MATCH (c)-[:TRIGGERS]->(result)
// RETURN result.text as answer;

// 2. "Madde 11 ne diyor?"
// MATCH (reg:Regulation {text: '(11)'})-[:DEFINES]->(content)
// RETURN content.text;

// 3. "Sağlık Bakanlığı hangi kurallara tabi?"
// MATCH (e:Entity)-[:APPLIES_TO]-(rule)
// WHERE toLower(e.text) CONTAINS 'sağlık bakanlığı'
// RETURN rule.text;

// 4. "Hangi durumlarda fatura kesilemez?"
// MATCH (p:Prohibition)
// WHERE toLower(p.text) CONTAINS 'fatura'
// OPTIONAL MATCH (c:Condition)-[:TRIGGERS]->(p)
// RETURN c.text as condition, p.text as prohibition;

// 5. "Bir maddenin tüm içeriğini getir"
// MATCH (reg:Regulation {text: '(10)'})-[:DEFINES*1..3]->(content)
// RETURN content;
"""
    ]
    
    # Dosyaya yaz
    batch_size = 25
    total_batches = (len(queries) + batch_size - 1) // batch_size
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("// ═══════════════════════════════════════════════════════\n")
        f.write("// CHATBOT İÇİN OPTİMİZE EDİLMİŞ NEO4J GRAPH\n")
        f.write("// Yasal Sorgu Motoru - Semantic Relationships\n")
        f.write(f"// Toplam Node: {len(extractions)}\n")
        f.write(f"// Toplam Batch: {total_batches}\n")
        f.write("// ═══════════════════════════════════════════════════════\n\n")
        
        f.write("// 🔗 SEMANTİK İLİŞKİLER:\n")
        f.write("// • DEFINES: Regulation → Rules (Madde kuralları tanımlar)\n")
        f.write("// • TRIGGERS: Condition → Prohibition (Şart yasağı tetikler)\n")
        f.write("// • REQUIRES: Condition → Obligation (Şart yükümlülük gerektirir)\n")
        f.write("// • APPLIES_TO: Rule → Entity (Kural varlığa uygulanır)\n")
        f.write("// • PROHIBITS: Prohibition → Entity (Yasak varlığı kısıtlar)\n")
        f.write("// • REFERENCES: Rule → ReferenceDoc (Kural belgeye atıfta bulunur)\n")
        f.write("// • HAS_REQUIREMENT: Process → Requirement (Süreç gereklilik içerir)\n")
        f.write("// • HAS_EXCEPTION: Regulation → Exception (Maddenin istisnası)\n")
        f.write("// • IN_CONTEXT: Sequential (Aynı grup içinde sıralı bağlam)\n\n")
        
        for batch_num in range(total_batches):
            start = batch_num * batch_size
            end = min(start + batch_size, len(queries))
            
            f.write(f"\n// ───────── BATCH {batch_num + 1}/{total_batches} ─────────\n\n")
            
            for query in queries[start:end]:
                f.write(query.strip() + ";\n\n")
        
        # Helper queries ekle
        for helper in helper_queries:
            f.write(helper + "\n\n")
    
    print(f"✅ CHATBOT GRAPH HAZIR: '{output_file}'")
    print(f"📦 {total_batches} batch")
    print(f"📊 {len(queries)} sorgu")
    print("\n🤖 CHATBOT ÖZELLİKLERİ:")
    print("   ✓ Full-text search (text üzerinde)")
    print("   ✓ Keyword search (hızlı arama)")
    print("   ✓ Semantic relationships (anlamlı ilişkiler)")
    print("   ✓ Contextual queries (bağlamsal sorgular)")
    print("   ✓ Entity-based queries (aktör bazlı)")
    print("   ✓ Regulation navigation (madde navigasyonu)")
    print("\n💡 Örnek sorgular dosyada mevcut!\n")


# KULLANIM
if __name__ == "__main__":
    
    with open('./gemini-3.0-preview/pdf_extractions.jsonl', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    json_to_chatbot_graph(json_data, "CHATBOT_GRAPH.cypher")