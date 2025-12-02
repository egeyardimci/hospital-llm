// ═══════════════════════════════════════════════════════
// CHATBOT İÇİN OPTİMİZE EDİLMİŞ NEO4J GRAPH
// Yasal Sorgu Motoru - Semantic Relationships
// Toplam Node: 137
// Toplam Batch: 12
// ═══════════════════════════════════════════════════════

// 🔗 SEMANTİK İLİŞKİLER:
// • DEFINES: Regulation → Rules (Madde kuralları tanımlar)
// • TRIGGERS: Condition → Prohibition (Şart yasağı tetikler)
// • REQUIRES: Condition → Obligation (Şart yükümlülük gerektirir)
// • APPLIES_TO: Rule → Entity (Kural varlığa uygulanır)
// • PROHIBITS: Prohibition → Entity (Yasak varlığı kısıtlar)
// • REFERENCES: Rule → ReferenceDoc (Kural belgeye atıfta bulunur)
// • HAS_REQUIREMENT: Process → Requirement (Süreç gereklilik içerir)
// • HAS_EXCEPTION: Regulation → Exception (Maddenin istisnası)
// • IN_CONTEXT: Sequential (Aynı grup içinde sıralı bağlam)


// ───────── BATCH 1/12 ─────────

CREATE (n:PaymentRule {
    id: 1,
    text: 'tem belgesine dayanılarak kişilere ödenir',
    group_id: 0,
    extraction_class: 'payment_rule',
    keywords: ['tem', 'belgesine', 'dayanılarak', 'kişilere', 'ödenir'],
    basis: 'istem belgesi (implied)',
    recipient: 'kişiler',
    action: 'payment'
});

CREATE (n:DeductionRule {
    id: 2,
    text: 'sevk/istem belgesini düzenleyen sözleşme li sağlık hi zmeti sunucusunun alacağından mahsup edilir',
    group_id: 1,
    extraction_class: 'deduction_rule',
    keywords: ['sevk/istem', 'belgesini', 'düzenleyen', 'sözleşme', 'sağlık', 'zmeti', 'sunucusunun', 'alacağından', 'mahsup', 'edilir'],
    target_entity: 'sözleşmeli sağlık hizmeti sunucusu',
    action: 'deduction_from_receivables',
    reason: 'issuing_document'
});

CREATE (n:Entity {
    id: 3,
    text: 'Sağlık Bakanlığına bağlı sağlık hizmeti sunucuları',
    group_id: 2,
    extraction_class: 'entity',
    keywords: ['sağlık', 'bakanlığına', 'bağlı', 'sağlık', 'hizmeti', 'sunucuları'],
    affiliation: 'Sağlık Bakanlığı',
    type: 'public_healthcare_provider'
});

CREATE (n:FinancialMechanism {
    id: 4,
    text: 'Bakanlığa yapılan global bütçe ödemesinden mahsup edilir',
    group_id: 3,
    extraction_class: 'financial_mechanism',
    keywords: ['bakanlığa', 'yapılan', 'global', 'bütçe', 'ödemesinden', 'mahsup', 'edilir'],
    source: 'global bütçe',
    action: 'deduction',
    beneficiary: 'Sağlık Bakanlığı'
});

CREATE (n:Regulation {
    id: 5,
    text: '(10)',
    group_id: 4,
    extraction_class: 'regulation_id',
    keywords: ['(10)'],
    type: 'clause_number'
});

CREATE (n:Entity {
    id: 6,
    text: 'Kurumla sözleşmeli sağlık hizmeti sunucuları',
    group_id: 5,
    extraction_class: 'entity',
    keywords: ['kurumla', 'sözleşmeli', 'sağlık', 'hizmeti', 'sunucuları'],
    relationship: 'contracted',
    counterparty: 'Kurum (SGK)',
    role: 'provider'
});

CREATE (n:Process {
    id: 7,
    text: 'bir başka sağlık hizmeti sunucusundan hizmet alımı yoluyla sağladıkları',
    group_id: 6,
    extraction_class: 'process',
    keywords: ['bir', 'başka', 'sağlık', 'hizmeti', 'sunucusundan', 'hizmet', 'alımı', 'yoluyla', 'sağladıkları'],
    type: 'outsourcing',
    method: 'service_procurement'
});

CREATE (n:ScopeLimitation {
    id: 8,
    text: 'ruhsat/faaliyet veya uygunluk belgesinde yer al an tetkik ve/veya tahlil dışındaki tedavilere',
    group_id: 7,
    extraction_class: 'scope_limitation',
    keywords: ['ruhsat/faaliyet', 'veya', 'uygunluk', 'belgesinde', 'yer', 'tetkik', 've/veya', 'tahlil', 'dışındaki', 'tedavilere'],
    document_basis: 'ruhsat/faaliyet/uygunluk belgesi',
    included: 'tetkik ve tahlil',
    excluded: 'diğer tedaviler'
});

CREATE (n:MedicalProcedures {
    id: 9,
    text: '(gastroskopi, kolonoskopi, rektosigmoidoskopi, rektoskopi, bronkoskopi, anjiyografi gibi işlemler de dahil olmak üzere)',
    group_id: 8,
    extraction_class: 'medical_procedures',
    keywords: ['(gastroskopi,', 'kolonoskopi,', 'rektosigmoidoskopi,', 'rektoskopi,', 'bronkoskopi,', 'anjiyografi', 'gibi', 'işlemler', 'dahil', 'olmak', 'üzere)'],
    type: 'examples_of_excluded_treatments',
    category: 'interventional_procedures'
});

CREATE (n:Prohibition {
    id: 10,
    text: 'ait giderleri Kuruma faturalandıramazlar',
    group_id: 9,
    extraction_class: 'prohibition',
    keywords: ['ait', 'giderleri', 'kuruma', 'faturalandıramazlar'],
    action: 'billing',
    target: 'Kurum',
    status: 'prohibited',
    context: 'outsourced_treatments_outside_license'
});

CREATE (n:Condition {
    id: 11,
    text: 'Hekim veya diş hekimlerinin, özel sağlık hizmeti sunucusu bünyesinde çalışması halinde',
    group_id: 10,
    extraction_class: 'condition',
    keywords: ['hekim', 'veya', 'diş', 'hekimlerinin,', 'özel', 'sağlık', 'hizmeti', 'sunucusu', 'bünyesinde', 'çalışması', 'halinde'],
    subject: 'hekim veya diş hekimleri',
    setting: 'özel sağlık hizmeti sunucusu',
    employment_status: 'working_within'
});

CREATE (n:Exception {
    id: 12,
    text: 'bu hekimler tarafından fatura düzenlenerek alınan/sunulan sağlık hizmetleri bu kapsamda değerlendirilmez',
    group_id: 11,
    extraction_class: 'exception',
    keywords: ['hekimler', 'tarafından', 'fatura', 'düzenlenerek', 'alınan/sunulan', 'sağlık', 'hizmetleri', 'kapsamda', 'değerlendirilmez'],
    action: 'individual_invoicing',
    effect: 'exemption_from_prohibition',
    subject: 'doctors_dentists'
});

CREATE (n:Regulation {
    id: 1,
    text: '(11)',
    group_id: 0,
    extraction_class: 'regulation',
    keywords: ['(11)'],
    type: 'article_number',
    context: 'service_procurement_rules'
});

CREATE (n:Condition {
    id: 2,
    text: 'Başka bir sağlık hizmeti sunucusundan laboratuvar hizmeti alınması durumunda',
    group_id: 1,
    extraction_class: 'condition',
    keywords: ['başka', 'bir', 'sağlık', 'hizmeti', 'sunucusundan', 'laboratuvar', 'hizmeti', 'alınması', 'durumunda'],
    context: 'outsourced_laboratory_services',
    trigger: 'service_procurement'
});

CREATE (n:Prohibition {
    id: 3,
    text: 'hasta hastane dışına numune almak için gönderilmez',
    group_id: 2,
    extraction_class: 'prohibition',
    keywords: ['hasta', 'hastane', 'dışına', 'numune', 'almak', 'için', 'gönderilmez'],
    subject: 'hasta',
    forbidden_action: 'sending_patient_for_sample_collection',
    responsible_party: 'sağlık hizmeti sunucusu'
});

CREATE (n:Prohibition {
    id: 4,
    text: 'alınan numunenin transferi veya sonucu hasta veya yakını aracılığı ile istenilemez',
    group_id: 3,
    extraction_class: 'prohibition',
    keywords: ['alınan', 'numunenin', 'transferi', 'veya', 'sonucu', 'hasta', 'veya', 'yakını', 'aracılığı', 'ile', 'istenilemez'],
    forbidden_action: 'transfer_via_patient_or_relative',
    items: 'numune transferi veya sonucu',
    intermediary: 'hasta veya yakını'
});

CREATE (n:Condition {
    id: 5,
    text: 'Görüntüleme hizmetlerinin hizmet alım ı yoluyla sağlanması halinde',
    group_id: 4,
    extraction_class: 'condition',
    keywords: ['görüntüleme', 'hizmetlerinin', 'hizmet', 'alım', 'yoluyla', 'sağlanması', 'halinde'],
    context: 'outsourced_imaging_services',
    trigger: 'service_procurement'
});

CREATE (n:Obligation {
    id: 6,
    text: 'acil ve yatan hastaların transferi sağlık hizmeti sunucuları tarafından yapılacaktır',
    group_id: 5,
    extraction_class: 'obligation',
    keywords: ['acil', 'yatan', 'hastaların', 'transferi', 'sağlık', 'hizmeti', 'sunucuları', 'tarafından', 'yapılacaktır'],
    responsible_party: 'sağlık hizmeti sunucuları',
    action: 'patient_transfer',
    patient_type: 'acil ve yatan hastalar',
    requirement: 'mandatory'
});

CREATE (n:Regulation {
    id: 7,
    text: '(12)',
    group_id: 6,
    extraction_class: 'regulation',
    keywords: ['(12)'],
    type: 'article_number',
    context: 'documentation_and_audit'
});

CREATE (n:Entity {
    id: 8,
    text: 'Kurum ile sözleşmeli sağlık hizmeti sunucuları',
    group_id: 7,
    extraction_class: 'entity',
    keywords: ['kurum', 'ile', 'sözleşmeli', 'sağlık', 'hizmeti', 'sunucuları'],
    type: 'healthcare_provider',
    contract_status: 'contracted_with_institution'
});

CREATE (n:Obligation {
    id: 9,
    text: 'tetkik, tahlil ve tedaviye ait her türlü bilgi, belge ve raporu, istenildiğinde Kuruma ibraz edeceklerdir',
    group_id: 8,
    extraction_class: 'obligation',
    keywords: ['tetkik,', 'tahlil', 'tedaviye', 'ait', 'her', 'türlü', 'bilgi,', 'belge', 'raporu,', 'istenildiğinde', 'kuruma', 'ibraz', 'edeceklerdir'],
    action: 'submit_documents',
    recipient: 'Kurum (SGK)',
    trigger: 'upon_request',
    content: 'tetkik, tahlil, tedavi bilgileri'
});

CREATE (n:Condition {
    id: 10,
    text: 'İbraz edilememesi durumunda',
    group_id: 9,
    extraction_class: 'condition',
    keywords: ['i̇braz', 'edilememesi', 'durumunda'],
    context: 'failure_to_submit_documents',
    consequence_trigger: 'true'
});

