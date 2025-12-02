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
            2.2.1.B - İkinci ve üçüncü basamak sağlık kurumları 
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
                extraction_class="subsubsection-title",
                extraction_text="2.2.1.B - İkinci ve üçüncü basamak sağlık kurumları ",
                attributes={
                    "identifier": "2.2.1.B",
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "title": "Hizmet başına ödeme yöntemi ile faturalandırılacak ayakta tedaviler",
                    "payment_method": "hizmet başına ödeme yöntemi",
                    "care_setting": "ayakta tedavi",
                }
            ),
            lx.data.Extraction(
                extraction_class="leafsection-title",
                extraction_text="2.2.1.B-2 - Hizmet başına ödeme yöntemi ile faturalandırılacak ayakta tedaviler",
                attributes={
                    "identifier": "2.2.1.B-2",
                    "title": "Hizmet başına ödeme yöntemi ile faturalandırılacak ayakta tedaviler",
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "2",
                    "payment_method": "hizmet başına ödeme yöntemi",
                    "care_setting": "ayakta tedavi",
                }
            ),
            # Extract the scope/applicability
            lx.data.Extraction(
                extraction_class="scope",
                extraction_text="İkinci ve üçüncü basamak sağlık hizmeti sunucularında",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "2",
                    "paragraph": "2",
                    "scopes": ["ikinci basamak", "üçüncü basamak"],
                    "provider_type": "sağlık hizmeti sunucuları",
                }
            ),
            # THEN: Each service with parent_section link
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Acil sağlık hizmetleri",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "2",
                    "paragraph": "2",
                    "type" : "medical_service",
                    "content": "Acil sağlık hizmetleri",
                    "service_type": "emergency_services",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="İş kazasına yönelik sağlanan sağlık hizmetleri",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "2",
                    "paragraph": "2",
                    "content": "İş kazasına yönelik sağlanan sağlık hizmetleri",
                    "service_type": "occupational_accident",
                    "type": "medical_service",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Meslek hastalıkları hastanelerince sağlanan meslek hastalığına yönelik sağlık hizmetleri",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "2",
                    "paragraph": "2",
                    "content": "Meslek hastalıkları hastanelerince sağlanan meslek hastalığına yönelik sağlık hizmetleri",
                    "service_type": "occupational_disease",
                    "provider_restriction": "meslek hastalıkları hastaneleri",
                    "type": "medical_service",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="MEDULA'da tedavi tipi onkolojik tedavi olarak seçilmiş hastalıklar ile ilgili tüm işlemler",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "2",
                    "paragraph": "2",
                    "content": "MEDULA'da tedavi tipi onkolojik tedavi olarak seçilmiş hastalıklar ile ilgili tüm işlemler",
                    "service_type": "oncology",
                    "type": "medical_service",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Organ ve doku nakline ilişkin donöre yapılan hazırlık tetkik ve tahlilleri",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "2",
                    "paragraph": "2",
                    "content": "Organ ve doku nakline ilişkin donöre yapılan hazırlık tetkik ve tahlilleri",
                    "service_type": "transplant_donor_preparation",
                    "type": "medical_service",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Diş tedavilerine yönelik işlemler",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "2",
                    "paragraph": "2",
                    "content": "Diş tedavilerine yönelik işlemler",
                    "service_type": "dental",
                    "type": "medical_service",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Kurum birimlerince sevk belgesi düzenlenmek suretiyle sevk edilen kişilere sunulan sağlık hizmetleri",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "2",
                    "paragraph": "2",
                    "content": "Kurum birimlerince sevk belgesi düzenlenmek suretiyle sevk edilen kişilere sunulan sağlık hizmetleri",
                    "service_type": "referred_services",
                    "type": "medical_service",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Enjeksiyon/pansuman",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "2",
                    "paragraph": "2",
                    "content": "Enjeksiyon/pansuman",
                    "service_type": "injection_dressing",
                    "type": "medical_service",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Alkol, madde bağımlılığı tedavisi",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "2",
                    "content": "Alkol ve madde bağımlılığı tedavisi",
                    "service_type": "addiction_treatment",
                    "type": "medical_service",
                }
            ),
            # Extract the billing prohibition rule
            lx.data.Extraction(
                extraction_class="billing_exception",
                extraction_text="Bu durumda SUT eki EK-2/A Listesinde yer alan tutarlar faturalandırılamaz",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "2",
                    "rule_type": "prohibition",
                    "content": "Bu durumda SUT eki EK-2/A Listesinde yer alan tutarlar faturalandırılamaz",
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
            # FIRST: Extract the section headers
            lx.data.Extraction(
                extraction_class="section-title",
                extraction_text="1.4 - Sağlık hizmeti sunucuları",
                attributes={
                    "identifier": "1.4",
                    "main_section": "1.4",
                    "title": "Sağlık hizmeti sunucuları",
                }
            ),
            lx.data.Extraction(
                extraction_class="subsection-title",
                extraction_text="1.4.1- Birinci basamak sağlık hizmeti sunucuları",
                attributes={
                    "identifier": "1.4.1",
                    "main_section": "1.4",
                    "subsection": "1",
                    "title": "Birinci basamak sağlık hizmeti sunucuları",
                    "healthcare_level": "birinci basamak",
                }
            ),
            lx.data.Extraction(
                extraction_class="subsubsection-title",
                extraction_text="1.4.1.A - Birinci basamak resmi sağlık hizmeti sunucuları",
                attributes={
                    "identifier": "1.4.1.A",
                    "main_section": "1.4",
                    "subsection": "1",
                    "subsubsection": "A",
                    "title": "Birinci basamak resmi sağlık hizmeti sunucuları",
                    "healthcare_level": "birinci basamak",
                    "ownership": "resmi",
                }
            ),
            # Institution entries under 1.4.1.A
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Toplum sağlığı merkezi (TSM)",
                attributes={
                    "main_section": "1.4",
                    "subsection": "1",
                    "subsubsection": "A",
                    "item": "1",
                    "type": "institution",
                    "content": "Toplum sağlığı merkezi (TSM)",
                    "abbreviation": "TSM",
                    "healthcare_level": "birinci basamak",
                    "ownership": "resmi",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Aile sağlığı merkezi (ASM)",
                attributes={
                    "main_section": "1.4",
                    "subsection": "1",
                    "subsubsection": "A",
                    "item": "2",
                    "type": "institution",
                    "content": "Aile sağlığı merkezi (ASM)",
                    "abbreviation": "ASM",
                    "healthcare_level": "birinci basamak",
                    "ownership": "resmi",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="112 Acil sağlık hizmeti birimleri",
                attributes={
                    "main_section": "1.4",
                    "subsection": "1",
                    "subsubsection": "A",
                    "item": "3",
                    "type": "institution",
                    "content": "112 Acil sağlık hizmeti birimleri",
                    "service_type": "emergency",
                    "healthcare_level": "birinci basamak",
                    "ownership": "resmi",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Üniversiteler bünyesindeki mediko-sosyal birimler",
                attributes={
                    "main_section": "1.4",
                    "subsection": "1",
                    "subsubsection": "A",
                    "item": "4",
                    "type": "institution",
                    "content": "Üniversiteler bünyesindeki mediko-sosyal birimler",
                    "affiliation": "üniversiteler",
                    "healthcare_level": "birinci basamak",
                    "ownership": "resmi",
                }
            ),
            # Sub-section for private providers
            lx.data.Extraction(
                extraction_class="subsubsection-title",
                extraction_text="1.4.1.B - Birinci basamak özel sağlık hizmeti sunucuları",
                attributes={
                    "identifier": "1.4.1.B",
                    "main_section": "1.4",
                    "subsection": "1",
                    "subsubsection": "B",
                    "title": "Birinci basamak özel sağlık hizmeti sunucuları",
                    "healthcare_level": "birinci basamak",
                    "ownership": "özel",
                }
            ),
            # Institution entries under 1.4.1.B
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Evde bakım merkezleri veya birimler",
                attributes={
                    "main_section": "1.4",
                    "subsection": "1",
                    "subsubsection": "B",
                    "item": "1",
                    "type": "institution",
                    "content": "Evde bakım merkezleri veya birimler",
                    "service_type": "home_care",
                    "healthcare_level": "birinci basamak",
                    "ownership": "özel",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Özel poliklinikler",
                attributes={
                    "main_section": "1.4",
                    "subsection": "1",
                    "subsubsection": "B",
                    "item": "2",
                    "type": "institution",
                    "content": "Özel poliklinikler",
                    "healthcare_level": "birinci basamak",
                    "ownership": "özel",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Ağız ve diş sağlığı hizmeti veren özel sağlık kuruluşları",
                attributes={
                    "main_section": "1.4",
                    "subsection": "1",
                    "subsubsection": "B",
                    "item": "3",
                    "type": "institution",
                    "content": "Ağız ve diş sağlığı hizmeti veren özel sağlık kuruluşları",
                    "service_type": "dental",
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
            # FIRST: Extract the section header
            lx.data.Extraction(
                extraction_class="subsubsection-title",
                extraction_text="2.2.1.A - Birinci basamak sağlık kuruluşları",
                attributes={
                    "identifier": "2.2.1.A",
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "A",
                    "title": "Birinci basamak sağlık kuruluşları",
                    "healthcare_level": "birinci basamak",
                    "care_setting": "ayakta tedavi",
                }
            ),
            # Extract the scope
            lx.data.Extraction(
                extraction_class="scope",
                extraction_text="Birinci basamak sağlık kuruluşlarındaki ayakta tedavilerde",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "A",
                    "paragraph": "1",
                    "scopes": ["birinci basamak"],
                    "care_setting": "ayakta tedavi",
                }
            ),
            # Payment rules as articles
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="her başvuru için 11 (onbir) TL ödeme yapılır",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "A",
                    "paragraph": "1",
                    "type": "payment_rule",
                    "content": "her başvuru için 11 (onbir) TL ödeme yapılır",
                    "payment_type": "per_visit",
                    "amount": 11,
                    "currency": "TL",
                    "condition": "standart başvuru",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Hastanın diğer bir sağlık kurumuna sevk edilmesi halinde ise sadece 5 (beş) TL ödeme yapılır",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "A",
                    "paragraph": "1",
                    "type": "payment_rule",
                    "content": "Hastanın diğer bir sağlık kurumuna sevk edilmesi halinde ise sadece 5 (beş) TL ödeme yapılır",
                    "payment_type": "per_referral",
                    "amount": 5,
                    "currency": "TL",
                    "condition": "hastanın sevk edilmesi",
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
            # FIRST: Extract the section header
            lx.data.Extraction(
                extraction_class="leafsection-title",
                extraction_text="2.2.1.B-1 - Ayakta tedavilerde ödeme uygulaması",
                attributes={
                    "identifier": "2.2.1.B-1",
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "1",
                    "title": "Ayakta tedavilerde ödeme uygulaması",
                    "care_setting": "ayakta tedavi",
                }
            ),
            # Extract the scope/condition
            lx.data.Extraction(
                extraction_class="scope",
                extraction_text="Hastanın aynı sağlık hizmeti sunucusuna, acil servise başvuruları hariç olmak üzere ayaktan başvurduğu gün dâhil, 10 (on) gün içindeki aynı uzmanlık dalına diğer ayaktan başvurularında",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "1",
                    "paragraph": "2",
                    "time_window": "10 gün",
                    "time_window_start": "ayaktan başvurulan gün dahil",
                    "scope_detail": "aynı uzmanlık dalı",
                    "provider_scope": "aynı sağlık hizmeti sunucusu",
                    "exception": "acil servis başvuruları",
                }
            ),
            # Billing rules as articles
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="SUT eki EK-2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılabilecek",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "1",
                    "paragraph": "2",
                    "type": "billing_rule",
                    "content": "SUT eki EK-2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılabilecek",
                    "list_reference": "EK-2/A-2",
                    "billing_status": "billable",
                    "condition": "10 gün içinde tekrar başvuru",
                }
            ),
            lx.data.Extraction(
                extraction_class="billing_exception",
                extraction_text="SUT eki EK-2/A Listesinde yer alan tutar faturalandırılamaz",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "1",
                    "paragraph": "2",
                    "rule_type": "prohibition",
                    "content": "SUT eki EK-2/A Listesinde yer alan tutar faturalandırılamaz",
                    "list_reference": "EK-2/A",
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
            # FIRST: Extract the section header
            lx.data.Extraction(
                extraction_class="subsection-title",
                extraction_text="1.8.1 - Ayakta tedavide hekim ve diş hekimi muayenesi katılım payı",
                attributes={
                    "identifier": "1.8.1",
                    "main_section": "1.8",
                    "subsection": "1",
                    "title": "Ayakta tedavide hekim ve diş hekimi muayenesi katılım payı",
                    "care_setting": "ayakta tedavi",
                    "topic": "co_payment",
                }
            ),
            # Extract the scope
            lx.data.Extraction(
                extraction_class="scope",
                extraction_text="Ayakta tedavide hekim ve diş hekimi muayenesi için kişilerden",
                attributes={
                    "main_section": "1.8",
                    "subsection": "1",
                    "paragraph": "1",
                    "care_setting": "ayakta tedavi",
                    "service_type": "hekim ve diş hekimi muayenesi",
                }
            ),
            # Co-payment rules as articles
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Birinci basamak sağlık hizmeti sunucularında: 2 (iki) TL",
                attributes={
                    "main_section": "1.8",
                    "subsection": "1",
                    "paragraph": "1",
                    "item": "a",
                    "type": "co_payment_rule",
                    "content": "Birinci basamak sağlık hizmeti sunucularında: 2 (iki) TL",
                    "healthcare_level": "birinci basamak",
                    "amount": 2,
                    "currency": "TL",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="İkinci ve üçüncü basamak resmi sağlık hizmeti sunucularında: 6 (altı) TL",
                attributes={
                    "main_section": "1.8",
                    "subsection": "1",
                    "paragraph": "1",
                    "item": "b",
                    "type": "co_payment_rule",
                    "content": "İkinci ve üçüncü basamak resmi sağlık hizmeti sunucularında: 6 (altı) TL",
                    "healthcare_level": ["ikinci basamak", "üçüncü basamak"],
                    "ownership": "resmi",
                    "amount": 6,
                    "currency": "TL",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Özel sağlık hizmeti sunucularında: 15 (onbeş) TL",
                attributes={
                    "main_section": "1.8",
                    "subsection": "1",
                    "paragraph": "1",
                    "item": "c",
                    "type": "co_payment_rule",
                    "content": "Özel sağlık hizmeti sunucularında: 15 (onbeş) TL",
                    "ownership": "özel",
                    "amount": 15,
                    "currency": "TL",
                }
            ),
            # Surcharge rule
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="10 gün içerisinde aynı uzmanlık dalında farklı sağlık hizmeti sunucusuna yapılan başvurularda katılım payı tutarları 5 TL artırılarak tahsil edilir",
                attributes={
                    "main_section": "1.8",
                    "subsection": "1",
                    "paragraph": "2",
                    "type": "co_payment_surcharge",
                    "content": "10 gün içerisinde aynı uzmanlık dalında farklı sağlık hizmeti sunucusuna yapılan başvurularda katılım payı tutarları 5 TL artırılarak tahsil edilir",
                    "surcharge_amount": 5,
                    "currency": "TL",
                    "time_window": "10 gün",
                    "scope_detail": "aynı uzmanlık dalı",
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
            # FIRST: Extract the section header
            lx.data.Extraction(
                extraction_class="subsection-title",
                extraction_text="3.3.4 - Greftler",
                attributes={
                    "identifier": "3.3.4",
                    "main_section": "3.3",
                    "subsection": "4",
                    "title": "Greftler",
                    "category": "tıbbi malzeme",
                }
            ),
            # Extract the scope/coverage condition
            lx.data.Extraction(
                extraction_class="scope",
                extraction_text="Aşağıdaki deri taklitleri (yedekleri) sadece yanık tedavisinde kullanılması halinde ödenir",
                attributes={
                    "main_section": "3.3",
                    "subsection": "4",
                    "paragraph": "9",
                    "item_category": "deri taklitleri (yedekleri)",
                    "usage_condition": "yanık tedavisi",
                    "coverage_status": "conditional",
                }
            ),
            # Medical items as articles
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Dermis iskeleti: dermisin tam kat hasar gördüğü üçüncü derece yanık bölgelerinin tedavisinde, %40'ı (0-12 yaş için %20) geçen yanıklarda sağlık kurulu raporu ile Kurumca karşılanır",
                attributes={
                    "main_section": "3.3",
                    "subsection": "4",
                    "paragraph": "9",
                    "item": "a",
                    "type": "medical_item",
                    "content": "Dermis iskeleti",
                    "indication": "üçüncü derece yanık",
                    "indication_detail": "dermisin tam kat hasar gördüğü bölge",
                    "threshold_adult": ">%40 vücut yüzeyi",
                    "threshold_pediatric": ">%20 vücut yüzeyi",
                    "pediatric_age_range": "0-12 yaş",
                    "document_requirement": "sağlık kurulu raporu",
                    "payer": "Kurum",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Deri benzerleri: en az derin ikinci derece yanıkların tedavisinde, yüz, boyun, el, ayak, perine, eklem bölgelerini içeren veya %40'ı (0-12 yaş için %20) geçen yanıklarda sağlık kurulu raporu ile Kurumca karşılanır",
                attributes={
                    "main_section": "3.3",
                    "subsection": "4",
                    "paragraph": "9",
                    "item": "b",
                    "type": "medical_item",
                    "content": "Deri benzerleri",
                    "indication": "en az derin ikinci derece yanık",
                    "body_areas": ["yüz", "boyun", "el", "ayak", "perine", "eklem"],
                    "threshold_adult": ">%40 vücut yüzeyi",
                    "threshold_pediatric": ">%20 vücut yüzeyi",
                    "pediatric_age_range": "0-12 yaş",
                    "document_requirement": "sağlık kurulu raporu",
                    "payer": "Kurum",
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
            # FIRST: Extract the section header
            lx.data.Extraction(
                extraction_class="subsection-title",
                extraction_text="4.1.4 - Reçetelere yazılabilecek ilaç miktarı",
                attributes={
                    "identifier": "4.1.4",
                    "main_section": "4.1",
                    "subsection": "4",
                    "title": "Reçetelere yazılabilecek ilaç miktarı",
                    "topic": "prescription_limits",
                }
            ),
            # Prescription rules as articles
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="bir reçeteye en fazla dört kalem ve her kalem ilaçtan bir kutunun miktarı kadar ilaç yazılabilir",
                attributes={
                    "main_section": "4.1",
                    "subsection": "4",
                    "paragraph": "1",
                    "type": "prescription_rule",
                    "content": "bir reçeteye en fazla dört kalem ve her kalem ilaçtan bir kutunun miktarı kadar ilaç yazılabilir",
                    "care_setting": "ayaktan tedavi",
                    "max_items_per_prescription": 4,
                    "max_quantity_per_item": "1 kutu",
                    "rule_type": "quantity_limit",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Kronik hastalıklarda üç aya kadar tedavi dozunda ilaç yazılabilir",
                attributes={
                    "main_section": "4.1",
                    "subsection": "4",
                    "paragraph": "2",
                    "type": "prescription_rule",
                    "content": "Kronik hastalıklarda üç aya kadar tedavi dozunda ilaç yazılabilir",
                    "condition": "kronik hastalık",
                    "max_duration": "3 ay",
                    "max_duration_days": 90,
                    "rule_type": "duration_limit",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="tedaviye yeni başlanan hastalarda ilk reçete en fazla bir aylık dozda düzenlenir",
                attributes={
                    "main_section": "4.1",
                    "subsection": "4",
                    "paragraph": "2",
                    "type": "prescription_rule",
                    "content": "tedaviye yeni başlanan hastalarda ilk reçete en fazla bir aylık dozda düzenlenir",
                    "condition": "tedaviye yeni başlama",
                    "max_duration": "1 ay",
                    "max_duration_days": 30,
                    "applies_to": "ilk reçete",
                    "rule_type": "duration_limit",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="antibiyotikler için en fazla 10 günlük doz yazılabilir",
                attributes={
                    "main_section": "4.1",
                    "subsection": "4",
                    "paragraph": "3",
                    "type": "prescription_rule",
                    "content": "antibiyotikler için en fazla 10 günlük doz yazılabilir",
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
            # FIRST: Extract the section header
            lx.data.Extraction(
                extraction_class="leafsection-title",
                extraction_text="1.5.1.A-2 - Hasta sevk işlemleri",
                attributes={
                    "identifier": "1.5.1.A-2",
                    "main_section": "1.5",
                    "subsection": "1",
                    "subsubsection": "A",
                    "leafsection": "2",
                    "title": "Hasta sevk işlemleri",
                    "topic": "patient_referral",
                }
            ),
            # Extract the general condition/scope
            lx.data.Extraction(
                extraction_class="scope",
                extraction_text="Tedavinin sağlanamaması halinde",
                attributes={
                    "main_section": "1.5",
                    "subsection": "1",
                    "subsubsection": "A",
                    "leafsection": "2",
                    "paragraph": "1",
                    "condition": "tedavinin sağlanamaması",
                }
            ),
            # Referral rules as articles
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Birinci basamak sağlık hizmeti sunucularınca; sevkler aynı yerleşim yeri içindeki Sağlık Bakanlığı ikinci veya üçüncü basamak sağlık hizmeti sunucusuna yapılabilir",
                attributes={
                    "main_section": "1.5",
                    "subsection": "1",
                    "subsubsection": "A",
                    "leafsection": "2",
                    "paragraph": "1",
                    "item": "a",
                    "type": "referral_rule",
                    "content": "Birinci basamak sağlık hizmeti sunucularınca; sevkler aynı yerleşim yeri içindeki Sağlık Bakanlığı ikinci veya üçüncü basamak sağlık hizmeti sunucusuna yapılabilir",
                    "referring_level": "birinci basamak",
                    "target_levels": ["ikinci basamak", "üçüncü basamak"],
                    "target_authority": "Sağlık Bakanlığı",
                    "geographic_scope": "aynı yerleşim yeri",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Kişiler, aynı yerleşim yeri içindeki Sağlık Bakanlığı ikinci veya üçüncü basamak sağlık hizmeti sunucusuna sevk edilebilir",
                attributes={
                    "main_section": "1.5",
                    "subsection": "1",
                    "subsubsection": "A",
                    "leafsection": "2",
                    "paragraph": "1",
                    "item": "b-1",
                    "type": "referral_rule",
                    "content": "Kişiler, aynı yerleşim yeri içindeki Sağlık Bakanlığı ikinci veya üçüncü basamak sağlık hizmeti sunucusuna sevk edilebilir",
                    "referring_level": "ikinci basamak",
                    "target_levels": ["ikinci basamak", "üçüncü basamak"],
                    "target_authority": "Sağlık Bakanlığı",
                    "geographic_scope": "aynı yerleşim yeri",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="resmi sağlık hizmeti sunucularında uygun yoğun bakım yatağının bulunmaması halinde özel sağlık hizmeti sunucularına sevk edilebilir",
                attributes={
                    "main_section": "1.5",
                    "subsection": "1",
                    "subsubsection": "A",
                    "leafsection": "2",
                    "paragraph": "1",
                    "item": "b-2",
                    "type": "referral_rule",
                    "content": "resmi sağlık hizmeti sunucularında uygun yoğun bakım yatağının bulunmaması halinde özel sağlık hizmeti sunucularına sevk edilebilir",
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
            # FIRST: Extract the section header
            lx.data.Extraction(
                extraction_class="subsection-title",
                extraction_text="1.9.1 - İlave ücret alınması",
                attributes={
                    "identifier": "1.9.1",
                    "main_section": "1.9",
                    "subsection": "1",
                    "title": "İlave ücret alınması",
                    "topic": "additional_fee",
                }
            ),
            # Extract the scope
            lx.data.Extraction(
                extraction_class="scope",
                extraction_text="Özel sağlık hizmeti sunucuları tarafından",
                attributes={
                    "main_section": "1.9",
                    "subsection": "1",
                    "paragraph": "1",
                    "provider_type": "özel sağlık hizmeti sunucuları",
                }
            ),
            # Additional fee rules as articles
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="SUT eki EK-2/B ve EK-2/C listelerinde yer alan işlemler için Kurumca belirlenen bedelin iki katına kadar ilave ücret alınabilir",
                attributes={
                    "main_section": "1.9",
                    "subsection": "1",
                    "paragraph": "1",
                    "type": "additional_fee_rule",
                    "content": "SUT eki EK-2/B ve EK-2/C listelerinde yer alan işlemler için Kurumca belirlenen bedelin iki katına kadar ilave ücret alınabilir",
                    "fee_limit": "2x",
                    "fee_base": "Kurumca belirlenen bedel",
                    "applicable_lists": ["EK-2/B", "EK-2/C"],
                    "rule_type": "permitted_with_limit",
                }
            ),
            lx.data.Extraction(
                extraction_class="billing_exception",
                extraction_text="acil hallerde verilen sağlık hizmetleri için ilave ücret alınamaz",
                attributes={
                    "main_section": "1.9",
                    "subsection": "1",
                    "paragraph": "2",
                    "rule_type": "prohibition",
                    "content": "acil hallerde verilen sağlık hizmetleri için ilave ücret alınamaz",
                    "condition": "acil hal",
                    "exception": "otelcilik hizmetleri",
                    "provider_type": "özel sağlık hizmeti sunucuları",
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
            # Extract the scope/context
            lx.data.Extraction(
                extraction_class="scope",
                extraction_text="Özel sağlık hizmet sunucularında",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "1",
                    "paragraph": "11",
                    "provider_type": "özel sağlık hizmeti sunucuları",
                }
            ),
            # Billing rule as article
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="her bir işlem için muayene sayısından bir muayene sayısı düşülerek yeni günlük muayene sayısı hesaplanır",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "1",
                    "paragraph": "11",
                    "type": "billing_rule",
                    "content": "her bir işlem için muayene sayısından bir muayene sayısı düşülerek yeni günlük muayene sayısı hesaplanır",
                    "rule_type": "quota_adjustment",
                    "adjustment": "-1 muayene sayısı",
                    "per": "her bir işlem",
                    "affected_metric": "günlük muayene sayısı",
                }
            ),
            # Medical procedures as articles
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="700610 kodlu Transözefajiyal ekokardiyografi",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "1",
                    "paragraph": "11",
                    "type": "medical_procedure",
                    "content": "Transözefajiyal ekokardiyografi",
                    "code": "700610",
                    "list_reference": "EK-2/B",
                    "specialty": "kardiyoloji",
                    "modality": "ekokardiyografi",
                    "approach": "transözefajiyal",
                    "patient_group": "adult",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="700611 kodlu Transözefajiyal ekokardiyografi, çocuk",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "1",
                    "paragraph": "11",
                    "type": "medical_procedure",
                    "content": "Transözefajiyal ekokardiyografi, çocuk",
                    "code": "700611",
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
            # Extract the scope
            lx.data.Extraction(
                extraction_class="scope",
                extraction_text="Ayaktan başvurularda ikinci ve üçüncü basamak özel sağlık hizmeti sunucuları için",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "1",
                    "paragraph": "11",
                    "scopes": ["ikinci basamak", "üçüncü basamak"],
                    "provider_type": "özel sağlık hizmeti sunucuları",
                    "care_setting": "ayaktan başvuru",
                }
            ),
            # Quota/limit rules as articles
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="günlük muayene sınırı sözleşme kapsamında çalışan hekimlerin çalışma saatlerinin 6 ile çarpılması ile bulunur",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "1",
                    "paragraph": "11",
                    "type": "quota_rule",
                    "content": "günlük muayene sınırı sözleşme kapsamında çalışan hekimlerin çalışma saatlerinin 6 ile çarpılması ile bulunur",
                    "calculation_formula": "çalışma saati × 6",
                    "exception": "acil servis/poliklinik başvuruları",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Her bir hekim için günlük muayene sayısı her halükarda 60'ı geçemez",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "1",
                    "paragraph": "11",
                    "type": "limit",
                    "content": "Her bir hekim için günlük muayene sayısı her halükarda 60'ı geçemez",
                    "limit_type": "absolute_maximum",
                    "metric": "günlük muayene sayısı",
                    "max_value": 60,
                    "per": "hekim",
                    "context": "genel poliklinik",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Acil servis/polikliniğine başvurularda bir acil servis doktoru için günlük muayene sayısı 90'ı geçemez",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "1",
                    "paragraph": "11",
                    "type": "limit",
                    "content": "Acil servis/polikliniğine başvurularda bir acil servis doktoru için günlük muayene sayısı 90'ı geçemez",
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
            # Extract the scope/context
            lx.data.Extraction(
                extraction_class="scope",
                extraction_text="Hastanın aynı sağlık hizmeti sunucusunda aynı uzmanlık dalına ayaktan başvurusu sonrasında aynı gün yatarak tedavi kapsamında",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "1",
                    "paragraph": "4",
                    "provider_scope": "aynı sağlık hizmeti sunucusu",
                    "specialty_scope": "aynı uzmanlık dalı",
                    "time_scope": "aynı gün",
                    "transition": "ayaktan başvuru → yatarak tedavi",
                }
            ),
            # Billing rules as articles
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="SUT eki EK-2/C Listesinde yer alan bir işlem yapılması halinde bu işlem ile birlikte ayaktan yapılan işlemler bu maddenin birinci fıkrasındaki hükümlere göre faturalandırılır",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "1",
                    "paragraph": "4",
                    "type": "billing_rule",
                    "content": "SUT eki EK-2/C Listesinde yer alan bir işlem yapılması halinde bu işlem ile birlikte ayaktan yapılan işlemler bu maddenin birinci fıkrasındaki hükümlere göre faturalandırılır",
                    "scenario": "EK-2/C listesi işlemi",
                    "inpatient_billing": "EK-2/C listesi üzerinden",
                    "outpatient_billing": "birinci fıkra hükümlerine göre",
                    "list_reference": "EK-2/C",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="yatarak tedavi kapsamında hizmet başına ödeme yöntemi ile bir işlem yapılması durumunda ayaktan başvurular da hizmet başına ödeme yöntemine göre faturalandırılacaktır",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "1",
                    "paragraph": "4",
                    "type": "billing_rule",
                    "content": "yatarak tedavi kapsamında hizmet başına ödeme yöntemi ile bir işlem yapılması durumunda ayaktan başvurular da hizmet başına ödeme yöntemine göre faturalandırılacaktır",
                    "scenario": "hizmet başına ödeme işlemi",
                    "condition": "yatarak tedavide hizmet başına ödeme yöntemi kullanılması",
                    "outpatient_billing": "hizmet başına ödeme yöntemi",
                    "payment_method": "hizmet başına ödeme",
                }
            ),
            lx.data.Extraction(
                extraction_class="billing_exception",
                extraction_text="SUT eki EK-2/A Listesinde yer alan tutarlar faturalandırılmayacak",
                attributes={
                    "main_section": "2.2",
                    "subsection": "1",
                    "subsubsection": "B",
                    "leafsection": "1",
                    "paragraph": "4",
                    "rule_type": "prohibition",
                    "content": "SUT eki EK-2/A Listesinde yer alan tutarlar faturalandırılmayacak",
                    "list_reference": "EK-2/A",
                    "condition": "yatarak tedavide hizmet başına ödeme yöntemi kullanılması",
                }
            ),
        ]
    ),
]