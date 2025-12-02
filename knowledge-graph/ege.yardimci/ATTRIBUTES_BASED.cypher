// ═══════════════════════════════════════════════════════
// NEO4J AURA - ATTRIBUTES-BASED RELATIONSHIPS
// JSON attributes'larından otomatik çıkarılan ilişkiler
// Toplam Batch: 14
// ═══════════════════════════════════════════════════════

// 🔗 ATTRIBUTES'LARDAN ÇIKARILAN İLİŞKİLER:
// • PAID_TO: recipient attribute'u varsa
// • APPLIES_TO: target_entity attribute'u varsa
// • PAID_BY: payer attribute'u varsa
// • BASED_ON: basis attribute'u varsa
// • RESPONSIBLE_FOR: responsible_party attribute'u varsa
// • WHEN_THEN: Condition + consequence_trigger varsa
// • REGULATES: Regulation → aynı gruptaki rules
// • REFERENCED_IN: ReferenceDocument → yakın rules
// • FOLLOWED_BY: Aynı group içinde sıralı


// ───────── BATCH 1/14 ─────────

CREATE (e:PaymentRule {
    extraction_index: 1,
    group_index: 0,
    text: 'tem belgesine dayanılarak kişilere ödenir',
    basis: 'istem belgesi (implied)',
    recipient: 'kişiler',
    action: 'payment'
});

CREATE (e:DeductionRule {
    extraction_index: 2,
    group_index: 1,
    text: 'sevk/istem belgesini düzenleyen sözleşme li sağlık hi zmeti sunucusunun alacağından mahsup edilir',
    target_entity: 'sözleşmeli sağlık hizmeti sunucusu',
    action: 'deduction_from_receivables',
    reason: 'issuing_document'
});

CREATE (e:Entity {
    extraction_index: 3,
    group_index: 2,
    text: 'Sağlık Bakanlığına bağlı sağlık hizmeti sunucuları',
    affiliation: 'Sağlık Bakanlığı',
    type: 'public_healthcare_provider'
});

CREATE (e:FinancialMechanism {
    extraction_index: 4,
    group_index: 3,
    text: 'Bakanlığa yapılan global bütçe ödemesinden mahsup edilir',
    source: 'global bütçe',
    action: 'deduction',
    beneficiary: 'Sağlık Bakanlığı'
});

CREATE (e:RegulationId {
    extraction_index: 5,
    group_index: 4,
    text: '(10)',
    type: 'clause_number'
});

CREATE (e:Entity {
    extraction_index: 6,
    group_index: 5,
    text: 'Kurumla sözleşmeli sağlık hizmeti sunucuları',
    relationship: 'contracted',
    counterparty: 'Kurum (SGK)',
    role: 'provider'
});

CREATE (e:Process {
    extraction_index: 7,
    group_index: 6,
    text: 'bir başka sağlık hizmeti sunucusundan hizmet alımı yoluyla sağladıkları',
    type: 'outsourcing',
    method: 'service_procurement'
});

CREATE (e:ScopeLimitation {
    extraction_index: 8,
    group_index: 7,
    text: 'ruhsat/faaliyet veya uygunluk belgesinde yer al an tetkik ve/veya tahlil dışındaki tedavilere',
    document_basis: 'ruhsat/faaliyet/uygunluk belgesi',
    included: 'tetkik ve tahlil',
    excluded: 'diğer tedaviler'
});

CREATE (e:MedicalProcedures {
    extraction_index: 9,
    group_index: 8,
    text: '(gastroskopi, kolonoskopi, rektosigmoidoskopi, rektoskopi, bronkoskopi, anjiyografi gibi işlemler de dahil olmak üzere)',
    type: 'examples_of_excluded_treatments',
    category: 'interventional_procedures'
});

CREATE (e:Prohibition {
    extraction_index: 10,
    group_index: 9,
    text: 'ait giderleri Kuruma faturalandıramazlar',
    action: 'billing',
    target: 'Kurum',
    status: 'prohibited',
    context: 'outsourced_treatments_outside_license'
});

CREATE (e:Condition {
    extraction_index: 11,
    group_index: 10,
    text: 'Hekim veya diş hekimlerinin, özel sağlık hizmeti sunucusu bünyesinde çalışması halinde',
    subject: 'hekim veya diş hekimleri',
    setting: 'özel sağlık hizmeti sunucusu',
    employment_status: 'working_within'
});

CREATE (e:Exception {
    extraction_index: 12,
    group_index: 11,
    text: 'bu hekimler tarafından fatura düzenlenerek alınan/sunulan sağlık hizmetleri bu kapsamda değerlendirilmez',
    action: 'individual_invoicing',
    effect: 'exemption_from_prohibition',
    subject: 'doctors_dentists'
});

CREATE (e:Regulation {
    extraction_index: 1,
    group_index: 0,
    text: '(11)',
    type: 'article_number',
    context: 'service_procurement_rules'
});

CREATE (e:Condition {
    extraction_index: 2,
    group_index: 1,
    text: 'Başka bir sağlık hizmeti sunucusundan laboratuvar hizmeti alınması durumunda',
    context: 'outsourced_laboratory_services',
    trigger: 'service_procurement'
});

CREATE (e:Prohibition {
    extraction_index: 3,
    group_index: 2,
    text: 'hasta hastane dışına numune almak için gönderilmez',
    subject: 'hasta',
    forbidden_action: 'sending_patient_for_sample_collection',
    responsible_party: 'sağlık hizmeti sunucusu'
});

CREATE (e:Prohibition {
    extraction_index: 4,
    group_index: 3,
    text: 'alınan numunenin transferi veya sonucu hasta veya yakını aracılığı ile istenilemez',
    forbidden_action: 'transfer_via_patient_or_relative',
    items: 'numune transferi veya sonucu',
    intermediary: 'hasta veya yakını'
});

CREATE (e:Condition {
    extraction_index: 5,
    group_index: 4,
    text: 'Görüntüleme hizmetlerinin hizmet alım ı yoluyla sağlanması halinde',
    context: 'outsourced_imaging_services',
    trigger: 'service_procurement'
});

CREATE (e:Obligation {
    extraction_index: 6,
    group_index: 5,
    text: 'acil ve yatan hastaların transferi sağlık hizmeti sunucuları tarafından yapılacaktır',
    responsible_party: 'sağlık hizmeti sunucuları',
    action: 'patient_transfer',
    patient_type: 'acil ve yatan hastalar',
    requirement: 'mandatory'
});

CREATE (e:Regulation {
    extraction_index: 7,
    group_index: 6,
    text: '(12)',
    type: 'article_number',
    context: 'documentation_and_audit'
});

CREATE (e:Entity {
    extraction_index: 8,
    group_index: 7,
    text: 'Kurum ile sözleşmeli sağlık hizmeti sunucuları',
    type: 'healthcare_provider',
    contract_status: 'contracted_with_institution'
});

CREATE (e:Obligation {
    extraction_index: 9,
    group_index: 8,
    text: 'tetkik, tahlil ve tedaviye ait her türlü bilgi, belge ve raporu, istenildiğinde Kuruma ibraz edeceklerdir',
    action: 'submit_documents',
    recipient: 'Kurum (SGK)',
    trigger: 'upon_request',
    content: 'tetkik, tahlil, tedavi bilgileri'
});

CREATE (e:Condition {
    extraction_index: 10,
    group_index: 9,
    text: 'İbraz edilememesi durumunda',
    context: 'failure_to_submit_documents',
    consequence_trigger: 'true'
});

CREATE (e:FinancialRule {
    extraction_index: 11,
    group_index: 10,
    text: 'Kuruma faturalandırılan ilgili tetkik, tahlil ve/veya tedavi bedelleri Kurumca karşılanmaz',
    result: 'payment_denial',
    payer: 'Kurum',
    reason: 'documentation_failure'
});

CREATE (e:Regulation {
    extraction_index: 12,
    group_index: 11,
    text: '(13)',
    type: 'article_number',
    context: 'billing_rules'
});

CREATE (e:FinancialTerm {
    extraction_index: 13,
    group_index: 12,
    text: 'Kişilere sağlanan sağlık hizmetlerine ilişkin düzenlenen sağlık raporu bedelleri',
    topic: 'health_report_fees',
    service_type: 'administrative'
});


// ───────── BATCH 2/14 ─────────

CREATE (e:ReferenceDocument {
    extraction_index: 14,
    group_index: 13,
    text: 'SUT eki EK-2/B Listesinde yer alan rapor puanları',
    document_name: 'SUT eki EK-2/B',
    usage: 'pricing_basis',
    metric: 'rapor puanları'
});

CREATE (e:BillingRule {
    extraction_index: 15,
    group_index: 14,
    text: 'sadece bir adet olarak faturalandırılır',
    constraint: 'quantity_limit',
    limit_value: '1',
    action: 'invoicing'
});

CREATE (e:Institution {
    extraction_index: 1,
    group_index: 0,
    text: 'Kurum birimlerince',
    type: 'government_agency',
    role: 'referral_authority',
    context: 'SGK (Social Security Institution)'
});

CREATE (e:Procedure {
    extraction_index: 2,
    group_index: 1,
    text: 'sevk belgesi düzenlenmek suretiyle',
    action: 'issue_referral_document',
    requirement: 'mandatory_for_referral'
});

CREATE (e:MedicalContext {
    extraction_index: 3,
    group_index: 2,
    text: 'maluliyet, meslek hastalığı ve kontrol muayeneleri',
    type: 'referral_reasons'
});

CREATE (e:Entity {
    extraction_index: 4,
    group_index: 3,
    text: 'sağlık hizmeti sunucusuna',
    type: 'healthcare_provider',
    role: 'service_provider'
});