CREATE (n:FinancialRule {
    id: 11,
    text: 'Kuruma faturalandırılan ilgili tetkik, tahlil ve/veya tedavi bedelleri Kurumca karşılanmaz',
    group_id: 10,
    extraction_class: 'financial_rule',
    keywords: ['kuruma', 'faturalandırılan', 'ilgili', 'tetkik,', 'tahlil', 've/veya', 'tedavi', 'bedelleri', 'kurumca', 'karşılanmaz'],
    result: 'payment_denial',
    payer: 'Kurum',
    reason: 'documentation_failure'
});

CREATE (n:Regulation {
    id: 12,
    text: '(13)',
    group_id: 11,
    extraction_class: 'regulation',
    keywords: ['(13)'],
    type: 'article_number',
    context: 'billing_rules'
});

CREATE (n:FinancialTerm {
    id: 13,
    text: 'Kişilere sağlanan sağlık hizmetlerine ilişkin düzenlenen sağlık raporu bedelleri',
    group_id: 12,
    extraction_class: 'financial_term',
    keywords: ['kişilere', 'sağlanan', 'sağlık', 'hizmetlerine', 'ilişkin', 'düzenlenen', 'sağlık', 'raporu', 'bedelleri'],
    topic: 'health_report_fees',
    service_type: 'administrative'
});


// ───────── BATCH 2/12 ─────────

CREATE (n:ReferenceDoc {
    id: 14,
    text: 'SUT eki EK-2/B Listesinde yer alan rapor puanları',
    group_id: 13,
    extraction_class: 'reference_document',
    keywords: ['sut', 'eki', 'ek-2/b', 'listesinde', 'yer', 'alan', 'rapor', 'puanları'],
    document_name: 'SUT eki EK-2/B',
    usage: 'pricing_basis',
    metric: 'rapor puanları'
});

CREATE (n:BillingRule {
    id: 15,
    text: 'sadece bir adet olarak faturalandırılır',
    group_id: 14,
    extraction_class: 'billing_rule',
    keywords: ['sadece', 'bir', 'adet', 'olarak', 'faturalandırılır'],
    constraint: 'quantity_limit',
    limit_value: '1',
    action: 'invoicing'
});

CREATE (n:Institution {
    id: 1,
    text: 'Kurum birimlerince',
    group_id: 0,
    extraction_class: 'institution',
    keywords: ['kurum', 'birimlerince'],
    type: 'government_agency',
    role: 'referral_authority',
    context: 'SGK (Social Security Institution)'
});

CREATE (n:Procedure {
    id: 2,
    text: 'sevk belgesi düzenlenmek suretiyle',
    group_id: 1,
    extraction_class: 'procedure',
    keywords: ['sevk', 'belgesi', 'düzenlenmek', 'suretiyle'],
    action: 'issue_referral_document',
    requirement: 'mandatory_for_referral'
});

CREATE (n:MedicalContext {
    id: 3,
    text: 'maluliyet, meslek hastalığı ve kontrol muayeneleri',
    group_id: 2,
    extraction_class: 'medical_context',
    keywords: ['maluliyet,', 'meslek', 'hastalığı', 'kontrol', 'muayeneleri'],
    type: 'referral_reasons'
});

CREATE (n:Entity {
    id: 4,
    text: 'sağlık hizmeti sunucusuna',
    group_id: 3,
    extraction_class: 'entity',
    keywords: ['sağlık', 'hizmeti', 'sunucusuna'],
    type: 'healthcare_provider',
    role: 'service_provider'
});

CREATE (n:ScopeDefinition {
    id: 5,
    text: 'tedavi amacıyla düzenlenen sağlık raporları dışında kalan',
    group_id: 4,
    extraction_class: 'scope_definition',
    keywords: ['tedavi', 'amacıyla', 'düzenlenen', 'sağlık', 'raporları', 'dışında', 'kalan'],
    type: 'exclusion_criteria',
    exception: 'treatment_purposes',
    status: 'defines_non_covered_scope'
});

CREATE (n:ExcludedServices {
    id: 6,
    text: 'engellilik raporu, adli rapor, ehliyet raporu, vasi tayini raporu, portör muayeneleri ve işlemleri, tarama amaçlı muayene ve işlemler',
    group_id: 5,
    extraction_class: 'excluded_services',
    keywords: ['engellilik', 'raporu,', 'adli', 'rapor,', 'ehliyet', 'raporu,', 'vasi', 'tayini', 'raporu,', 'portör', 'muayeneleri', 'işlemleri,', 'tarama', 'amaçlı', 'muayene', 'işlemler'],
    category: 'special_purpose_reports',
    coverage_status: 'not_covered'
});

CREATE (n:PaymentRule {
    id: 7,
    text: 'Kurumca karşılanmaz',
    group_id: 6,
    extraction_class: 'payment_rule',
    keywords: ['kurumca', 'karşılanmaz'],
    payer: 'Kurum (SGK)',
    status: 'payment_denied',
    target: 'special_purpose_reports_and_procedures'
});

CREATE (n:Regulation {
    id: 8,
    text: '(14)',
    group_id: 7,
    extraction_class: 'regulation_id',
    keywords: ['(14)'],
    type: 'clause_number',
    hierarchy: 'item_14'
});

CREATE (n:RegulatoryRequirement {
    id: 9,
    text: 'SUT gereği düzenlenmesi gereken sağlık kurulu raporu',
    group_id: 8,
    extraction_class: 'regulatory_requirement',
    keywords: ['sut', 'gereği', 'düzenlenmesi', 'gereken', 'sağlık', 'kurulu', 'raporu'],
    source_regulation: 'SUT (Sağlık Uygulama Tebliği)',
    document_type: 'health_board_report',
    context: 'medical_supplies_and_treatment'
});

CREATE (n:BillingRule {
    id: 10,
    text: 'sadece bir adet muayene bedeli faturalandırılabilir',
    group_id: 9,
    extraction_class: 'billing_rule',
    keywords: ['sadece', 'bir', 'adet', 'muayene', 'bedeli', 'faturalandırılabilir'],
    restriction: 'single_fee',
    item: 'examination_fee',
    context: 'report_issuance'
});

CREATE (n:Procedure {
    id: 1,
    text: 'Kurum birimlerince sevk belgesi düzenlenmek suretiyle',
    group_id: 0,
    extraction_class: 'procedure',
    keywords: ['kurum', 'birimlerince', 'sevk', 'belgesi', 'düzenlenmek', 'suretiyle'],
    action: 'referral_document_issuance',
    authority: 'Kurum birimleri',
    requirement: 'mandatory_for_referral'
});

CREATE (n:MedicalReason {
    id: 2,
    text: 'maluliyet, meslek hastalığı ve kontrol muayeneleri',
    group_id: 1,
    extraction_class: 'medical_reason',
    keywords: ['maluliyet,', 'meslek', 'hastalığı', 'kontrol', 'muayeneleri'],
    context: 'referral_reasons'
});

CREATE (n:Document {
    id: 3,
    text: 'sağlık kurulu raporları',
    group_id: 2,
    extraction_class: 'document',
    keywords: ['sağlık', 'kurulu', 'raporları'],
    type: 'medical_board_report',
    context: 'referred_patients'
});

CREATE (n:BillingRule {
    id: 4,
    text: 'kurula katılan her bir uzmanlık dalı için muayene bedeli faturalandırılabilir',
    group_id: 3,
    extraction_class: 'billing_rule',
    keywords: ['kurula', 'katılan', 'her', 'bir', 'uzmanlık', 'dalı', 'için', 'muayene', 'bedeli', 'faturalandırılabilir'],
    action: 'billing',
    item: 'examination_fee',
    condition: 'per_participating_specialty',
    permission: 'allowed'
});

CREATE (n:Regulation {
    id: 5,
    text: '(15)',
    group_id: 4,
    extraction_class: 'regulation_id',
    keywords: ['(15)'],
    type: 'article_number',
    context: 'SUT_pricing'
});

CREATE (n:Scope {
    id: 6,
    text: 'Kurumca finansmanı sağlanan sağlık hizmetleri',
    group_id: 5,
    extraction_class: 'scope',
    keywords: ['kurumca', 'finansmanı', 'sağlanan', 'sağlık', 'hizmetleri'],
    payer: 'Kurum (SGK)',
    subject: 'financed_health_services'
});

CREATE (n:Authority {
    id: 7,
    text: 'Sağlık Hizmetleri Fiyatlandırma Komisyonu',
    group_id: 6,
    extraction_class: 'authority',
    keywords: ['sağlık', 'hizmetleri', 'fiyatlandırma', 'komisyonu'],
    role: 'price_determination',
    type: 'commission'
});

CREATE (n:Reference {
    id: 8,
    text: 'SUT ve eki listelerde yer almaktadır',
    group_id: 7,
    extraction_class: 'reference',
    keywords: ['sut', 'eki', 'listelerde', 'yer', 'almaktadır'],
    source: 'SUT (Health Implementation Notification)',
    content: 'prices_to_be_paid'
});

CREATE (n:ListScope {
    id: 9,
    text: 'SUT eki EK-2/B, EK-2/C ve EK-2/Ç listelerinde yer alan işlemler',
    group_id: 8,
    extraction_class: 'list_scope',
    keywords: ['sut', 'eki', 'ek-2/b,', 'ek-2/c', 'ek-2/ç', 'listelerinde', 'yer', 'alan', 'işlemler'],
    subject: 'medical_procedures'
});

CREATE (n:Parameter {
    id: 10,
    text: 'katsayı (0,593)',
    group_id: 9,
    extraction_class: 'parameter',
    keywords: ['katsayı', '(0,593)'],
    type: 'pricing_coefficient',
    value: 0.593
});

CREATE (n:CalculationMethod {
    id: 11,
    text: 'işlem bedeli ilgili puan ile katsayının çarpımı sonucu bulunacak tutardır',
    group_id: 10,
    extraction_class: 'calculation_method',
    keywords: ['işlem', 'bedeli', 'ilgili', 'puan', 'ile', 'katsayının', 'çarpımı', 'sonucu', 'bulunacak', 'tutardır'],
    formula: 'score * coefficient',
    output: 'transaction_price'
});

CREATE (n:FormattingRule {
    id: 12,
    text: 'yuvarlama işlemi yapılmaksızın virgülden sonra iki basamak olacak şekilde alınır',
    group_id: 11,
    extraction_class: 'formatting_rule',
    keywords: ['yuvarlama', 'işlemi', 'yapılmaksızın', 'virgülden', 'sonra', 'iki', 'basamak', 'olacak', 'şekilde', 'alınır'],
    rounding: 'none',
    precision: 'two_decimal_places',
    context: 'price_calculation'
});

CREATE (n:Regulation {
    id: 1,
    text: '(16)',
    group_id: 0,
    extraction_class: 'regulation',
    keywords: ['(16)'],
    type: 'article_number',
    context: 'billing_exclusions'
});


// ───────── BATCH 3/12 ─────────

CREATE (n:MedicalScope {
    id: 2,
    text: 'Sağlık hizmeti sunucularınca gerçekleştirilecek check-up, kampanya ya da tarama kapsamında yapılan işlemler',
    group_id: 1,
    extraction_class: 'medical_scope',
    keywords: ['sağlık', 'hizmeti', 'sunucularınca', 'gerçekleştirilecek', 'check-up,', 'kampanya', 'tarama', 'kapsamında', 'yapılan', 'işlemler'],
    provider: 'sağlık hizmeti sunucuları',
    excluded_activities: 'check-up, kampanya, tarama',
    status: 'non_reimbursable'
});

