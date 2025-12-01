// ============================================================================
// AUTO-GENERATED HEALTHCARE REGULATIONS KNOWLEDGE GRAPH
// Generated from JSONL extraction data
// ============================================================================


// ============================================================================
// CONSTRAINTS
// ============================================================================

CREATE CONSTRAINT IF NOT EXISTS FOR (p:PaymentMethod) REQUIRE p.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (c:CareSetting) REQUIRE c.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (s:Section) REQUIRE s.identifier IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (i:Institution) REQUIRE i.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (m:MedicalService) REQUIRE m.type IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (p:MedicalProcedure) REQUIRE p.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (l:RegulationList) REQUIRE l.code IS UNIQUE;


// ============================================================================
// PAYMENT METHOD NODES (Central Hub Nodes)
// ============================================================================

MERGE (pm:PaymentMethod {name: 'adjusted_fee_for_service_based_on_points', type: 'other'});
MERGE (pm:PaymentMethod {name: 'hizmet başına ödeme', type: 'fee_for_service'});
MERGE (pm:PaymentMethod {name: 'hizmet başına ödeme yöntemi', type: 'fee_for_service'});
MERGE (pm:PaymentMethod {name: 'tanıya dayalı işlem üzerinden ödeme', type: 'diagnosis_based'});


// ============================================================================
// CARE SETTING NODES
// ============================================================================

MERGE (cs:CareSetting {name: 'Birinci basamak sağlık kuruluşlarındaki ayakta tedaviler', type: 'outpatient'});
MERGE (cs:CareSetting {name: 'acil servis/polikliniği', type: 'emergency'});
MERGE (cs:CareSetting {name: 'ayakta tedavi', type: 'outpatient'});
MERGE (cs:CareSetting {name: 'ayaktan', type: 'outpatient'});
MERGE (cs:CareSetting {name: 'ikinci ve üçüncü basamak sağlık hizmeti sunucuları', type: 'other'});
MERGE (cs:CareSetting {name: 'inpatient', type: 'other'});
MERGE (cs:CareSetting {name: 'inpatient (yatarak tedavi)', type: 'other'});
MERGE (cs:CareSetting {name: 'outpatient', type: 'other'});
MERGE (cs:CareSetting {name: 'polyclinic', type: 'other'});
MERGE (cs:CareSetting {name: 'sağlık hizmeti sunucusunda ayaktan', type: 'outpatient'});
MERGE (cs:CareSetting {name: 'yatarak tedavi', type: 'other'});


// ============================================================================
// SECTION/TOPIC NODES
// ============================================================================

MERGE (sec:Section {identifier: 'laboratuvar ve görüntüleme hizmet alımı', topic: 'laboratuvar ve görüntüleme hizmet alımı'});
MERGE (sec:Section {identifier: 'belge ibrazı ve ödeme koşulu', topic: 'belge ibrazı ve ödeme koşulu'});
MERGE (sec:Section {identifier: 'sağlık raporu bedellerinin faturalandırılması', topic: 'sağlık raporu bedellerinin faturalandırılması'});
MERGE (sec:Section {identifier: 'Ayakta tedavilerde ödeme', topic: 'Ayakta tedavilerde ödeme'});
MERGE (sec:Section {identifier: 'Birinci basamak sağlık kuruluşları', topic: 'Birinci basamak sağlık kuruluşları'});
MERGE (sec:Section {identifier: 'İkinci ve üçüncü basamak sağlık kurumları', topic: 'İkinci ve üçüncü basamak sağlık kurumları'});
MERGE (sec:Section {identifier: 'ayakta_tedavilerde_odeme', topic: 'ayakta_tedavilerde_odeme'});
MERGE (sec:Section {identifier: 'aynı gün başvuru ve faturalandırma kuralları', topic: 'aynı gün başvuru ve faturalandırma kuralları'});
MERGE (sec:Section {identifier: '2.2.1.B-2', topic: 'Hizmet başına ödeme yöntemi ile faturalandırılacak ayakta tedaviler', payment_model: 'hizmet başına ödeme', care_setting: 'ayakta tedavi'});