CREATE (e:ScopeDefinition {
    extraction_index: 5,
    group_index: 4,
    text: 'tedavi amacıyla düzenlenen sağlık raporları dışında kalan',
    type: 'exclusion_criteria',
    exception: 'treatment_purposes',
    status: 'defines_non_covered_scope'
});

CREATE (e:ExcludedServices {
    extraction_index: 6,
    group_index: 5,
    text: 'engellilik raporu, adli rapor, ehliyet raporu, vasi tayini raporu, portör muayeneleri ve işlemleri, tarama amaçlı muayene ve işlemler',
    category: 'special_purpose_reports',
    coverage_status: 'not_covered'
});

CREATE (e:PaymentRule {
    extraction_index: 7,
    group_index: 6,
    text: 'Kurumca karşılanmaz',
    payer: 'Kurum (SGK)',
    status: 'payment_denied',
    target: 'special_purpose_reports_and_procedures'
});

CREATE (e:RegulationId {
    extraction_index: 8,
    group_index: 7,
    text: '(14)',
    type: 'clause_number',
    hierarchy: 'item_14'
});

CREATE (e:RegulatoryRequirement {
    extraction_index: 9,
    group_index: 8,
    text: 'SUT gereği düzenlenmesi gereken sağlık kurulu raporu',
    source_regulation: 'SUT (Sağlık Uygulama Tebliği)',
    document_type: 'health_board_report',
    context: 'medical_supplies_and_treatment'
});

CREATE (e:BillingRule {
    extraction_index: 10,
    group_index: 9,
    text: 'sadece bir adet muayene bedeli faturalandırılabilir',
    restriction: 'single_fee',
    item: 'examination_fee',
    context: 'report_issuance'
});

CREATE (e:Procedure {
    extraction_index: 1,
    group_index: 0,
    text: 'Kurum birimlerince sevk belgesi düzenlenmek suretiyle',
    action: 'referral_document_issuance',
    authority: 'Kurum birimleri',
    requirement: 'mandatory_for_referral'
});

CREATE (e:MedicalReason {
    extraction_index: 2,
    group_index: 1,
    text: 'maluliyet, meslek hastalığı ve kontrol muayeneleri',
    context: 'referral_reasons'
});

CREATE (e:Document {
    extraction_index: 3,
    group_index: 2,
    text: 'sağlık kurulu raporları',
    type: 'medical_board_report',
    context: 'referred_patients'
});

CREATE (e:BillingRule {
    extraction_index: 4,
    group_index: 3,
    text: 'kurula katılan her bir uzmanlık dalı için muayene bedeli faturalandırılabilir',
    action: 'billing',
    item: 'examination_fee',
    condition: 'per_participating_specialty',
    permission: 'allowed'
});

CREATE (e:RegulationId {
    extraction_index: 5,
    group_index: 4,
    text: '(15)',
    type: 'article_number',
    context: 'SUT_pricing'
});

CREATE (e:Scope {
    extraction_index: 6,
    group_index: 5,
    text: 'Kurumca finansmanı sağlanan sağlık hizmetleri',
    payer: 'Kurum (SGK)',
    subject: 'financed_health_services'
});

CREATE (e:Authority {
    extraction_index: 7,
    group_index: 6,
    text: 'Sağlık Hizmetleri Fiyatlandırma Komisyonu',
    role: 'price_determination',
    type: 'commission'
});

CREATE (e:Reference {
    extraction_index: 8,
    group_index: 7,
    text: 'SUT ve eki listelerde yer almaktadır',
    source: 'SUT (Health Implementation Notification)',
    content: 'prices_to_be_paid'
});

CREATE (e:ListScope {
    extraction_index: 9,
    group_index: 8,
    text: 'SUT eki EK-2/B, EK-2/C ve EK-2/Ç listelerinde yer alan işlemler',
    subject: 'medical_procedures'
});

CREATE (e:Parameter {
    extraction_index: 10,
    group_index: 9,
    text: 'katsayı (0,593)',
    type: 'pricing_coefficient',
    value: 0.593
});

CREATE (e:CalculationMethod {
    extraction_index: 11,
    group_index: 10,
    text: 'işlem bedeli ilgili puan ile katsayının çarpımı sonucu bulunacak tutardır',
    formula: 'score * coefficient',
    output: 'transaction_price'
});

CREATE (e:FormattingRule {
    extraction_index: 12,
    group_index: 11,
    text: 'yuvarlama işlemi yapılmaksızın virgülden sonra iki basamak olacak şekilde alınır',
    rounding: 'none',
    precision: 'two_decimal_places',
    context: 'price_calculation'
});

CREATE (e:Regulation {
    extraction_index: 1,
    group_index: 0,
    text: '(16)',
    type: 'article_number',
    context: 'billing_exclusions'
});


// ───────── BATCH 3/14 ─────────

CREATE (e:MedicalScope {
    extraction_index: 2,
    group_index: 1,
    text: 'Sağlık hizmeti sunucularınca gerçekleştirilecek check-up, kampanya ya da tarama kapsamında yapılan işlemler',
    provider: 'sağlık hizmeti sunucuları',
    excluded_activities: 'check-up, kampanya, tarama',
    status: 'non_reimbursable'
});

CREATE (e:BillingRule {
    extraction_index: 3,
    group_index: 2,
    text: 'Kuruma faturalandırılmaz',
    action: 'billing_prohibition',
    payer: 'Kurum (SGK)',
    beneficiary: 'sağlık hizmeti sunucusu'
});

CREATE (e:Regulation {
    extraction_index: 4,
    group_index: 3,
    text: '(17)',
    type: 'article_number',
    context: 'surgical_method_pricing'
});

CREATE (e:ReferenceDocument {
    extraction_index: 5,
    group_index: 4,
    text: 'SUT eki EK-2/B ve EK-2/C listelerinde yer alan işlemlerin',
    document: 'SUT',
    content: 'medical_procedures'
});

CREATE (e:MedicalMethod {
    extraction_index: 6,
    group_index: 5,
    text: 'laparoskopik, perkütan, endoskopik, endosonografik, mikrocerrahi, robotik cerrahi gibi yöntemlerle yapılması halinde',
    type: 'advanced_surgical_techniques',
    condition: 'method_application'
});

CREATE (e:PaymentRule {
    extraction_index: 7,
    group_index: 6,
    text: 'SUT’ta yer alan işlem puanı esas alınarak Kurumca karşılanır',
    payer: 'Kurum',
    calculation_basis: 'standard_procedure_score',
    condition: 'no_separate_code'
});

CREATE (e:MedicalProcedure {
    extraction_index: 8,
    group_index: 7,
    text: 'ayrı kodu bulunan laparoskopik, perkütan, endoskopik, endosonografik, mikrocerrahi, robotik cerrahi gibi yöntemlerle yapılan işlemler',
    characteristic: 'has_separate_code',
    method_types: 'advanced_surgery'
});

CREATE (e:PaymentRule {
    extraction_index: 9,
    group_index: 8,
    text: 'kendi puanı esas alınarak Kurumca karşılanır',
    payer: 'Kurum',
    calculation_basis: 'specific_method_score',
    condition: 'separate_code_exists'
});

CREATE (e:Regulation {
    extraction_index: 10,
    group_index: 9,
    text: '(18)',
    type: 'article_number',
    context: 'traffic_accident_coverage'
});

CREATE (e:Scenario {
    extraction_index: 11,
    group_index: 10,
    text: 'Trafik kazası nedeniyle ilk müdahalenin sözleşmesiz sağlık hizmeti sunucularında sağlanması halinde',
    cause: 'traffic_accident',
    intervention_type: 'first_response',
    provider_status: 'non_contracted (sözleşmesiz)'
});

CREATE (e:CoverageScope {
    extraction_index: 12,
    group_index: 11,
    text: 'bu sağlık hizmeti sunucusunda trafik kazası nedeniyle sunulan sağlık hizmetinin devamı niteliğinde olan tedaviler',
    location: 'same_provider',
    nature: 'continuation_of_treatment',
    cause: 'traffic_accident'
});

CREATE (e:PaymentRule {
    extraction_index: 13,
    group_index: 12,
    text: 'SUT ve ekleri esas alınarak Kurumca karşılanacaktır',
    payer: 'Kurum',
    basis: 'SUT_and_appendices',
    status: 'covered'
});

CREATE (e:TimeLimitation {
    extraction_index: 14,
    group_index: 13,
    text: 'trafik kazasının oluştuğu tarihten itibaren 6 ayı geçemez',
    start_event: 'traffic_accident_date',
    duration: '6 months',
    restriction: 'maximum_coverage_period'
});

CREATE (e:RegulationClause {
    extraction_index: 1,
    group_index: 0,
    text: '(19)',
    type: 'paragraph_number',
    context: 'general_provisions'
});

CREATE (e:Requirement {
    extraction_index: 2,
    group_index: 1,
    text: 'geri ödeme kural ve/veya kriterleri belirlenmemiş sağlık hizmetleri için güncel bilimsel klinik uygunluğun bulunması gerekir',
    condition: 'geri ödeme kuralı/kriteri yokluğu',
    required_standard: 'güncel bilimsel klinik uygunluk',
    context: 'Kurumca finansmanı sağlanan hizmetler'
});

CREATE (e:RegulationClause {
    extraction_index: 3,
    group_index: 2,
    text: '(20)',
    type: 'paragraph_number',
    context: 'billing_procedures'
});

CREATE (e:ReferenceList {
    extraction_index: 4,
    group_index: 3,
    text: 'SUT eki EK -2/C-1 Listesinde',
    type: 'medical_procedure_list',
    document: 'SUT'
});