CREATE (n:BillingRule {
    id: 3,
    text: 'Kuruma faturalandırılmaz',
    group_id: 2,
    extraction_class: 'billing_rule',
    keywords: ['kuruma', 'faturalandırılmaz'],
    action: 'billing_prohibition',
    payer: 'Kurum (SGK)',
    beneficiary: 'sağlık hizmeti sunucusu'
});

CREATE (n:Regulation {
    id: 4,
    text: '(17)',
    group_id: 3,
    extraction_class: 'regulation',
    keywords: ['(17)'],
    type: 'article_number',
    context: 'surgical_method_pricing'
});

CREATE (n:ReferenceDoc {
    id: 5,
    text: 'SUT eki EK-2/B ve EK-2/C listelerinde yer alan işlemlerin',
    group_id: 4,
    extraction_class: 'reference_document',
    keywords: ['sut', 'eki', 'ek-2/b', 'ek-2/c', 'listelerinde', 'yer', 'alan', 'işlemlerin'],
    document: 'SUT',
    content: 'medical_procedures'
});

CREATE (n:MedicalMethod {
    id: 6,
    text: 'laparoskopik, perkütan, endoskopik, endosonografik, mikrocerrahi, robotik cerrahi gibi yöntemlerle yapılması halinde',
    group_id: 5,
    extraction_class: 'medical_method',
    keywords: ['laparoskopik,', 'perkütan,', 'endoskopik,', 'endosonografik,', 'mikrocerrahi,', 'robotik', 'cerrahi', 'gibi', 'yöntemlerle', 'yapılması', 'halinde'],
    type: 'advanced_surgical_techniques',
    condition: 'method_application'
});

CREATE (n:PaymentRule {
    id: 7,
    text: 'SUT’ta yer alan işlem puanı esas alınarak Kurumca karşılanır',
    group_id: 6,
    extraction_class: 'payment_rule',
    keywords: ['sut’ta', 'yer', 'alan', 'işlem', 'puanı', 'esas', 'alınarak', 'kurumca', 'karşılanır'],
    payer: 'Kurum',
    calculation_basis: 'standard_procedure_score',
    condition: 'no_separate_code'
});

CREATE (n:MedicalProcedure {
    id: 8,
    text: 'ayrı kodu bulunan laparoskopik, perkütan, endoskopik, endosonografik, mikrocerrahi, robotik cerrahi gibi yöntemlerle yapılan işlemler',
    group_id: 7,
    extraction_class: 'medical_procedure',
    keywords: ['ayrı', 'kodu', 'bulunan', 'laparoskopik,', 'perkütan,', 'endoskopik,', 'endosonografik,', 'mikrocerrahi,', 'robotik', 'cerrahi', 'gibi', 'yöntemlerle', 'yapılan', 'işlemler'],
    characteristic: 'has_separate_code',
    method_types: 'advanced_surgery'
});

CREATE (n:PaymentRule {
    id: 9,
    text: 'kendi puanı esas alınarak Kurumca karşılanır',
    group_id: 8,
    extraction_class: 'payment_rule',
    keywords: ['kendi', 'puanı', 'esas', 'alınarak', 'kurumca', 'karşılanır'],
    payer: 'Kurum',
    calculation_basis: 'specific_method_score',
    condition: 'separate_code_exists'
});

CREATE (n:Regulation {
    id: 10,
    text: '(18)',
    group_id: 9,
    extraction_class: 'regulation',
    keywords: ['(18)'],
    type: 'article_number',
    context: 'traffic_accident_coverage'
});

CREATE (n:Scenario {
    id: 11,
    text: 'Trafik kazası nedeniyle ilk müdahalenin sözleşmesiz sağlık hizmeti sunucularında sağlanması halinde',
    group_id: 10,
    extraction_class: 'scenario',
    keywords: ['trafik', 'kazası', 'nedeniyle', 'ilk', 'müdahalenin', 'sözleşmesiz', 'sağlık', 'hizmeti', 'sunucularında', 'sağlanması', 'halinde'],
    cause: 'traffic_accident',
    intervention_type: 'first_response',
    provider_status: 'non_contracted (sözleşmesiz)'
});

CREATE (n:CoverageScope {
    id: 12,
    text: 'bu sağlık hizmeti sunucusunda trafik kazası nedeniyle sunulan sağlık hizmetinin devamı niteliğinde olan tedaviler',
    group_id: 11,
    extraction_class: 'coverage_scope',
    keywords: ['sağlık', 'hizmeti', 'sunucusunda', 'trafik', 'kazası', 'nedeniyle', 'sunulan', 'sağlık', 'hizmetinin', 'devamı', 'niteliğinde', 'olan', 'tedaviler'],
    location: 'same_provider',
    nature: 'continuation_of_treatment',
    cause: 'traffic_accident'
});

CREATE (n:PaymentRule {
    id: 13,
    text: 'SUT ve ekleri esas alınarak Kurumca karşılanacaktır',
    group_id: 12,
    extraction_class: 'payment_rule',
    keywords: ['sut', 'ekleri', 'esas', 'alınarak', 'kurumca', 'karşılanacaktır'],
    payer: 'Kurum',
    basis: 'SUT_and_appendices',
    status: 'covered'
});

CREATE (n:TimeLimitation {
    id: 14,
    text: 'trafik kazasının oluştuğu tarihten itibaren 6 ayı geçemez',
    group_id: 13,
    extraction_class: 'time_limitation',
    keywords: ['trafik', 'kazasının', 'oluştuğu', 'tarihten', 'itibaren', 'ayı', 'geçemez'],
    start_event: 'traffic_accident_date',
    duration: '6 months',
    restriction: 'maximum_coverage_period'
});

CREATE (n:Regulation {
    id: 1,
    text: '(19)',
    group_id: 0,
    extraction_class: 'regulation_clause',
    keywords: ['(19)'],
    type: 'paragraph_number',
    context: 'general_provisions'
});

CREATE (n:Requirement {
    id: 2,
    text: 'geri ödeme kural ve/veya kriterleri belirlenmemiş sağlık hizmetleri için güncel bilimsel klinik uygunluğun bulunması gerekir',
    group_id: 1,
    extraction_class: 'requirement',
    keywords: ['geri', 'ödeme', 'kural', 've/veya', 'kriterleri', 'belirlenmemiş', 'sağlık', 'hizmetleri', 'için', 'güncel', 'bilimsel', 'klinik', 'uygunluğun', 'bulunması', 'gerekir'],
    condition: 'geri ödeme kuralı/kriteri yokluğu',
    required_standard: 'güncel bilimsel klinik uygunluk',
    context: 'Kurumca finansmanı sağlanan hizmetler'
});

CREATE (n:Regulation {
    id: 3,
    text: '(20)',
    group_id: 2,
    extraction_class: 'regulation_clause',
    keywords: ['(20)'],
    type: 'paragraph_number',
    context: 'billing_procedures'
});

CREATE (n:ReferenceList {
    id: 4,
    text: 'SUT eki EK -2/C-1 Listesinde',
    group_id: 3,
    extraction_class: 'reference_list',
    keywords: ['sut', 'eki', '-2/c-1', 'listesinde'],
    type: 'medical_procedure_list',
    document: 'SUT'
});

CREATE (n:ProviderDefinition {
    id: 5,
    text: 'SUT eki EK -2/A-1 Listesinde Sınıf -3 grubunda tanımlanan sağlık hizmeti sunucularınca',
    group_id: 4,
    extraction_class: 'provider_definition',
    keywords: ['sut', 'eki', '-2/a-1', 'listesinde', 'sınıf', 'grubunda', 'tanımlanan', 'sağlık', 'hizmeti', 'sunucularınca'],
    classification: 'Sınıf -3',
    reference_list: 'EK -2/A-1'
});

CREATE (n:BillingRule {
    id: 6,
    text: 'işlem puanlarına Listede belirtilen oranlar ilave edilerek faturalandırılır',
    group_id: 5,
    extraction_class: 'billing_rule',
    keywords: ['işlem', 'puanlarına', 'listede', 'belirtilen', 'oranlar', 'ilave', 'edilerek', 'faturalandırılır'],
    action: 'add_rate_to_points',
    trigger: 'specific_provider_class_performing_specific_list_items'
});

CREATE (n:LegalExclusion {
    id: 7,
    text: '“ 2.2.2.B- Tanıya dayalı işlem üzerinden ödeme yöntemi” başlıklı maddenin beşinci fıkrasında yer alan hüküm uygulanmaz',
    group_id: 6,
    extraction_class: 'legal_exclusion',
    keywords: ['2.2.2.b-', 'tanıya', 'dayalı', 'işlem', 'üzerinden', 'ödeme', 'yöntemi”', 'başlıklı', 'maddenin', 'beşinci', 'fıkrasında', 'yer', 'alan', 'hüküm', 'uygulanmaz'],
    excluded_regulation: '2.2.2.B - 5th paragraph',
    reason: 'special_billing_rule_application'
});

CREATE (n:RegulationHeader {
    id: 8,
    text: '2.2.1 - Ayakta tedavilerde ödeme',
    group_id: 7,
    extraction_class: 'regulation_header',
    keywords: ['2.2.1', 'ayakta', 'tedavilerde', 'ödeme'],
    topic: 'outpatient_payment',
    level: 'main_section'
});

CREATE (n:RegulationHeader {
    id: 9,
    text: '2.2.1.A - Birinci basamak sağlık kuruluşları',
    group_id: 8,
    extraction_class: 'regulation_header',
    keywords: ['2.2.1.a', 'birinci', 'basamak', 'sağlık', 'kuruluşları'],
    topic: 'primary_care_providers',
    level: 'subsection'
});

CREATE (n:Regulation {
    id: 10,
    text: '(1)',
    group_id: 9,
    extraction_class: 'regulation_clause',
    keywords: ['(1)'],
    type: 'paragraph_number',
    context: 'payment_amounts'
});

CREATE (n:PaymentRule {
    id: 11,
    text: 'Birinci basamak sağlık kuruluşlarındaki ayakta tedavilerde, her başvuru için 11 (onbir) TL ödeme yapılır',
    group_id: 10,
    extraction_class: 'payment_rule',
    keywords: ['birinci', 'basamak', 'sağlık', 'kuruluşlarındaki', 'ayakta', 'tedavilerde,', 'her', 'başvuru', 'için', '(onbir)', 'ödeme', 'yapılır'],
    provider_type: 'birinci basamak',
    service_type: 'ayakta tedavi',
    amount: '11 TL',
    unit: 'per_visit'
});

CREATE (n:PaymentRule {
    id: 12,
    text: 'Hastanın diğer bir sağlık kurumuna sevk edilmesi halinde ise sadece 5 (beş) TL ödeme yapılır',
    group_id: 11,
    extraction_class: 'payment_rule',
    keywords: ['hastanın', 'diğer', 'bir', 'sağlık', 'kurumuna', 'sevk', 'edilmesi', 'halinde', 'ise', 'sadece', '(beş)', 'ödeme', 'yapılır'],
    condition: 'patient_referral',
    amount: '5 TL',
    change_type: 'reduction'
});


// ───────── BATCH 4/12 ─────────

CREATE (n:RegulationHeader {
    id: 13,
    text: '2.2.1.B - İkinci ve üçüncü basamak sağlık kurumları',
    group_id: 12,
    extraction_class: 'regulation_header',
    keywords: ['2.2.1.b', 'i̇kinci', 'üçüncü', 'basamak', 'sağlık', 'kurumları'],
    topic: 'secondary_and_tertiary_care_providers',
    level: 'subsection'
});

