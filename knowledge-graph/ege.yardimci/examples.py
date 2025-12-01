"""
LangExtract Examples for SUT (Sağlık Uygulama Tebliği) Document Processing
==========================================================================

These examples are designed to teach the LLM to:
1. Extract section headers with proper identifiers
2. Link ALL child entities to their parent sections via `parent_section` attribute
3. Capture hierarchical relationships between sections
4. Extract structured rules, obligations, and coverage information

CRITICAL DESIGN PRINCIPLE:
Every entity extracted under a section MUST include `parent_section` attribute
pointing to the section identifier (e.g., "2.2.1.B-2", "1.8.1", "Madde 15")
section          → Main regulatory sections with identifiers
medical_service  → Services covered under payment methods
institution      → Healthcare providers by level
payment_rule     → Specific payment amounts/conditions
billing_rule     → What can/cannot be billed
co_payment_rule  → Patient co-payment amounts
coverage_rule    → What SGK covers
medical_item     → Specific items with coverage conditions
prescription_rule → Prescription duration/quantity limits
referral_rule    → Patient referral conditions
quota_rule       → Daily examination limits
limit            → Numeric limits (max values)
amendment        → Regulatory changes
scope            → Applicability scope
list_reference   → References to EK lists
medical_procedure → Specific procedures with codes

"""

import langextract as lx
import textwrap