CREATE (e:ProviderDefinition {
    extraction_index: 5,
    group_index: 4,
    text: 'SUT eki EK -2/A-1 Listesinde Sınıf -3 grubunda tanımlanan sağlık hizmeti sunucularınca',
    classification: 'Sınıf -3',
    reference_list: 'EK -2/A-1'
});

CREATE (e:BillingRule {
    extraction_index: 6,
    group_index: 5,
    text: 'işlem puanlarına Listede belirtilen oranlar ilave edilerek faturalandırılır',
    action: 'add_rate_to_points',
    trigger: 'specific_provider_class_performing_specific_list_items'
});

CREATE (e:LegalExclusion {
    extraction_index: 7,
    group_index: 6,
    text: '“ 2.2.2.B- Tanıya dayalı işlem üzerinden ödeme yöntemi” başlıklı maddenin beşinci fıkrasında yer alan hüküm uygulanmaz',
    excluded_regulation: '2.2.2.B - 5th paragraph',
    reason: 'special_billing_rule_application'
});

CREATE (e:RegulationHeader {
    extraction_index: 8,
    group_index: 7,
    text: '2.2.1 - Ayakta tedavilerde ödeme',
    topic: 'outpatient_payment',
    level: 'main_section'
});

CREATE (e:RegulationHeader {
    extraction_index: 9,
    group_index: 8,
    text: '2.2.1.A - Birinci basamak sağlık kuruluşları',
    topic: 'primary_care_providers',
    level: 'subsection'
});

CREATE (e:RegulationClause {
    extraction_index: 10,
    group_index: 9,
    text: '(1)',
    type: 'paragraph_number',
    context: 'payment_amounts'
});

CREATE (e:PaymentRule {
    extraction_index: 11,
    group_index: 10,
    text: 'Birinci basamak sağlık kuruluşlarındaki ayakta tedavilerde, her başvuru için 11 (onbir) TL ödeme yapılır',
    provider_type: 'birinci basamak',
    service_type: 'ayakta tedavi',
    amount: '11 TL',
    unit: 'per_visit'
});

CREATE (e:PaymentRule {
    extraction_index: 12,
    group_index: 11,
    text: 'Hastanın diğer bir sağlık kurumuna sevk edilmesi halinde ise sadece 5 (beş) TL ödeme yapılır',
    condition: 'patient_referral',
    amount: '5 TL',
    change_type: 'reduction'
});


// ───────── BATCH 4/14 ─────────

CREATE (e:RegulationHeader {
    extraction_index: 13,
    group_index: 12,
    text: '2.2.1.B - İkinci ve üçüncü basamak sağlık kurumları',
    topic: 'secondary_and_tertiary_care_providers',
    level: 'subsection'
});

CREATE (e:LegalAmendment {
    extraction_index: 14,
    group_index: 13,
    text: 'Değişik: RG- 25/08/2022- 31934/ 12-b md.',
    gazette_date: '25/08/2022',
    gazette_number: '31934',
    article: '12-b'
});

CREATE (e:EffectiveDate {
    extraction_index: 15,
    group_index: 14,
    text: 'Yürürlük: 03/09/2022',
    date: '03/09/2022',
    type: 'enforcement_date'
});

CREATE (e:RegulationHeader {
    extraction_index: 1,
    group_index: 0,
    text: '1.B-1 - Ayakta tedavilerde ödeme uygulaması',
    code: '1.B-1',
    topic: 'outpatient_payment_rules'
});

CREATE (e:Scope {
    extraction_index: 2,
    group_index: 1,
    text: '“Ayakta tedavilerde ödeme” uygulaması kapsamında',
    context: 'outpatient_services',
    type: 'payment_framework'
});

CREATE (e:BillingUnit {
    extraction_index: 3,
    group_index: 2,
    text: 'sağlık hizmeti sunucusunda ayaktan her bir başvuru için',
    unit: 'per_visit',
    setting: 'outpatient',
    provider: 'healthcare_provider'
});

CREATE (e:ReferenceDocument {
    extraction_index: 4,
    group_index: 3,
    text: 'SUT eki “Sağlık Hizmeti Sunucularının Ayakta Tedavilerde Sınıflandırılması Listesi” nde (EK -2/A-1)',
    code: 'EK-2/A-1',
    purpose: 'provider_classification',
    document_type: 'SUT_annex'
});

CREATE (e:PaymentRule {
    extraction_index: 5,
    group_index: 4,
    text: 'SUT eki EK-2/A Listesinde yer alan tutarlar esas alınarak ödeme yapılır',
    basis: 'EK-2/A List',
    action: 'payment_calculation',
    standard_rate: '1x'
});

CREATE (e:LegalAmendment {
    extraction_index: 6,
    group_index: 5,
    text: '(Ek:RG-09/05/2024-32541/1-a md. Yürürlük:11/05/2024)',
    gazette_date: '09/05/2024',
    gazette_number: '32541',
    effective_date: '11/05/2024',
    type: 'regulation_update'
});

CREATE (e:AdministrativeProcess {
    extraction_index: 7,
    group_index: 6,
    text: 'Sağlık Bakanlığı tarafından Kuruma bildirilen',
    sender: 'Ministry of Health',
    receiver: 'SGK (The Institution)',
    action: 'notification'
});

CREATE (e:Condition {
    extraction_index: 8,
    group_index: 7,
    text: 'mesai saatlerinde aynı gün randevusu dolu olan branşlarda',
    status: 'capacity_full',
    timing: 'working_hours',
    context: 'appointment_availability'
});

CREATE (e:InstitutionType {
    extraction_index: 9,
    group_index: 8,
    text: 'Sağlık Bakanlığına bağlı ikinci ve üçüncü basamak sağlık hizmeti sunucularında',
    affiliation: 'Ministry of Health',
    level: '2nd_and_3rd_tier',
    type: 'public_hospital'
});

CREATE (e:ServiceDetail {
    extraction_index: 10,
    group_index: 9,
    text: 'uzman hekimler tarafından mesai saatleri dışında sunulan poliklinik hizmetleri için',
    provider: 'specialist_doctor',
    timing: 'after_hours',
    service_type: 'polyclinic'
});

CREATE (e:PaymentCalculation {
    extraction_index: 11,
    group_index: 10,
    text: 'EK -2/A Listesinde yer alan tutarların iki katı esas alınarak ödeme yapılır',
    multiplier: '2.0',
    basis: 'EK-2/A List',
    reason: 'after_hours_capacity_overflow'
});

CREATE (e:ReferenceDocument {
    extraction_index: 12,
    group_index: 11,
    text: 'SUT eki “Ayaktan Başvurularda İlave Olarak Faturalandırılabilecek İşlemler Listesi” nde (EK -2/A-2)',
    code: 'EK-2/A-2',
    purpose: 'additional_billing',
    document_type: 'SUT_annex'
});

CREATE (e:CoverageRule {
    extraction_index: 13,
    group_index: 12,
    text: 'yer alan işlemlerin bedelleri Kurumca karşılanır',
    payer: 'SGK (The Institution)',
    status: 'covered',
    subject: 'additional_procedures'
});

CREATE (e:Condition {
    extraction_index: 1,
    group_index: 0,
    text: '(2) Hastanın aynı sağlık hizmeti sunucusuna',
    subject: 'hasta',
    context: 'recurring_visit',
    provider_scope: 'same_provider'
});

CREATE (e:Exception {
    extraction_index: 2,
    group_index: 1,
    text: 'acil servise başvuruları hariç olmak üzere',
    excluded_department: 'acil servis',
    rule_context: '10_day_limit'
});

CREATE (e:TimeframeRule {
    extraction_index: 3,
    group_index: 2,
    text: 'ayaktan başvurduğu gün dâhil, 10 (on) gün içindeki aynı uzmanlık dalına diğer ayaktan başvurularında',
    duration: '10 days',
    specialty_scope: 'same_specialty',
    visit_type: 'outpatient'
});

CREATE (e:BillingPermission {
    extraction_index: 4,
    group_index: 3,
    text: 'sadece SUT eki EK -2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılabilecek',
    status: 'allowed',
    reference_list: 'EK-2/A-2',
    item_type: 'procedures'
});

CREATE (e:BillingProhibition {
    extraction_index: 5,
    group_index: 4,
    text: 'SUT eki EK-2/A Listesinde yer alan tutar faturalandırılamaz',
    status: 'prohibited',
    reference_list: 'EK-2/A',
    item_type: 'examination_fee'
});

CREATE (e:LegalAmendment {
    extraction_index: 6,
    group_index: 5,
    text: '(Değişik:RG- 09/05/2024-32541/1-b md. Yürürlük: 11/05/2024)',
    official_gazette_date: '09/05/2024',
    effective_date: '11/05/2024',
    gazette_number: '32541'
});

CREATE (e:MedicalScope {
    extraction_index: 7,
    group_index: 6,
    text: 'EK-2/A-2 ve EK -2/C Listelerinde yer alan işlemlerin yapılmasının gerekli görülmesi',
    condition: 'medical_necessity'
});

CREATE (e:ProcessCondition {
    extraction_index: 8,
    group_index: 7,
    text: 'bu muayene başvurusundan sonra aynı sağlık hizmeti sunucusunda randevu verilmek suretiyle ileri bir tarihte yapılması durumunda',
    timing: 'deferred/future_date',
    mechanism: 'appointment',
    location: 'same_provider'
});