CREATE (n:Amendment {
    id: 14,
    text: 'Değişik: RG- 25/08/2022- 31934/ 12-b md.',
    group_id: 13,
    extraction_class: 'legal_amendment',
    keywords: ['değişik:', 'rg-', '25/08/2022-', '31934/', '12-b', 'md.'],
    gazette_date: '25/08/2022',
    gazette_number: '31934',
    article: '12-b'
});

CREATE (n:EffectiveDate {
    id: 15,
    text: 'Yürürlük: 03/09/2022',
    group_id: 14,
    extraction_class: 'effective_date',
    keywords: ['yürürlük:', '03/09/2022'],
    date: '03/09/2022',
    type: 'enforcement_date'
});

CREATE (n:RegulationHeader {
    id: 1,
    text: '1.B-1 - Ayakta tedavilerde ödeme uygulaması',
    group_id: 0,
    extraction_class: 'regulation_header',
    keywords: ['1.b-1', 'ayakta', 'tedavilerde', 'ödeme', 'uygulaması'],
    code: '1.B-1',
    topic: 'outpatient_payment_rules'
});

CREATE (n:Scope {
    id: 2,
    text: '“Ayakta tedavilerde ödeme” uygulaması kapsamında',
    group_id: 1,
    extraction_class: 'scope',
    keywords: ['“ayakta', 'tedavilerde', 'ödeme”', 'uygulaması', 'kapsamında'],
    context: 'outpatient_services',
    type: 'payment_framework'
});

CREATE (n:BillingUnit {
    id: 3,
    text: 'sağlık hizmeti sunucusunda ayaktan her bir başvuru için',
    group_id: 2,
    extraction_class: 'billing_unit',
    keywords: ['sağlık', 'hizmeti', 'sunucusunda', 'ayaktan', 'her', 'bir', 'başvuru', 'için'],
    unit: 'per_visit',
    setting: 'outpatient',
    provider: 'healthcare_provider'
});

CREATE (n:ReferenceDoc {
    id: 4,
    text: 'SUT eki “Sağlık Hizmeti Sunucularının Ayakta Tedavilerde Sınıflandırılması Listesi” nde (EK -2/A-1)',
    group_id: 3,
    extraction_class: 'reference_document',
    keywords: ['sut', 'eki', '“sağlık', 'hizmeti', 'sunucularının', 'ayakta', 'tedavilerde', 'sınıflandırılması', 'listesi”', 'nde', '(ek', '-2/a-1)'],
    code: 'EK-2/A-1',
    purpose: 'provider_classification',
    document_type: 'SUT_annex'
});

CREATE (n:PaymentRule {
    id: 5,
    text: 'SUT eki EK-2/A Listesinde yer alan tutarlar esas alınarak ödeme yapılır',
    group_id: 4,
    extraction_class: 'payment_rule',
    keywords: ['sut', 'eki', 'ek-2/a', 'listesinde', 'yer', 'alan', 'tutarlar', 'esas', 'alınarak', 'ödeme', 'yapılır'],
    basis: 'EK-2/A List',
    action: 'payment_calculation',
    standard_rate: '1x'
});

CREATE (n:Amendment {
    id: 6,
    text: '(Ek:RG-09/05/2024-32541/1-a md. Yürürlük:11/05/2024)',
    group_id: 5,
    extraction_class: 'legal_amendment',
    keywords: ['(ek:rg-09/05/2024-32541/1-a', 'md.', 'yürürlük:11/05/2024)'],
    gazette_date: '09/05/2024',
    gazette_number: '32541',
    effective_date: '11/05/2024',
    type: 'regulation_update'
});

CREATE (n:AdministrativeProcess {
    id: 7,
    text: 'Sağlık Bakanlığı tarafından Kuruma bildirilen',
    group_id: 6,
    extraction_class: 'administrative_process',
    keywords: ['sağlık', 'bakanlığı', 'tarafından', 'kuruma', 'bildirilen'],
    sender: 'Ministry of Health',
    receiver: 'SGK (The Institution)',
    action: 'notification'
});

CREATE (n:Condition {
    id: 8,
    text: 'mesai saatlerinde aynı gün randevusu dolu olan branşlarda',
    group_id: 7,
    extraction_class: 'condition',
    keywords: ['mesai', 'saatlerinde', 'aynı', 'gün', 'randevusu', 'dolu', 'olan', 'branşlarda'],
    status: 'capacity_full',
    timing: 'working_hours',
    context: 'appointment_availability'
});

CREATE (n:InstitutionType {
    id: 9,
    text: 'Sağlık Bakanlığına bağlı ikinci ve üçüncü basamak sağlık hizmeti sunucularında',
    group_id: 8,
    extraction_class: 'institution_type',
    keywords: ['sağlık', 'bakanlığına', 'bağlı', 'ikinci', 'üçüncü', 'basamak', 'sağlık', 'hizmeti', 'sunucularında'],
    affiliation: 'Ministry of Health',
    level: '2nd_and_3rd_tier',
    type: 'public_hospital'
});

CREATE (n:ServiceDetail {
    id: 10,
    text: 'uzman hekimler tarafından mesai saatleri dışında sunulan poliklinik hizmetleri için',
    group_id: 9,
    extraction_class: 'service_detail',
    keywords: ['uzman', 'hekimler', 'tarafından', 'mesai', 'saatleri', 'dışında', 'sunulan', 'poliklinik', 'hizmetleri', 'için'],
    provider: 'specialist_doctor',
    timing: 'after_hours',
    service_type: 'polyclinic'
});

CREATE (n:PaymentCalculation {
    id: 11,
    text: 'EK -2/A Listesinde yer alan tutarların iki katı esas alınarak ödeme yapılır',
    group_id: 10,
    extraction_class: 'payment_calculation',
    keywords: ['-2/a', 'listesinde', 'yer', 'alan', 'tutarların', 'iki', 'katı', 'esas', 'alınarak', 'ödeme', 'yapılır'],
    multiplier: '2.0',
    basis: 'EK-2/A List',
    reason: 'after_hours_capacity_overflow'
});

CREATE (n:ReferenceDoc {
    id: 12,
    text: 'SUT eki “Ayaktan Başvurularda İlave Olarak Faturalandırılabilecek İşlemler Listesi” nde (EK -2/A-2)',
    group_id: 11,
    extraction_class: 'reference_document',
    keywords: ['sut', 'eki', '“ayaktan', 'başvurularda', 'i̇lave', 'olarak', 'faturalandırılabilecek', 'i̇şlemler', 'listesi”', 'nde', '(ek', '-2/a-2)'],
    code: 'EK-2/A-2',
    purpose: 'additional_billing',
    document_type: 'SUT_annex'
});

CREATE (n:CoverageRule {
    id: 13,
    text: 'yer alan işlemlerin bedelleri Kurumca karşılanır',
    group_id: 12,
    extraction_class: 'coverage_rule',
    keywords: ['yer', 'alan', 'işlemlerin', 'bedelleri', 'kurumca', 'karşılanır'],
    payer: 'SGK (The Institution)',
    status: 'covered',
    subject: 'additional_procedures'
});

CREATE (n:Condition {
    id: 1,
    text: '(2) Hastanın aynı sağlık hizmeti sunucusuna',
    group_id: 0,
    extraction_class: 'condition',
    keywords: ['(2)', 'hastanın', 'aynı', 'sağlık', 'hizmeti', 'sunucusuna'],
    subject: 'hasta',
    context: 'recurring_visit',
    provider_scope: 'same_provider'
});

CREATE (n:Exception {
    id: 2,
    text: 'acil servise başvuruları hariç olmak üzere',
    group_id: 1,
    extraction_class: 'exception',
    keywords: ['acil', 'servise', 'başvuruları', 'hariç', 'olmak', 'üzere'],
    excluded_department: 'acil servis',
    rule_context: '10_day_limit'
});

CREATE (n:TimeframeRule {
    id: 3,
    text: 'ayaktan başvurduğu gün dâhil, 10 (on) gün içindeki aynı uzmanlık dalına diğer ayaktan başvurularında',
    group_id: 2,
    extraction_class: 'timeframe_rule',
    keywords: ['ayaktan', 'başvurduğu', 'gün', 'dâhil,', '(on)', 'gün', 'içindeki', 'aynı', 'uzmanlık', 'dalına', 'diğer', 'ayaktan', 'başvurularında'],
    duration: '10 days',
    specialty_scope: 'same_specialty',
    visit_type: 'outpatient'
});

CREATE (n:BillingPermission {
    id: 4,
    text: 'sadece SUT eki EK -2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılabilecek',
    group_id: 3,
    extraction_class: 'billing_permission',
    keywords: ['sadece', 'sut', 'eki', '-2/a-2', 'listesinde', 'yer', 'alan', 'işlemlerin', 'bedelleri', 'faturalandırılabilecek'],
    status: 'allowed',
    reference_list: 'EK-2/A-2',
    item_type: 'procedures'
});

CREATE (n:BillingProhibition {
    id: 5,
    text: 'SUT eki EK-2/A Listesinde yer alan tutar faturalandırılamaz',
    group_id: 4,
    extraction_class: 'billing_prohibition',
    keywords: ['sut', 'eki', 'ek-2/a', 'listesinde', 'yer', 'alan', 'tutar', 'faturalandırılamaz'],
    status: 'prohibited',
    reference_list: 'EK-2/A',
    item_type: 'examination_fee'
});

CREATE (n:Amendment {
    id: 6,
    text: '(Değişik:RG- 09/05/2024-32541/1-b md. Yürürlük: 11/05/2024)',
    group_id: 5,
    extraction_class: 'legal_amendment',
    keywords: ['(değişik:rg-', '09/05/2024-32541/1-b', 'md.', 'yürürlük:', '11/05/2024)'],
    official_gazette_date: '09/05/2024',
    effective_date: '11/05/2024',
    gazette_number: '32541'
});

CREATE (n:MedicalScope {
    id: 7,
    text: 'EK-2/A-2 ve EK -2/C Listelerinde yer alan işlemlerin yapılmasının gerekli görülmesi',
    group_id: 6,
    extraction_class: 'medical_scope',
    keywords: ['ek-2/a-2', '-2/c', 'listelerinde', 'yer', 'alan', 'işlemlerin', 'yapılmasının', 'gerekli', 'görülmesi'],
    condition: 'medical_necessity'
});

CREATE (n:ProcessCondition {
    id: 8,
    text: 'bu muayene başvurusundan sonra aynı sağlık hizmeti sunucusunda randevu verilmek suretiyle ileri bir tarihte yapılması durumunda',
    group_id: 7,
    extraction_class: 'process_condition',
    keywords: ['muayene', 'başvurusundan', 'sonra', 'aynı', 'sağlık', 'hizmeti', 'sunucusunda', 'randevu', 'verilmek', 'suretiyle', 'ileri', 'bir', 'tarihte', 'yapılması', 'durumunda'],
    timing: 'deferred/future_date',
    mechanism: 'appointment',
    location: 'same_provider'
});

CREATE (n:BillingRule {
    id: 9,
    text: 'SUT eki EK-2/A Listesinde yer alan tutarlar ikinci bir defa girilmeksizin sadece yapılan işlem faturalandırılır',
    group_id: 8,
    extraction_class: 'billing_rule',
    keywords: ['sut', 'eki', 'ek-2/a', 'listesinde', 'yer', 'alan', 'tutarlar', 'ikinci', 'bir', 'defa', 'girilmeksizin', 'sadece', 'yapılan', 'işlem', 'faturalandırılır'],
    restriction: 'no_double_billing_for_exam',
    allowed_billing: 'procedure_only',
    reference_list_excluded: 'EK-2/A'
});