// ============================================================================
// INSTITUTION NODES
// ============================================================================

MERGE (inst:Institution {name: 'Sağlık Bakanlığına bağlı sağlık hizmeti sunucuları', type: 'public_healthcare_provider', supervising_authority: 'Sağlık Bakanlığı', funding_model: 'global_bütçe'});
MERGE (inst:Institution {name: 'Kurumla sözleşmeli sağlık hizmeti sunucuları', type: 'contracted_healthcare_provider', role: 'service_provider'});
MERGE (inst:Institution {name: 'özel sağlık hizmeti  sunucusu', type: 'private_healthcare_provider', role: 'institutional_framework_for_hekim_ve_diș_hekimleri'});
MERGE (inst:Institution {name: 'Kurum ile sözleşmeli sağlık hizmeti sunucuları', type: 'contracted_healthcare_providers', role: 'service_provider'});
MERGE (inst:Institution {name: 'sağlık hizmeti sunucusuna', type: 'healthcare_provider', role: 'hizmeti_sunan_kurum'});
MERGE (inst:Institution {name: 'Kurum birimlerince', type: 'kurum_birimleri', role: 'referral_authority'});
MERGE (inst:Institution {name: 'Kurumca', type: 'public_payer', role: 'financer'});
MERGE (inst:Institution {name: 'Sağlık Hizmetleri Fiyatlandırma Komisyonu', type: 'pricing_commission', role: 'tariff_setter'});
MERGE (inst:Institution {name: 'Kurum', type: 'payer_institution', role: 'ödeme yapan ve bedelleri karşılayan kurum'});
MERGE (inst:Institution {name: 'Sağlık Bakanlığı', type: 'government_health_authority', role: 'bildirim_makami'});
MERGE (inst:Institution {name: 'sağlık hizmeti sunucusu', type: 'healthcare_provider', role: 'service_provider'});
MERGE (inst:Institution {name: 'aynı sağlık hizmeti sunucusunda', type: 'healthcare_provider', role: 'service_provider'});
MERGE (inst:Institution {name: 'aynı sağlık hizmeti sunucusundaki', type: 'healthcare_provider', role: 'service_provider'});
MERGE (inst:Institution {name: 'sağl ık hizmeti sunucusunda', type: 'healthcare_provider', role: 'treatment_provider'});
MERGE (inst:Institution {name: 'başka bir sağlık hizmeti sunucusuna', type: 'healthcare_provider', role: 'receiving_provider'});
MERGE (inst:Institution {name: 'sevk eden sağlık kurumu', type: 'referring_institution', role: 'payment_recipient'});
MERGE (inst:Institution {name: 'Sağlık Bakanlığına bağlı eğitim ve araştırma hastaneler', type: 'public_hospital'});
MERGE (inst:Institution {name: 'Tıp Fakülteleri Bulunan Devlet Üniversiteleri Sağlık Uygulama ve Araştırma Merkezleri', type: 'university_hospital', ownership: 'devlet'});
MERGE (inst:Institution {name: 'Tıp Fakülteleri Bulunan Vakıf Üniversiteleri Sağlık Uygulama ve Araştırma Merkezleri', type: 'university_hospital', ownership: 'vakıf'});
MERGE (inst:Institution {name: 'Sağlık Bakanlığının', type: 'government_ministry', role: 'regulatory_authority'});


// ============================================================================
// MEDICAL SERVICE NODES (Surrounding Payment Method Hub)
// ============================================================================