CREATE (e:BillingRule {
    extraction_index: 9,
    group_index: 8,
    text: 'SUT eki EK-2/A Listesinde yer alan tutarlar ikinci bir defa girilmeksizin sadece yapılan işlem faturalandırılır',
    restriction: 'no_double_billing_for_exam',
    allowed_billing: 'procedure_only',
    reference_list_excluded: 'EK-2/A'
});


// ───────── BATCH 5/14 ─────────

CREATE (e:RegulationId {
    extraction_index: 1,
    group_index: 0,
    text: '(4)',
    type: 'paragraph_number',
    context: 'billing_regulations'
});

CREATE (e:MedicalEvent {
    extraction_index: 2,
    group_index: 1,
    text: 'Hastanın aynı sağlık hizmeti sunucusunda aynı uzmanlık dalına ayaktan başvurusu',
    actor: 'hasta',
    location: 'aynı sağlık hizmeti sunucusu',
    specialty: 'aynı uzmanlık dalı',
    type: 'outpatient_visit'
});

CREATE (e:TemporalContext {
    extraction_index: 3,
    group_index: 2,
    text: 'sonrasında aynı gün “yatarak tedavi” kapsamında',
    timing: 'same_day',
    treatment_type: 'inpatient',
    relation: 'follows_outpatient_visit'
});

CREATE (e:Condition {
    extraction_index: 4,
    group_index: 3,
    text: 'SUT eki EK -2/C Listesinde yer alan bir işlem yapılması halinde',
    reference_list: 'SUT EK-2/C',
    trigger_event: 'procedure_performance',
    context: 'inpatient_transition'
});

CREATE (e:BillingRule {
    extraction_index: 5,
    group_index: 4,
    text: 'bu işlem ile birlikte ayaktan yapılan işlemler bu maddenin b irinci fıkrasındaki hükümlere göre faturalandırılır',
    scope: 'combined_procedures',
    reference_regulation: 'madde 1. fıkra',
    action: 'bill_accordingly'
});

CREATE (e:ExceptionCondition {
    extraction_index: 6,
    group_index: 5,
    text: 'Ancak “yatarak tedavi” kapsamında hizmet başına ödeme yöntemi ile bir işlem yapılması durumunda',
    type: 'exception',
    payment_method: 'fee_for_service',
    context: 'inpatient_treatment'
});

CREATE (e:BillingProhibition {
    extraction_index: 7,
    group_index: 6,
    text: 'SUT eki EK -2/A Listesinde yer alan tutarlar faturalandırılmayacak',
    reference_list: 'SUT EK-2/A',
    action: 'do_not_bill',
    status: 'prohibited'
});

CREATE (e:BillingRequirement {
    extraction_index: 8,
    group_index: 7,
    text: 'ayaktan başvurular da hizmet başına ödeme yöntemine göre faturalandırılacaktır',
    scope: 'outpatient_visits',
    payment_method: 'fee_for_service',
    obligation: 'mandatory'
});

CREATE (e:Regulation {
    extraction_index: 1,
    group_index: 0,
    text: '(5)',
    type: 'clause_number',
    context: 'billing_regulations'
});

CREATE (e:Scenario {
    extraction_index: 2,
    group_index: 1,
    text: 'Hastanın aynı gün içerisinde, aynı sağlık hizmeti sunucusunda; birden fazla uzmanlık dalına başvurusu sonrasında',
    subject: 'hasta',
    timeframe: 'same_day',
    location: 'same_provider',
    event: 'multiple_specialty_applications'
});

CREATE (e:Condition {
    extraction_index: 3,
    group_index: 2,
    text: 'bu uzmanlık dallarından herhangi birinde aynı gün “yatarak tedavi” kapsamında SUT eki EK-2/C Listesinde yer alan bir işlem yapılması halind e',
    treatment_type: 'inpatient',
    reference_list: 'SUT EK-2/C',
    trigger_event: 'procedure_performance'
});

CREATE (e:BillingRule {
    extraction_index: 4,
    group_index: 3,
    text: 'bu işlem ile birlikte, o uzmanlık dalına ait ayaktan yapılan işlemler bu maddenin birinci fıkrasındaki hükümlere göre',
    scope: 'related_specialty_outpatient_procedures',
    reference_regulation: 'paragraph_1',
    billing_method: 'standard_procedure'
});

CREATE (e:BillingRule {
    extraction_index: 5,
    group_index: 4,
    text: 'diğer uzmanlık dallarındaki ayakta tedavi kapsamındaki başvuruları SUT eki EK -2/B Listesindeki “normal poliklinik muayenesi” bedeli',
    scope: 'other_specialties',
    reference_list: 'SUT EK-2/B',
    billable_item: 'normal_polyclinic_exam'
});

CREATE (e:BillingRule {
    extraction_index: 6,
    group_index: 5,
    text: 've yapılması halinde SUT eki EK -2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılacaktır',
    condition: 'if_performed',
    reference_list: 'SUT EK-2/A-2',
    action: 'bill_procedure_cost'
});

CREATE (e:ExceptionCondition {
    extraction_index: 7,
    group_index: 6,
    text: 'Ancak, yatarak tedavi kapsamında hizmet başına ödeme yöntemi ile bir işlem yapılması durumunda',
    context: 'inpatient_treatment',
    payment_method: 'fee_for_service',
    type: 'exception_trigger'
});

CREATE (e:Prohibition {
    extraction_index: 8,
    group_index: 7,
    text: 'SUT eki EK-2/A Listesinde yer alan tutarlar faturalandırılmay acak',
    reference_list: 'SUT EK-2/A',
    action: 'do_not_bill',
    status: 'prohibited'
});

CREATE (e:BillingInstruction {
    extraction_index: 9,
    group_index: 8,
    text: 'olup ayaktan yapılan işlemler hizmet başına ödeme yöntemine göre faturalandırılacaktır',
    scope: 'outpatient_procedures',
    billing_method: 'fee_for_service',
    requirement: 'mandatory'
});

CREATE (e:RegulationMarker {
    extraction_index: 1,
    group_index: 0,
    text: '(6)',
    type: 'paragraph_number',
    context: 'billing_rules'
});

CREATE (e:MedicalScenario {
    extraction_index: 2,
    group_index: 1,
    text: 'Hastanın, aynı gün içinde aynı sağlık hizmeti sunucusunda ilk muayenesini takip eden diğer uzmanlık dallarındaki ayakta tedavi kapsamında yer alan başvuruları',
    condition: 'multiple_visits_same_day',
    location: 'same_health_provider',
    specialty_context: 'different_specialties',
    treatment_type: 'outpatient'
});

CREATE (e:BillingRule {
    extraction_index: 3,
    group_index: 2,
    text: '“ayakta tedavilerde ödeme” uygulaması kapsamında değerlendirilmez',
    payment_model: 'ayakta tedavilerde ödeme',
    status: 'excluded'
});

CREATE (e:BillingProhibition {
    extraction_index: 4,
    group_index: 3,
    text: 'SUT eki EK-2/A Listesinde yer alan tutarlar faturalandırılamaz',
    reference_list: 'SUT eki EK-2/A',
    action: 'billing',
    permission: 'forbidden'
});

CREATE (e:BillingPermission {
    extraction_index: 5,
    group_index: 4,
    text: 'SUT eki EK-2/B Listesindeki “normal poliklinik muayenesi” bedeli ve yapılması halinde SUT eki EK-2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılacaktır',
    reference_list_1: 'SUT eki EK-2/B',
    item_1: 'normal poliklinik muayenesi',
    reference_list_2: 'SUT eki EK-2/A-2',
    permission: 'mandatory'
});

CREATE (e:RegulationMarker {
    extraction_index: 6,
    group_index: 5,
    text: '(7)',
    type: 'paragraph_number',
    context: 'main_branch_sub_branch_billing'
});

CREATE (e:MedicalScenario {
    extraction_index: 7,
    group_index: 6,
    text: 'Hastanın aynı gün içinde aynı sağlık hizmeti sunucusundaki ilk başvurusunun ana dal, sonraki başvurusunun yan dal olması durumunda',
    condition: 'main_branch_to_sub_branch',
    timing: 'same_day',
    location: 'same_health_provider'
});

CREATE (e:BillingRule {
    extraction_index: 8,
    group_index: 7,
    text: 'yan dala olan başvuru "ayakta tedavilerde ödeme” uygulaması kapsamında faturalandırılır',
    subject: 'yan dal başvurusu',
    payment_model: 'ayakta tedavilerde ödeme',
    status: 'included'
});


// ───────── BATCH 6/14 ─────────

CREATE (e:ContextSwitch {
    extraction_index: 9,
    group_index: 8,
    text: 'Ana dala başvuru ise',
    subject: 'ana dal başvurusu',
    role: 'contrast_case'
});

CREATE (e:BillingRestriction {
    extraction_index: 10,
    group_index: 9,
    text: 'SUT eki EK -2/A Listesinde yer alan tuta rlar girilmeksizin',
    reference_list: 'SUT eki EK -2/A',
    action: 'data_entry',
    status: 'omitted'
});

CREATE (e:BillingPermission {
    extraction_index: 11,
    group_index: 10,
    text: 'SUT eki EK -2/B Listesindeki “normal poliklinik muayenesi” bedeli ve yapılması halinde SUT eki EK-2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılabilir',
    reference_list_1: 'SUT eki EK -2/B',
    item_1: 'normal poliklinik muayenesi',
    reference_list_2: 'SUT eki EK-2/A-2',
    permission: 'allowed'
});

CREATE (e:RegulationClause {
    extraction_index: 1,
    group_index: 0,
    text: '(8)',
    number: '8',
    type: 'article_subsection'
});

