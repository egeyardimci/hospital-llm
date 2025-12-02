// Neo4j Cypher Queries - Batched
// Generated from document: doc_16562783

// Batch 1
// -----------------------------

MERGE (doc:Document {document_id: 'doc_16562783'})
ON CREATE SET 
    doc.text_length = 10000,
    doc.extraction_count = 137
RETURN doc.document_id as document_id;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:PaymentRule {
    extraction_index: 1,
    group_index: 0,
    extraction_text: 'tem belgesine dayanılarak kişilere ödenir',
    extraction_class: 'payment_rule',
    start_pos: 0,
    end_pos: 41,
    basis: 'istem belgesi (implied)',
    recipient: 'kişiler',
    action: 'payment'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:DeductionRule {
    extraction_index: 2,
    group_index: 1,
    extraction_text: 'sevk/istem belgesini düzenleyen sözleşme li sağlık hi zmeti sunucusunun alacağından mahsup edilir',
    extraction_class: 'deduction_rule',
    start_pos: 45,
    end_pos: 143,
    target_entity: 'sözleşmeli sağlık hizmeti sunucusu',
    action: 'deduction_from_receivables',
    reason: 'issuing_document'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Entity {
    extraction_index: 3,
    group_index: 2,
    extraction_text: 'Sağlık Bakanlığına bağlı sağlık hizmeti sunucuları',
    extraction_class: 'entity',
    start_pos: 145,
    end_pos: 195,
    affiliation: 'Sağlık Bakanlığı',
    type: 'public_healthcare_provider'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:FinancialMechanism {
    extraction_index: 4,
    group_index: 3,
    extraction_text: 'Bakanlığa yapılan global bütçe ödemesinden mahsup edilir',
    extraction_class: 'financial_mechanism',
    start_pos: 201,
    end_pos: 258,
    source: 'global bütçe',
    action: 'deduction',
    beneficiary: 'Sağlık Bakanlığı'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:RegulationId {
    extraction_index: 5,
    group_index: 4,
    extraction_text: '(10)',
    extraction_class: 'regulation_id',
    start_pos: 261,
    end_pos: 265,
    type: 'clause_number'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Entity {
    extraction_index: 6,
    group_index: 5,
    extraction_text: 'Kurumla sözleşmeli sağlık hizmeti sunucuları',
    extraction_class: 'entity',
    start_pos: 266,
    end_pos: 309,
    relationship: 'contracted',
    counterparty: 'Kurum (SGK)',
    role: 'provider'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Process {
    extraction_index: 7,
    group_index: 6,
    extraction_text: 'bir başka sağlık hizmeti sunucusundan hizmet alımı yoluyla sağladıkları',
    extraction_class: 'process',
    start_pos: 312,
    end_pos: 384,
    type: 'outsourcing',
    method: 'service_procurement'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:ScopeLimitation {
    extraction_index: 8,
    group_index: 7,
    extraction_text: 'ruhsat/faaliyet veya uygunluk belgesinde yer al an tetkik ve/veya tahlil dışındaki tedavilere',
    extraction_class: 'scope_limitation',
    start_pos: 471,
    end_pos: 565,
    document_basis: 'ruhsat/faaliyet/uygunluk belgesi',
    included: 'tetkik ve tahlil',
    excluded: 'diğer tedaviler'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:MedicalProcedures {
    extraction_index: 9,
    group_index: 8,
    extraction_text: '(gastroskopi, kolonoskopi, rektosigmoidoskopi, rektoskopi, bronkoskopi, anjiyografi gibi işlemler de dahil olmak üzere)',
    extraction_class: 'medical_procedures',
    start_pos: 566,
    end_pos: 686,
    type: 'examples_of_excluded_treatments',
    category: 'interventional_procedures'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Prohibition {
    extraction_index: 10,
    group_index: 9,
    extraction_text: 'ait giderleri Kuruma faturalandıramazlar',
    extraction_class: 'prohibition',
    start_pos: 687,
    end_pos: 727,
    action: 'billing',
    target: 'Kurum',
    status: 'prohibited',
    context: 'outsourced_treatments_outside_license'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Condition {
    extraction_index: 11,
    group_index: 10,
    extraction_text: 'Hekim veya diş hekimlerinin, özel sağlık hizmeti sunucusu bünyesinde çalışması halinde',
    extraction_class: 'condition',
    start_pos: 729,
    end_pos: 817,
    subject: 'hekim veya diş hekimleri',
    setting: 'özel sağlık hizmeti sunucusu',
    employment_status: 'working_within'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Exception {
    extraction_index: 12,
    group_index: 11,
    extraction_text: 'bu hekimler tarafından fatura düzenlenerek alınan/sunulan sağlık hizmetleri bu kapsamda değerlendirilmez',
    extraction_class: 'exception',
    start_pos: 819,
    end_pos: 924,
    action: 'individual_invoicing',
    effect: 'exemption_from_prohibition',
    subject: 'doctors_dentists'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Regulation {
    extraction_index: 1,
    group_index: 0,
    extraction_text: '(11)',
    extraction_class: 'regulation',
    start_pos: 927,
    end_pos: 931,
    type: 'article_number',
    context: 'service_procurement_rules'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Condition {
    extraction_index: 2,
    group_index: 1,
    extraction_text: 'Başka bir sağlık hizmeti sunucusundan laboratuvar hizmeti alınması durumunda',
    extraction_class: 'condition',
    start_pos: 932,
    end_pos: 1008,
    context: 'outsourced_laboratory_services',
    trigger: 'service_procurement'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Prohibition {
    extraction_index: 3,
    group_index: 2,
    extraction_text: 'hasta hastane dışına numune almak için gönderilmez',
    extraction_class: 'prohibition',
    start_pos: 1010,
    end_pos: 1061,
    subject: 'hasta',
    forbidden_action: 'sending_patient_for_sample_collection',
    responsible_party: 'sağlık hizmeti sunucusu'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Prohibition {
    extraction_index: 4,
    group_index: 3,
    extraction_text: 'alınan numunenin transferi veya sonucu hasta veya yakını aracılığı ile istenilemez',
    extraction_class: 'prohibition',
    start_pos: 1063,
    end_pos: 1145,
    forbidden_action: 'transfer_via_patient_or_relative',
    items: 'numune transferi veya sonucu',
    intermediary: 'hasta veya yakını'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Condition {
    extraction_index: 5,
    group_index: 4,
    extraction_text: 'Görüntüleme hizmetlerinin hizmet alım ı yoluyla sağlanması halinde',
    extraction_class: 'condition',
    start_pos: 1147,
    end_pos: 1214,
    context: 'outsourced_imaging_services',
    trigger: 'service_procurement'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Obligation {
    extraction_index: 6,
    group_index: 5,
    extraction_text: 'acil ve yatan hastaların transferi sağlık hizmeti sunucuları tarafından yapılacaktır',
    extraction_class: 'obligation',
    start_pos: 1215,
    end_pos: 1300,
    responsible_party: 'sağlık hizmeti sunucuları',
    action: 'patient_transfer',
    patient_type: 'acil ve yatan hastalar',
    requirement: 'mandatory'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Regulation {
    extraction_index: 7,
    group_index: 6,
    extraction_text: '(12)',
    extraction_class: 'regulation',
    start_pos: 1304,
    end_pos: 1308,
    type: 'article_number',
    context: 'documentation_and_audit'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Entity {
    extraction_index: 8,
    group_index: 7,
    extraction_text: 'Kurum ile sözleşmeli sağlık hizmeti sunucuları',
    extraction_class: 'entity',
    start_pos: 1309,
    end_pos: 1354,
    type: 'healthcare_provider',
    contract_status: 'contracted_with_institution'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Obligation {
    extraction_index: 9,
    group_index: 8,
    extraction_text: 'tetkik, tahlil ve tedaviye ait her türlü bilgi, belge ve raporu, istenildiğinde Kuruma ibraz edeceklerdir',
    extraction_class: 'obligation',
    start_pos: 1357,
    end_pos: 1463,
    action: 'submit_documents',
    recipient: 'Kurum (SGK)',
    trigger: 'upon_request',
    content: 'tetkik, tahlil, tedavi bilgileri'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Condition {
    extraction_index: 10,
    group_index: 9,
    extraction_text: 'İbraz edilememesi durumunda',
    extraction_class: 'condition',
    start_pos: 1465,
    end_pos: 1492,
    context: 'failure_to_submit_documents',
    consequence_trigger: 'true'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:FinancialRule {
    extraction_index: 11,
    group_index: 10,
    extraction_text: 'Kuruma faturalandırılan ilgili tetkik, tahlil ve/veya tedavi bedelleri Kurumca karşılanmaz',
    extraction_class: 'financial_rule',
    start_pos: 1493,
    end_pos: 1584,
    result: 'payment_denial',
    payer: 'Kurum',
    reason: 'documentation_failure'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Regulation {
    extraction_index: 12,
    group_index: 11,
    extraction_text: '(13)',
    extraction_class: 'regulation',
    start_pos: 1588,
    end_pos: 1592,
    type: 'article_number',
    context: 'billing_rules'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:FinancialTerm {
    extraction_index: 13,
    group_index: 12,
    extraction_text: 'Kişilere sağlanan sağlık hizmetlerine ilişkin düzenlenen sağlık raporu bedelleri',
    extraction_class: 'financial_term',
    start_pos: 1593,
    end_pos: 1673,
    topic: 'health_report_fees',
    service_type: 'administrative'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:ReferenceDocument {
    extraction_index: 14,
    group_index: 13,
    extraction_text: 'SUT eki EK-2/B Listesinde yer alan rapor puanları',
    extraction_class: 'reference_document',
    start_pos: 1675,
    end_pos: 1725,
    document_name: 'SUT eki EK-2/B',
    usage: 'pricing_basis',
    metric: 'rapor puanları'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:BillingRule {
    extraction_index: 15,
    group_index: 14,
    extraction_text: 'sadece bir adet olarak faturalandırılır',
    extraction_class: 'billing_rule',
    start_pos: 1740,
    end_pos: 1779,
    constraint: 'quantity_limit',
    limit_value: '1',
    action: 'invoicing'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Institution {
    extraction_index: 1,
    group_index: 0,
    extraction_text: 'Kurum birimlerince',
    extraction_class: 'institution',
    start_pos: 1787,
    end_pos: 1805,
    type: 'government_agency',
    role: 'referral_authority',
    context: 'SGK (Social Security Institution)'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Procedure {
    extraction_index: 2,
    group_index: 1,
    extraction_text: 'sevk belgesi düzenlenmek suretiyle',
    extraction_class: 'procedure',
    start_pos: 1806,
    end_pos: 1841,
    action: 'issue_referral_document',
    requirement: 'mandatory_for_referral'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:MedicalContext {
    extraction_index: 3,
    group_index: 2,
    extraction_text: 'maluliyet, meslek hastalığı ve kontrol muayeneleri',
    extraction_class: 'medical_context',
    start_pos: 1842,
    end_pos: 1892,
    type: 'referral_reasons',
    conditions: ['disability', 'occupational_disease', 'control_exam']
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Entity {
    extraction_index: 4,
    group_index: 3,
    extraction_text: 'sağlık hizmeti sunucusuna',
    extraction_class: 'entity',
    start_pos: 1907,
    end_pos: 1932,
    type: 'healthcare_provider',
    role: 'service_provider'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:ScopeDefinition {
    extraction_index: 5,
    group_index: 4,
    extraction_text: 'tedavi amacıyla düzenlenen sağlık raporları dışında kalan',
    extraction_class: 'scope_definition',
    start_pos: 2041,
    end_pos: 2100,
    type: 'exclusion_criteria',
    exception: 'treatment_purposes',
    status: 'defines_non_covered_scope'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:ExcludedServices {
    extraction_index: 6,
    group_index: 5,
    extraction_text: 'engellilik raporu, adli rapor, ehliyet raporu, vasi tayini raporu, portör muayeneleri ve işlemleri, tarama amaçlı muayene ve işlemler',
    extraction_class: 'excluded_services',
    start_pos: 2102,
    end_pos: 2236,
    category: 'special_purpose_reports',
    coverage_status: 'not_covered',
    examples: ['disability_report', 'forensic_report', 'driver_license_report', 'guardianship_report', 'porter_exam', 'screening']
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:PaymentRule {
    extraction_index: 7,
    group_index: 6,
    extraction_text: 'Kurumca karşılanmaz',
    extraction_class: 'payment_rule',
    start_pos: 2357,
    end_pos: 2376,
    payer: 'Kurum (SGK)',
    status: 'payment_denied',
    target: 'special_purpose_reports_and_procedures'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:RegulationId {
    extraction_index: 8,
    group_index: 7,
    extraction_text: '(14)',
    extraction_class: 'regulation_id',
    start_pos: 2379,
    end_pos: 2383,
    type: 'clause_number',
    hierarchy: 'item_14'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:RegulatoryRequirement {
    extraction_index: 9,
    group_index: 8,
    extraction_text: 'SUT gereği düzenlenmesi gereken sağlık kurulu raporu',
    extraction_class: 'regulatory_requirement',
    start_pos: 2456,
    end_pos: 2509,
    source_regulation: 'SUT (Sağlık Uygulama Tebliği)',
    document_type: 'health_board_report',
    context: 'medical_supplies_and_treatment'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:BillingRule {
    extraction_index: 10,
    group_index: 9,
    extraction_text: 'sadece bir adet muayene bedeli faturalandırılabilir',
    extraction_class: 'billing_rule',
    start_pos: 2528,
    end_pos: 2579,
    restriction: 'single_fee',
    item: 'examination_fee',
    context: 'report_issuance'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Procedure {
    extraction_index: 1,
    group_index: 0,
    extraction_text: 'Kurum birimlerince sevk belgesi düzenlenmek suretiyle',
    extraction_class: 'procedure',
    start_pos: 2587,
    end_pos: 2641,
    action: 'referral_document_issuance',
    authority: 'Kurum birimleri',
    requirement: 'mandatory_for_referral'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:MedicalReason {
    extraction_index: 2,
    group_index: 1,
    extraction_text: 'maluliyet, meslek hastalığı ve kontrol muayeneleri',
    extraction_class: 'medical_reason',
    start_pos: 2642,
    end_pos: 2692,
    context: 'referral_reasons',
    types: ['disability', 'occupational_disease', 'control_examination']
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Document {
    extraction_index: 3,
    group_index: 2,
    extraction_text: 'sağlık kurulu raporları',
    extraction_class: 'document',
    start_pos: 2770,
    end_pos: 2793,
    type: 'medical_board_report',
    context: 'referred_patients'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:BillingRule {
    extraction_index: 4,
    group_index: 3,
    extraction_text: 'kurula katılan her bir uzmanlık dalı için muayene bedeli faturalandırılabilir',
    extraction_class: 'billing_rule',
    start_pos: 2813,
    end_pos: 2891,
    action: 'billing',
    item: 'examination_fee',
    condition: 'per_participating_specialty',
    permission: 'allowed'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:RegulationId {
    extraction_index: 5,
    group_index: 4,
    extraction_text: '(15)',
    extraction_class: 'regulation_id',
    start_pos: 2895,
    end_pos: 2899,
    type: 'article_number',
    context: 'SUT_pricing'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Scope {
    extraction_index: 6,
    group_index: 5,
    extraction_text: 'Kurumca finansmanı sağlanan sağlık hizmetleri',
    extraction_class: 'scope',
    start_pos: 2900,
    end_pos: 2945,
    payer: 'Kurum (SGK)',
    subject: 'financed_health_services'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Authority {
    extraction_index: 7,
    group_index: 6,
    extraction_text: 'Sağlık Hizmetleri Fiyatlandırma Komisyonu',
    extraction_class: 'authority',
    start_pos: 2951,
    end_pos: 2992,
    role: 'price_determination',
    type: 'commission'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Reference {
    extraction_index: 8,
    group_index: 7,
    extraction_text: 'SUT ve eki listelerde yer almaktadır',
    extraction_class: 'reference',
    start_pos: 3042,
    end_pos: 3078,
    source: 'SUT (Health Implementation Notification)',
    content: 'prices_to_be_paid'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:ListScope {
    extraction_index: 9,
    group_index: 8,
    extraction_text: 'SUT eki EK-2/B, EK-2/C ve EK-2/Ç listelerinde yer alan işlemler',
    extraction_class: 'list_scope',
    start_pos: 3097,
    end_pos: 3161,
    specific_lists: ['EK-2/B', 'EK-2/C', 'EK-2/Ç'],
    subject: 'medical_procedures'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Parameter {
    extraction_index: 10,
    group_index: 9,
    extraction_text: 'katsayı (0,593)',
    extraction_class: 'parameter',
    start_pos: 3192,
    end_pos: 3207,
    type: 'pricing_coefficient',
    value: 0.593
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:CalculationMethod {
    extraction_index: 11,
    group_index: 10,
    extraction_text: 'işlem bedeli ilgili puan ile katsayının çarpımı sonucu bulunacak tutardır',
    extraction_class: 'calculation_method',
    start_pos: 3225,
    end_pos: 3299,
    formula: 'score * coefficient',
    output: 'transaction_price'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:FormattingRule {
    extraction_index: 12,
    group_index: 11,
    extraction_text: 'yuvarlama işlemi yapılmaksızın virgülden sonra iki basamak olacak şekilde alınır',
    extraction_class: 'formatting_rule',
    start_pos: 3442,
    end_pos: 3523,
    rounding: 'none',
    precision: 'two_decimal_places',
    context: 'price_calculation'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;


// Batch 2
// -----------------------------

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Regulation {
    extraction_index: 1,
    group_index: 0,
    extraction_text: '(16)',
    extraction_class: 'regulation',
    start_pos: 3526,
    end_pos: 3530,
    type: 'article_number',
    context: 'billing_exclusions'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:MedicalScope {
    extraction_index: 2,
    group_index: 1,
    extraction_text: 'Sağlık hizmeti sunucularınca gerçekleştirilecek check-up, kampanya ya da tarama kapsamında yapılan işlemler',
    extraction_class: 'medical_scope',
    start_pos: 3531,
    end_pos: 3638,
    provider: 'sağlık hizmeti sunucuları',
    excluded_activities: 'check-up, kampanya, tarama',
    status: 'non_reimbursable'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:BillingRule {
    extraction_index: 3,
    group_index: 2,
    extraction_text: 'Kuruma faturalandırılmaz',
    extraction_class: 'billing_rule',
    start_pos: 3640,
    end_pos: 3664,
    action: 'billing_prohibition',
    payer: 'Kurum (SGK)',
    beneficiary: 'sağlık hizmeti sunucusu'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Regulation {
    extraction_index: 4,
    group_index: 3,
    extraction_text: '(17)',
    extraction_class: 'regulation',
    start_pos: 3667,
    end_pos: 3671,
    type: 'article_number',
    context: 'surgical_method_pricing'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:ReferenceDocument {
    extraction_index: 5,
    group_index: 4,
    extraction_text: 'SUT eki EK-2/B ve EK-2/C listelerinde yer alan işlemlerin',
    extraction_class: 'reference_document',
    start_pos: 3672,
    end_pos: 3729,
    document: 'SUT',
    appendices: ['EK-2/B', 'EK-2/C'],
    content: 'medical_procedures'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:MedicalMethod {
    extraction_index: 6,
    group_index: 5,
    extraction_text: 'laparoskopik, perkütan, endoskopik, endosonografik, mikrocerrahi, robotik cerrahi gibi yöntemlerle yapılması halinde',
    extraction_class: 'medical_method',
    start_pos: 3730,
    end_pos: 3847,
    type: 'advanced_surgical_techniques',
    condition: 'method_application'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:PaymentRule {
    extraction_index: 7,
    group_index: 6,
    extraction_text: 'SUT’ta yer alan işlem puanı esas alınarak Kurumca karşılanır',
    extraction_class: 'payment_rule',
    start_pos: 3857,
    end_pos: 3918,
    payer: 'Kurum',
    calculation_basis: 'standard_procedure_score',
    condition: 'no_separate_code'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:MedicalProcedure {
    extraction_index: 8,
    group_index: 7,
    extraction_text: 'ayrı kodu bulunan laparoskopik, perkütan, endoskopik, endosonografik, mikrocerrahi, robotik cerrahi gibi yöntemlerle yapılan işlemler',
    extraction_class: 'medical_procedure',
    start_pos: 3926,
    end_pos: 4060,
    characteristic: 'has_separate_code',
    method_types: 'advanced_surgery'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:PaymentRule {
    extraction_index: 9,
    group_index: 8,
    extraction_text: 'kendi puanı esas alınarak Kurumca karşılanır',
    extraction_class: 'payment_rule',
    start_pos: 4061,
    end_pos: 4105,
    payer: 'Kurum',
    calculation_basis: 'specific_method_score',
    condition: 'separate_code_exists'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Regulation {
    extraction_index: 10,
    group_index: 9,
    extraction_text: '(18)',
    extraction_class: 'regulation',
    start_pos: 4109,
    end_pos: 4113,
    type: 'article_number',
    context: 'traffic_accident_coverage'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Scenario {
    extraction_index: 11,
    group_index: 10,
    extraction_text: 'Trafik kazası nedeniyle ilk müdahalenin sözleşmesiz sağlık hizmeti sunucularında sağlanması halinde',
    extraction_class: 'scenario',
    start_pos: 4114,
    end_pos: 4213,
    cause: 'traffic_accident',
    intervention_type: 'first_response',
    provider_status: 'non_contracted (sözleşmesiz)'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:CoverageScope {
    extraction_index: 12,
    group_index: 11,
    extraction_text: 'bu sağlık hizmeti sunucusunda trafik kazası nedeniyle sunulan sağlık hizmetinin devamı niteliğinde olan tedaviler',
    extraction_class: 'coverage_scope',
    start_pos: 4214,
    end_pos: 4328,
    location: 'same_provider',
    nature: 'continuation_of_treatment',
    cause: 'traffic_accident'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:PaymentRule {
    extraction_index: 13,
    group_index: 12,
    extraction_text: 'SUT ve ekleri esas alınarak Kurumca karşılanacaktır',
    extraction_class: 'payment_rule',
    start_pos: 4329,
    end_pos: 4381,
    payer: 'Kurum',
    basis: 'SUT_and_appendices',
    status: 'covered'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:TimeLimitation {
    extraction_index: 14,
    group_index: 13,
    extraction_text: 'trafik kazasının oluştuğu tarihten itibaren 6 ayı geçemez',
    extraction_class: 'time_limitation',
    start_pos: 4397,
    end_pos: 4454,
    start_event: 'traffic_accident_date',
    duration: '6 months',
    restriction: 'maximum_coverage_period'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:RegulationClause {
    extraction_index: 1,
    group_index: 0,
    extraction_text: '(19)',
    extraction_class: 'regulation_clause',
    start_pos: 4457,
    end_pos: 4461,
    type: 'paragraph_number',
    context: 'general_provisions'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Requirement {
    extraction_index: 2,
    group_index: 1,
    extraction_text: 'geri ödeme kural ve/veya kriterleri belirlenmemiş sağlık hizmetleri için güncel bilimsel klinik uygunluğun bulunması gerekir',
    extraction_class: 'requirement',
    start_pos: 4511,
    end_pos: 4636,
    condition: 'geri ödeme kuralı/kriteri yokluğu',
    required_standard: 'güncel bilimsel klinik uygunluk',
    context: 'Kurumca finansmanı sağlanan hizmetler'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:RegulationClause {
    extraction_index: 3,
    group_index: 2,
    extraction_text: '(20)',
    extraction_class: 'regulation_clause',
    start_pos: 4639,
    end_pos: 4643,
    type: 'paragraph_number',
    context: 'billing_procedures'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:ReferenceList {
    extraction_index: 4,
    group_index: 3,
    extraction_text: 'SUT eki EK -2/C-1 Listesinde',
    extraction_class: 'reference_list',
    start_pos: 4644,
    end_pos: 4672,
    type: 'medical_procedure_list',
    document: 'SUT'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:ProviderDefinition {
    extraction_index: 5,
    group_index: 4,
    extraction_text: 'SUT eki EK -2/A-1 Listesinde Sınıf -3 grubunda tanımlanan sağlık hizmeti sunucularınca',
    extraction_class: 'provider_definition',
    start_pos: 4693,
    end_pos: 4780,
    classification: 'Sınıf -3',
    reference_list: 'EK -2/A-1'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:BillingRule {
    extraction_index: 6,
    group_index: 5,
    extraction_text: 'işlem puanlarına Listede belirtilen oranlar ilave edilerek faturalandırılır',
    extraction_class: 'billing_rule',
    start_pos: 4799,
    end_pos: 4874,
    action: 'add_rate_to_points',
    trigger: 'specific_provider_class_performing_specific_list_items'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:LegalExclusion {
    extraction_index: 7,
    group_index: 6,
    extraction_text: '“ 2.2.2.B- Tanıya dayalı işlem üzerinden ödeme yöntemi” başlıklı maddenin beşinci fıkrasında yer alan hüküm uygulanmaz',
    extraction_class: 'legal_exclusion',
    start_pos: 4921,
    end_pos: 5040,
    excluded_regulation: '2.2.2.B - 5th paragraph',
    reason: 'special_billing_rule_application'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:RegulationHeader {
    extraction_index: 8,
    group_index: 7,
    extraction_text: '2.2.1 - Ayakta tedavilerde ödeme',
    extraction_class: 'regulation_header',
    start_pos: 5043,
    end_pos: 5075,
    topic: 'outpatient_payment',
    level: 'main_section'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:RegulationHeader {
    extraction_index: 9,
    group_index: 8,
    extraction_text: '2.2.1.A - Birinci basamak sağlık kuruluşları',
    extraction_class: 'regulation_header',
    start_pos: 5077,
    end_pos: 5121,
    topic: 'primary_care_providers',
    level: 'subsection'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:RegulationClause {
    extraction_index: 10,
    group_index: 9,
    extraction_text: '(1)',
    extraction_class: 'regulation_clause',
    start_pos: 5123,
    end_pos: 5126,
    type: 'paragraph_number',
    context: 'payment_amounts'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:PaymentRule {
    extraction_index: 11,
    group_index: 10,
    extraction_text: 'Birinci basamak sağlık kuruluşlarındaki ayakta tedavilerde, her başvuru için 11 (onbir) TL ödeme yapılır',
    extraction_class: 'payment_rule',
    start_pos: 5127,
    end_pos: 5231,
    provider_type: 'birinci basamak',
    service_type: 'ayakta tedavi',
    amount: '11 TL',
    unit: 'per_visit'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:PaymentRule {
    extraction_index: 12,
    group_index: 11,
    extraction_text: 'Hastanın diğer bir sağlık kurumuna sevk edilmesi halinde ise sadece 5 (beş) TL ödeme yapılır',
    extraction_class: 'payment_rule',
    start_pos: 5234,
    end_pos: 5326,
    condition: 'patient_referral',
    amount: '5 TL',
    change_type: 'reduction'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:RegulationHeader {
    extraction_index: 13,
    group_index: 12,
    extraction_text: '2.2.1.B - İkinci ve üçüncü basamak sağlık kurumları',
    extraction_class: 'regulation_header',
    start_pos: 5334,
    end_pos: 5385,
    topic: 'secondary_and_tertiary_care_providers',
    level: 'subsection'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:LegalAmendment {
    extraction_index: 14,
    group_index: 13,
    extraction_text: 'Değişik: RG- 25/08/2022- 31934/ 12-b md.',
    extraction_class: 'legal_amendment',
    start_pos: 5388,
    end_pos: 5428,
    gazette_date: '25/08/2022',
    gazette_number: '31934',
    article: '12-b'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:EffectiveDate {
    extraction_index: 15,
    group_index: 14,
    extraction_text: 'Yürürlük: 03/09/2022',
    extraction_class: 'effective_date',
    start_pos: 5429,
    end_pos: 5449,
    date: '03/09/2022',
    type: 'enforcement_date'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:RegulationHeader {
    extraction_index: 1,
    group_index: 0,
    extraction_text: '1.B-1 - Ayakta tedavilerde ödeme uygulaması',
    extraction_class: 'regulation_header',
    start_pos: 5457,
    end_pos: 5500,
    code: '1.B-1',
    topic: 'outpatient_payment_rules'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Scope {
    extraction_index: 2,
    group_index: 1,
    extraction_text: '“Ayakta tedavilerde ödeme” uygulaması kapsamında',
    extraction_class: 'scope',
    start_pos: 5506,
    end_pos: 5554,
    context: 'outpatient_services',
    type: 'payment_framework'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:BillingUnit {
    extraction_index: 3,
    group_index: 2,
    extraction_text: 'sağlık hizmeti sunucusunda ayaktan her bir başvuru için',
    extraction_class: 'billing_unit',
    start_pos: 5556,
    end_pos: 5611,
    unit: 'per_visit',
    setting: 'outpatient',
    provider: 'healthcare_provider'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:ReferenceDocument {
    extraction_index: 4,
    group_index: 3,
    extraction_text: 'SUT eki “Sağlık Hizmeti Sunucularının Ayakta Tedavilerde Sınıflandırılması Listesi” nde (EK -2/A-1)',
    extraction_class: 'reference_document',
    start_pos: 5614,
    end_pos: 5713,
    code: 'EK-2/A-1',
    purpose: 'provider_classification',
    document_type: 'SUT_annex'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:PaymentRule {
    extraction_index: 5,
    group_index: 4,
    extraction_text: 'SUT eki EK-2/A Listesinde yer alan tutarlar esas alınarak ödeme yapılır',
    extraction_class: 'payment_rule',
    start_pos: 5754,
    end_pos: 5825,
    basis: 'EK-2/A List',
    action: 'payment_calculation',
    standard_rate: '1x'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:LegalAmendment {
    extraction_index: 6,
    group_index: 5,
    extraction_text: '(Ek:RG-09/05/2024-32541/1-a md. Yürürlük:11/05/2024)',
    extraction_class: 'legal_amendment',
    start_pos: 5827,
    end_pos: 5880,
    gazette_date: '09/05/2024',
    gazette_number: '32541',
    effective_date: '11/05/2024',
    type: 'regulation_update'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:AdministrativeProcess {
    extraction_index: 7,
    group_index: 6,
    extraction_text: 'Sağlık Bakanlığı tarafından Kuruma bildirilen',
    extraction_class: 'administrative_process',
    start_pos: 5881,
    end_pos: 5926,
    sender: 'Ministry of Health',
    receiver: 'SGK (The Institution)',
    action: 'notification'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Condition {
    extraction_index: 8,
    group_index: 7,
    extraction_text: 'mesai saatlerinde aynı gün randevusu dolu olan branşlarda',
    extraction_class: 'condition',
    start_pos: 5928,
    end_pos: 5986,
    status: 'capacity_full',
    timing: 'working_hours',
    context: 'appointment_availability'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:InstitutionType {
    extraction_index: 9,
    group_index: 8,
    extraction_text: 'Sağlık Bakanlığına bağlı ikinci ve üçüncü basamak sağlık hizmeti sunucularında',
    extraction_class: 'institution_type',
    start_pos: 5988,
    end_pos: 6066,
    affiliation: 'Ministry of Health',
    level: '2nd_and_3rd_tier',
    type: 'public_hospital'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:ServiceDetail {
    extraction_index: 10,
    group_index: 9,
    extraction_text: 'uzman hekimler tarafından mesai saatleri dışında sunulan poliklinik hizmetleri için',
    extraction_class: 'service_detail',
    start_pos: 6067,
    end_pos: 6151,
    provider: 'specialist_doctor',
    timing: 'after_hours',
    service_type: 'polyclinic'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:PaymentCalculation {
    extraction_index: 11,
    group_index: 10,
    extraction_text: 'EK -2/A Listesinde yer alan tutarların iki katı esas alınarak ödeme yapılır',
    extraction_class: 'payment_calculation',
    start_pos: 6152,
    end_pos: 6227,
    multiplier: '2.0',
    basis: 'EK-2/A List',
    reason: 'after_hours_capacity_overflow'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:ReferenceDocument {
    extraction_index: 12,
    group_index: 11,
    extraction_text: 'SUT eki “Ayaktan Başvurularda İlave Olarak Faturalandırılabilecek İşlemler Listesi” nde (EK -2/A-2)',
    extraction_class: 'reference_document',
    start_pos: 6238,
    end_pos: 6337,
    code: 'EK-2/A-2',
    purpose: 'additional_billing',
    document_type: 'SUT_annex'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:CoverageRule {
    extraction_index: 13,
    group_index: 12,
    extraction_text: 'yer alan işlemlerin bedelleri Kurumca karşılanır',
    extraction_class: 'coverage_rule',
    start_pos: 6338,
    end_pos: 6387,
    payer: 'SGK (The Institution)',
    status: 'covered',
    subject: 'additional_procedures'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Condition {
    extraction_index: 1,
    group_index: 0,
    extraction_text: '(2) Hastanın aynı sağlık hizmeti sunucusuna',
    extraction_class: 'condition',
    start_pos: 6390,
    end_pos: 6433,
    subject: 'hasta',
    context: 'recurring_visit',
    provider_scope: 'same_provider'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Exception {
    extraction_index: 2,
    group_index: 1,
    extraction_text: 'acil servise başvuruları hariç olmak üzere',
    extraction_class: 'exception',
    start_pos: 6435,
    end_pos: 6477,
    excluded_department: 'acil servis',
    rule_context: '10_day_limit'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:TimeframeRule {
    extraction_index: 3,
    group_index: 2,
    extraction_text: 'ayaktan başvurduğu gün dâhil, 10 (on) gün içindeki aynı uzmanlık dalına diğer ayaktan başvurularında',
    extraction_class: 'timeframe_rule',
    start_pos: 6478,
    end_pos: 6579,
    duration: '10 days',
    specialty_scope: 'same_specialty',
    visit_type: 'outpatient'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:BillingPermission {
    extraction_index: 4,
    group_index: 3,
    extraction_text: 'sadece SUT eki EK -2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılabilecek',
    extraction_class: 'billing_permission',
    start_pos: 6581,
    end_pos: 6670,
    status: 'allowed',
    reference_list: 'EK-2/A-2',
    item_type: 'procedures'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:BillingProhibition {
    extraction_index: 5,
    group_index: 4,
    extraction_text: 'SUT eki EK-2/A Listesinde yer alan tutar faturalandırılamaz',
    extraction_class: 'billing_prohibition',
    start_pos: 6676,
    end_pos: 6735,
    status: 'prohibited',
    reference_list: 'EK-2/A',
    item_type: 'examination_fee'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:LegalAmendment {
    extraction_index: 6,
    group_index: 5,
    extraction_text: '(Değişik:RG- 09/05/2024-32541/1-b md. Yürürlük: 11/05/2024)',
    extraction_class: 'legal_amendment',
    start_pos: 6758,
    end_pos: 6817,
    official_gazette_date: '09/05/2024',
    effective_date: '11/05/2024',
    gazette_number: '32541'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:MedicalScope {
    extraction_index: 7,
    group_index: 6,
    extraction_text: 'EK-2/A-2 ve EK -2/C Listelerinde yer alan işlemlerin yapılmasının gerekli görülmesi',
    extraction_class: 'medical_scope',
    start_pos: 6820,
    end_pos: 6904,
    reference_lists: ['EK-2/A-2', 'EK-2/C'],
    condition: 'medical_necessity'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:ProcessCondition {
    extraction_index: 8,
    group_index: 7,
    extraction_text: 'bu muayene başvurusundan sonra aynı sağlık hizmeti sunucusunda randevu verilmek suretiyle ileri bir tarihte yapılması durumunda',
    extraction_class: 'process_condition',
    start_pos: 6935,
    end_pos: 7063,
    timing: 'deferred/future_date',
    mechanism: 'appointment',
    location: 'same_provider'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;


// Batch 3
// -----------------------------

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:BillingRule {
    extraction_index: 9,
    group_index: 8,
    extraction_text: 'SUT eki EK-2/A Listesinde yer alan tutarlar ikinci bir defa girilmeksizin sadece yapılan işlem faturalandırılır',
    extraction_class: 'billing_rule',
    start_pos: 7065,
    end_pos: 7177,
    restriction: 'no_double_billing_for_exam',
    allowed_billing: 'procedure_only',
    reference_list_excluded: 'EK-2/A'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:RegulationId {
    extraction_index: 1,
    group_index: 0,
    extraction_text: '(4)',
    extraction_class: 'regulation_id',
    start_pos: 7180,
    end_pos: 7183,
    type: 'paragraph_number',
    context: 'billing_regulations'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:MedicalEvent {
    extraction_index: 2,
    group_index: 1,
    extraction_text: 'Hastanın aynı sağlık hizmeti sunucusunda aynı uzmanlık dalına ayaktan başvurusu',
    extraction_class: 'medical_event',
    start_pos: 7184,
    end_pos: 7263,
    actor: 'hasta',
    location: 'aynı sağlık hizmeti sunucusu',
    specialty: 'aynı uzmanlık dalı',
    type: 'outpatient_visit'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:TemporalContext {
    extraction_index: 3,
    group_index: 2,
    extraction_text: 'sonrasında aynı gün “yatarak tedavi” kapsamında',
    extraction_class: 'temporal_context',
    start_pos: 7264,
    end_pos: 7312,
    timing: 'same_day',
    treatment_type: 'inpatient',
    relation: 'follows_outpatient_visit'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Condition {
    extraction_index: 4,
    group_index: 3,
    extraction_text: 'SUT eki EK -2/C Listesinde yer alan bir işlem yapılması halinde',
    extraction_class: 'condition',
    start_pos: 7314,
    end_pos: 7377,
    reference_list: 'SUT EK-2/C',
    trigger_event: 'procedure_performance',
    context: 'inpatient_transition'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:BillingRule {
    extraction_index: 5,
    group_index: 4,
    extraction_text: 'bu işlem ile birlikte ayaktan yapılan işlemler bu maddenin b irinci fıkrasındaki hükümlere göre faturalandırılır',
    extraction_class: 'billing_rule',
    start_pos: 7378,
    end_pos: 7491,
    scope: 'combined_procedures',
    reference_regulation: 'madde 1. fıkra',
    action: 'bill_accordingly'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:ExceptionCondition {
    extraction_index: 6,
    group_index: 5,
    extraction_text: 'Ancak “yatarak tedavi” kapsamında hizmet başına ödeme yöntemi ile bir işlem yapılması durumunda',
    extraction_class: 'exception_condition',
    start_pos: 7493,
    end_pos: 7589,
    type: 'exception',
    payment_method: 'fee_for_service',
    context: 'inpatient_treatment'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:BillingProhibition {
    extraction_index: 7,
    group_index: 6,
    extraction_text: 'SUT eki EK -2/A Listesinde yer alan tutarlar faturalandırılmayacak',
    extraction_class: 'billing_prohibition',
    start_pos: 7590,
    end_pos: 7656,
    reference_list: 'SUT EK-2/A',
    action: 'do_not_bill',
    status: 'prohibited'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:BillingRequirement {
    extraction_index: 8,
    group_index: 7,
    extraction_text: 'ayaktan başvurular da hizmet başına ödeme yöntemine göre faturalandırılacaktır',
    extraction_class: 'billing_requirement',
    start_pos: 7663,
    end_pos: 7741,
    scope: 'outpatient_visits',
    payment_method: 'fee_for_service',
    obligation: 'mandatory'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Regulation {
    extraction_index: 1,
    group_index: 0,
    extraction_text: '(5)',
    extraction_class: 'regulation',
    start_pos: 7745,
    end_pos: 7748,
    type: 'clause_number',
    context: 'billing_regulations'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Scenario {
    extraction_index: 2,
    group_index: 1,
    extraction_text: 'Hastanın aynı gün içerisinde, aynı sağlık hizmeti sunucusunda; birden fazla uzmanlık dalına başvurusu sonrasında',
    extraction_class: 'scenario',
    start_pos: 7749,
    end_pos: 7861,
    subject: 'hasta',
    timeframe: 'same_day',
    location: 'same_provider',
    event: 'multiple_specialty_applications'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Condition {
    extraction_index: 3,
    group_index: 2,
    extraction_text: 'bu uzmanlık dallarından herhangi birinde aynı gün “yatarak tedavi” kapsamında SUT eki EK-2/C Listesinde yer alan bir işlem yapılması halind e',
    extraction_class: 'condition',
    start_pos: 7863,
    end_pos: 8005,
    treatment_type: 'inpatient',
    reference_list: 'SUT EK-2/C',
    trigger_event: 'procedure_performance'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:BillingRule {
    extraction_index: 4,
    group_index: 3,
    extraction_text: 'bu işlem ile birlikte, o uzmanlık dalına ait ayaktan yapılan işlemler bu maddenin birinci fıkrasındaki hükümlere göre',
    extraction_class: 'billing_rule',
    start_pos: 8006,
    end_pos: 8124,
    scope: 'related_specialty_outpatient_procedures',
    reference_regulation: 'paragraph_1',
    billing_method: 'standard_procedure'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:BillingRule {
    extraction_index: 5,
    group_index: 4,
    extraction_text: 'diğer uzmanlık dallarındaki ayakta tedavi kapsamındaki başvuruları SUT eki EK -2/B Listesindeki “normal poliklinik muayenesi” bedeli',
    extraction_class: 'billing_rule',
    start_pos: 8126,
    end_pos: 8259,
    scope: 'other_specialties',
    reference_list: 'SUT EK-2/B',
    billable_item: 'normal_polyclinic_exam'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:BillingRule {
    extraction_index: 6,
    group_index: 5,
    extraction_text: 've yapılması halinde SUT eki EK -2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılacaktır',
    extraction_class: 'billing_rule',
    start_pos: 8260,
    end_pos: 8362,
    condition: 'if_performed',
    reference_list: 'SUT EK-2/A-2',
    action: 'bill_procedure_cost'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:ExceptionCondition {
    extraction_index: 7,
    group_index: 6,
    extraction_text: 'Ancak, yatarak tedavi kapsamında hizmet başına ödeme yöntemi ile bir işlem yapılması durumunda',
    extraction_class: 'exception_condition',
    start_pos: 8364,
    end_pos: 8458,
    context: 'inpatient_treatment',
    payment_method: 'fee_for_service',
    type: 'exception_trigger'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Prohibition {
    extraction_index: 8,
    group_index: 7,
    extraction_text: 'SUT eki EK-2/A Listesinde yer alan tutarlar faturalandırılmay acak',
    extraction_class: 'prohibition',
    start_pos: 8460,
    end_pos: 8527,
    reference_list: 'SUT EK-2/A',
    action: 'do_not_bill',
    status: 'prohibited'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:BillingInstruction {
    extraction_index: 9,
    group_index: 8,
    extraction_text: 'olup ayaktan yapılan işlemler hizmet başına ödeme yöntemine göre faturalandırılacaktır',
    extraction_class: 'billing_instruction',
    start_pos: 8528,
    end_pos: 8615,
    scope: 'outpatient_procedures',
    billing_method: 'fee_for_service',
    requirement: 'mandatory'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:RegulationMarker {
    extraction_index: 1,
    group_index: 0,
    extraction_text: '(6)',
    extraction_class: 'regulation_marker',
    start_pos: 8619,
    end_pos: 8622,
    type: 'paragraph_number',
    context: 'billing_rules'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:MedicalScenario {
    extraction_index: 2,
    group_index: 1,
    extraction_text: 'Hastanın, aynı gün içinde aynı sağlık hizmeti sunucusunda ilk muayenesini takip eden diğer uzmanlık dallarındaki ayakta tedavi kapsamında yer alan başvuruları',
    extraction_class: 'medical_scenario',
    start_pos: 8623,
    end_pos: 8781,
    condition: 'multiple_visits_same_day',
    location: 'same_health_provider',
    specialty_context: 'different_specialties',
    treatment_type: 'outpatient'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:BillingRule {
    extraction_index: 3,
    group_index: 2,
    extraction_text: '“ayakta tedavilerde ödeme” uygulaması kapsamında değerlendirilmez',
    extraction_class: 'billing_rule',
    start_pos: 8784,
    end_pos: 8849,
    payment_model: 'ayakta tedavilerde ödeme',
    status: 'excluded'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:BillingProhibition {
    extraction_index: 4,
    group_index: 3,
    extraction_text: 'SUT eki EK-2/A Listesinde yer alan tutarlar faturalandırılamaz',
    extraction_class: 'billing_prohibition',
    start_pos: 8853,
    end_pos: 8916,
    reference_list: 'SUT eki EK-2/A',
    action: 'billing',
    permission: 'forbidden'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:BillingPermission {
    extraction_index: 5,
    group_index: 4,
    extraction_text: 'SUT eki EK-2/B Listesindeki “normal poliklinik muayenesi” bedeli ve yapılması halinde SUT eki EK-2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılacaktır',
    extraction_class: 'billing_permission',
    start_pos: 8924,
    end_pos: 9090,
    reference_list_1: 'SUT eki EK-2/B',
    item_1: 'normal poliklinik muayenesi',
    reference_list_2: 'SUT eki EK-2/A-2',
    permission: 'mandatory'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:RegulationMarker {
    extraction_index: 6,
    group_index: 5,
    extraction_text: '(7)',
    extraction_class: 'regulation_marker',
    start_pos: 9093,
    end_pos: 9096,
    type: 'paragraph_number',
    context: 'main_branch_sub_branch_billing'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:MedicalScenario {
    extraction_index: 7,
    group_index: 6,
    extraction_text: 'Hastanın aynı gün içinde aynı sağlık hizmeti sunucusundaki ilk başvurusunun ana dal, sonraki başvurusunun yan dal olması durumunda',
    extraction_class: 'medical_scenario',
    start_pos: 9097,
    end_pos: 9228,
    condition: 'main_branch_to_sub_branch',
    timing: 'same_day',
    location: 'same_health_provider'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:BillingRule {
    extraction_index: 8,
    group_index: 7,
    extraction_text: 'yan dala olan başvuru "ayakta tedavilerde ödeme” uygulaması kapsamında faturalandırılır',
    extraction_class: 'billing_rule',
    start_pos: 9229,
    end_pos: 9316,
    subject: 'yan dal başvurusu',
    payment_model: 'ayakta tedavilerde ödeme',
    status: 'included'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:ContextSwitch {
    extraction_index: 9,
    group_index: 8,
    extraction_text: 'Ana dala başvuru ise',
    extraction_class: 'context_switch',
    start_pos: 9318,
    end_pos: 9339,
    subject: 'ana dal başvurusu',
    role: 'contrast_case'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:BillingRestriction {
    extraction_index: 10,
    group_index: 9,
    extraction_text: 'SUT eki EK -2/A Listesinde yer alan tuta rlar girilmeksizin',
    extraction_class: 'billing_restriction',
    start_pos: 9341,
    end_pos: 9400,
    reference_list: 'SUT eki EK -2/A',
    action: 'data_entry',
    status: 'omitted'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:BillingPermission {
    extraction_index: 11,
    group_index: 10,
    extraction_text: 'SUT eki EK -2/B Listesindeki “normal poliklinik muayenesi” bedeli ve yapılması halinde SUT eki EK-2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılabilir',
    extraction_class: 'billing_permission',
    start_pos: 9402,
    end_pos: 9568,
    reference_list_1: 'SUT eki EK -2/B',
    item_1: 'normal poliklinik muayenesi',
    reference_list_2: 'SUT eki EK-2/A-2',
    permission: 'allowed'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:RegulationClause {
    extraction_index: 1,
    group_index: 0,
    extraction_text: '(8)',
    extraction_class: 'regulation_clause',
    start_pos: 9571,
    end_pos: 9574,
    number: '8',
    type: 'article_subsection'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Requirement {
    extraction_index: 2,
    group_index: 1,
    extraction_text: 'Sağlık raporu ile yapılması gerekli görülen',
    extraction_class: 'requirement',
    start_pos: 9575,
    end_pos: 9618,
    document: 'sağlık raporu',
    necessity: 'mandatory',
    context: 'treatment_prerequisite'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:MedicalScope {
    extraction_index: 3,
    group_index: 2,
    extraction_text: 'hiperbarik oksijen tedavisi, fizik tedavi ve rehabilitasyon, ESWL ve ESWT tedavilerinde',
    extraction_class: 'medical_scope',
    start_pos: 9619,
    end_pos: 9707,
    treatments: ['hiperbarik oksijen', 'fizik tedavi', 'rehabilitasyon', 'ESWL', 'ESWT'],
    category: 'specialized_treatments'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:PatientStatus {
    extraction_index: 4,
    group_index: 3,
    extraction_text: 'ayaktan başvurularda',
    extraction_class: 'patient_status',
    start_pos: 9709,
    end_pos: 9729,
    type: 'outpatient',
    context: 'application_mode'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:ProcessStep {
    extraction_index: 5,
    group_index: 4,
    extraction_text: 'tedavi için sağlık raporu düzenlendikten sonra',
    extraction_class: 'process_step',
    start_pos: 9730,
    end_pos: 9776,
    action: 'report_issuance',
    timing: 'post_issuance',
    sequence: 'prerequisite_met'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Condition {
    extraction_index: 6,
    group_index: 5,
    extraction_text: 'tedavinin sonraki günlerde aynı veya başka bir sağl ık hizmeti sunucusunda yapılması halinde',
    extraction_class: 'condition',
    start_pos: 9777,
    end_pos: 9870,
    timing: 'subsequent_days',
    provider_flexibility: 'same_or_different_provider',
    scenario: 'continuation_of_treatment'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:Subject {
    extraction_index: 7,
    group_index: 6,
    extraction_text: 'bu sağlık raporu ile yapılan tedavi başvuruları',
    extraction_class: 'subject',
    start_pos: 9872,
    end_pos: 9919,
    reference: 'treatment_applications',
    basis: 'health_report'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:PaymentContext {
    extraction_index: 8,
    group_index: 7,
    extraction_text: '"ayakta tedavilerde ödeme” uygulaması kapsamında',
    extraction_class: 'payment_context',
    start_pos: 9920,
    end_pos: 9969,
    scheme: 'outpatient_payment',
    type: 'reimbursement_model'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (doc:Document {document_id: 'doc_16562783'})
CREATE (e:RegulationReference {
    extraction_index: 9,
    group_index: 8,
    extraction_text: 'SUT eki EK-2/A Listesinde yer',
    extraction_class: 'regulation_reference',
    start_pos: 9970,
    end_pos: 9999,
    source: 'SUT (Sağlık Uygulama Tebliği)',
    list_code: 'EK-2/A',
    status: 'listed/included'
})
CREATE (doc)-[:HAS_EXTRACTION]->(e)
RETURN e.extraction_index as created_index;

MATCH (e1:PaymentRule {extraction_index: 1}),
      (e2:Regulation {extraction_index: 1})
CREATE (e1)-[:GROUPED_WITH {group_index: 0}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Regulation {extraction_index: 1}),
      (e2:Institution {extraction_index: 1})
CREATE (e1)-[:GROUPED_WITH {group_index: 0}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Institution {extraction_index: 1}),
      (e2:Procedure {extraction_index: 1})
CREATE (e1)-[:GROUPED_WITH {group_index: 0}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Procedure {extraction_index: 1}),
      (e2:Regulation {extraction_index: 1})
CREATE (e1)-[:GROUPED_WITH {group_index: 0}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Regulation {extraction_index: 1}),
      (e2:RegulationClause {extraction_index: 1})
CREATE (e1)-[:GROUPED_WITH {group_index: 0}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:RegulationClause {extraction_index: 1}),
      (e2:RegulationHeader {extraction_index: 1})
CREATE (e1)-[:GROUPED_WITH {group_index: 0}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:RegulationHeader {extraction_index: 1}),
      (e2:Condition {extraction_index: 1})
CREATE (e1)-[:GROUPED_WITH {group_index: 0}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Condition {extraction_index: 1}),
      (e2:RegulationId {extraction_index: 1})
CREATE (e1)-[:GROUPED_WITH {group_index: 0}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:RegulationId {extraction_index: 1}),
      (e2:Regulation {extraction_index: 1})
CREATE (e1)-[:GROUPED_WITH {group_index: 0}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Regulation {extraction_index: 1}),
      (e2:RegulationMarker {extraction_index: 1})
CREATE (e1)-[:GROUPED_WITH {group_index: 0}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:RegulationMarker {extraction_index: 1}),
      (e2:RegulationClause {extraction_index: 1})
CREATE (e1)-[:GROUPED_WITH {group_index: 0}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:DeductionRule {extraction_index: 2}),
      (e2:Condition {extraction_index: 2})
CREATE (e1)-[:GROUPED_WITH {group_index: 1}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;


// Batch 4
// -----------------------------

MATCH (e1:Condition {extraction_index: 2}),
      (e2:Procedure {extraction_index: 2})
CREATE (e1)-[:GROUPED_WITH {group_index: 1}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Procedure {extraction_index: 2}),
      (e2:MedicalReason {extraction_index: 2})
CREATE (e1)-[:GROUPED_WITH {group_index: 1}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:MedicalReason {extraction_index: 2}),
      (e2:MedicalScope {extraction_index: 2})
CREATE (e1)-[:GROUPED_WITH {group_index: 1}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:MedicalScope {extraction_index: 2}),
      (e2:Requirement {extraction_index: 2})
CREATE (e1)-[:GROUPED_WITH {group_index: 1}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Requirement {extraction_index: 2}),
      (e2:Scope {extraction_index: 2})
CREATE (e1)-[:GROUPED_WITH {group_index: 1}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Scope {extraction_index: 2}),
      (e2:Exception {extraction_index: 2})
CREATE (e1)-[:GROUPED_WITH {group_index: 1}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Exception {extraction_index: 2}),
      (e2:MedicalEvent {extraction_index: 2})
CREATE (e1)-[:GROUPED_WITH {group_index: 1}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:MedicalEvent {extraction_index: 2}),
      (e2:Scenario {extraction_index: 2})
CREATE (e1)-[:GROUPED_WITH {group_index: 1}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Scenario {extraction_index: 2}),
      (e2:MedicalScenario {extraction_index: 2})
CREATE (e1)-[:GROUPED_WITH {group_index: 1}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:MedicalScenario {extraction_index: 2}),
      (e2:Requirement {extraction_index: 2})
CREATE (e1)-[:GROUPED_WITH {group_index: 1}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Entity {extraction_index: 3}),
      (e2:Prohibition {extraction_index: 3})
CREATE (e1)-[:GROUPED_WITH {group_index: 2}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Prohibition {extraction_index: 3}),
      (e2:MedicalContext {extraction_index: 3})
CREATE (e1)-[:GROUPED_WITH {group_index: 2}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:MedicalContext {extraction_index: 3}),
      (e2:Document {extraction_index: 3})
CREATE (e1)-[:GROUPED_WITH {group_index: 2}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Document {extraction_index: 3}),
      (e2:BillingRule {extraction_index: 3})
CREATE (e1)-[:GROUPED_WITH {group_index: 2}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:BillingRule {extraction_index: 3}),
      (e2:RegulationClause {extraction_index: 3})
CREATE (e1)-[:GROUPED_WITH {group_index: 2}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:RegulationClause {extraction_index: 3}),
      (e2:BillingUnit {extraction_index: 3})
CREATE (e1)-[:GROUPED_WITH {group_index: 2}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:BillingUnit {extraction_index: 3}),
      (e2:TimeframeRule {extraction_index: 3})
CREATE (e1)-[:GROUPED_WITH {group_index: 2}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:TimeframeRule {extraction_index: 3}),
      (e2:TemporalContext {extraction_index: 3})
CREATE (e1)-[:GROUPED_WITH {group_index: 2}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:TemporalContext {extraction_index: 3}),
      (e2:Condition {extraction_index: 3})
CREATE (e1)-[:GROUPED_WITH {group_index: 2}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Condition {extraction_index: 3}),
      (e2:BillingRule {extraction_index: 3})
CREATE (e1)-[:GROUPED_WITH {group_index: 2}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:BillingRule {extraction_index: 3}),
      (e2:MedicalScope {extraction_index: 3})
CREATE (e1)-[:GROUPED_WITH {group_index: 2}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:FinancialMechanism {extraction_index: 4}),
      (e2:Prohibition {extraction_index: 4})
CREATE (e1)-[:GROUPED_WITH {group_index: 3}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Prohibition {extraction_index: 4}),
      (e2:Entity {extraction_index: 4})
CREATE (e1)-[:GROUPED_WITH {group_index: 3}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Entity {extraction_index: 4}),
      (e2:BillingRule {extraction_index: 4})
CREATE (e1)-[:GROUPED_WITH {group_index: 3}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:BillingRule {extraction_index: 4}),
      (e2:Regulation {extraction_index: 4})
CREATE (e1)-[:GROUPED_WITH {group_index: 3}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Regulation {extraction_index: 4}),
      (e2:ReferenceList {extraction_index: 4})
CREATE (e1)-[:GROUPED_WITH {group_index: 3}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:ReferenceList {extraction_index: 4}),
      (e2:ReferenceDocument {extraction_index: 4})
CREATE (e1)-[:GROUPED_WITH {group_index: 3}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:ReferenceDocument {extraction_index: 4}),
      (e2:BillingPermission {extraction_index: 4})
CREATE (e1)-[:GROUPED_WITH {group_index: 3}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:BillingPermission {extraction_index: 4}),
      (e2:Condition {extraction_index: 4})
CREATE (e1)-[:GROUPED_WITH {group_index: 3}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Condition {extraction_index: 4}),
      (e2:BillingRule {extraction_index: 4})
CREATE (e1)-[:GROUPED_WITH {group_index: 3}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:BillingRule {extraction_index: 4}),
      (e2:BillingProhibition {extraction_index: 4})
CREATE (e1)-[:GROUPED_WITH {group_index: 3}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:BillingProhibition {extraction_index: 4}),
      (e2:PatientStatus {extraction_index: 4})
CREATE (e1)-[:GROUPED_WITH {group_index: 3}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:RegulationId {extraction_index: 5}),
      (e2:Condition {extraction_index: 5})
CREATE (e1)-[:GROUPED_WITH {group_index: 4}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Condition {extraction_index: 5}),
      (e2:ScopeDefinition {extraction_index: 5})
CREATE (e1)-[:GROUPED_WITH {group_index: 4}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:ScopeDefinition {extraction_index: 5}),
      (e2:RegulationId {extraction_index: 5})
CREATE (e1)-[:GROUPED_WITH {group_index: 4}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:RegulationId {extraction_index: 5}),
      (e2:ReferenceDocument {extraction_index: 5})
CREATE (e1)-[:GROUPED_WITH {group_index: 4}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:ReferenceDocument {extraction_index: 5}),
      (e2:ProviderDefinition {extraction_index: 5})
CREATE (e1)-[:GROUPED_WITH {group_index: 4}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:ProviderDefinition {extraction_index: 5}),
      (e2:PaymentRule {extraction_index: 5})
CREATE (e1)-[:GROUPED_WITH {group_index: 4}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:PaymentRule {extraction_index: 5}),
      (e2:BillingProhibition {extraction_index: 5})
CREATE (e1)-[:GROUPED_WITH {group_index: 4}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:BillingProhibition {extraction_index: 5}),
      (e2:BillingRule {extraction_index: 5})
CREATE (e1)-[:GROUPED_WITH {group_index: 4}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:BillingRule {extraction_index: 5}),
      (e2:BillingRule {extraction_index: 5})
CREATE (e1)-[:GROUPED_WITH {group_index: 4}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:BillingRule {extraction_index: 5}),
      (e2:BillingPermission {extraction_index: 5})
CREATE (e1)-[:GROUPED_WITH {group_index: 4}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:BillingPermission {extraction_index: 5}),
      (e2:ProcessStep {extraction_index: 5})
CREATE (e1)-[:GROUPED_WITH {group_index: 4}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Entity {extraction_index: 6}),
      (e2:Obligation {extraction_index: 6})
CREATE (e1)-[:GROUPED_WITH {group_index: 5}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Obligation {extraction_index: 6}),
      (e2:ExcludedServices {extraction_index: 6})
CREATE (e1)-[:GROUPED_WITH {group_index: 5}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:ExcludedServices {extraction_index: 6}),
      (e2:Scope {extraction_index: 6})
CREATE (e1)-[:GROUPED_WITH {group_index: 5}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Scope {extraction_index: 6}),
      (e2:MedicalMethod {extraction_index: 6})
CREATE (e1)-[:GROUPED_WITH {group_index: 5}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:MedicalMethod {extraction_index: 6}),
      (e2:BillingRule {extraction_index: 6})
CREATE (e1)-[:GROUPED_WITH {group_index: 5}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:BillingRule {extraction_index: 6}),
      (e2:LegalAmendment {extraction_index: 6})
CREATE (e1)-[:GROUPED_WITH {group_index: 5}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:LegalAmendment {extraction_index: 6}),
      (e2:LegalAmendment {extraction_index: 6})
CREATE (e1)-[:GROUPED_WITH {group_index: 5}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;


// Batch 5
// -----------------------------

MATCH (e1:LegalAmendment {extraction_index: 6}),
      (e2:ExceptionCondition {extraction_index: 6})
CREATE (e1)-[:GROUPED_WITH {group_index: 5}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:ExceptionCondition {extraction_index: 6}),
      (e2:BillingRule {extraction_index: 6})
CREATE (e1)-[:GROUPED_WITH {group_index: 5}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:BillingRule {extraction_index: 6}),
      (e2:RegulationMarker {extraction_index: 6})
CREATE (e1)-[:GROUPED_WITH {group_index: 5}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:RegulationMarker {extraction_index: 6}),
      (e2:Condition {extraction_index: 6})
CREATE (e1)-[:GROUPED_WITH {group_index: 5}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Process {extraction_index: 7}),
      (e2:Regulation {extraction_index: 7})
CREATE (e1)-[:GROUPED_WITH {group_index: 6}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Regulation {extraction_index: 7}),
      (e2:PaymentRule {extraction_index: 7})
CREATE (e1)-[:GROUPED_WITH {group_index: 6}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:PaymentRule {extraction_index: 7}),
      (e2:Authority {extraction_index: 7})
CREATE (e1)-[:GROUPED_WITH {group_index: 6}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Authority {extraction_index: 7}),
      (e2:PaymentRule {extraction_index: 7})
CREATE (e1)-[:GROUPED_WITH {group_index: 6}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:PaymentRule {extraction_index: 7}),
      (e2:LegalExclusion {extraction_index: 7})
CREATE (e1)-[:GROUPED_WITH {group_index: 6}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:LegalExclusion {extraction_index: 7}),
      (e2:AdministrativeProcess {extraction_index: 7})
CREATE (e1)-[:GROUPED_WITH {group_index: 6}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:AdministrativeProcess {extraction_index: 7}),
      (e2:MedicalScope {extraction_index: 7})
CREATE (e1)-[:GROUPED_WITH {group_index: 6}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:MedicalScope {extraction_index: 7}),
      (e2:BillingProhibition {extraction_index: 7})
CREATE (e1)-[:GROUPED_WITH {group_index: 6}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:BillingProhibition {extraction_index: 7}),
      (e2:ExceptionCondition {extraction_index: 7})
CREATE (e1)-[:GROUPED_WITH {group_index: 6}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:ExceptionCondition {extraction_index: 7}),
      (e2:MedicalScenario {extraction_index: 7})
CREATE (e1)-[:GROUPED_WITH {group_index: 6}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:MedicalScenario {extraction_index: 7}),
      (e2:Subject {extraction_index: 7})
CREATE (e1)-[:GROUPED_WITH {group_index: 6}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:ScopeLimitation {extraction_index: 8}),
      (e2:Entity {extraction_index: 8})
CREATE (e1)-[:GROUPED_WITH {group_index: 7}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Entity {extraction_index: 8}),
      (e2:RegulationId {extraction_index: 8})
CREATE (e1)-[:GROUPED_WITH {group_index: 7}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:RegulationId {extraction_index: 8}),
      (e2:Reference {extraction_index: 8})
CREATE (e1)-[:GROUPED_WITH {group_index: 7}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Reference {extraction_index: 8}),
      (e2:MedicalProcedure {extraction_index: 8})
CREATE (e1)-[:GROUPED_WITH {group_index: 7}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:MedicalProcedure {extraction_index: 8}),
      (e2:RegulationHeader {extraction_index: 8})
CREATE (e1)-[:GROUPED_WITH {group_index: 7}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:RegulationHeader {extraction_index: 8}),
      (e2:Condition {extraction_index: 8})
CREATE (e1)-[:GROUPED_WITH {group_index: 7}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Condition {extraction_index: 8}),
      (e2:ProcessCondition {extraction_index: 8})
CREATE (e1)-[:GROUPED_WITH {group_index: 7}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:ProcessCondition {extraction_index: 8}),
      (e2:BillingRequirement {extraction_index: 8})
CREATE (e1)-[:GROUPED_WITH {group_index: 7}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:BillingRequirement {extraction_index: 8}),
      (e2:Prohibition {extraction_index: 8})
CREATE (e1)-[:GROUPED_WITH {group_index: 7}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Prohibition {extraction_index: 8}),
      (e2:BillingRule {extraction_index: 8})
CREATE (e1)-[:GROUPED_WITH {group_index: 7}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:BillingRule {extraction_index: 8}),
      (e2:PaymentContext {extraction_index: 8})
CREATE (e1)-[:GROUPED_WITH {group_index: 7}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:MedicalProcedures {extraction_index: 9}),
      (e2:Obligation {extraction_index: 9})
CREATE (e1)-[:GROUPED_WITH {group_index: 8}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Obligation {extraction_index: 9}),
      (e2:RegulatoryRequirement {extraction_index: 9})
CREATE (e1)-[:GROUPED_WITH {group_index: 8}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:RegulatoryRequirement {extraction_index: 9}),
      (e2:ListScope {extraction_index: 9})
CREATE (e1)-[:GROUPED_WITH {group_index: 8}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:ListScope {extraction_index: 9}),
      (e2:PaymentRule {extraction_index: 9})
CREATE (e1)-[:GROUPED_WITH {group_index: 8}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:PaymentRule {extraction_index: 9}),
      (e2:RegulationHeader {extraction_index: 9})
CREATE (e1)-[:GROUPED_WITH {group_index: 8}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:RegulationHeader {extraction_index: 9}),
      (e2:InstitutionType {extraction_index: 9})
CREATE (e1)-[:GROUPED_WITH {group_index: 8}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:InstitutionType {extraction_index: 9}),
      (e2:BillingRule {extraction_index: 9})
CREATE (e1)-[:GROUPED_WITH {group_index: 8}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:BillingRule {extraction_index: 9}),
      (e2:BillingInstruction {extraction_index: 9})
CREATE (e1)-[:GROUPED_WITH {group_index: 8}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:BillingInstruction {extraction_index: 9}),
      (e2:ContextSwitch {extraction_index: 9})
CREATE (e1)-[:GROUPED_WITH {group_index: 8}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:ContextSwitch {extraction_index: 9}),
      (e2:RegulationReference {extraction_index: 9})
CREATE (e1)-[:GROUPED_WITH {group_index: 8}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Prohibition {extraction_index: 10}),
      (e2:Condition {extraction_index: 10})
CREATE (e1)-[:GROUPED_WITH {group_index: 9}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Condition {extraction_index: 10}),
      (e2:BillingRule {extraction_index: 10})
CREATE (e1)-[:GROUPED_WITH {group_index: 9}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:BillingRule {extraction_index: 10}),
      (e2:Parameter {extraction_index: 10})
CREATE (e1)-[:GROUPED_WITH {group_index: 9}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Parameter {extraction_index: 10}),
      (e2:Regulation {extraction_index: 10})
CREATE (e1)-[:GROUPED_WITH {group_index: 9}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Regulation {extraction_index: 10}),
      (e2:RegulationClause {extraction_index: 10})
CREATE (e1)-[:GROUPED_WITH {group_index: 9}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:RegulationClause {extraction_index: 10}),
      (e2:ServiceDetail {extraction_index: 10})
CREATE (e1)-[:GROUPED_WITH {group_index: 9}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:ServiceDetail {extraction_index: 10}),
      (e2:BillingRestriction {extraction_index: 10})
CREATE (e1)-[:GROUPED_WITH {group_index: 9}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Condition {extraction_index: 11}),
      (e2:FinancialRule {extraction_index: 11})
CREATE (e1)-[:GROUPED_WITH {group_index: 10}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:FinancialRule {extraction_index: 11}),
      (e2:CalculationMethod {extraction_index: 11})
CREATE (e1)-[:GROUPED_WITH {group_index: 10}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:CalculationMethod {extraction_index: 11}),
      (e2:Scenario {extraction_index: 11})
CREATE (e1)-[:GROUPED_WITH {group_index: 10}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Scenario {extraction_index: 11}),
      (e2:PaymentRule {extraction_index: 11})
CREATE (e1)-[:GROUPED_WITH {group_index: 10}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:PaymentRule {extraction_index: 11}),
      (e2:PaymentCalculation {extraction_index: 11})
CREATE (e1)-[:GROUPED_WITH {group_index: 10}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:PaymentCalculation {extraction_index: 11}),
      (e2:BillingPermission {extraction_index: 11})
CREATE (e1)-[:GROUPED_WITH {group_index: 10}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:Exception {extraction_index: 12}),
      (e2:Regulation {extraction_index: 12})
CREATE (e1)-[:GROUPED_WITH {group_index: 11}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;


// Batch 6
// -----------------------------

MATCH (e1:Regulation {extraction_index: 12}),
      (e2:FormattingRule {extraction_index: 12})
CREATE (e1)-[:GROUPED_WITH {group_index: 11}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:FormattingRule {extraction_index: 12}),
      (e2:CoverageScope {extraction_index: 12})
CREATE (e1)-[:GROUPED_WITH {group_index: 11}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:CoverageScope {extraction_index: 12}),
      (e2:PaymentRule {extraction_index: 12})
CREATE (e1)-[:GROUPED_WITH {group_index: 11}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:PaymentRule {extraction_index: 12}),
      (e2:ReferenceDocument {extraction_index: 12})
CREATE (e1)-[:GROUPED_WITH {group_index: 11}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:FinancialTerm {extraction_index: 13}),
      (e2:PaymentRule {extraction_index: 13})
CREATE (e1)-[:GROUPED_WITH {group_index: 12}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:PaymentRule {extraction_index: 13}),
      (e2:RegulationHeader {extraction_index: 13})
CREATE (e1)-[:GROUPED_WITH {group_index: 12}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:RegulationHeader {extraction_index: 13}),
      (e2:CoverageRule {extraction_index: 13})
CREATE (e1)-[:GROUPED_WITH {group_index: 12}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:ReferenceDocument {extraction_index: 14}),
      (e2:TimeLimitation {extraction_index: 14})
CREATE (e1)-[:GROUPED_WITH {group_index: 13}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:TimeLimitation {extraction_index: 14}),
      (e2:LegalAmendment {extraction_index: 14})
CREATE (e1)-[:GROUPED_WITH {group_index: 13}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (e1:BillingRule {extraction_index: 15}),
      (e2:EffectiveDate {extraction_index: 15})
CREATE (e1)-[:GROUPED_WITH {group_index: 14}]->(e2)
RETURN e1.extraction_index as from_index, e2.extraction_index as to_index;

MATCH (pr:PaymentRule {extraction_index: 1}),
      (e:Entity {extraction_index: 3})
CREATE (pr)-[:APPLIES_TO]->(e)
RETURN pr.extraction_index as rule_id, e.extraction_index as entity_id;

MATCH (pr:PaymentRule {extraction_index: 7}),
      (e:Entity {extraction_index: 6})
CREATE (pr)-[:APPLIES_TO]->(e)
RETURN pr.extraction_index as rule_id, e.extraction_index as entity_id;

MATCH (pr:PaymentRule {extraction_index: 7}),
      (e:Entity {extraction_index: 8})
CREATE (pr)-[:APPLIES_TO]->(e)
RETURN pr.extraction_index as rule_id, e.extraction_index as entity_id;

MATCH (pr:PaymentRule {extraction_index: 7}),
      (e:Entity {extraction_index: 6})
CREATE (pr)-[:APPLIES_TO]->(e)
RETURN pr.extraction_index as rule_id, e.extraction_index as entity_id;

MATCH (pr:PaymentRule {extraction_index: 7}),
      (e:Entity {extraction_index: 8})
CREATE (pr)-[:APPLIES_TO]->(e)
RETURN pr.extraction_index as rule_id, e.extraction_index as entity_id;

MATCH (pr:PaymentRule {extraction_index: 9}),
      (e:Entity {extraction_index: 8})
CREATE (pr)-[:APPLIES_TO]->(e)
RETURN pr.extraction_index as rule_id, e.extraction_index as entity_id;

MATCH (pr:PaymentRule {extraction_index: 5}),
      (e:Entity {extraction_index: 3})
CREATE (pr)-[:APPLIES_TO]->(e)
RETURN pr.extraction_index as rule_id, e.extraction_index as entity_id;

MATCH (pr:PaymentRule {extraction_index: 5}),
      (e:Entity {extraction_index: 6})
CREATE (pr)-[:APPLIES_TO]->(e)
RETURN pr.extraction_index as rule_id, e.extraction_index as entity_id;

MATCH (pr:PaymentRule {extraction_index: 5}),
      (e:Entity {extraction_index: 4})
CREATE (pr)-[:APPLIES_TO]->(e)
RETURN pr.extraction_index as rule_id, e.extraction_index as entity_id;