// ───────── BATCH 5/12 ─────────

CREATE (n:Regulation {
    id: 1,
    text: '(4)',
    group_id: 0,
    extraction_class: 'regulation_id',
    keywords: ['(4)'],
    type: 'paragraph_number',
    context: 'billing_regulations'
});

CREATE (n:MedicalEvent {
    id: 2,
    text: 'Hastanın aynı sağlık hizmeti sunucusunda aynı uzmanlık dalına ayaktan başvurusu',
    group_id: 1,
    extraction_class: 'medical_event',
    keywords: ['hastanın', 'aynı', 'sağlık', 'hizmeti', 'sunucusunda', 'aynı', 'uzmanlık', 'dalına', 'ayaktan', 'başvurusu'],
    actor: 'hasta',
    location: 'aynı sağlık hizmeti sunucusu',
    specialty: 'aynı uzmanlık dalı',
    type: 'outpatient_visit'
});

CREATE (n:TemporalContext {
    id: 3,
    text: 'sonrasında aynı gün “yatarak tedavi” kapsamında',
    group_id: 2,
    extraction_class: 'temporal_context',
    keywords: ['sonrasında', 'aynı', 'gün', '“yatarak', 'tedavi”', 'kapsamında'],
    timing: 'same_day',
    treatment_type: 'inpatient',
    relation: 'follows_outpatient_visit'
});

CREATE (n:Condition {
    id: 4,
    text: 'SUT eki EK -2/C Listesinde yer alan bir işlem yapılması halinde',
    group_id: 3,
    extraction_class: 'condition',
    keywords: ['sut', 'eki', '-2/c', 'listesinde', 'yer', 'alan', 'bir', 'işlem', 'yapılması', 'halinde'],
    reference_list: 'SUT EK-2/C',
    trigger_event: 'procedure_performance',
    context: 'inpatient_transition'
});

CREATE (n:BillingRule {
    id: 5,
    text: 'bu işlem ile birlikte ayaktan yapılan işlemler bu maddenin b irinci fıkrasındaki hükümlere göre faturalandırılır',
    group_id: 4,
    extraction_class: 'billing_rule',
    keywords: ['işlem', 'ile', 'birlikte', 'ayaktan', 'yapılan', 'işlemler', 'maddenin', 'irinci', 'fıkrasındaki', 'hükümlere', 'göre', 'faturalandırılır'],
    scope: 'combined_procedures',
    reference_regulation: 'madde 1. fıkra',
    action: 'bill_accordingly'
});

CREATE (n:ExceptionCondition {
    id: 6,
    text: 'Ancak “yatarak tedavi” kapsamında hizmet başına ödeme yöntemi ile bir işlem yapılması durumunda',
    group_id: 5,
    extraction_class: 'exception_condition',
    keywords: ['ancak', '“yatarak', 'tedavi”', 'kapsamında', 'hizmet', 'başına', 'ödeme', 'yöntemi', 'ile', 'bir', 'işlem', 'yapılması', 'durumunda'],
    type: 'exception',
    payment_method: 'fee_for_service',
    context: 'inpatient_treatment'
});

CREATE (n:BillingProhibition {
    id: 7,
    text: 'SUT eki EK -2/A Listesinde yer alan tutarlar faturalandırılmayacak',
    group_id: 6,
    extraction_class: 'billing_prohibition',
    keywords: ['sut', 'eki', '-2/a', 'listesinde', 'yer', 'alan', 'tutarlar', 'faturalandırılmayacak'],
    reference_list: 'SUT EK-2/A',
    action: 'do_not_bill',
    status: 'prohibited'
});

CREATE (n:BillingRequirement {
    id: 8,
    text: 'ayaktan başvurular da hizmet başına ödeme yöntemine göre faturalandırılacaktır',
    group_id: 7,
    extraction_class: 'billing_requirement',
    keywords: ['ayaktan', 'başvurular', 'hizmet', 'başına', 'ödeme', 'yöntemine', 'göre', 'faturalandırılacaktır'],
    scope: 'outpatient_visits',
    payment_method: 'fee_for_service',
    obligation: 'mandatory'
});

CREATE (n:Regulation {
    id: 1,
    text: '(5)',
    group_id: 0,
    extraction_class: 'regulation',
    keywords: ['(5)'],
    type: 'clause_number',
    context: 'billing_regulations'
});

CREATE (n:Scenario {
    id: 2,
    text: 'Hastanın aynı gün içerisinde, aynı sağlık hizmeti sunucusunda; birden fazla uzmanlık dalına başvurusu sonrasında',
    group_id: 1,
    extraction_class: 'scenario',
    keywords: ['hastanın', 'aynı', 'gün', 'içerisinde,', 'aynı', 'sağlık', 'hizmeti', 'sunucusunda;', 'birden', 'fazla', 'uzmanlık', 'dalına', 'başvurusu', 'sonrasında'],
    subject: 'hasta',
    timeframe: 'same_day',
    location: 'same_provider',
    event: 'multiple_specialty_applications'
});

CREATE (n:Condition {
    id: 3,
    text: 'bu uzmanlık dallarından herhangi birinde aynı gün “yatarak tedavi” kapsamında SUT eki EK-2/C Listesinde yer alan bir işlem yapılması halind e',
    group_id: 2,
    extraction_class: 'condition',
    keywords: ['uzmanlık', 'dallarından', 'herhangi', 'birinde', 'aynı', 'gün', '“yatarak', 'tedavi”', 'kapsamında', 'sut', 'eki', 'ek-2/c', 'listesinde', 'yer', 'alan', 'bir', 'işlem', 'yapılması', 'halind'],
    treatment_type: 'inpatient',
    reference_list: 'SUT EK-2/C',
    trigger_event: 'procedure_performance'
});

CREATE (n:BillingRule {
    id: 4,
    text: 'bu işlem ile birlikte, o uzmanlık dalına ait ayaktan yapılan işlemler bu maddenin birinci fıkrasındaki hükümlere göre',
    group_id: 3,
    extraction_class: 'billing_rule',
    keywords: ['işlem', 'ile', 'birlikte,', 'uzmanlık', 'dalına', 'ait', 'ayaktan', 'yapılan', 'işlemler', 'maddenin', 'birinci', 'fıkrasındaki', 'hükümlere', 'göre'],
    scope: 'related_specialty_outpatient_procedures',
    reference_regulation: 'paragraph_1',
    billing_method: 'standard_procedure'
});

CREATE (n:BillingRule {
    id: 5,
    text: 'diğer uzmanlık dallarındaki ayakta tedavi kapsamındaki başvuruları SUT eki EK -2/B Listesindeki “normal poliklinik muayenesi” bedeli',
    group_id: 4,
    extraction_class: 'billing_rule',
    keywords: ['diğer', 'uzmanlık', 'dallarındaki', 'ayakta', 'tedavi', 'kapsamındaki', 'başvuruları', 'sut', 'eki', '-2/b', 'listesindeki', '“normal', 'poliklinik', 'muayenesi”', 'bedeli'],
    scope: 'other_specialties',
    reference_list: 'SUT EK-2/B',
    billable_item: 'normal_polyclinic_exam'
});

CREATE (n:BillingRule {
    id: 6,
    text: 've yapılması halinde SUT eki EK -2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılacaktır',
    group_id: 5,
    extraction_class: 'billing_rule',
    keywords: ['yapılması', 'halinde', 'sut', 'eki', '-2/a-2', 'listesinde', 'yer', 'alan', 'işlemlerin', 'bedelleri', 'faturalandırılacaktır'],
    condition: 'if_performed',
    reference_list: 'SUT EK-2/A-2',
    action: 'bill_procedure_cost'
});

CREATE (n:ExceptionCondition {
    id: 7,
    text: 'Ancak, yatarak tedavi kapsamında hizmet başına ödeme yöntemi ile bir işlem yapılması durumunda',
    group_id: 6,
    extraction_class: 'exception_condition',
    keywords: ['ancak,', 'yatarak', 'tedavi', 'kapsamında', 'hizmet', 'başına', 'ödeme', 'yöntemi', 'ile', 'bir', 'işlem', 'yapılması', 'durumunda'],
    context: 'inpatient_treatment',
    payment_method: 'fee_for_service',
    type: 'exception_trigger'
});

CREATE (n:Prohibition {
    id: 8,
    text: 'SUT eki EK-2/A Listesinde yer alan tutarlar faturalandırılmay acak',
    group_id: 7,
    extraction_class: 'prohibition',
    keywords: ['sut', 'eki', 'ek-2/a', 'listesinde', 'yer', 'alan', 'tutarlar', 'faturalandırılmay', 'acak'],
    reference_list: 'SUT EK-2/A',
    action: 'do_not_bill',
    status: 'prohibited'
});

CREATE (n:BillingInstruction {
    id: 9,
    text: 'olup ayaktan yapılan işlemler hizmet başına ödeme yöntemine göre faturalandırılacaktır',
    group_id: 8,
    extraction_class: 'billing_instruction',
    keywords: ['olup', 'ayaktan', 'yapılan', 'işlemler', 'hizmet', 'başına', 'ödeme', 'yöntemine', 'göre', 'faturalandırılacaktır'],
    scope: 'outpatient_procedures',
    billing_method: 'fee_for_service',
    requirement: 'mandatory'
});

CREATE (n:RegulationMarker {
    id: 1,
    text: '(6)',
    group_id: 0,
    extraction_class: 'regulation_marker',
    keywords: ['(6)'],
    type: 'paragraph_number',
    context: 'billing_rules'
});

CREATE (n:MedicalScenario {
    id: 2,
    text: 'Hastanın, aynı gün içinde aynı sağlık hizmeti sunucusunda ilk muayenesini takip eden diğer uzmanlık dallarındaki ayakta tedavi kapsamında yer alan başvuruları',
    group_id: 1,
    extraction_class: 'medical_scenario',
    keywords: ['hastanın,', 'aynı', 'gün', 'içinde', 'aynı', 'sağlık', 'hizmeti', 'sunucusunda', 'ilk', 'muayenesini', 'takip', 'eden', 'diğer', 'uzmanlık', 'dallarındaki', 'ayakta', 'tedavi', 'kapsamında', 'yer', 'alan'],
    condition: 'multiple_visits_same_day',
    location: 'same_health_provider',
    specialty_context: 'different_specialties',
    treatment_type: 'outpatient'
});

CREATE (n:BillingRule {
    id: 3,
    text: '“ayakta tedavilerde ödeme” uygulaması kapsamında değerlendirilmez',
    group_id: 2,
    extraction_class: 'billing_rule',
    keywords: ['“ayakta', 'tedavilerde', 'ödeme”', 'uygulaması', 'kapsamında', 'değerlendirilmez'],
    payment_model: 'ayakta tedavilerde ödeme',
    status: 'excluded'
});

CREATE (n:BillingProhibition {
    id: 4,
    text: 'SUT eki EK-2/A Listesinde yer alan tutarlar faturalandırılamaz',
    group_id: 3,
    extraction_class: 'billing_prohibition',
    keywords: ['sut', 'eki', 'ek-2/a', 'listesinde', 'yer', 'alan', 'tutarlar', 'faturalandırılamaz'],
    reference_list: 'SUT eki EK-2/A',
    action: 'billing',
    permission: 'forbidden'
});