CREATE (e:Requirement {
    extraction_index: 2,
    group_index: 1,
    text: 'Sağlık raporu ile yapılması gerekli görülen',
    document: 'sağlık raporu',
    necessity: 'mandatory',
    context: 'treatment_prerequisite'
});

CREATE (e:MedicalScope {
    extraction_index: 3,
    group_index: 2,
    text: 'hiperbarik oksijen tedavisi, fizik tedavi ve rehabilitasyon, ESWL ve ESWT tedavilerinde',
    category: 'specialized_treatments'
});

CREATE (e:PatientStatus {
    extraction_index: 4,
    group_index: 3,
    text: 'ayaktan başvurularda',
    type: 'outpatient',
    context: 'application_mode'
});

CREATE (e:ProcessStep {
    extraction_index: 5,
    group_index: 4,
    text: 'tedavi için sağlık raporu düzenlendikten sonra',
    action: 'report_issuance',
    timing: 'post_issuance',
    sequence: 'prerequisite_met'
});

CREATE (e:Condition {
    extraction_index: 6,
    group_index: 5,
    text: 'tedavinin sonraki günlerde aynı veya başka bir sağl ık hizmeti sunucusunda yapılması halinde',
    timing: 'subsequent_days',
    provider_flexibility: 'same_or_different_provider',
    scenario: 'continuation_of_treatment'
});

CREATE (e:Subject {
    extraction_index: 7,
    group_index: 6,
    text: 'bu sağlık raporu ile yapılan tedavi başvuruları',
    reference: 'treatment_applications',
    basis: 'health_report'
});

CREATE (e:PaymentContext {
    extraction_index: 8,
    group_index: 7,
    text: '"ayakta tedavilerde ödeme” uygulaması kapsamında',
    scheme: 'outpatient_payment',
    type: 'reimbursement_model'
});

CREATE (e:RegulationReference {
    extraction_index: 9,
    group_index: 8,
    text: 'SUT eki EK-2/A Listesinde yer',
    source: 'SUT (Sağlık Uygulama Tebliği)',
    list_code: 'EK-2/A',
    status: 'listed/included'
});

MATCH (source:PaymentRule {extraction_index: 1}),
      (doc:Document {extraction_index: 3})
CREATE (source)-[:BASED_ON {basis: 'istem belgesi (implied)'}]->(doc);

MATCH (source:DeductionRule {extraction_index: 2}),
      (target:Entity {extraction_index: 3})
CREATE (source)-[:APPLIES_TO {entity: 'sözleşmeli sağlık hizmeti sunucusu'}]->(target);

MATCH (obligation:Prohibition {extraction_index: 3}),
      (responsible:Entity {extraction_index: 3})
CREATE (responsible)-[:RESPONSIBLE_FOR]->(obligation);

MATCH (obligation:Prohibition {extraction_index: 3}),
      (responsible:Entity {extraction_index: 4})
CREATE (responsible)-[:RESPONSIBLE_FOR]->(obligation);

MATCH (obligation:Obligation {extraction_index: 6}),
      (responsible:Entity {extraction_index: 6})
CREATE (responsible)-[:RESPONSIBLE_FOR]->(obligation);

MATCH (condition:Condition {extraction_index: 10}),
      (result:Prohibition {extraction_index: 10})
CREATE (condition)-[:WHEN_THEN {trigger: 'true'}]->(result);

MATCH (source:FinancialRule {extraction_index: 11}),
      (payer:Entity {extraction_index: 6})
CREATE (payer)-[:PAYS {amount_info: 'Kurum'}]->(source);

MATCH (source:FinancialRule {extraction_index: 11}),
      (payer:Entity {extraction_index: 8})
CREATE (payer)-[:PAYS {amount_info: 'Kurum'}]->(source);

MATCH (source:FinancialRule {extraction_index: 11}),
      (payer:Institution {extraction_index: 1})
CREATE (payer)-[:PAYS {amount_info: 'Kurum'}]->(source);

MATCH (doc:ReferenceDocument {extraction_index: 14}),
      (rule:BillingRule {extraction_index: 15})
CREATE (doc)-[:REFERENCED_IN {document: 'SUT eki EK-2/B'}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 14}),
      (rule:FormattingRule {extraction_index: 12})
CREATE (doc)-[:REFERENCED_IN {document: 'SUT eki EK-2/B'}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 14}),
      (rule:PaymentRule {extraction_index: 13})
CREATE (doc)-[:REFERENCED_IN {document: 'SUT eki EK-2/B'}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 14}),
      (rule:PaymentRule {extraction_index: 12})
CREATE (doc)-[:REFERENCED_IN {document: 'SUT eki EK-2/B'}]->(rule);


// ───────── BATCH 7/14 ─────────

MATCH (doc:ReferenceDocument {extraction_index: 14}),
      (rule:CoverageRule {extraction_index: 13})
CREATE (doc)-[:REFERENCED_IN {document: 'SUT eki EK-2/B'}]->(rule);

MATCH (source:PaymentRule {extraction_index: 7}),
      (payer:Entity {extraction_index: 6})
CREATE (payer)-[:PAYS {amount_info: 'Kurum (SGK)'}]->(source);

MATCH (source:PaymentRule {extraction_index: 7}),
      (payer:Entity {extraction_index: 8})
CREATE (payer)-[:PAYS {amount_info: 'Kurum (SGK)'}]->(source);

MATCH (source:PaymentRule {extraction_index: 7}),
      (payer:Institution {extraction_index: 1})
CREATE (payer)-[:PAYS {amount_info: 'Kurum (SGK)'}]->(source);

MATCH (source:Scope {extraction_index: 6}),
      (payer:Entity {extraction_index: 6})
CREATE (payer)-[:PAYS {amount_info: 'Kurum (SGK)'}]->(source);

MATCH (source:Scope {extraction_index: 6}),
      (payer:Entity {extraction_index: 8})
CREATE (payer)-[:PAYS {amount_info: 'Kurum (SGK)'}]->(source);

MATCH (source:Scope {extraction_index: 6}),
      (payer:Institution {extraction_index: 1})
CREATE (payer)-[:PAYS {amount_info: 'Kurum (SGK)'}]->(source);

MATCH (source:BillingRule {extraction_index: 3}),
      (payer:Entity {extraction_index: 6})
CREATE (payer)-[:PAYS {amount_info: 'Kurum (SGK)'}]->(source);

MATCH (source:BillingRule {extraction_index: 3}),
      (payer:Entity {extraction_index: 8})
CREATE (payer)-[:PAYS {amount_info: 'Kurum (SGK)'}]->(source);

MATCH (source:BillingRule {extraction_index: 3}),
      (payer:Institution {extraction_index: 1})
CREATE (payer)-[:PAYS {amount_info: 'Kurum (SGK)'}]->(source);

MATCH (doc:ReferenceDocument {extraction_index: 5}),
      (rule:PaymentRule {extraction_index: 7})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 5}),
      (rule:BillingRule {extraction_index: 4})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 5}),
      (rule:BillingRule {extraction_index: 3})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 5}),
      (rule:PaymentRule {extraction_index: 7})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 5}),
      (rule:BillingRule {extraction_index: 6})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 5}),
      (rule:PaymentRule {extraction_index: 5})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 5}),
      (rule:TimeframeRule {extraction_index: 3})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 5}),
      (rule:BillingRule {extraction_index: 5})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 5}),
      (rule:BillingRule {extraction_index: 4})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 5}),
      (rule:BillingRule {extraction_index: 5})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 5}),
      (rule:BillingRule {extraction_index: 6})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 5}),
      (rule:BillingRule {extraction_index: 3})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (source:PaymentRule {extraction_index: 7}),
      (payer:Entity {extraction_index: 6})
CREATE (payer)-[:PAYS {amount_info: 'Kurum'}]->(source);

MATCH (source:PaymentRule {extraction_index: 7}),
      (payer:Entity {extraction_index: 8})
CREATE (payer)-[:PAYS {amount_info: 'Kurum'}]->(source);

MATCH (source:PaymentRule {extraction_index: 7}),
      (payer:Institution {extraction_index: 1})
CREATE (payer)-[:PAYS {amount_info: 'Kurum'}]->(source);


// ───────── BATCH 8/14 ─────────

MATCH (source:PaymentRule {extraction_index: 9}),
      (payer:Entity {extraction_index: 6})
CREATE (payer)-[:PAYS {amount_info: 'Kurum'}]->(source);

MATCH (source:PaymentRule {extraction_index: 9}),
      (payer:Entity {extraction_index: 8})
CREATE (payer)-[:PAYS {amount_info: 'Kurum'}]->(source);

MATCH (source:PaymentRule {extraction_index: 9}),
      (payer:Institution {extraction_index: 1})
CREATE (payer)-[:PAYS {amount_info: 'Kurum'}]->(source);

MATCH (source:PaymentRule {extraction_index: 13}),
      (payer:Entity {extraction_index: 6})
CREATE (payer)-[:PAYS {amount_info: 'Kurum'}]->(source);

MATCH (source:PaymentRule {extraction_index: 13}),
      (payer:Entity {extraction_index: 8})
CREATE (payer)-[:PAYS {amount_info: 'Kurum'}]->(source);

MATCH (source:PaymentRule {extraction_index: 13}),
      (payer:Institution {extraction_index: 1})
CREATE (payer)-[:PAYS {amount_info: 'Kurum'}]->(source);

MATCH (source:PaymentRule {extraction_index: 13}),
      (doc:ReferenceDocument {extraction_index: 14})
CREATE (source)-[:BASED_ON {basis: 'SUT_and_appendices'}]->(doc);

MATCH (source:PaymentRule {extraction_index: 13}),
      (doc:ReferenceDocument {extraction_index: 12})