MERGE (ms:MedicalService {type: 'emergency_health_services', name: 'Acil sağlık hizmetleri', payment_method: 'hizmet başına ödeme yöntemi', coverage_status: 'covered_under_fee_for_service'});
MERGE (ms:MedicalService {type: 'occupational_accident_health_services', name: 'İş kazasına yönelik sağlanan sağlık hizmetleri', payment_method: 'hizmet başına ödeme yöntemi', legal_context: 'iş kazası kapsamında sunulan sağlık hizmetleri', coverage_status: 'covered_under_fee_for_service'});
MERGE (ms:MedicalService {type: 'occupational_disease_health_services', name: 'Meslek hastalıkları hastanelerince sağlanan meslek hastalığına yönelik sağlık hizmetleri', payment_method: 'hizmet başına ödeme yöntemi', coverage_status: 'covered_under_fee_for_service', provider: 'Meslek hastalıkları hastaneleri'});
MERGE (ms:MedicalService {type: 'pre_transplant_tests_for_donor', name: 'Organ ve doku nakline ilişkin donöre yapılan hazırlık tetkik ve tahlilleri', payment_method: 'hizmet başına ödeme yöntemi', coverage_status: 'covered_under_fee_for_service'});
MERGE (ms:MedicalService {type: 'dental_treatment_procedures', name: 'Diş tedavilerine yönelik işlemler', payment_method: 'hizmet başına ödeme yöntemi', coverage_status: 'covered_under_fee_for_service', specialty: 'dentistry'});
MERGE (ms:MedicalService {type: 'referred_health_services', name: 'sağlık hizmeti sunucusuna sevk edilen kişilere sunulan sağlık hizmetleri', payment_method: 'hizmet başına ödeme yöntemi', coverage_status: 'covered_under_fee_for_service'});
MERGE (ms:MedicalService {type: 'injection_dressing_procedures', name: 'Enjeksiyon/pansuman', payment_method: 'hizmet başına ödeme yöntemi', coverage_status: 'covered_under_fee_for_service'});
MERGE (ms:MedicalService {type: 'addiction_treatment', name: 'Alkol, madde bağımlılığı tedavisi', payment_method: 'hizmet başına ödeme yöntemi', coverage_status: 'covered_under_fee_for_service'});


// ============================================================================
// MEDICAL PROCEDURE NODES
// ============================================================================

MERGE (proc:MedicalProcedure {name: 'gastroskopi', type: 'endoscopic_procedure', body_system: 'gastrointestinal', category: 'tetkik / tanısal işlem'});
MERGE (proc:MedicalProcedure {name: 'kolonoskopi', type: 'endoscopic_procedure', body_system: 'gastrointestinal', category: 'tetkik / tanısal işlem'});
MERGE (proc:MedicalProcedure {name: 'rektosigmoidoskopi', type: 'endoscopic_procedure', body_system: 'gastrointestinal', category: 'tetkik / tanısal işlem'});
MERGE (proc:MedicalProcedure {name: 'rektoskopi', type: 'endoscopic_procedure', body_system: 'gastrointestinal', category: 'tetkik / tanısal işlem'});
MERGE (proc:MedicalProcedure {name: 'bronkoskopi', type: 'endoscopic_procedure', body_system: 'solunum', category: 'tetkik / tanısal işlem'});
MERGE (proc:MedicalProcedure {name: 'anjiyografi', type: 'görüntüleme_prosedürü', body_system: 'vasküler', category: 'tetkik / tanısal işlem'});
MERGE (proc:MedicalProcedure {name: 'kontrol muayeneleri', category: 'follow_up_examination'});
MERGE (proc:MedicalProcedure {name: '700610 kodlu “Transözefajiyal ekokardiyografi”', code: '700610', type: 'diagnostic_imaging', specialty: 'kardiyoloji'});
MERGE (proc:MedicalProcedure {name: '70 0611  kodlu “Transözefajiyal ekokardiyografi, ç', code: '700611', type: 'diagnostic_imaging', specialty: 'pediatrik kardiyoloji'});


// ============================================================================
// REGULATION LIST/ANNEX NODES
// ============================================================================