CREATE (n:BillingPermission {
    id: 5,
    text: 'SUT eki EK-2/B Listesindeki “normal poliklinik muayenesi” bedeli ve yapılması halinde SUT eki EK-2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılacaktır',
    group_id: 4,
    extraction_class: 'billing_permission',
    keywords: ['sut', 'eki', 'ek-2/b', 'listesindeki', '“normal', 'poliklinik', 'muayenesi”', 'bedeli', 'yapılması', 'halinde', 'sut', 'eki', 'ek-2/a-2', 'listesinde', 'yer', 'alan', 'işlemlerin', 'bedelleri', 'faturalandırılacaktır'],
    reference_list_1: 'SUT eki EK-2/B',
    item_1: 'normal poliklinik muayenesi',
    reference_list_2: 'SUT eki EK-2/A-2',
    permission: 'mandatory'
});

CREATE (n:RegulationMarker {
    id: 6,
    text: '(7)',
    group_id: 5,
    extraction_class: 'regulation_marker',
    keywords: ['(7)'],
    type: 'paragraph_number',
    context: 'main_branch_sub_branch_billing'
});

CREATE (n:MedicalScenario {
    id: 7,
    text: 'Hastanın aynı gün içinde aynı sağlık hizmeti sunucusundaki ilk başvurusunun ana dal, sonraki başvurusunun yan dal olması durumunda',
    group_id: 6,
    extraction_class: 'medical_scenario',
    keywords: ['hastanın', 'aynı', 'gün', 'içinde', 'aynı', 'sağlık', 'hizmeti', 'sunucusundaki', 'ilk', 'başvurusunun', 'ana', 'dal,', 'sonraki', 'başvurusunun', 'yan', 'dal', 'olması', 'durumunda'],
    condition: 'main_branch_to_sub_branch',
    timing: 'same_day',
    location: 'same_health_provider'
});

CREATE (n:BillingRule {
    id: 8,
    text: 'yan dala olan başvuru "ayakta tedavilerde ödeme” uygulaması kapsamında faturalandırılır',
    group_id: 7,
    extraction_class: 'billing_rule',
    keywords: ['yan', 'dala', 'olan', 'başvuru', '"ayakta', 'tedavilerde', 'ödeme”', 'uygulaması', 'kapsamında', 'faturalandırılır'],
    subject: 'yan dal başvurusu',
    payment_model: 'ayakta tedavilerde ödeme',
    status: 'included'
});


// ───────── BATCH 6/12 ─────────

CREATE (n:ContextSwitch {
    id: 9,
    text: 'Ana dala başvuru ise',
    group_id: 8,
    extraction_class: 'context_switch',
    keywords: ['ana', 'dala', 'başvuru', 'ise'],
    subject: 'ana dal başvurusu',
    role: 'contrast_case'
});

CREATE (n:BillingRestriction {
    id: 10,
    text: 'SUT eki EK -2/A Listesinde yer alan tuta rlar girilmeksizin',
    group_id: 9,
    extraction_class: 'billing_restriction',
    keywords: ['sut', 'eki', '-2/a', 'listesinde', 'yer', 'alan', 'tuta', 'rlar', 'girilmeksizin'],
    reference_list: 'SUT eki EK -2/A',
    action: 'data_entry',
    status: 'omitted'
});

CREATE (n:BillingPermission {
    id: 11,
    text: 'SUT eki EK -2/B Listesindeki “normal poliklinik muayenesi” bedeli ve yapılması halinde SUT eki EK-2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılabilir',
    group_id: 10,
    extraction_class: 'billing_permission',
    keywords: ['sut', 'eki', '-2/b', 'listesindeki', '“normal', 'poliklinik', 'muayenesi”', 'bedeli', 'yapılması', 'halinde', 'sut', 'eki', 'ek-2/a-2', 'listesinde', 'yer', 'alan', 'işlemlerin', 'bedelleri'],
    reference_list_1: 'SUT eki EK -2/B',
    item_1: 'normal poliklinik muayenesi',
    reference_list_2: 'SUT eki EK-2/A-2',
    permission: 'allowed'
});

CREATE (n:Regulation {
    id: 1,
    text: '(8)',
    group_id: 0,
    extraction_class: 'regulation_clause',
    keywords: ['(8)'],
    number: '8',
    type: 'article_subsection'
});

CREATE (n:Requirement {
    id: 2,
    text: 'Sağlık raporu ile yapılması gerekli görülen',
    group_id: 1,
    extraction_class: 'requirement',
    keywords: ['sağlık', 'raporu', 'ile', 'yapılması', 'gerekli', 'görülen'],
    document: 'sağlık raporu',
    necessity: 'mandatory',
    context: 'treatment_prerequisite'
});

CREATE (n:MedicalScope {
    id: 3,
    text: 'hiperbarik oksijen tedavisi, fizik tedavi ve rehabilitasyon, ESWL ve ESWT tedavilerinde',
    group_id: 2,
    extraction_class: 'medical_scope',
    keywords: ['hiperbarik', 'oksijen', 'tedavisi,', 'fizik', 'tedavi', 'rehabilitasyon,', 'eswl', 'eswt', 'tedavilerinde'],
    category: 'specialized_treatments'
});

CREATE (n:PatientStatus {
    id: 4,
    text: 'ayaktan başvurularda',
    group_id: 3,
    extraction_class: 'patient_status',
    keywords: ['ayaktan', 'başvurularda'],
    type: 'outpatient',
    context: 'application_mode'
});

CREATE (n:ProcessStep {
    id: 5,
    text: 'tedavi için sağlık raporu düzenlendikten sonra',
    group_id: 4,
    extraction_class: 'process_step',
    keywords: ['tedavi', 'için', 'sağlık', 'raporu', 'düzenlendikten', 'sonra'],
    action: 'report_issuance',
    timing: 'post_issuance',
    sequence: 'prerequisite_met'
});

CREATE (n:Condition {
    id: 6,
    text: 'tedavinin sonraki günlerde aynı veya başka bir sağl ık hizmeti sunucusunda yapılması halinde',
    group_id: 5,
    extraction_class: 'condition',
    keywords: ['tedavinin', 'sonraki', 'günlerde', 'aynı', 'veya', 'başka', 'bir', 'sağl', 'hizmeti', 'sunucusunda', 'yapılması', 'halinde'],
    timing: 'subsequent_days',
    provider_flexibility: 'same_or_different_provider',
    scenario: 'continuation_of_treatment'
});

CREATE (n:Subject {
    id: 7,
    text: 'bu sağlık raporu ile yapılan tedavi başvuruları',
    group_id: 6,
    extraction_class: 'subject',
    keywords: ['sağlık', 'raporu', 'ile', 'yapılan', 'tedavi', 'başvuruları'],
    reference: 'treatment_applications',
    basis: 'health_report'
});

CREATE (n:PaymentContext {
    id: 8,
    text: '"ayakta tedavilerde ödeme” uygulaması kapsamında',
    group_id: 7,
    extraction_class: 'payment_context',
    keywords: ['"ayakta', 'tedavilerde', 'ödeme”', 'uygulaması', 'kapsamında'],
    scheme: 'outpatient_payment',
    type: 'reimbursement_model'
});

CREATE (n:RegulationReference {
    id: 9,
    text: 'SUT eki EK-2/A Listesinde yer',
    group_id: 8,
    extraction_class: 'regulation_reference',
    keywords: ['sut', 'eki', 'ek-2/a', 'listesinde', 'yer'],
    source: 'SUT (Sağlık Uygulama Tebliği)',
    list_code: 'EK-2/A',
    status: 'listed/included'
});

MATCH (c:Condition {id: 10}),
      (p:Prohibition {id: 10})
CREATE (c)-[:TRIGGERS {type: 'prohibition'}]->(p);

MATCH (c:Condition {id: 8}),
      (p:Prohibition {id: 8})
CREATE (c)-[:TRIGGERS {type: 'prohibition'}]->(p);

MATCH (c:Condition {id: 4}),
      (p:Prohibition {id: 4})
CREATE (c)-[:TRIGGERS {type: 'prohibition'}]->(p);

MATCH (c:Condition {id: 3}),
      (p:Prohibition {id: 3})
CREATE (c)-[:TRIGGERS {type: 'prohibition'}]->(p);

MATCH (c:Condition {id: 6}),
      (o:Obligation {id: 6})
CREATE (c)-[:REQUIRES {type: 'obligation'}]->(o);

MATCH (r:DeductionRule {id: 2}),
      (e:Entity {id: 3})
CREATE (r)-[:APPLIES_TO {target: 'sözleşmeli sağlık hizmeti sunucusu'}]->(e);

MATCH (r:DeductionRule {id: 2}),
      (e:Entity {id: 4})
CREATE (r)-[:APPLIES_TO {target: 'sözleşmeli sağlık hizmeti sunucusu'}]->(e);

MATCH (rule:PaymentRule {id: 13}),
      (ref:ReferenceDoc {id: 14})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:PaymentRule {id: 12}),
      (ref:ReferenceDoc {id: 14})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:BillingRule {id: 15}),
      (ref:ReferenceDoc {id: 14})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:PaymentRule {id: 7}),
      (ref:ReferenceDoc {id: 5})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:PaymentRule {id: 7}),
      (ref:ReferenceDoc {id: 5})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:PaymentRule {id: 5}),
      (ref:ReferenceDoc {id: 5})
CREATE (rule)-[:REFERENCES]->(ref);


// ───────── BATCH 7/12 ─────────

MATCH (rule:BillingRule {id: 4}),
      (ref:ReferenceDoc {id: 5})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:BillingRule {id: 3}),
      (ref:ReferenceDoc {id: 5})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:BillingRule {id: 6}),
      (ref:ReferenceDoc {id: 5})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:BillingRule {id: 5}),
      (ref:ReferenceDoc {id: 5})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:BillingRule {id: 4}),
      (ref:ReferenceDoc {id: 5})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:BillingRule {id: 5}),
      (ref:ReferenceDoc {id: 5})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:BillingRule {id: 6}),
      (ref:ReferenceDoc {id: 5})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:BillingRule {id: 3}),
      (ref:ReferenceDoc {id: 5})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:PaymentRule {id: 5}),
      (ref:ReferenceDoc {id: 4})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:BillingRule {id: 4}),
      (ref:ReferenceDoc {id: 4})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:BillingRule {id: 3}),
      (ref:ReferenceDoc {id: 4})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:BillingRule {id: 6}),
      (ref:ReferenceDoc {id: 4})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:BillingRule {id: 5}),
      (ref:ReferenceDoc {id: 4})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:BillingRule {id: 4}),
      (ref:ReferenceDoc {id: 4})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:BillingRule {id: 5}),
      (ref:ReferenceDoc {id: 4})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:BillingRule {id: 6}),
      (ref:ReferenceDoc {id: 4})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:BillingRule {id: 3}),
      (ref:ReferenceDoc {id: 4})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:DeductionRule {id: 2}),
      (ref:ReferenceDoc {id: 4})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:PaymentRule {id: 13}),
      (ref:ReferenceDoc {id: 12})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:PaymentRule {id: 11}),
      (ref:ReferenceDoc {id: 12})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:PaymentRule {id: 12}),
      (ref:ReferenceDoc {id: 12})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:BillingRule {id: 10}),
      (ref:ReferenceDoc {id: 12})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (rule:FinancialRule {id: 11}),
      (ref:ReferenceDoc {id: 12})
CREATE (rule)-[:REFERENCES]->(ref);

MATCH (p:Procedure {id: 2}),
      (r:Requirement {id: 2})
CREATE (p)-[:HAS_REQUIREMENT]->(r);