CREATE (source)-[:BASED_ON {basis: 'SUT_and_appendices'}]->(doc);

MATCH (doc:ReferenceDocument {extraction_index: 4}),
      (rule:DeductionRule {extraction_index: 2})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 4}),
      (rule:BillingRule {extraction_index: 4})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 4}),
      (rule:BillingRule {extraction_index: 3})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 4}),
      (rule:BillingRule {extraction_index: 6})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 4}),
      (rule:PaymentRule {extraction_index: 5})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 4}),
      (rule:TimeframeRule {extraction_index: 3})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 4}),
      (rule:BillingRule {extraction_index: 5})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 4}),
      (rule:BillingRule {extraction_index: 4})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 4}),
      (rule:BillingRule {extraction_index: 5})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 4}),
      (rule:BillingRule {extraction_index: 6})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 4}),
      (rule:BillingRule {extraction_index: 3})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (source:PaymentRule {extraction_index: 5}),
      (doc:Document {extraction_index: 3})
CREATE (source)-[:BASED_ON {basis: 'EK-2/A List'}]->(doc);

MATCH (source:PaymentRule {extraction_index: 5}),
      (doc:ReferenceDocument {extraction_index: 5})
CREATE (source)-[:BASED_ON {basis: 'EK-2/A List'}]->(doc);

MATCH (source:PaymentRule {extraction_index: 5}),
      (doc:ReferenceDocument {extraction_index: 4})
CREATE (source)-[:BASED_ON {basis: 'EK-2/A List'}]->(doc);

MATCH (condition:Condition {extraction_index: 8}),
      (result:Prohibition {extraction_index: 8})
CREATE (condition)-[:WHEN_THEN {trigger: 'None'}]->(result);

MATCH (source:PaymentCalculation {extraction_index: 11}),
      (doc:ReferenceDocument {extraction_index: 12})
CREATE (source)-[:BASED_ON {basis: 'EK-2/A List'}]->(doc);

MATCH (doc:ReferenceDocument {extraction_index: 12}),
      (rule:FinancialRule {extraction_index: 11})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);


// ───────── BATCH 9/14 ─────────

MATCH (doc:ReferenceDocument {extraction_index: 12}),
      (rule:BillingRule {extraction_index: 10})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 12}),
      (rule:FormattingRule {extraction_index: 12})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 12}),
      (rule:PaymentRule {extraction_index: 13})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 12}),
      (rule:PaymentRule {extraction_index: 11})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 12}),
      (rule:PaymentRule {extraction_index: 12})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (doc:ReferenceDocument {extraction_index: 12}),
      (rule:CoverageRule {extraction_index: 13})
CREATE (doc)-[:REFERENCED_IN {document: ''}]->(rule);

MATCH (source:CoverageRule {extraction_index: 13}),
      (payer:Entity {extraction_index: 6})
CREATE (payer)-[:PAYS {amount_info: 'SGK (The Institution)'}]->(source);

MATCH (source:CoverageRule {extraction_index: 13}),
      (payer:Entity {extraction_index: 8})
CREATE (payer)-[:PAYS {amount_info: 'SGK (The Institution)'}]->(source);

MATCH (source:CoverageRule {extraction_index: 13}),
      (payer:Institution {extraction_index: 1})
CREATE (payer)-[:PAYS {amount_info: 'SGK (The Institution)'}]->(source);

MATCH (condition:Condition {extraction_index: 4}),
      (result:Prohibition {extraction_index: 4})
CREATE (condition)-[:WHEN_THEN {trigger: 'None'}]->(result);

MATCH (condition:Condition {extraction_index: 3}),
      (result:Prohibition {extraction_index: 3})
CREATE (condition)-[:WHEN_THEN {trigger: 'None'}]->(result);

MATCH (condition:Condition {extraction_index: 6}),
      (result:Obligation {extraction_index: 6})
CREATE (condition)-[:WHEN_THEN {trigger: 'None'}]->(result);

MATCH (source:Subject {extraction_index: 7}),
      (doc:ReferenceDocument {extraction_index: 5})
CREATE (source)-[:BASED_ON {basis: 'health_report'}]->(doc);

MATCH (e1:PaymentRule {extraction_index: 1}),
      (e2:Regulation {extraction_index: 1})
CREATE (e1)-[:FOLLOWED_BY {group: 0}]->(e2);

MATCH (e1:Regulation {extraction_index: 1}),
      (e2:Institution {extraction_index: 1})
CREATE (e1)-[:FOLLOWED_BY {group: 0}]->(e2);

MATCH (e1:Institution {extraction_index: 1}),
      (e2:Procedure {extraction_index: 1})
CREATE (e1)-[:FOLLOWED_BY {group: 0}]->(e2);

MATCH (e1:Procedure {extraction_index: 1}),
      (e2:Regulation {extraction_index: 1})
CREATE (e1)-[:FOLLOWED_BY {group: 0}]->(e2);

MATCH (e1:Regulation {extraction_index: 1}),
      (e2:RegulationClause {extraction_index: 1})
CREATE (e1)-[:FOLLOWED_BY {group: 0}]->(e2);

MATCH (e1:RegulationClause {extraction_index: 1}),
      (e2:RegulationHeader {extraction_index: 1})
CREATE (e1)-[:FOLLOWED_BY {group: 0}]->(e2);

MATCH (e1:RegulationHeader {extraction_index: 1}),
      (e2:Condition {extraction_index: 1})
CREATE (e1)-[:FOLLOWED_BY {group: 0}]->(e2);

MATCH (e1:Condition {extraction_index: 1}),
      (e2:RegulationId {extraction_index: 1})
CREATE (e1)-[:FOLLOWED_BY {group: 0}]->(e2);

MATCH (e1:RegulationId {extraction_index: 1}),
      (e2:Regulation {extraction_index: 1})
CREATE (e1)-[:FOLLOWED_BY {group: 0}]->(e2);

MATCH (e1:Regulation {extraction_index: 1}),
      (e2:RegulationMarker {extraction_index: 1})
CREATE (e1)-[:FOLLOWED_BY {group: 0}]->(e2);

MATCH (e1:RegulationMarker {extraction_index: 1}),
      (e2:RegulationClause {extraction_index: 1})
CREATE (e1)-[:FOLLOWED_BY {group: 0}]->(e2);

MATCH (e1:DeductionRule {extraction_index: 2}),
      (e2:Condition {extraction_index: 2})
CREATE (e1)-[:FOLLOWED_BY {group: 1}]->(e2);


// ───────── BATCH 10/14 ─────────

MATCH (e1:Condition {extraction_index: 2}),
      (e2:Procedure {extraction_index: 2})
CREATE (e1)-[:FOLLOWED_BY {group: 1}]->(e2);

MATCH (e1:Procedure {extraction_index: 2}),
      (e2:MedicalReason {extraction_index: 2})
CREATE (e1)-[:FOLLOWED_BY {group: 1}]->(e2);

MATCH (e1:MedicalReason {extraction_index: 2}),
      (e2:MedicalScope {extraction_index: 2})
CREATE (e1)-[:FOLLOWED_BY {group: 1}]->(e2);

MATCH (e1:MedicalScope {extraction_index: 2}),
      (e2:Requirement {extraction_index: 2})
CREATE (e1)-[:FOLLOWED_BY {group: 1}]->(e2);

MATCH (e1:Requirement {extraction_index: 2}),
      (e2:Scope {extraction_index: 2})
CREATE (e1)-[:FOLLOWED_BY {group: 1}]->(e2);

MATCH (e1:Scope {extraction_index: 2}),
      (e2:Exception {extraction_index: 2})
CREATE (e1)-[:FOLLOWED_BY {group: 1}]->(e2);

MATCH (e1:Exception {extraction_index: 2}),
      (e2:MedicalEvent {extraction_index: 2})
CREATE (e1)-[:FOLLOWED_BY {group: 1}]->(e2);

MATCH (e1:MedicalEvent {extraction_index: 2}),
      (e2:Scenario {extraction_index: 2})
CREATE (e1)-[:FOLLOWED_BY {group: 1}]->(e2);

MATCH (e1:Scenario {extraction_index: 2}),
      (e2:MedicalScenario {extraction_index: 2})
CREATE (e1)-[:FOLLOWED_BY {group: 1}]->(e2);

MATCH (e1:MedicalScenario {extraction_index: 2}),
      (e2:Requirement {extraction_index: 2})
CREATE (e1)-[:FOLLOWED_BY {group: 1}]->(e2);

MATCH (e1:Entity {extraction_index: 3}),
      (e2:Prohibition {extraction_index: 3})
CREATE (e1)-[:FOLLOWED_BY {group: 2}]->(e2);

MATCH (e1:Prohibition {extraction_index: 3}),
      (e2:MedicalContext {extraction_index: 3})
CREATE (e1)-[:FOLLOWED_BY {group: 2}]->(e2);

MATCH (e1:MedicalContext {extraction_index: 3}),
      (e2:Document {extraction_index: 3})
CREATE (e1)-[:FOLLOWED_BY {group: 2}]->(e2);

MATCH (e1:Document {extraction_index: 3}),
      (e2:BillingRule {extraction_index: 3})
CREATE (e1)-[:FOLLOWED_BY {group: 2}]->(e2);

MATCH (e1:BillingRule {extraction_index: 3}),
      (e2:RegulationClause {extraction_index: 3})
CREATE (e1)-[:FOLLOWED_BY {group: 2}]->(e2);

MATCH (e1:RegulationClause {extraction_index: 3}),
      (e2:BillingUnit {extraction_index: 3})