MERGE (list:RegulationList {code: 'EK -2/A-1', name: 'SUT eki “Sağlık Hizmeti Sunucularının Ayakta Tedavilerde Sınıflandırılması Listesi”', function: 'sağlık hizmeti sunucularını sınıflandırma', scope: 'Sağlık Hizmeti Sunucularının Ayakta Tedavilerde Sınıflandırılması', type: 'classification_list'});
MERGE (list:RegulationList {code: 'EK-2/A', name: 'SUT eki EK-2/A Listesi', function: 'ödeme tutarlarını belirleme', scope: 'ayakta tedavilerde ödeme tutarları', type: 'tariff_list'});
MERGE (list:RegulationList {code: 'EK -2/A-2', name: 'SUT eki “Ayaktan Başvurularda İlave Olarak Faturalandırılabilecek İşlemler Listesi”', function: 'ayaktan başvurularda ilave faturalandırılabilecek işlemleri belirleme', scope: 'Ayaktan Başvurularda İlave Olarak Faturalandırılabilecek İşlemler', type: 'additional_billable_procedures_list'});


// ============================================================================
// BILLING RULE NODES
// ============================================================================

MERGE (br:BillingRule {identifier: 'BR-001', action: 'Kuruma faturalandırma', responsible_party: 'Kurumla sözleşmeli sağlık hizmeti sunucuları', requirement_type: 'prohibition'});
MERGE (br:BillingRule {identifier: 'BR-002', action: 'fatura düzenleyerek sağlık hizmeti sunma', responsible_party: 'bu hekimler', context: 'özel sağlık hizmeti  sunucusu bünyesinde çalışan hekim veya diş hekimleri'});
MERGE (br:BillingRule {identifier: 'BR-003', payer: 'Kurum', context: 'SUT gereği düzenlenmesi gereken sağlık kurulu raporu ile ilgili'});
MERGE (br:BillingRule {identifier: 'BR-004', action: 'muayene bedeli faturalandırma'});
MERGE (br:BillingRule {identifier: 'BR-005', action: 'faturalandırılır'});
MERGE (br:BillingRule {identifier: 'BR-006'});
MERGE (br:BillingRule {identifier: 'BR-007'});
MERGE (br:BillingRule {identifier: 'BR-008', action: 'faturalandırılamaz'});
MERGE (br:BillingRule {identifier: 'BR-009', action: 'faturalandırılacaktır'});
MERGE (br:BillingRule {identifier: 'BR-010'});
MERGE (br:BillingRule {identifier: 'BR-011'});
MERGE (br:BillingRule {identifier: 'BR-012', action: 'faturalandırma'});
MERGE (br:BillingRule {identifier: 'BR-013', requirement_type: 'mandatory'});
MERGE (br:BillingRule {identifier: 'BR-014', requirement_type: 'permitted'});
MERGE (br:BillingRule {identifier: 'BR-015', requirement_type: 'permitted'});
MERGE (br:BillingRule {identifier: 'BR-016', requirement_type: 'mandatory'});
MERGE (br:BillingRule {identifier: 'BR-017', context: 'Transözefajiyal ekokardiyografi işlemlerinin yapılması durumunda'});
MERGE (br:BillingRule {identifier: 'BR-018', action: 'faturalandırma', responsible_party: 'ikinci ve üçüncü basamak özel sağlık hizmeti sunucuları', requirement_type: 'quantitative_limit'});
MERGE (br:BillingRule {identifier: 'BR-019', action: 'Kuruma faturalandırma', requirement_type: 'absolute_prohibition', payer: 'Kurum'});
MERGE (br:BillingRule {identifier: 'BR-020'});
MERGE (br:BillingRule {identifier: 'BR-021', action: 'faturalandırılamaz', context: 'hizmet başına ödeme yöntemi ile faturalandırılan yukarıdaki hizmetler'});


// ============================================================================
// AMENDMENT NODES
// ============================================================================

MERGE (amd:Amendment {official_gazette_number: '31934', official_gazette_date: '25/08/2022', effective_date: '03/09/2022', scope: '2.2.1.B - İkinci ve üçüncü basamak sağlık kurumları'});
MERGE (amd:Amendment {official_gazette_number: '32541', official_gazette_date: '09/05/2024', article_reference: '1-a md.', type: 'regulation_amendment'});
MERGE (amd:Amendment {official_gazette_number: '29850', official_gazette_date: '07/10/2016', article_reference: '5 md.', type: 'regulatory_amendment'});