EXAMPLES = [
    # ==========================================================================
    # Example 1: Section with listed medical services (fee-for-service)
    # This is the CORE example showing how to link services to sections
    # ==========================================================================
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            2.2.1.B-2 - Hizmet başına ödeme yöntemi ile faturalandırılacak ayakta tedaviler
            (Değişik: RG- 25/08/2022- 31934/ 12-c md. Yürürlük: 03/09/2022)
            (2) İkinci ve üçüncü basamak sağlık hizmeti sunucularında;
            a) Acil sağlık hizmetleri,
            b) İş kazasına yönelik sağlanan sağlık hizmetleri,
            c) Meslek hastalıkları hastanelerince sağlanan meslek hastalığına yönelik sağlık hizmetleri,
            ç) MEDULA'da tedavi tipi "onkolojik tedavi" olarak seçilmiş onkolojik ön tanı/tanı konulmuş 
            hastalıklar ile ilgili tüm işlemler,
            d) Organ ve doku nakline ilişkin donöre yapılan hazırlık tetkik ve tahlilleri,
            e) Diş tedavilerine yönelik işlemler,
            f) Kurum birimlerince sevk belgesi düzenlenmek suretiyle sağlık hizmeti sunucusuna 
            sevk edilen kişilere sunulan sağlık hizmetleri,
            g) Enjeksiyon/pansuman,
            ğ) Alkol, madde bağımlılığı tedavisi,
            "hizmet başına ödeme yöntemi" ile faturalandırılır. Bu durumda SUT eki EK-2/A 
            Listesinde yer alan tutarlar faturalandırılamaz."""),
        extractions=[
            # FIRST: Extract the section header
            lx.data.Extraction(
                extraction_class="section",
                extraction_text="2.2.1.B-2 - Hizmet başına ödeme yöntemi ile faturalandırılacak ayakta tedaviler",
                attributes={
                    "identifier": "2.2.1.B-2",
                    "title": "Hizmet başına ödeme yöntemi ile faturalandırılacak ayakta tedaviler",
                    "parent_section": "2.2.1.B",
                    "payment_method": "hizmet başına ödeme yöntemi",
                    "care_setting": "ayakta tedavi",
                }
            ),
            # Extract the scope/applicability
            lx.data.Extraction(
                extraction_class="scope",
                extraction_text="İkinci ve üçüncü basamak sağlık hizmeti sunucularında",
                attributes={
                    "parent_section": "2.2.1.B-2",
                    "paragraph": "2",
                    "applicable_level": ["ikinci basamak", "üçüncü basamak"],
                    "provider_type": "sağlık hizmeti sunucuları",
                }
            ),
            # THEN: Each service with parent_section link
            lx.data.Extraction(
                extraction_class="medical_service",
                extraction_text="Acil sağlık hizmetleri",
                attributes={
                    "parent_section": "2.2.1.B-2",
                    "paragraph": "2",
                    "item": "a",
                    "name": "Acil sağlık hizmetleri",
                    "service_type": "emergency_services",
                    "payment_method": "hizmet başına ödeme yöntemi",
                    "coverage_status": "covered",
                }
            ),
            lx.data.Extraction(
                extraction_class="medical_service",
                extraction_text="İş kazasına yönelik sağlanan sağlık hizmetleri",
                attributes={
                    "parent_section": "2.2.1.B-2",
                    "paragraph": "2",
                    "item": "b",
                    "name": "İş kazasına yönelik sağlık hizmetleri",
                    "service_type": "occupational_accident",
                    "legal_context": "iş kazası",
                    "payment_method": "hizmet başına ödeme yöntemi",
                    "coverage_status": "covered",
                }
            ),
            lx.data.Extraction(
                extraction_class="medical_service",
                extraction_text="Meslek hastalıkları hastanelerince sağlanan meslek hastalığına yönelik sağlık hizmetleri",
                attributes={
                    "parent_section": "2.2.1.B-2",
                    "paragraph": "2",
                    "item": "c",
                    "name": "Meslek hastalığına yönelik sağlık hizmetleri",
                    "service_type": "occupational_disease",
                    "provider_restriction": "meslek hastalıkları hastaneleri",
                    "payment_method": "hizmet başına ödeme yöntemi",
                    "coverage_status": "covered",
                }
            ),
            lx.data.Extraction(
                extraction_class="medical_service",
                extraction_text="MEDULA'da tedavi tipi onkolojik tedavi olarak seçilmiş hastalıklar ile ilgili tüm işlemler",
                attributes={
                    "parent_section": "2.2.1.B-2",
                    "paragraph": "2",
                    "item": "ç",
                    "name": "Onkolojik tedavi işlemleri",
                    "service_type": "oncology",
                    "system_requirement": "MEDULA tedavi tipi: onkolojik tedavi",
                    "scope": "tüm işlemler",
                    "payment_method": "hizmet başına ödeme yöntemi",
                    "coverage_status": "covered",
                }
            ),
            lx.data.Extraction(
                extraction_class="medical_service",
                extraction_text="Organ ve doku nakline ilişkin donöre yapılan hazırlık tetkik ve tahlilleri",
                attributes={
                    "parent_section": "2.2.1.B-2",
                    "paragraph": "2",
                    "item": "d",
                    "name": "Donör hazırlık tetkik ve tahlilleri",
                    "service_type": "transplant_donor_preparation",
                    "clinical_context": "organ ve doku nakli",
                    "payment_method": "hizmet başına ödeme yöntemi",
                    "coverage_status": "covered",
                }
            ),
            lx.data.Extraction(
                extraction_class="medical_service",
                extraction_text="Diş tedavilerine yönelik işlemler",
                attributes={
                    "parent_section": "2.2.1.B-2",
                    "paragraph": "2",
                    "item": "e",
                    "name": "Diş tedavileri",
                    "service_type": "dental",
                    "payment_method": "hizmet başına ödeme yöntemi",
                    "coverage_status": "covered",
                }
            ),
            lx.data.Extraction(
                extraction_class="medical_service",
                extraction_text="Kurum birimlerince sevk belgesi düzenlenmek suretiyle sevk edilen kişilere sunulan sağlık hizmetleri",
                attributes={
                    "parent_section": "2.2.1.B-2",
                    "paragraph": "2",
                    "item": "f",
                    "name": "Kurum sevkli sağlık hizmetleri",
                    "service_type": "referred_services",
                    "referral_authority": "Kurum birimleri",
                    "document_requirement": "sevk belgesi",
                    "examples": "maluliyet, meslek hastalığı, kontrol muayeneleri",
                    "payment_method": "hizmet başına ödeme yöntemi",
                    "coverage_status": "covered",
                }
            ),
            lx.data.Extraction(
                extraction_class="medical_service",
                extraction_text="Enjeksiyon/pansuman",
                attributes={
                    "parent_section": "2.2.1.B-2",
                    "paragraph": "2",
                    "item": "g",
                    "name": "Enjeksiyon/pansuman",
                    "service_type": "injection_dressing",
                    "payment_method": "hizmet başına ödeme yöntemi",
                    "coverage_status": "covered",
                    "note": "sadece bu amaçla gelen hasta için sadece bu bedel karşılanır",
                }
            ),
            lx.data.Extraction(
                extraction_class="medical_service",
                extraction_text="Alkol, madde bağımlılığı tedavisi",
                attributes={
                    "parent_section": "2.2.1.B-2",
                    "paragraph": "2",
                    "item": "ğ",
                    "name": "Alkol ve madde bağımlılığı tedavisi",
                    "service_type": "addiction_treatment",
                    "payment_method": "hizmet başına ödeme yöntemi",
                    "coverage_status": "covered",
                }
            ),
            # Extract the billing prohibition rule
            lx.data.Extraction(
                extraction_class="billing_rule",
                extraction_text="Bu durumda SUT eki EK-2/A Listesinde yer alan tutarlar faturalandırılamaz",
                attributes={
                    "parent_section": "2.2.1.B-2",
                    "paragraph": "2",
                    "rule_type": "prohibition",
                    "condition": "hizmet başına ödeme yöntemi ile faturalandırma",
                    "prohibited_item": "EK-2/A Listesi tutarları",
                    "list_reference": "EK-2/A",
                }
            ),
        ]
    ),

    # ==========================================================================
    # Example 2: Section hierarchy and healthcare provider levels
    # ==========================================================================
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            1.4 - Sağlık hizmeti sunucuları
            1.4.1- Birinci basamak sağlık hizmeti sunucuları
            1.4.1.A - Birinci basamak resmi sağlık hizmeti sunucuları
            1) Toplum sağlığı merkezi (TSM)
            2) Aile sağlığı merkezi (ASM)
            3) 112 Acil sağlık hizmeti birimleri
            4) Üniversiteler bünyesindeki mediko-sosyal birimler
            1.4.1.B - Birinci basamak özel sağlık hizmeti sunucuları
            1) Evde bakım merkezleri veya birimler
            2) Özel poliklinikler
            3) Ağız ve diş sağlığı hizmeti veren özel sağlık kuruluşları"""),
        extractions=[
            # Parent section
            lx.data.Extraction(
                extraction_class="section",
                extraction_text="1.4 - Sağlık hizmeti sunucuları",
                attributes={
                    "identifier": "1.4",
                    "title": "Sağlık hizmeti sunucuları",
                    "level": "chapter",
                }
            ),
            # Child section
            lx.data.Extraction(
                extraction_class="section",
                extraction_text="1.4.1- Birinci basamak sağlık hizmeti sunucuları",
                attributes={
                    "identifier": "1.4.1",
                    "title": "Birinci basamak sağlık hizmeti sunucuları",
                    "parent_section": "1.4",
                    "healthcare_level": "birinci basamak",
                }
            ),
            # Sub-section for public providers
            lx.data.Extraction(
                extraction_class="section",
                extraction_text="1.4.1.A - Birinci basamak resmi sağlık hizmeti sunucuları",
                attributes={
                    "identifier": "1.4.1.A",
                    "title": "Birinci basamak resmi sağlık hizmeti sunucuları",
                    "parent_section": "1.4.1",
                    "healthcare_level": "birinci basamak",
                    "ownership": "resmi",
                }
            ),
            # Institution entries linked to section
            lx.data.Extraction(
                extraction_class="institution",
                extraction_text="Toplum sağlığı merkezi (TSM)",
                attributes={
                    "parent_section": "1.4.1.A",
                    "item_number": "1",
                    "name": "Toplum sağlığı merkezi",
                    "abbreviation": "TSM",
                    "healthcare_level": "birinci basamak",
                    "ownership": "resmi",
                }
            ),
            lx.data.Extraction(
                extraction_class="institution",
                extraction_text="Aile sağlığı merkezi (ASM)",
                attributes={
                    "parent_section": "1.4.1.A",
                    "item_number": "2",
                    "name": "Aile sağlığı merkezi",
                    "abbreviation": "ASM",
                    "healthcare_level": "birinci basamak",
                    "ownership": "resmi",
                }
            ),
            lx.data.Extraction(
                extraction_class="institution",
                extraction_text="112 Acil sağlık hizmeti birimleri",
                attributes={
                    "parent_section": "1.4.1.A",
                    "item_number": "3",
                    "name": "112 Acil sağlık hizmeti birimleri",
                    "code": "112",
                    "service_type": "emergency",
                    "healthcare_level": "birinci basamak",
                    "ownership": "resmi",
                }
            ),
            lx.data.Extraction(
                extraction_class="institution",
                extraction_text="Üniversiteler bünyesindeki mediko-sosyal birimler",
                attributes={
                    "parent_section": "1.4.1.A",
                    "item_number": "4",
                    "name": "Üniversite mediko-sosyal birimleri",
                    "affiliation": "üniversiteler",
                    "healthcare_level": "birinci basamak",
                    "ownership": "resmi",
                }
            ),
            # Sub-section for private providers
            lx.data.Extraction(
                extraction_class="section",
                extraction_text="1.4.1.B - Birinci basamak özel sağlık hizmeti sunucuları",
                attributes={
                    "identifier": "1.4.1.B",
                    "title": "Birinci basamak özel sağlık hizmeti sunucuları",
                    "parent_section": "1.4.1",
                    "healthcare_level": "birinci basamak",
                    "ownership": "özel",
                }
            ),
            lx.data.Extraction(
                extraction_class="institution",
                extraction_text="Evde bakım merkezleri veya birimler",
                attributes={
                    "parent_section": "1.4.1.B",
                    "item_number": "1",
                    "name": "Evde bakım merkezleri",
                    "service_type": "home_care",
                    "healthcare_level": "birinci basamak",
                    "ownership": "özel",
                }
            ),
            lx.data.Extraction(
                extraction_class="institution",
                extraction_text="Özel poliklinikler",
                attributes={
                    "parent_section": "1.4.1.B",
                    "item_number": "2",
                    "name": "Özel poliklinikler",
                    "healthcare_level": "birinci basamak",
                    "ownership": "özel",
                }
            ),
            lx.data.Extraction(
                extraction_class="institution",
                extraction_text="Ağız ve diş sağlığı hizmeti veren özel sağlık kuruluşları",
                attributes={
                    "parent_section": "1.4.1.B",
                    "item_number": "3",
                    "name": "Özel ağız ve diş sağlığı kuruluşları",
                    "specialty": "dental",
                    "healthcare_level": "birinci basamak",
                    "ownership": "özel",
                }
            ),
        ]
    ),

    # ==========================================================================
    # Example 3: Payment rules with amounts and conditions
    # ==========================================================================
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            2.2.1.A - Birinci basamak sağlık kuruluşları
            (1) Birinci basamak sağlık kuruluşlarındaki ayakta tedavilerde, her başvuru için 
            11 (onbir) TL ödeme yapılır. Hastanın diğer bir sağlık kurumuna sevk edilmesi 
            halinde ise sadece 5 (beş) TL ödeme yapılır."""),
        extractions=[
            lx.data.Extraction(
                extraction_class="section",
                extraction_text="2.2.1.A - Birinci basamak sağlık kuruluşları",
                attributes={
                    "identifier": "2.2.1.A",
                    "title": "Birinci basamak sağlık kuruluşları",
                    "parent_section": "2.2.1",
                    "healthcare_level": "birinci basamak",
                    "care_setting": "ayakta tedavi",
                }
            ),
            lx.data.Extraction(
                extraction_class="payment_rule",
                extraction_text="her başvuru için 11 (onbir) TL ödeme yapılır",
                attributes={
                    "parent_section": "2.2.1.A",
                    "paragraph": "1",
                    "payment_type": "per_visit",
                    "amount": 11,
                    "amount_text": "onbir",
                    "currency": "TL",
                    "care_setting": "ayakta tedavi",
                    "healthcare_level": "birinci basamak",
                    "condition": "standart başvuru",
                }
            ),
            lx.data.Extraction(
                extraction_class="payment_rule",
                extraction_text="Hastanın diğer bir sağlık kurumuna sevk edilmesi halinde ise sadece 5 (beş) TL ödeme yapılır",
                attributes={
                    "parent_section": "2.2.1.A",
                    "paragraph": "1",
                    "payment_type": "per_referral",
                    "amount": 5,
                    "amount_text": "beş",
                    "currency": "TL",
                    "condition": "hastanın sevk edilmesi",
                    "note": "sadece",
                }
            ),
        ]
    ),

    # ==========================================================================
    # Example 4: Complex billing rules with multiple conditions
    # ==========================================================================
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            2.2.1.B-1 - Ayakta tedavilerde ödeme uygulaması
            (2) Hastanın aynı sağlık hizmeti sunucusuna, acil servise başvuruları hariç olmak 
            üzere ayaktan başvurduğu gün dâhil, 10 (on) gün içindeki aynı uzmanlık dalına 
            diğer ayaktan başvurularında; sadece SUT eki EK-2/A-2 Listesinde yer alan 
            işlemlerin bedelleri faturalandırılabilecek olup SUT eki EK-2/A Listesinde yer 
            alan tutar faturalandırılamaz."""),
        extractions=[
            lx.data.Extraction(
                extraction_class="section",
                extraction_text="2.2.1.B-1 - Ayakta tedavilerde ödeme uygulaması",
                attributes={
                    "identifier": "2.2.1.B-1",
                    "title": "Ayakta tedavilerde ödeme uygulaması",
                    "parent_section": "2.2.1.B",
                    "care_setting": "ayakta tedavi",
                }
            ),
            lx.data.Extraction(
                extraction_class="billing_rule",
                extraction_text="10 gün içindeki aynı uzmanlık dalına diğer ayaktan başvurularında",
                attributes={
                    "parent_section": "2.2.1.B-1",
                    "paragraph": "2",
                    "rule_type": "repeat_visit_restriction",
                    "time_window": "10 gün",
                    "time_window_start": "ayaktan başvurulan gün dahil",
                    "scope": "aynı uzmanlık dalı",
                    "provider_scope": "aynı sağlık hizmeti sunucusu",
                    "exception": "acil servis başvuruları",
                    "billable_items": "EK-2/A-2 Listesi işlemleri",
                    "non_billable_items": "EK-2/A Listesi tutarları",
                }
            ),
            lx.data.Extraction(
                extraction_class="list_reference",
                extraction_text="SUT eki EK-2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılabilecek",
                attributes={
                    "parent_section": "2.2.1.B-1",
                    "paragraph": "2",
                    "list_code": "EK-2/A-2",
                    "list_name": "Ayaktan Başvurularda İlave Olarak Faturalandırılabilecek İşlemler Listesi",
                    "billing_status": "billable",
                    "condition": "10 gün içinde tekrar başvuru",
                }
            ),
            lx.data.Extraction(
                extraction_class="list_reference",
                extraction_text="SUT eki EK-2/A Listesinde yer alan tutar faturalandırılamaz",
                attributes={
                    "parent_section": "2.2.1.B-1",
                    "paragraph": "2",
                    "list_code": "EK-2/A",
                    "billing_status": "not_billable",
                    "condition": "10 gün içinde tekrar başvuru",
                }
            ),
        ]
    ),

    # ==========================================================================
    # Example 5: Co-payment rules with exceptions
    # ==========================================================================
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            1.8.1 - Ayakta tedavide hekim ve diş hekimi muayenesi katılım payı
            (1) Ayakta tedavide hekim ve diş hekimi muayenesi için kişilerden 
            aşağıda belirtilen tutarlarda katılım payı alınır.
            a) Birinci basamak sağlık hizmeti sunucularında: 2 (iki) TL,
            b) İkinci ve üçüncü basamak resmi sağlık hizmeti sunucularında: 6 (altı) TL,
            c) Özel sağlık hizmeti sunucularında: 15 (onbeş) TL.
            (2) Birinci basamak sağlık hizmeti sunucuları muayeneleri, kronik hastalıklar, 
            sevkli hastalar ve acil haller hariç olmak üzere 10 gün içerisinde aynı 
            uzmanlık dalında farklı sağlık hizmeti sunucusuna yapılan başvurularda 
            katılım payı tutarları 5 TL artırılarak tahsil edilir."""),
        extractions=[
            lx.data.Extraction(
                extraction_class="section",
                extraction_text="1.8.1 - Ayakta tedavide hekim ve diş hekimi muayenesi katılım payı",
                attributes={
                    "identifier": "1.8.1",
                    "title": "Ayakta tedavide hekim ve diş hekimi muayenesi katılım payı",
                    "parent_section": "1.8",
                    "topic": "co_payment",
                    "care_setting": "ayakta tedavi",
                }
            ),
            lx.data.Extraction(
                extraction_class="co_payment_rule",
                extraction_text="Birinci basamak sağlık hizmeti sunucularında: 2 TL",
                attributes={
                    "parent_section": "1.8.1",
                    "paragraph": "1",
                    "item": "a",
                    "healthcare_level": "birinci basamak",
                    "amount": 2,
                    "currency": "TL",
                    "service_type": "hekim ve diş hekimi muayenesi",
                }
            ),
            lx.data.Extraction(
                extraction_class="co_payment_rule",
                extraction_text="İkinci ve üçüncü basamak resmi sağlık hizmeti sunucularında: 6 TL",
                attributes={
                    "parent_section": "1.8.1",
                    "paragraph": "1",
                    "item": "b",
                    "healthcare_level": ["ikinci basamak", "üçüncü basamak"],
                    "ownership": "resmi",
                    "amount": 6,
                    "currency": "TL",
                    "service_type": "hekim ve diş hekimi muayenesi",
                }
            ),
            lx.data.Extraction(
                extraction_class="co_payment_rule",
                extraction_text="Özel sağlık hizmeti sunucularında: 15 TL",
                attributes={
                    "parent_section": "1.8.1",
                    "paragraph": "1",
                    "item": "c",
                    "ownership": "özel",
                    "amount": 15,
                    "currency": "TL",
                    "service_type": "hekim ve diş hekimi muayenesi",
                }
            ),
            lx.data.Extraction(
                extraction_class="co_payment_surcharge",
                extraction_text="10 gün içerisinde aynı uzmanlık dalında farklı sağlık hizmeti sunucusuna yapılan başvurularda katılım payı tutarları 5 TL artırılarak tahsil edilir",
                attributes={
                    "parent_section": "1.8.1",
                    "paragraph": "2",
                    "surcharge_amount": 5,
                    "currency": "TL",
                    "condition": "10 gün içinde aynı uzmanlık dalında farklı sunucuya başvuru",
                    "time_window": "10 gün",
                    "scope": "aynı uzmanlık dalı",
                    "exceptions": ["birinci basamak muayeneleri", "kronik hastalıklar", "sevkli hastalar", "acil haller"],
                }
            ),
        ]
    ),

    # ==========================================================================
    # Example 6: Coverage rules with medical item conditions
    # ==========================================================================
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            3.3.4 - Greftler
            (9) Aşağıdaki deri taklitleri (yedekleri) sadece yanık tedavisinde kullanılması 
            halinde ödenir.
            a) Dermis iskeleti: dermisin tam kat hasar gördüğü üçüncü derece yanık 
            bölgelerinin tedavisinde, %40'ı (0-12 yaş için %20) geçen yanıklarda sağlık 
            kurulu raporu ile Kurumca karşılanır.
            b) Deri benzerleri: en az derin ikinci derece yanıkların tedavisinde, yüz, 
            boyun, el, ayak, perine, eklem bölgelerini içeren veya %40'ı (0-12 yaş için %20) 
            geçen yanıklarda sağlık kurulu raporu ile Kurumca karşılanır."""),
        extractions=[
            lx.data.Extraction(
                extraction_class="section",
                extraction_text="3.3.4 - Greftler",
                attributes={
                    "identifier": "3.3.4",
                    "title": "Greftler",
                    "parent_section": "3.3",
                    "category": "tıbbi malzeme",
                }
            ),
            lx.data.Extraction(
                extraction_class="coverage_rule",
                extraction_text="deri taklitleri sadece yanık tedavisinde kullanılması halinde ödenir",
                attributes={
                    "parent_section": "3.3.4",
                    "paragraph": "9",
                    "item_category": "deri taklitleri (yedekleri)",
                    "usage_condition": "yanık tedavisi",
                    "coverage_status": "conditional",
                }
            ),
            lx.data.Extraction(
                extraction_class="medical_item",
                extraction_text="Dermis iskeleti",
                attributes={
                    "parent_section": "3.3.4",
                    "paragraph": "9",
                    "item": "a",
                    "name": "Dermis iskeleti",
                    "category": "deri taklidi",
                    "indication": "üçüncü derece yanık",
                    "indication_detail": "dermisin tam kat hasar gördüğü bölge",
                    "threshold_adult": ">%40 vücut yüzeyi",
                    "threshold_pediatric": ">%20 vücut yüzeyi",
                    "pediatric_age_range": "0-12 yaş",
                    "document_requirement": "sağlık kurulu raporu",
                    "payer": "Kurum",
                    "coverage_status": "covered",
                }
            ),
            lx.data.Extraction(
                extraction_class="medical_item",
                extraction_text="Deri benzerleri",
                attributes={
                    "parent_section": "3.3.4",
                    "paragraph": "9",
                    "item": "b",
                    "name": "Deri benzerleri",
                    "category": "deri taklidi",
                    "indication": "en az derin ikinci derece yanık",
                    "body_areas": ["yüz", "boyun", "el", "ayak", "perine", "eklem"],
                    "threshold_adult": ">%40 vücut yüzeyi",
                    "threshold_pediatric": ">%20 vücut yüzeyi",
                    "pediatric_age_range": "0-12 yaş",
                    "document_requirement": "sağlık kurulu raporu",
                    "payer": "Kurum",
                    "coverage_status": "covered",
                }
            ),
        ]
    ),

    # ==========================================================================
    # Example 7: Prescription rules with duration limits
    # ==========================================================================
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            4.1.4 - Reçetelere yazılabilecek ilaç miktarı
            (1) Ayaktan tedavide, bir reçeteye en fazla dört kalem ve her kalem ilaçtan 
            bir kutunun miktarı kadar ilaç yazılabilir.
            (2) Kronik hastalıklarda üç aya kadar tedavi dozunda ilaç yazılabilir. Ancak 
            tedaviye yeni başlanan hastalarda ilk reçete en fazla bir aylık dozda düzenlenir.
            (3) Ayakta tedavide antibiyotikler için en fazla 10 günlük doz yazılabilir."""),
        extractions=[
            lx.data.Extraction(
                extraction_class="section",
                extraction_text="4.1.4 - Reçetelere yazılabilecek ilaç miktarı",
                attributes={
                    "identifier": "4.1.4",
                    "title": "Reçetelere yazılabilecek ilaç miktarı",
                    "parent_section": "4.1",
                    "topic": "prescription_limits",
                }
            ),
            lx.data.Extraction(
                extraction_class="prescription_rule",
                extraction_text="bir reçeteye en fazla dört kalem ve her kalem ilaçtan bir kutunun miktarı kadar ilaç yazılabilir",
                attributes={
                    "parent_section": "4.1.4",
                    "paragraph": "1",
                    "care_setting": "ayaktan tedavi",
                    "max_items_per_prescription": 4,
                    "max_quantity_per_item": "1 kutu",
                    "rule_type": "quantity_limit",
                }
            ),
            lx.data.Extraction(
                extraction_class="prescription_rule",
                extraction_text="Kronik hastalıklarda üç aya kadar tedavi dozunda ilaç yazılabilir",
                attributes={
                    "parent_section": "4.1.4",
                    "paragraph": "2",
                    "condition": "kronik hastalık",
                    "max_duration": "3 ay",
                    "max_duration_days": 90,
                    "rule_type": "duration_limit",
                }
            ),
            lx.data.Extraction(
                extraction_class="prescription_rule",
                extraction_text="tedaviye yeni başlanan hastalarda ilk reçete en fazla bir aylık dozda düzenlenir",
                attributes={
                    "parent_section": "4.1.4",
                    "paragraph": "2",
                    "condition": "tedaviye yeni başlama",
                    "max_duration": "1 ay",
                    "max_duration_days": 30,
                    "applies_to": "ilk reçete",
                    "rule_type": "duration_limit",
                }
            ),
            lx.data.Extraction(
                extraction_class="prescription_rule",
                extraction_text="antibiyotikler için en fazla 10 günlük doz yazılabilir",
                attributes={
                    "parent_section": "4.1.4",
                    "paragraph": "3",
                    "care_setting": "ayakta tedavi",
                    "drug_category": "antibiyotik",
                    "max_duration": "10 gün",
                    "max_duration_days": 10,
                    "rule_type": "duration_limit",
                }
            ),
        ]
    ),

    # ==========================================================================
    # Example 8: Referral rules with conditions
    # ==========================================================================
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            1.5.1.A-2 - Hasta sevk işlemleri
            (1) Tedavinin sağlanamaması halinde;
            a) Birinci basamak sağlık hizmeti sunucularınca; sevkler aynı yerleşim yeri 
            içindeki Sağlık Bakanlığı ikinci veya üçüncü basamak sağlık hizmeti sunucusuna 
            yapılabilir.
            b) İkinci basamak sağlık hizmeti sunucularınca;
            1) Kişiler, aynı yerleşim yeri içindeki Sağlık Bakanlığı ikinci veya üçüncü 
            basamak sağlık hizmeti sunucusuna sevk edilebilir.
            2) Kişiler, resmi sağlık hizmeti sunucularında uygun yoğun bakım yatağının 
            bulunmaması halinde özel sağlık hizmeti sunucularına sevk edilebilir."""),
        extractions=[
            lx.data.Extraction(
                extraction_class="section",
                extraction_text="1.5.1.A-2 - Hasta sevk işlemleri",
                attributes={
                    "identifier": "1.5.1.A-2",
                    "title": "Hasta sevk işlemleri",
                    "parent_section": "1.5.1.A",
                    "topic": "patient_referral",
                }
            ),
            lx.data.Extraction(
                extraction_class="referral_rule",
                extraction_text="Birinci basamak sağlık hizmeti sunucularınca sevkler aynı yerleşim yeri içindeki Sağlık Bakanlığı ikinci veya üçüncü basamak sağlık hizmeti sunucusuna yapılabilir",
                attributes={
                    "parent_section": "1.5.1.A-2",
                    "paragraph": "1",
                    "item": "a",
                    "referring_level": "birinci basamak",
                    "condition": "tedavinin sağlanamaması",
                    "target_levels": ["ikinci basamak", "üçüncü basamak"],
                    "target_authority": "Sağlık Bakanlığı",
                    "geographic_scope": "aynı yerleşim yeri",
                }
            ),
            lx.data.Extraction(
                extraction_class="referral_rule",
                extraction_text="İkinci basamak sağlık hizmeti sunucularınca kişiler aynı yerleşim yeri içindeki Sağlık Bakanlığı ikinci veya üçüncü basamak sağlık hizmeti sunucusuna sevk edilebilir",
                attributes={
                    "parent_section": "1.5.1.A-2",
                    "paragraph": "1",
                    "item": "b-1",
                    "referring_level": "ikinci basamak",
                    "condition": "tedavinin sağlanamaması",
                    "target_levels": ["ikinci basamak", "üçüncü basamak"],
                    "target_authority": "Sağlık Bakanlığı",
                    "geographic_scope": "aynı yerleşim yeri",
                }
            ),
            lx.data.Extraction(
                extraction_class="referral_rule",
                extraction_text="resmi sağlık hizmeti sunucularında uygun yoğun bakım yatağının bulunmaması halinde özel sağlık hizmeti sunucularına sevk edilebilir",
                attributes={
                    "parent_section": "1.5.1.A-2",
                    "paragraph": "1",
                    "item": "b-2",
                    "referring_level": "ikinci basamak",
                    "condition": "resmi sunucularda uygun yoğun bakım yatağı bulunmaması",
                    "target_ownership": "özel",
                    "service_type": "yoğun bakım",
                    "exception_type": "capacity_based",
                }
            ),
        ]
    ),

    # ==========================================================================
    # Example 9: Additional fee rules (ilave ücret)
    # ==========================================================================
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            1.9.1 - İlave ücret alınması
            (1) Özel sağlık hizmeti sunucuları tarafından SUT eki EK-2/B ve EK-2/C 
            listelerinde yer alan işlemler için Kurumca belirlenen bedelin iki katına 
            kadar ilave ücret alınabilir.
            (2) Otelcilik hizmetleri hariç olmak üzere, özel sağlık hizmeti sunucularında 
            acil hallerde verilen sağlık hizmetleri için ilave ücret alınamaz."""),
        extractions=[
            lx.data.Extraction(
                extraction_class="section",
                extraction_text="1.9.1 - İlave ücret alınması",
                attributes={
                    "identifier": "1.9.1",
                    "title": "İlave ücret alınması",
                    "parent_section": "1.9",
                    "topic": "additional_fee",
                }
            ),
            lx.data.Extraction(
                extraction_class="additional_fee_rule",
                extraction_text="Özel sağlık hizmeti sunucuları tarafından Kurumca belirlenen bedelin iki katına kadar ilave ücret alınabilir",
                attributes={
                    "parent_section": "1.9.1",
                    "paragraph": "1",
                    "provider_type": "özel sağlık hizmeti sunucuları",
                    "fee_limit": "2x",
                    "fee_base": "Kurumca belirlenen bedel",
                    "applicable_lists": ["EK-2/B", "EK-2/C"],
                    "rule_type": "permitted_with_limit",
                }
            ),
            lx.data.Extraction(
                extraction_class="additional_fee_rule",
                extraction_text="acil hallerde verilen sağlık hizmetleri için ilave ücret alınamaz",
                attributes={
                    "parent_section": "1.9.1",
                    "paragraph": "2",
                    "provider_type": "özel sağlık hizmeti sunucuları",
                    "condition": "acil hal",
                    "rule_type": "prohibition",
                    "exception": "otelcilik hizmetleri",
                }
            ),
        ]
    ),

    # ==========================================================================
    # Example 10: Procedure codes and specific medical procedures
    # ==========================================================================
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            2.2.1.B-1 (11) - Özel sağlık hizmet sunucularında SUT eki EK-2/B Listesindeki 
            700610 kodlu "Transözefajiyal ekokardiyografi" ve 700611 kodlu "Transözefajiyal 
            ekokardiyografi, çocuk" işlemlerinin yapılması durumunda her bir işlem için 
            muayene sayısından bir muayene sayısı düşülerek yeni günlük muayene sayısı 
            hesaplanır."""),
        extractions=[
            lx.data.Extraction(
                extraction_class="billing_rule",
                extraction_text="Transözefajiyal ekokardiyografi işlemlerinin yapılması durumunda muayene sayısından bir muayene sayısı düşülerek hesaplanır",
                attributes={
                    "parent_section": "2.2.1.B-1",
                    "paragraph": "11",
                    "rule_type": "quota_adjustment",
                    "provider_type": "özel sağlık hizmeti sunucuları",
                    "adjustment": "-1 muayene sayısı",
                    "per": "her bir işlem",
                    "affected_metric": "günlük muayene sayısı",
                }
            ),
            lx.data.Extraction(
                extraction_class="medical_procedure",
                extraction_text="Transözefajiyal ekokardiyografi",
                attributes={
                    "parent_section": "2.2.1.B-1",
                    "paragraph": "11",
                    "code": "700610",
                    "name": "Transözefajiyal ekokardiyografi",
                    "list_reference": "EK-2/B",
                    "specialty": "kardiyoloji",
                    "modality": "ekokardiyografi",
                    "approach": "transözefajiyal",
                    "patient_group": "adult",
                }
            ),
            lx.data.Extraction(
                extraction_class="medical_procedure",
                extraction_text="Transözefajiyal ekokardiyografi, çocuk",
                attributes={
                    "parent_section": "2.2.1.B-1",
                    "paragraph": "11",
                    "code": "700611",
                    "name": "Transözefajiyal ekokardiyografi, çocuk",
                    "list_reference": "EK-2/B",
                    "specialty": "pediatrik kardiyoloji",
                    "modality": "ekokardiyografi",
                    "approach": "transözefajiyal",
                    "patient_group": "pediatric",
                }
            ),
        ]
    ),

    # ==========================================================================
    # Example 11: Daily examination limits
    # ==========================================================================
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            2.2.1.B-1 (11) - Ayaktan başvurularda ikinci ve üçüncü basamak özel sağlık 
            hizmeti sunucuları için günlük muayene sınırı acil servis/polikliniğe başvurular 
            hariç olmak üzere, sağlık hizmeti sunucusundaki sözleşme kapsamında çalışan 
            hekimlerin çalışma saatlerinin 6 ile çarpılması ile bulunur. Her bir hekim için 
            günlük muayene sayısı her halükarda 60'ı geçemez. Acil servis/polikliniğine 
            başvurularda ise bir acil servis doktoru için günlük muayene sayısı 90'ı geçemez."""),
        extractions=[
            lx.data.Extraction(
                extraction_class="quota_rule",
                extraction_text="günlük muayene sınırı sözleşme kapsamında çalışan hekimlerin çalışma saatlerinin 6 ile çarpılması ile bulunur",
                attributes={
                    "parent_section": "2.2.1.B-1",
                    "paragraph": "11",
                    "rule_type": "daily_examination_limit",
                    "provider_type": "özel sağlık hizmeti sunucuları",
                    "healthcare_level": ["ikinci basamak", "üçüncü basamak"],
                    "calculation_formula": "çalışma saati × 6",
                    "exception": "acil servis/poliklinik başvuruları",
                    "care_setting": "ayaktan başvuru",
                }
            ),
            lx.data.Extraction(
                extraction_class="limit",
                extraction_text="Her bir hekim için günlük muayene sayısı her halükarda 60'ı geçemez",
                attributes={
                    "parent_section": "2.2.1.B-1",
                    "paragraph": "11",
                    "limit_type": "absolute_maximum",
                    "metric": "günlük muayene sayısı",
                    "max_value": 60,
                    "per": "hekim",
                    "context": "genel poliklinik",
                }
            ),
            lx.data.Extraction(
                extraction_class="limit",
                extraction_text="Acil servis/polikliniğine başvurularda bir acil servis doktoru için günlük muayene sayısı 90'ı geçemez",
                attributes={
                    "parent_section": "2.2.1.B-1",
                    "paragraph": "11",
                    "limit_type": "absolute_maximum",
                    "metric": "günlük muayene sayısı",
                    "max_value": 90,
                    "per": "acil servis doktoru",
                    "context": "acil servis/poliklinik",
                }
            ),
        ]
    ),

    # ==========================================================================
    # Example 12: Inpatient to outpatient transition rules
    # ==========================================================================
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            2.2.1.B-1 (4) - Hastanın aynı sağlık hizmeti sunucusunda aynı uzmanlık dalına 
            ayaktan başvurusu sonrasında aynı gün "yatarak tedavi" kapsamında, SUT eki 
            EK-2/C Listesinde yer alan bir işlem yapılması halinde bu işlem ile birlikte 
            ayaktan yapılan işlemler bu maddenin birinci fıkrasındaki hükümlere göre 
            faturalandırılır. Ancak "yatarak tedavi" kapsamında hizmet başına ödeme yöntemi 
            ile bir işlem yapılması durumunda SUT eki EK-2/A Listesinde yer alan tutarlar 
            faturalandırılmayacak olup ayaktan başvurular da hizmet başına ödeme yöntemine 
            göre faturalandırılacaktır."""),
        extractions=[
            lx.data.Extraction(
                extraction_class="billing_rule",
                extraction_text="ayaktan başvuru sonrasında aynı gün yatarak tedavi kapsamında EK-2/C işlem yapılması halinde",
                attributes={
                    "parent_section": "2.2.1.B-1",
                    "paragraph": "4",
                    "rule_type": "outpatient_to_inpatient_same_day",
                    "scenario": "EK-2/C listesi işlemi",
                    "condition": "aynı gün, aynı sağlık hizmeti sunucusu, aynı uzmanlık dalı",
                    "inpatient_billing": "EK-2/C listesi üzerinden",
                    "outpatient_billing": "birinci fıkra hükümlerine göre",
                }
            ),
            lx.data.Extraction(
                extraction_class="billing_rule",
                extraction_text="yatarak tedavi kapsamında hizmet başına ödeme yöntemi ile işlem yapılması durumunda",
                attributes={
                    "parent_section": "2.2.1.B-1",
                    "paragraph": "4",
                    "rule_type": "outpatient_to_inpatient_same_day",
                    "scenario": "hizmet başına ödeme işlemi",
                    "condition": "yatarak tedavide hizmet başına ödeme yöntemi kullanılması",
                    "non_billable": "EK-2/A Listesi tutarları",
                    "outpatient_billing": "hizmet başına ödeme yöntemi",
                    "note": "ayaktan başvurular da hizmet başına ödeme yöntemine göre faturalandırılır",
                }
            ),
        ]
    ),
]