CREATE (e1)-[:FOLLOWED_BY {group: 2}]->(e2);

MATCH (e1:BillingUnit {extraction_index: 3}),
      (e2:TimeframeRule {extraction_index: 3})
CREATE (e1)-[:FOLLOWED_BY {group: 2}]->(e2);

MATCH (e1:TimeframeRule {extraction_index: 3}),
      (e2:TemporalContext {extraction_index: 3})
CREATE (e1)-[:FOLLOWED_BY {group: 2}]->(e2);

MATCH (e1:TemporalContext {extraction_index: 3}),
      (e2:Condition {extraction_index: 3})
CREATE (e1)-[:FOLLOWED_BY {group: 2}]->(e2);

MATCH (e1:Condition {extraction_index: 3}),
      (e2:BillingRule {extraction_index: 3})
CREATE (e1)-[:FOLLOWED_BY {group: 2}]->(e2);

MATCH (e1:BillingRule {extraction_index: 3}),
      (e2:MedicalScope {extraction_index: 3})
CREATE (e1)-[:FOLLOWED_BY {group: 2}]->(e2);

MATCH (e1:FinancialMechanism {extraction_index: 4}),
      (e2:Prohibition {extraction_index: 4})
CREATE (e1)-[:FOLLOWED_BY {group: 3}]->(e2);

MATCH (e1:Prohibition {extraction_index: 4}),
      (e2:Entity {extraction_index: 4})
CREATE (e1)-[:FOLLOWED_BY {group: 3}]->(e2);

MATCH (e1:Entity {extraction_index: 4}),
      (e2:BillingRule {extraction_index: 4})
CREATE (e1)-[:FOLLOWED_BY {group: 3}]->(e2);

MATCH (e1:BillingRule {extraction_index: 4}),
      (e2:Regulation {extraction_index: 4})
CREATE (e1)-[:FOLLOWED_BY {group: 3}]->(e2);


// ───────── BATCH 11/14 ─────────

MATCH (e1:Regulation {extraction_index: 4}),
      (e2:ReferenceList {extraction_index: 4})
CREATE (e1)-[:FOLLOWED_BY {group: 3}]->(e2);

MATCH (e1:ReferenceList {extraction_index: 4}),
      (e2:ReferenceDocument {extraction_index: 4})
CREATE (e1)-[:FOLLOWED_BY {group: 3}]->(e2);

MATCH (e1:ReferenceDocument {extraction_index: 4}),
      (e2:BillingPermission {extraction_index: 4})
CREATE (e1)-[:FOLLOWED_BY {group: 3}]->(e2);

MATCH (e1:BillingPermission {extraction_index: 4}),
      (e2:Condition {extraction_index: 4})
CREATE (e1)-[:FOLLOWED_BY {group: 3}]->(e2);

MATCH (e1:Condition {extraction_index: 4}),
      (e2:BillingRule {extraction_index: 4})
CREATE (e1)-[:FOLLOWED_BY {group: 3}]->(e2);

MATCH (e1:BillingRule {extraction_index: 4}),
      (e2:BillingProhibition {extraction_index: 4})
CREATE (e1)-[:FOLLOWED_BY {group: 3}]->(e2);

MATCH (e1:BillingProhibition {extraction_index: 4}),
      (e2:PatientStatus {extraction_index: 4})
CREATE (e1)-[:FOLLOWED_BY {group: 3}]->(e2);

MATCH (e1:RegulationId {extraction_index: 5}),
      (e2:Condition {extraction_index: 5})
CREATE (e1)-[:FOLLOWED_BY {group: 4}]->(e2);

MATCH (e1:Condition {extraction_index: 5}),
      (e2:ScopeDefinition {extraction_index: 5})
CREATE (e1)-[:FOLLOWED_BY {group: 4}]->(e2);

MATCH (e1:ScopeDefinition {extraction_index: 5}),
      (e2:RegulationId {extraction_index: 5})
CREATE (e1)-[:FOLLOWED_BY {group: 4}]->(e2);

MATCH (e1:RegulationId {extraction_index: 5}),
      (e2:ReferenceDocument {extraction_index: 5})
CREATE (e1)-[:FOLLOWED_BY {group: 4}]->(e2);

MATCH (e1:ReferenceDocument {extraction_index: 5}),
      (e2:ProviderDefinition {extraction_index: 5})
CREATE (e1)-[:FOLLOWED_BY {group: 4}]->(e2);

MATCH (e1:ProviderDefinition {extraction_index: 5}),
      (e2:PaymentRule {extraction_index: 5})
CREATE (e1)-[:FOLLOWED_BY {group: 4}]->(e2);

MATCH (e1:PaymentRule {extraction_index: 5}),
      (e2:BillingProhibition {extraction_index: 5})
CREATE (e1)-[:FOLLOWED_BY {group: 4}]->(e2);

MATCH (e1:BillingProhibition {extraction_index: 5}),
      (e2:BillingRule {extraction_index: 5})
CREATE (e1)-[:FOLLOWED_BY {group: 4}]->(e2);

MATCH (e1:BillingRule {extraction_index: 5}),
      (e2:BillingRule {extraction_index: 5})
CREATE (e1)-[:FOLLOWED_BY {group: 4}]->(e2);

MATCH (e1:BillingRule {extraction_index: 5}),
      (e2:BillingPermission {extraction_index: 5})
CREATE (e1)-[:FOLLOWED_BY {group: 4}]->(e2);

MATCH (e1:BillingPermission {extraction_index: 5}),
      (e2:ProcessStep {extraction_index: 5})
CREATE (e1)-[:FOLLOWED_BY {group: 4}]->(e2);

MATCH (e1:Entity {extraction_index: 6}),
      (e2:Obligation {extraction_index: 6})
CREATE (e1)-[:FOLLOWED_BY {group: 5}]->(e2);

MATCH (e1:Obligation {extraction_index: 6}),
      (e2:ExcludedServices {extraction_index: 6})
CREATE (e1)-[:FOLLOWED_BY {group: 5}]->(e2);

MATCH (e1:ExcludedServices {extraction_index: 6}),
      (e2:Scope {extraction_index: 6})
CREATE (e1)-[:FOLLOWED_BY {group: 5}]->(e2);

MATCH (e1:Scope {extraction_index: 6}),
      (e2:MedicalMethod {extraction_index: 6})
CREATE (e1)-[:FOLLOWED_BY {group: 5}]->(e2);

MATCH (e1:MedicalMethod {extraction_index: 6}),
      (e2:BillingRule {extraction_index: 6})
CREATE (e1)-[:FOLLOWED_BY {group: 5}]->(e2);

MATCH (e1:BillingRule {extraction_index: 6}),
      (e2:LegalAmendment {extraction_index: 6})
CREATE (e1)-[:FOLLOWED_BY {group: 5}]->(e2);

MATCH (e1:LegalAmendment {extraction_index: 6}),
      (e2:LegalAmendment {extraction_index: 6})
CREATE (e1)-[:FOLLOWED_BY {group: 5}]->(e2);


// ───────── BATCH 12/14 ─────────

MATCH (e1:LegalAmendment {extraction_index: 6}),
      (e2:ExceptionCondition {extraction_index: 6})
CREATE (e1)-[:FOLLOWED_BY {group: 5}]->(e2);

MATCH (e1:ExceptionCondition {extraction_index: 6}),
      (e2:BillingRule {extraction_index: 6})
CREATE (e1)-[:FOLLOWED_BY {group: 5}]->(e2);

MATCH (e1:BillingRule {extraction_index: 6}),
      (e2:RegulationMarker {extraction_index: 6})
CREATE (e1)-[:FOLLOWED_BY {group: 5}]->(e2);

MATCH (e1:RegulationMarker {extraction_index: 6}),
      (e2:Condition {extraction_index: 6})
CREATE (e1)-[:FOLLOWED_BY {group: 5}]->(e2);

MATCH (e1:Process {extraction_index: 7}),
      (e2:Regulation {extraction_index: 7})
CREATE (e1)-[:FOLLOWED_BY {group: 6}]->(e2);

MATCH (e1:Regulation {extraction_index: 7}),
      (e2:PaymentRule {extraction_index: 7})
CREATE (e1)-[:FOLLOWED_BY {group: 6}]->(e2);

MATCH (e1:PaymentRule {extraction_index: 7}),
      (e2:Authority {extraction_index: 7})
CREATE (e1)-[:FOLLOWED_BY {group: 6}]->(e2);

MATCH (e1:Authority {extraction_index: 7}),
      (e2:PaymentRule {extraction_index: 7})
CREATE (e1)-[:FOLLOWED_BY {group: 6}]->(e2);

MATCH (e1:PaymentRule {extraction_index: 7}),
      (e2:LegalExclusion {extraction_index: 7})
CREATE (e1)-[:FOLLOWED_BY {group: 6}]->(e2);

MATCH (e1:LegalExclusion {extraction_index: 7}),
      (e2:AdministrativeProcess {extraction_index: 7})
CREATE (e1)-[:FOLLOWED_BY {group: 6}]->(e2);

MATCH (e1:AdministrativeProcess {extraction_index: 7}),
      (e2:MedicalScope {extraction_index: 7})
CREATE (e1)-[:FOLLOWED_BY {group: 6}]->(e2);

MATCH (e1:MedicalScope {extraction_index: 7}),
      (e2:BillingProhibition {extraction_index: 7})
CREATE (e1)-[:FOLLOWED_BY {group: 6}]->(e2);

MATCH (e1:BillingProhibition {extraction_index: 7}),
      (e2:ExceptionCondition {extraction_index: 7})
CREATE (e1)-[:FOLLOWED_BY {group: 6}]->(e2);