MATCH (p:Procedure {id: 2}),
      (r:Requirement {id: 2})
CREATE (p)-[:HAS_REQUIREMENT]->(r);


// ───────── BATCH 8/12 ─────────

MATCH (reg:Regulation {id: 12}),
      (exc:Exception {id: 12})
CREATE (reg)-[:HAS_EXCEPTION]->(exc);

MATCH (curr:PaymentRule {id: 1}),
      (next:Regulation {id: 1})
CREATE (curr)-[:IN_CONTEXT {group: 0, order: 0}]->(next);

MATCH (curr:Regulation {id: 1}),
      (next:Institution {id: 1})
CREATE (curr)-[:IN_CONTEXT {group: 0, order: 1}]->(next);

MATCH (curr:Institution {id: 1}),
      (next:Procedure {id: 1})
CREATE (curr)-[:IN_CONTEXT {group: 0, order: 2}]->(next);

MATCH (curr:Procedure {id: 1}),
      (next:Regulation {id: 1})
CREATE (curr)-[:IN_CONTEXT {group: 0, order: 3}]->(next);

MATCH (curr:Regulation {id: 1}),
      (next:Regulation {id: 1})
CREATE (curr)-[:IN_CONTEXT {group: 0, order: 4}]->(next);

MATCH (curr:Regulation {id: 1}),
      (next:RegulationHeader {id: 1})
CREATE (curr)-[:IN_CONTEXT {group: 0, order: 5}]->(next);

MATCH (curr:RegulationHeader {id: 1}),
      (next:Condition {id: 1})
CREATE (curr)-[:IN_CONTEXT {group: 0, order: 6}]->(next);

MATCH (curr:Condition {id: 1}),
      (next:Regulation {id: 1})
CREATE (curr)-[:IN_CONTEXT {group: 0, order: 7}]->(next);

MATCH (curr:Regulation {id: 1}),
      (next:Regulation {id: 1})
CREATE (curr)-[:IN_CONTEXT {group: 0, order: 8}]->(next);

MATCH (curr:Regulation {id: 1}),
      (next:RegulationMarker {id: 1})
CREATE (curr)-[:IN_CONTEXT {group: 0, order: 9}]->(next);

MATCH (curr:RegulationMarker {id: 1}),
      (next:Regulation {id: 1})
CREATE (curr)-[:IN_CONTEXT {group: 0, order: 10}]->(next);

MATCH (curr:DeductionRule {id: 2}),
      (next:Condition {id: 2})
CREATE (curr)-[:IN_CONTEXT {group: 1, order: 0}]->(next);

MATCH (curr:Condition {id: 2}),
      (next:Procedure {id: 2})
CREATE (curr)-[:IN_CONTEXT {group: 1, order: 1}]->(next);

MATCH (curr:Procedure {id: 2}),
      (next:MedicalReason {id: 2})
CREATE (curr)-[:IN_CONTEXT {group: 1, order: 2}]->(next);

MATCH (curr:MedicalReason {id: 2}),
      (next:MedicalScope {id: 2})
CREATE (curr)-[:IN_CONTEXT {group: 1, order: 3}]->(next);

MATCH (curr:MedicalScope {id: 2}),
      (next:Requirement {id: 2})
CREATE (curr)-[:IN_CONTEXT {group: 1, order: 4}]->(next);

MATCH (curr:Requirement {id: 2}),
      (next:Scope {id: 2})
CREATE (curr)-[:IN_CONTEXT {group: 1, order: 5}]->(next);

MATCH (curr:Scope {id: 2}),
      (next:Exception {id: 2})
CREATE (curr)-[:IN_CONTEXT {group: 1, order: 6}]->(next);

MATCH (curr:Exception {id: 2}),
      (next:MedicalEvent {id: 2})
CREATE (curr)-[:IN_CONTEXT {group: 1, order: 7}]->(next);

MATCH (curr:MedicalEvent {id: 2}),
      (next:Scenario {id: 2})
CREATE (curr)-[:IN_CONTEXT {group: 1, order: 8}]->(next);

MATCH (curr:Scenario {id: 2}),
      (next:MedicalScenario {id: 2})
CREATE (curr)-[:IN_CONTEXT {group: 1, order: 9}]->(next);

MATCH (curr:MedicalScenario {id: 2}),
      (next:Requirement {id: 2})
CREATE (curr)-[:IN_CONTEXT {group: 1, order: 10}]->(next);

MATCH (curr:Entity {id: 3}),
      (next:Prohibition {id: 3})
CREATE (curr)-[:IN_CONTEXT {group: 2, order: 0}]->(next);

MATCH (curr:Prohibition {id: 3}),
      (next:MedicalContext {id: 3})
CREATE (curr)-[:IN_CONTEXT {group: 2, order: 1}]->(next);


// ───────── BATCH 9/12 ─────────

MATCH (curr:MedicalContext {id: 3}),
      (next:Document {id: 3})
CREATE (curr)-[:IN_CONTEXT {group: 2, order: 2}]->(next);

MATCH (curr:Document {id: 3}),
      (next:BillingRule {id: 3})
CREATE (curr)-[:IN_CONTEXT {group: 2, order: 3}]->(next);

MATCH (curr:BillingRule {id: 3}),
      (next:Regulation {id: 3})
CREATE (curr)-[:IN_CONTEXT {group: 2, order: 4}]->(next);

MATCH (curr:Regulation {id: 3}),
      (next:BillingUnit {id: 3})
CREATE (curr)-[:IN_CONTEXT {group: 2, order: 5}]->(next);

MATCH (curr:BillingUnit {id: 3}),
      (next:TimeframeRule {id: 3})
CREATE (curr)-[:IN_CONTEXT {group: 2, order: 6}]->(next);

MATCH (curr:TimeframeRule {id: 3}),
      (next:TemporalContext {id: 3})
CREATE (curr)-[:IN_CONTEXT {group: 2, order: 7}]->(next);

MATCH (curr:TemporalContext {id: 3}),
      (next:Condition {id: 3})
CREATE (curr)-[:IN_CONTEXT {group: 2, order: 8}]->(next);

MATCH (curr:Condition {id: 3}),
      (next:BillingRule {id: 3})
CREATE (curr)-[:IN_CONTEXT {group: 2, order: 9}]->(next);

MATCH (curr:BillingRule {id: 3}),
      (next:MedicalScope {id: 3})
CREATE (curr)-[:IN_CONTEXT {group: 2, order: 10}]->(next);

MATCH (curr:FinancialMechanism {id: 4}),
      (next:Prohibition {id: 4})
CREATE (curr)-[:IN_CONTEXT {group: 3, order: 0}]->(next);

MATCH (curr:Prohibition {id: 4}),
      (next:Entity {id: 4})
CREATE (curr)-[:IN_CONTEXT {group: 3, order: 1}]->(next);

MATCH (curr:Entity {id: 4}),
      (next:BillingRule {id: 4})
CREATE (curr)-[:IN_CONTEXT {group: 3, order: 2}]->(next);

MATCH (curr:BillingRule {id: 4}),
      (next:Regulation {id: 4})
CREATE (curr)-[:IN_CONTEXT {group: 3, order: 3}]->(next);

MATCH (curr:Regulation {id: 4}),
      (next:ReferenceList {id: 4})
CREATE (curr)-[:IN_CONTEXT {group: 3, order: 4}]->(next);

MATCH (curr:ReferenceList {id: 4}),
      (next:ReferenceDoc {id: 4})
CREATE (curr)-[:IN_CONTEXT {group: 3, order: 5}]->(next);

MATCH (curr:ReferenceDoc {id: 4}),
      (next:BillingPermission {id: 4})
CREATE (curr)-[:IN_CONTEXT {group: 3, order: 6}]->(next);

MATCH (curr:BillingPermission {id: 4}),
      (next:Condition {id: 4})
CREATE (curr)-[:IN_CONTEXT {group: 3, order: 7}]->(next);

MATCH (curr:Condition {id: 4}),
      (next:BillingRule {id: 4})
CREATE (curr)-[:IN_CONTEXT {group: 3, order: 8}]->(next);

MATCH (curr:BillingRule {id: 4}),
      (next:BillingProhibition {id: 4})
CREATE (curr)-[:IN_CONTEXT {group: 3, order: 9}]->(next);

MATCH (curr:BillingProhibition {id: 4}),
      (next:PatientStatus {id: 4})
CREATE (curr)-[:IN_CONTEXT {group: 3, order: 10}]->(next);

MATCH (curr:Regulation {id: 5}),
      (next:Condition {id: 5})
CREATE (curr)-[:IN_CONTEXT {group: 4, order: 0}]->(next);

MATCH (curr:Condition {id: 5}),
      (next:ScopeDefinition {id: 5})
CREATE (curr)-[:IN_CONTEXT {group: 4, order: 1}]->(next);

MATCH (curr:ScopeDefinition {id: 5}),
      (next:Regulation {id: 5})
CREATE (curr)-[:IN_CONTEXT {group: 4, order: 2}]->(next);

MATCH (curr:Regulation {id: 5}),
      (next:ReferenceDoc {id: 5})
CREATE (curr)-[:IN_CONTEXT {group: 4, order: 3}]->(next);

MATCH (curr:ReferenceDoc {id: 5}),
      (next:ProviderDefinition {id: 5})
CREATE (curr)-[:IN_CONTEXT {group: 4, order: 4}]->(next);


// ───────── BATCH 10/12 ─────────

MATCH (curr:ProviderDefinition {id: 5}),
      (next:PaymentRule {id: 5})
CREATE (curr)-[:IN_CONTEXT {group: 4, order: 5}]->(next);

MATCH (curr:PaymentRule {id: 5}),
      (next:BillingProhibition {id: 5})
CREATE (curr)-[:IN_CONTEXT {group: 4, order: 6}]->(next);

MATCH (curr:BillingProhibition {id: 5}),
      (next:BillingRule {id: 5})
CREATE (curr)-[:IN_CONTEXT {group: 4, order: 7}]->(next);

MATCH (curr:BillingRule {id: 5}),
      (next:BillingRule {id: 5})
CREATE (curr)-[:IN_CONTEXT {group: 4, order: 8}]->(next);

MATCH (curr:BillingRule {id: 5}),
      (next:BillingPermission {id: 5})
CREATE (curr)-[:IN_CONTEXT {group: 4, order: 9}]->(next);

MATCH (curr:BillingPermission {id: 5}),
      (next:ProcessStep {id: 5})
CREATE (curr)-[:IN_CONTEXT {group: 4, order: 10}]->(next);

MATCH (curr:Entity {id: 6}),
      (next:Obligation {id: 6})
CREATE (curr)-[:IN_CONTEXT {group: 5, order: 0}]->(next);

MATCH (curr:Obligation {id: 6}),
      (next:ExcludedServices {id: 6})
CREATE (curr)-[:IN_CONTEXT {group: 5, order: 1}]->(next);

MATCH (curr:ExcludedServices {id: 6}),
      (next:Scope {id: 6})
CREATE (curr)-[:IN_CONTEXT {group: 5, order: 2}]->(next);

MATCH (curr:Scope {id: 6}),
      (next:MedicalMethod {id: 6})
CREATE (curr)-[:IN_CONTEXT {group: 5, order: 3}]->(next);

MATCH (curr:MedicalMethod {id: 6}),
      (next:BillingRule {id: 6})
CREATE (curr)-[:IN_CONTEXT {group: 5, order: 4}]->(next);

MATCH (curr:BillingRule {id: 6}),
      (next:Amendment {id: 6})