// ============================================================================
// PROFESSIONAL ROLE NODES
// ============================================================================

MERGE (role:ProfessionalRole {type: 'physician', name: 'Hekim', sector: 'özel sağlık hizmeti sunucusu bünyesinde çalışması', regulatory_status: 'sağlık meslek mensubu'});
MERGE (role:ProfessionalRole {type: 'dentist', name: 'diş hekimlerinin', sector: 'özel sağlık hizmeti sunucusu bünyesinde çalışması', regulatory_status: 'sağlık meslek mensubu'});


// ============================================================================
// RELATIONSHIPS
// ============================================================================

// Connect Medical Services to Payment Methods

MATCH (ms:MedicalService {type: 'emergency_health_services'})
MATCH (pm:PaymentMethod {name: 'hizmet başına ödeme yöntemi'})
MERGE (ms)-[:BILLED_VIA]->(pm);

MATCH (ms:MedicalService {type: 'occupational_accident_health_services'})
MATCH (pm:PaymentMethod {name: 'hizmet başına ödeme yöntemi'})
MERGE (ms)-[:BILLED_VIA]->(pm);

MATCH (ms:MedicalService {type: 'occupational_disease_health_services'})
MATCH (pm:PaymentMethod {name: 'hizmet başına ödeme yöntemi'})
MERGE (ms)-[:BILLED_VIA]->(pm);

MATCH (ms:MedicalService {type: 'pre_transplant_tests_for_donor'})
MATCH (pm:PaymentMethod {name: 'hizmet başına ödeme yöntemi'})
MERGE (ms)-[:BILLED_VIA]->(pm);

MATCH (ms:MedicalService {type: 'dental_treatment_procedures'})
MATCH (pm:PaymentMethod {name: 'hizmet başına ödeme yöntemi'})
MERGE (ms)-[:BILLED_VIA]->(pm);

MATCH (ms:MedicalService {type: 'referred_health_services'})
MATCH (pm:PaymentMethod {name: 'hizmet başına ödeme yöntemi'})
MERGE (ms)-[:BILLED_VIA]->(pm);

MATCH (ms:MedicalService {type: 'injection_dressing_procedures'})
MATCH (pm:PaymentMethod {name: 'hizmet başına ödeme yöntemi'})
MERGE (ms)-[:BILLED_VIA]->(pm);

MATCH (ms:MedicalService {type: 'addiction_treatment'})
MATCH (pm:PaymentMethod {name: 'hizmet başına ödeme yöntemi'})
MERGE (ms)-[:BILLED_VIA]->(pm);

// Connect Sections to Payment Methods

MATCH (sec:Section {identifier: '2.2.1.B-2'})
MATCH (pm:PaymentMethod) WHERE pm.name CONTAINS 'hizmet başına ödeme'
MERGE (sec)-[:USES_PAYMENT_METHOD]->(pm);

// Connect Sections to Care Settings

MATCH (sec:Section {identifier: '2.2.1.B-2'})
MATCH (cs:CareSetting {name: 'ayakta tedavi'})
MERGE (sec)-[:APPLIES_TO_SETTING]->(cs);

// Connect Sections to Medical Services

MATCH (sec:Section)
WHERE sec.payment_model IS NOT NULL
MATCH (ms:MedicalService)
WHERE ms.payment_method CONTAINS sec.payment_model OR sec.payment_model CONTAINS ms.payment_method
MERGE (sec)-[:INCLUDES_SERVICE]->(ms);

// Connect Medical Services to Institutions

MATCH (ms:MedicalService {type: 'occupational_disease_health_services'})
MATCH (inst:Institution) WHERE inst.name CONTAINS 'Meslek hastalıkları hastaneler'
MERGE (ms)-[:PROVIDED_BY]->(inst);