MATCH (e1:ExceptionCondition {extraction_index: 7}),
      (e2:MedicalScenario {extraction_index: 7})
CREATE (e1)-[:FOLLOWED_BY {group: 6}]->(e2);

MATCH (e1:MedicalScenario {extraction_index: 7}),
      (e2:Subject {extraction_index: 7})
CREATE (e1)-[:FOLLOWED_BY {group: 6}]->(e2);

MATCH (e1:ScopeLimitation {extraction_index: 8}),
      (e2:Entity {extraction_index: 8})
CREATE (e1)-[:FOLLOWED_BY {group: 7}]->(e2);

MATCH (e1:Entity {extraction_index: 8}),
      (e2:RegulationId {extraction_index: 8})
CREATE (e1)-[:FOLLOWED_BY {group: 7}]->(e2);

MATCH (e1:RegulationId {extraction_index: 8}),
      (e2:Reference {extraction_index: 8})
CREATE (e1)-[:FOLLOWED_BY {group: 7}]->(e2);

MATCH (e1:Reference {extraction_index: 8}),
      (e2:MedicalProcedure {extraction_index: 8})
CREATE (e1)-[:FOLLOWED_BY {group: 7}]->(e2);

MATCH (e1:MedicalProcedure {extraction_index: 8}),
      (e2:RegulationHeader {extraction_index: 8})
CREATE (e1)-[:FOLLOWED_BY {group: 7}]->(e2);

MATCH (e1:RegulationHeader {extraction_index: 8}),
      (e2:Condition {extraction_index: 8})
CREATE (e1)-[:FOLLOWED_BY {group: 7}]->(e2);

MATCH (e1:Condition {extraction_index: 8}),
      (e2:ProcessCondition {extraction_index: 8})
CREATE (e1)-[:FOLLOWED_BY {group: 7}]->(e2);

MATCH (e1:ProcessCondition {extraction_index: 8}),
      (e2:BillingRequirement {extraction_index: 8})
CREATE (e1)-[:FOLLOWED_BY {group: 7}]->(e2);

MATCH (e1:BillingRequirement {extraction_index: 8}),
      (e2:Prohibition {extraction_index: 8})
CREATE (e1)-[:FOLLOWED_BY {group: 7}]->(e2);

MATCH (e1:Prohibition {extraction_index: 8}),
      (e2:BillingRule {extraction_index: 8})
CREATE (e1)-[:FOLLOWED_BY {group: 7}]->(e2);


// ───────── BATCH 13/14 ─────────

MATCH (e1:BillingRule {extraction_index: 8}),
      (e2:PaymentContext {extraction_index: 8})
CREATE (e1)-[:FOLLOWED_BY {group: 7}]->(e2);

MATCH (e1:MedicalProcedures {extraction_index: 9}),
      (e2:Obligation {extraction_index: 9})
CREATE (e1)-[:FOLLOWED_BY {group: 8}]->(e2);

MATCH (e1:Obligation {extraction_index: 9}),
      (e2:RegulatoryRequirement {extraction_index: 9})
CREATE (e1)-[:FOLLOWED_BY {group: 8}]->(e2);

MATCH (e1:RegulatoryRequirement {extraction_index: 9}),
      (e2:ListScope {extraction_index: 9})
CREATE (e1)-[:FOLLOWED_BY {group: 8}]->(e2);

MATCH (e1:ListScope {extraction_index: 9}),
      (e2:PaymentRule {extraction_index: 9})
CREATE (e1)-[:FOLLOWED_BY {group: 8}]->(e2);

MATCH (e1:PaymentRule {extraction_index: 9}),
      (e2:RegulationHeader {extraction_index: 9})
CREATE (e1)-[:FOLLOWED_BY {group: 8}]->(e2);

MATCH (e1:RegulationHeader {extraction_index: 9}),
      (e2:InstitutionType {extraction_index: 9})
CREATE (e1)-[:FOLLOWED_BY {group: 8}]->(e2);

MATCH (e1:InstitutionType {extraction_index: 9}),
      (e2:BillingRule {extraction_index: 9})
CREATE (e1)-[:FOLLOWED_BY {group: 8}]->(e2);

MATCH (e1:BillingRule {extraction_index: 9}),
      (e2:BillingInstruction {extraction_index: 9})
CREATE (e1)-[:FOLLOWED_BY {group: 8}]->(e2);

MATCH (e1:BillingInstruction {extraction_index: 9}),
      (e2:ContextSwitch {extraction_index: 9})
CREATE (e1)-[:FOLLOWED_BY {group: 8}]->(e2);

MATCH (e1:ContextSwitch {extraction_index: 9}),
      (e2:RegulationReference {extraction_index: 9})
CREATE (e1)-[:FOLLOWED_BY {group: 8}]->(e2);

MATCH (e1:Prohibition {extraction_index: 10}),
      (e2:Condition {extraction_index: 10})
CREATE (e1)-[:FOLLOWED_BY {group: 9}]->(e2);

MATCH (e1:Condition {extraction_index: 10}),
      (e2:BillingRule {extraction_index: 10})
CREATE (e1)-[:FOLLOWED_BY {group: 9}]->(e2);

MATCH (e1:BillingRule {extraction_index: 10}),
      (e2:Parameter {extraction_index: 10})
CREATE (e1)-[:FOLLOWED_BY {group: 9}]->(e2);

MATCH (e1:Parameter {extraction_index: 10}),
      (e2:Regulation {extraction_index: 10})
CREATE (e1)-[:FOLLOWED_BY {group: 9}]->(e2);

MATCH (e1:Regulation {extraction_index: 10}),
      (e2:RegulationClause {extraction_index: 10})
CREATE (e1)-[:FOLLOWED_BY {group: 9}]->(e2);

MATCH (e1:RegulationClause {extraction_index: 10}),
      (e2:ServiceDetail {extraction_index: 10})
CREATE (e1)-[:FOLLOWED_BY {group: 9}]->(e2);

MATCH (e1:ServiceDetail {extraction_index: 10}),
      (e2:BillingRestriction {extraction_index: 10})
CREATE (e1)-[:FOLLOWED_BY {group: 9}]->(e2);

MATCH (e1:Condition {extraction_index: 11}),
      (e2:FinancialRule {extraction_index: 11})
CREATE (e1)-[:FOLLOWED_BY {group: 10}]->(e2);

MATCH (e1:FinancialRule {extraction_index: 11}),
      (e2:CalculationMethod {extraction_index: 11})
CREATE (e1)-[:FOLLOWED_BY {group: 10}]->(e2);

MATCH (e1:CalculationMethod {extraction_index: 11}),
      (e2:Scenario {extraction_index: 11})
CREATE (e1)-[:FOLLOWED_BY {group: 10}]->(e2);

MATCH (e1:Scenario {extraction_index: 11}),
      (e2:PaymentRule {extraction_index: 11})
CREATE (e1)-[:FOLLOWED_BY {group: 10}]->(e2);

MATCH (e1:PaymentRule {extraction_index: 11}),
      (e2:PaymentCalculation {extraction_index: 11})
CREATE (e1)-[:FOLLOWED_BY {group: 10}]->(e2);

MATCH (e1:PaymentCalculation {extraction_index: 11}),
      (e2:BillingPermission {extraction_index: 11})
CREATE (e1)-[:FOLLOWED_BY {group: 10}]->(e2);

MATCH (e1:Exception {extraction_index: 12}),
      (e2:Regulation {extraction_index: 12})
CREATE (e1)-[:FOLLOWED_BY {group: 11}]->(e2);


// ───────── BATCH 14/14 ─────────

MATCH (e1:Regulation {extraction_index: 12}),
      (e2:FormattingRule {extraction_index: 12})
CREATE (e1)-[:FOLLOWED_BY {group: 11}]->(e2);

MATCH (e1:FormattingRule {extraction_index: 12}),
      (e2:CoverageScope {extraction_index: 12})
CREATE (e1)-[:FOLLOWED_BY {group: 11}]->(e2);

MATCH (e1:CoverageScope {extraction_index: 12}),
      (e2:PaymentRule {extraction_index: 12})
CREATE (e1)-[:FOLLOWED_BY {group: 11}]->(e2);

MATCH (e1:PaymentRule {extraction_index: 12}),
      (e2:ReferenceDocument {extraction_index: 12})
CREATE (e1)-[:FOLLOWED_BY {group: 11}]->(e2);

MATCH (e1:FinancialTerm {extraction_index: 13}),
      (e2:PaymentRule {extraction_index: 13})
CREATE (e1)-[:FOLLOWED_BY {group: 12}]->(e2);

MATCH (e1:PaymentRule {extraction_index: 13}),
      (e2:RegulationHeader {extraction_index: 13})
CREATE (e1)-[:FOLLOWED_BY {group: 12}]->(e2);

MATCH (e1:RegulationHeader {extraction_index: 13}),
      (e2:CoverageRule {extraction_index: 13})
CREATE (e1)-[:FOLLOWED_BY {group: 12}]->(e2);

MATCH (e1:ReferenceDocument {extraction_index: 14}),
      (e2:TimeLimitation {extraction_index: 14})
CREATE (e1)-[:FOLLOWED_BY {group: 13}]->(e2);

MATCH (e1:TimeLimitation {extraction_index: 14}),
      (e2:LegalAmendment {extraction_index: 14})
CREATE (e1)-[:FOLLOWED_BY {group: 13}]->(e2);

MATCH (e1:BillingRule {extraction_index: 15}),
      (e2:EffectiveDate {extraction_index: 15})
CREATE (e1)-[:FOLLOWED_BY {group: 14}]->(e2);