CREATE (curr)-[:IN_CONTEXT {group: 5, order: 5}]->(next);

MATCH (curr:Amendment {id: 6}),
      (next:Amendment {id: 6})
CREATE (curr)-[:IN_CONTEXT {group: 5, order: 6}]->(next);

MATCH (curr:Amendment {id: 6}),
      (next:ExceptionCondition {id: 6})
CREATE (curr)-[:IN_CONTEXT {group: 5, order: 7}]->(next);

MATCH (curr:ExceptionCondition {id: 6}),
      (next:BillingRule {id: 6})
CREATE (curr)-[:IN_CONTEXT {group: 5, order: 8}]->(next);

MATCH (curr:BillingRule {id: 6}),
      (next:RegulationMarker {id: 6})
CREATE (curr)-[:IN_CONTEXT {group: 5, order: 9}]->(next);

MATCH (curr:RegulationMarker {id: 6}),
      (next:Condition {id: 6})
CREATE (curr)-[:IN_CONTEXT {group: 5, order: 10}]->(next);

MATCH (curr:Process {id: 7}),
      (next:Regulation {id: 7})
CREATE (curr)-[:IN_CONTEXT {group: 6, order: 0}]->(next);

MATCH (curr:Regulation {id: 7}),
      (next:PaymentRule {id: 7})
CREATE (curr)-[:IN_CONTEXT {group: 6, order: 1}]->(next);

MATCH (curr:PaymentRule {id: 7}),
      (next:Authority {id: 7})
CREATE (curr)-[:IN_CONTEXT {group: 6, order: 2}]->(next);

MATCH (curr:Authority {id: 7}),
      (next:PaymentRule {id: 7})
CREATE (curr)-[:IN_CONTEXT {group: 6, order: 3}]->(next);

MATCH (curr:PaymentRule {id: 7}),
      (next:LegalExclusion {id: 7})
CREATE (curr)-[:IN_CONTEXT {group: 6, order: 4}]->(next);

MATCH (curr:LegalExclusion {id: 7}),
      (next:AdministrativeProcess {id: 7})
CREATE (curr)-[:IN_CONTEXT {group: 6, order: 5}]->(next);

MATCH (curr:AdministrativeProcess {id: 7}),
      (next:MedicalScope {id: 7})
CREATE (curr)-[:IN_CONTEXT {group: 6, order: 6}]->(next);

MATCH (curr:MedicalScope {id: 7}),
      (next:BillingProhibition {id: 7})
CREATE (curr)-[:IN_CONTEXT {group: 6, order: 7}]->(next);


// ───────── BATCH 11/12 ─────────

MATCH (curr:BillingProhibition {id: 7}),
      (next:ExceptionCondition {id: 7})
CREATE (curr)-[:IN_CONTEXT {group: 6, order: 8}]->(next);

MATCH (curr:ExceptionCondition {id: 7}),
      (next:MedicalScenario {id: 7})
CREATE (curr)-[:IN_CONTEXT {group: 6, order: 9}]->(next);

MATCH (curr:MedicalScenario {id: 7}),
      (next:Subject {id: 7})
CREATE (curr)-[:IN_CONTEXT {group: 6, order: 10}]->(next);

MATCH (curr:ScopeLimitation {id: 8}),
      (next:Entity {id: 8})
CREATE (curr)-[:IN_CONTEXT {group: 7, order: 0}]->(next);

MATCH (curr:Entity {id: 8}),
      (next:Regulation {id: 8})
CREATE (curr)-[:IN_CONTEXT {group: 7, order: 1}]->(next);

MATCH (curr:Regulation {id: 8}),
      (next:Reference {id: 8})
CREATE (curr)-[:IN_CONTEXT {group: 7, order: 2}]->(next);

MATCH (curr:Reference {id: 8}),
      (next:MedicalProcedure {id: 8})
CREATE (curr)-[:IN_CONTEXT {group: 7, order: 3}]->(next);

MATCH (curr:MedicalProcedure {id: 8}),
      (next:RegulationHeader {id: 8})
CREATE (curr)-[:IN_CONTEXT {group: 7, order: 4}]->(next);

MATCH (curr:RegulationHeader {id: 8}),
      (next:Condition {id: 8})
CREATE (curr)-[:IN_CONTEXT {group: 7, order: 5}]->(next);

MATCH (curr:Condition {id: 8}),
      (next:ProcessCondition {id: 8})
CREATE (curr)-[:IN_CONTEXT {group: 7, order: 6}]->(next);

MATCH (curr:ProcessCondition {id: 8}),
      (next:BillingRequirement {id: 8})
CREATE (curr)-[:IN_CONTEXT {group: 7, order: 7}]->(next);

MATCH (curr:BillingRequirement {id: 8}),
      (next:Prohibition {id: 8})
CREATE (curr)-[:IN_CONTEXT {group: 7, order: 8}]->(next);

MATCH (curr:Prohibition {id: 8}),
      (next:BillingRule {id: 8})
CREATE (curr)-[:IN_CONTEXT {group: 7, order: 9}]->(next);

MATCH (curr:BillingRule {id: 8}),
      (next:PaymentContext {id: 8})
CREATE (curr)-[:IN_CONTEXT {group: 7, order: 10}]->(next);

MATCH (curr:MedicalProcedures {id: 9}),
      (next:Obligation {id: 9})
CREATE (curr)-[:IN_CONTEXT {group: 8, order: 0}]->(next);

MATCH (curr:Obligation {id: 9}),
      (next:RegulatoryRequirement {id: 9})
CREATE (curr)-[:IN_CONTEXT {group: 8, order: 1}]->(next);

MATCH (curr:RegulatoryRequirement {id: 9}),
      (next:ListScope {id: 9})
CREATE (curr)-[:IN_CONTEXT {group: 8, order: 2}]->(next);

MATCH (curr:ListScope {id: 9}),
      (next:PaymentRule {id: 9})
CREATE (curr)-[:IN_CONTEXT {group: 8, order: 3}]->(next);

MATCH (curr:PaymentRule {id: 9}),
      (next:RegulationHeader {id: 9})
CREATE (curr)-[:IN_CONTEXT {group: 8, order: 4}]->(next);

MATCH (curr:RegulationHeader {id: 9}),
      (next:InstitutionType {id: 9})
CREATE (curr)-[:IN_CONTEXT {group: 8, order: 5}]->(next);

MATCH (curr:InstitutionType {id: 9}),
      (next:BillingRule {id: 9})
CREATE (curr)-[:IN_CONTEXT {group: 8, order: 6}]->(next);

MATCH (curr:BillingRule {id: 9}),
      (next:BillingInstruction {id: 9})
CREATE (curr)-[:IN_CONTEXT {group: 8, order: 7}]->(next);

MATCH (curr:BillingInstruction {id: 9}),
      (next:ContextSwitch {id: 9})
CREATE (curr)-[:IN_CONTEXT {group: 8, order: 8}]->(next);

MATCH (curr:ContextSwitch {id: 9}),
      (next:RegulationReference {id: 9})
CREATE (curr)-[:IN_CONTEXT {group: 8, order: 9}]->(next);

MATCH (curr:Prohibition {id: 10}),
      (next:Condition {id: 10})
CREATE (curr)-[:IN_CONTEXT {group: 9, order: 0}]->(next);


// ───────── BATCH 12/12 ─────────

MATCH (curr:Condition {id: 10}),
      (next:BillingRule {id: 10})
CREATE (curr)-[:IN_CONTEXT {group: 9, order: 1}]->(next);

MATCH (curr:BillingRule {id: 10}),
      (next:Parameter {id: 10})
CREATE (curr)-[:IN_CONTEXT {group: 9, order: 2}]->(next);

MATCH (curr:Parameter {id: 10}),
      (next:Regulation {id: 10})
CREATE (curr)-[:IN_CONTEXT {group: 9, order: 3}]->(next);

MATCH (curr:Regulation {id: 10}),
      (next:Regulation {id: 10})
CREATE (curr)-[:IN_CONTEXT {group: 9, order: 4}]->(next);

MATCH (curr:Regulation {id: 10}),
      (next:ServiceDetail {id: 10})
CREATE (curr)-[:IN_CONTEXT {group: 9, order: 5}]->(next);

MATCH (curr:ServiceDetail {id: 10}),
      (next:BillingRestriction {id: 10})
CREATE (curr)-[:IN_CONTEXT {group: 9, order: 6}]->(next);

MATCH (curr:Condition {id: 11}),
      (next:FinancialRule {id: 11})
CREATE (curr)-[:IN_CONTEXT {group: 10, order: 0}]->(next);

MATCH (curr:FinancialRule {id: 11}),
      (next:CalculationMethod {id: 11})
CREATE (curr)-[:IN_CONTEXT {group: 10, order: 1}]->(next);

MATCH (curr:CalculationMethod {id: 11}),
      (next:Scenario {id: 11})
CREATE (curr)-[:IN_CONTEXT {group: 10, order: 2}]->(next);

MATCH (curr:Scenario {id: 11}),
      (next:PaymentRule {id: 11})
CREATE (curr)-[:IN_CONTEXT {group: 10, order: 3}]->(next);

MATCH (curr:PaymentRule {id: 11}),
      (next:PaymentCalculation {id: 11})
CREATE (curr)-[:IN_CONTEXT {group: 10, order: 4}]->(next);

MATCH (curr:PaymentCalculation {id: 11}),
      (next:BillingPermission {id: 11})
CREATE (curr)-[:IN_CONTEXT {group: 10, order: 5}]->(next);

MATCH (curr:Exception {id: 12}),
      (next:Regulation {id: 12})
CREATE (curr)-[:IN_CONTEXT {group: 11, order: 0}]->(next);

MATCH (curr:Regulation {id: 12}),
      (next:FormattingRule {id: 12})
CREATE (curr)-[:IN_CONTEXT {group: 11, order: 1}]->(next);

MATCH (curr:FormattingRule {id: 12}),
      (next:CoverageScope {id: 12})
CREATE (curr)-[:IN_CONTEXT {group: 11, order: 2}]->(next);

MATCH (curr:CoverageScope {id: 12}),
      (next:PaymentRule {id: 12})
CREATE (curr)-[:IN_CONTEXT {group: 11, order: 3}]->(next);

MATCH (curr:PaymentRule {id: 12}),
      (next:ReferenceDoc {id: 12})
CREATE (curr)-[:IN_CONTEXT {group: 11, order: 4}]->(next);

MATCH (curr:FinancialTerm {id: 13}),
      (next:PaymentRule {id: 13})
CREATE (curr)-[:IN_CONTEXT {group: 12, order: 0}]->(next);

MATCH (curr:PaymentRule {id: 13}),
      (next:RegulationHeader {id: 13})
CREATE (curr)-[:IN_CONTEXT {group: 12, order: 1}]->(next);

MATCH (curr:RegulationHeader {id: 13}),
      (next:CoverageRule {id: 13})
CREATE (curr)-[:IN_CONTEXT {group: 12, order: 2}]->(next);

MATCH (curr:ReferenceDoc {id: 14}),
      (next:TimeLimitation {id: 14})
CREATE (curr)-[:IN_CONTEXT {group: 13, order: 0}]->(next);

MATCH (curr:TimeLimitation {id: 14}),
      (next:Amendment {id: 14})
CREATE (curr)-[:IN_CONTEXT {group: 13, order: 1}]->(next);

MATCH (curr:BillingRule {id: 15}),
      (next:EffectiveDate {id: 15})
CREATE (curr)-[:IN_CONTEXT {group: 14, order: 0}]->(next);


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


