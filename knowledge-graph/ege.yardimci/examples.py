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
            lx.data.Extraction(
                extraction_class="level-3-title",
                extraction_text="2.2.1.B - İkinci ve üçüncü basamak sağlık kurumları ",
                attributes={
                    "parent-identifier": "2.2.1",
                    "identifier": "2.2.1.B",
                    "content": "2.2.1.B - İkinci ve üçüncü basamak sağlık kurumları ",
                }
            ),
            lx.data.Extraction(
                extraction_class="level-4-title",
                extraction_text="2.2.1.B-2 - Hizmet başına ödeme yöntemi ile faturalandırılacak ayakta tedaviler",
                attributes={
                    "parent-identifier": "2.2.1.B",
                    "identifier": "2.2.1.B-2",
                    "content": "2.2.1.B-2 - Hizmet başına ödeme yöntemi ile faturalandırılacak ayakta tedaviler",
                }
            ),
            lx.data.Extraction(
                extraction_class="paragraph",
                extraction_text="(2) İkinci ve üçüncü basamak sağlık hizmeti sunucularında",
                attributes={
                    "parent-identifier": "2.2.1.B-2",
                    "identifier": "(2)",
                    "content": "(2) İkinci ve üçüncü basamak sağlık hizmeti sunucularında",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="a) Acil sağlık hizmetleri",
                attributes={
                    "parent-identifier": "2.2.1.B-2",
                    "identifier": "a)",
                    "content": "a) Acil sağlık hizmetleri",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="b) İş kazasına yönelik sağlanan sağlık hizmetleri",
                attributes={
                    "parent-identifier": "2.2.1.B-2",
                    "identifier": "b)",
                    "content": "b) İş kazasına yönelik sağlanan sağlık hizmetleri",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="c) Meslek hastalıkları hastanelerince sağlanan meslek hastalığına yönelik sağlık hizmetleri",
                attributes={
                    "parent-identifier": "2.2.1.B-2",
                    "identifier": "c)",
                    "content": "c) Meslek hastalıkları hastanelerince sağlanan meslek hastalığına yönelik sağlık hizmetleri",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="ç) MEDULA'da tedavi tipi onkolojik tedavi olarak seçilmiş hastalıklar ile ilgili tüm işlemler",
                attributes={
                    "parent-identifier": "2.2.1.B-2",
                    "identifier": "ç)",
                    "content": "ç) MEDULA'da tedavi tipi onkolojik tedavi olarak seçilmiş hastalıklar ile ilgili tüm işlemler",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="d) Organ ve doku nakline ilişkin donöre yapılan hazırlık tetkik ve tahlilleri",
                attributes={
                    "parent-identifier": "2.2.1.B-2",
                    "identifier": "d)",
                    "content": "d) Organ ve doku nakline ilişkin donöre yapılan hazırlık tetkik ve tahlilleri",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="e) Diş tedavilerine yönelik işlemler",
                attributes={
                    "parent-identifier": "2.2.1.B-2",
                    "identifier": "e)",
                    "content": "e) Diş tedavilerine yönelik işlemler",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="f) Kurum birimlerince sevk belgesi düzenlenmek suretiyle sevk edilen kişilere sunulan sağlık hizmetleri",
                attributes={
                    "parent-identifier": "2.2.1.B-2",
                    "identifier": "f)",
                    "content": "f) Kurum birimlerince sevk belgesi düzenlenmek suretiyle sevk edilen kişilere sunulan sağlık hizmetleri",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="g) Enjeksiyon/pansuman",
                attributes={
                    "parent-identifier": "2.2.1.B-2",
                    "identifier": "g)",
                    "content": "g) Enjeksiyon/pansuman",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="ğ) Alkol, madde bağımlılığı tedavisi",
                attributes={
                    "parent-identifier": "2.2.1.B-2",
                    "identifier": "ğ)",
                    "content": "ğ) Alkol, madde bağımlılığı tedavisi",
                }
            ),
            lx.data.Extraction(
                extraction_class="paragraph",
                extraction_text="Bu durumda SUT eki EK-2/A Listesinde yer alan tutarlar faturalandırılamaz",
                attributes={
                    "parent-identifier": "2.2.1.B-2",
                    "identifier": "billing_rule_1",
                    "content": "Bu durumda SUT eki EK-2/A Listesinde yer alan tutarlar faturalandırılamaz",
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
                extraction_class="level-1-title",
                extraction_text="1.4 - Sağlık hizmeti sunucuları",
                attributes={
                    "identifier": "1.4",
                    "content": "1.4 - Sağlık hizmeti sunucuları",
                }
            ),
            lx.data.Extraction(
                extraction_class="level-2-title",
                extraction_text="1.4.1- Birinci basamak sağlık hizmeti sunucuları",
                attributes={
                    "parent-identifier": "1.4",
                    "identifier": "1.4.1",
                    "content": "1.4.1- Birinci basamak sağlık hizmeti sunucuları",
                }
            ),
            lx.data.Extraction(
                extraction_class="level-3-title",
                extraction_text="1.4.1.A - Birinci basamak resmi sağlık hizmeti sunucuları",
                attributes={
                    "parent-identifier": "1.4.1",
                    "identifier": "1.4.1.A",
                    "content": "1.4.1.A - Birinci basamak resmi sağlık hizmeti sunucuları",
                }
            ),
            # Institution entries under 1.4.1.A
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="1) Toplum sağlığı merkezi (TSM)",
                attributes={
                    "parent-identifier": "1.4.1.A",
                    "identifier": "1)",
                    "content": "1) Toplum sağlığı merkezi (TSM)",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="2) Aile sağlığı merkezi (ASM)",
                attributes={
                    "parent-identifier": "1.4.1.A",
                    "identifier": "2)",
                    "content": "2) Aile sağlığı merkezi (ASM)",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="3) 112 Acil sağlık hizmeti birimleri",
                attributes={
                    "parent-identifier": "1.4.1.A",
                    "identifier": "3)",
                    "content": "3) 112 Acil sağlık hizmeti birimleri",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="4) Üniversiteler bünyesindeki mediko-sosyal birimler",
                attributes={
                    "parent-identifier": "1.4.1.A",
                    "identifier": "4)",
                    "content": "4) Üniversiteler bünyesindeki mediko-sosyal birimler",
                }
            ),
            # Sub-section for private providers
            lx.data.Extraction(
                extraction_class="level-3-title",
                extraction_text="1.4.1.B - Birinci basamak özel sağlık hizmeti sunucuları",
                attributes={
                    "parent-identifier": "1.4.1",
                    "identifier": "1.4.1.B",
                    "content": "1.4.1.B - Birinci basamak özel sağlık hizmeti sunucuları",
                }
            ),
            # Institution entries under 1.4.1.B
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="1) Evde bakım merkezleri veya birimler",
                attributes={
                    "parent-identifier": "1.4.1.B",
                    "identifier": "1)",
                    "content": "1) Evde bakım merkezleri veya birimler",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="2) Özel poliklinikler",
                attributes={
                    "parent-identifier": "1.4.1.B",
                    "identifier": "2)",
                    "content": "2) Özel poliklinikler",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="3) Ağız ve diş sağlığı hizmeti veren özel sağlık kuruluşları",
                attributes={
                    "parent-identifier": "1.4.1.B",
                    "identifier": "3)",
                    "content": "3) Ağız ve diş sağlığı hizmeti veren özel sağlık kuruluşları",
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
            (1) Birinci basamak sağlık kuruluşlarındaki ayakta tedavilerde, her başvuru için 11 (onbir) TL ödeme yapılır. Hastanın diğer bir sağlık kurumuna sevk edilmesi halinde ise sadece 5 (beş) TL ödeme yapılır."""),
        extractions=[
            # FIRST: Extract the section header
            lx.data.Extraction(
                extraction_class="level-3-title",
                extraction_text="2.2.1.A - Birinci basamak sağlık kuruluşları",
                attributes={
                    "parent-identifier": "2.2.1",
                    "identifier": "2.2.1.A",
                    "content": "2.2.1.A - Birinci basamak sağlık kuruluşları",
                }
            ),
            # Extract the scope
            lx.data.Extraction(
                extraction_class="paragraph",
                extraction_text="(1) Birinci basamak sağlık kuruluşlarındaki ayakta tedavilerde, her başvuru için 11 (onbir) TL ödeme yapılır. Hastanın diğer bir sağlık kurumuna sevk edilmesi halinde ise sadece 5 (beş) TL ödeme yapılır.",
                attributes={
                    "parent-identifier": "2.2.1.A",
                    "identifier": "(1)",
                    "content": "(1) Birinci basamak sağlık kuruluşlarındaki ayakta tedavilerde, her başvuru için 11 (onbir) TL ödeme yapılır. Hastanın diğer bir sağlık kurumuna sevk edilmesi halinde ise sadece 5 (beş) TL ödeme yapılır.",
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
                extraction_class="level-4-title",
                extraction_text="2.2.1.B-1 - Ayakta tedavilerde ödeme uygulaması",
                attributes={
                    "parent-identifier": "2.2.1.B",
                    "identifier": "2.2.1.B-1",
                    "content": "2.2.1.B-1 - Ayakta tedavilerde ödeme uygulaması",
                }
            ),
            # Extract the scope/condition
            lx.data.Extraction(
                extraction_class="paragraph",
                extraction_text="(2) Hastanın aynı sağlık hizmeti sunucusuna, acil servise başvuruları hariç olmak üzere ayaktan başvurduğu gün dâhil, 10 (on) gün içindeki aynı uzmanlık dalına diğer ayaktan başvurularında; sadece SUT eki EK-2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılabilecek olup SUT eki EK-2/A Listesinde yer alan tutar faturalandırılamaz.",
                attributes={
                    "parent-identifier": "2.2.1.B-1",
                    "identifier": "(2)",
                    "content": "Hastanın aynı sağlık hizmeti sunucusuna, acil servise başvuruları hariç olmak üzere ayaktan başvurduğu gün dâhil, 10 (on) gün içindeki aynı uzmanlık dalına diğer ayaktan başvurularında; sadece SUT eki EK-2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılabilecek olup SUT eki EK-2/A Listesinde yer alan tutar faturalandırılamaz.",
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
            (1) Ayakta tedavide hekim ve diş hekimi muayenesi için kişilerden aşağıda belirtilen tutarlarda katılım payı alınır.
            a) Birinci basamak sağlık hizmeti sunucularında: 2 (iki) TL,
            b) İkinci ve üçüncü basamak resmi sağlık hizmeti sunucularında: 6 (altı) TL,
            c) Özel sağlık hizmeti sunucularında: 15 (onbeş) TL.
            (2) Birinci basamak sağlık hizmeti sunucuları muayeneleri, kronik hastalıklar, sevkli hastalar ve acil haller hariç olmak üzere 10 gün içerisinde aynı uzmanlık dalında farklı sağlık hizmeti sunucusuna yapılan başvurularda katılım payı tutarları 5 TL artırılarak tahsil edilir."""),
        extractions=[
            # FIRST: Extract the section header
            lx.data.Extraction(
                extraction_class="level-3-title",
                extraction_text="1.8.1 - Ayakta tedavide hekim ve diş hekimi muayenesi katılım payı",
                attributes={
                    "identifier": "1.8.1",
                    "parent-identifier": "1.8",
                    "content": "Ayakta tedavide hekim ve diş hekimi muayenesi katılım payı",
                }
            ),
            # Extract the scope
            lx.data.Extraction(
                extraction_class="paragraph",
                extraction_text="(1) Ayakta tedavide hekim ve diş hekimi muayenesi için kişilerden aşağıda belirtilen tutarlarda katılım payı alınır.",
                attributes={
                    "parent-identifier": "1.8.1",
                    "identifier": "(1)",
                    "content": "Ayakta tedavide hekim ve diş hekimi muayenesi için kişilerden aşağıda belirtilen tutarlarda katılım payı alınır.",
                }
            ),
            # Co-payment rules as articles
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Birinci basamak sağlık hizmeti sunucularında: 2 (iki) TL",
                attributes={
                    "parent-identifier": "1.8.1",
                    "identifier": "a)",
                    "content": "Birinci basamak sağlık hizmeti sunucularında: 2 (iki) TL",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="İkinci ve üçüncü basamak resmi sağlık hizmeti sunucularında: 6 (altı) TL",
                attributes={
                    "parent-identifier": "1.8.1",
                    "identifier": "b)",
                    "content": "İkinci ve üçüncü basamak resmi sağlık hizmeti sunucularında: 6 (altı) TL",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Özel sağlık hizmeti sunucularında: 15 (onbeş) TL",
                attributes={
                    "parent-identifier": "1.8.1",
                    "identifier": "c)",
                    "content": "Özel sağlık hizmeti sunucularında: 15 (onbeş) TL",
                }
            ),
            # Surcharge rule
            lx.data.Extraction(
                extraction_class="paragraph",
                extraction_text="10 gün içerisinde aynı uzmanlık dalında farklı sağlık hizmeti sunucusuna yapılan başvurularda katılım payı tutarları 5 TL artırılarak tahsil edilir.",
                attributes={
                    "parent-identifier": "1.8.1",
                    "identifier": "(2)",
                    "content": "10 gün içerisinde aynı uzmanlık dalında farklı sağlık hizmeti sunucusuna yapılan başvurularda katılım payı tutarları 5 TL artırılarak tahsil edilir.",
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
                extraction_class="level-2-title",
                extraction_text="3.3.4 - Greftler",
                attributes={
                    "identifier": "3.3.4",
                    "parent-identifier": "3.3",
                    "content": "Greftler",
                }
            ),
            # Extract the scope/coverage condition
            lx.data.Extraction(
                extraction_class="paragraph",
                extraction_text="(9) Aşağıdaki deri taklitleri (yedekleri) sadece yanık tedavisinde kullanılması halinde ödenir",
                attributes={
                    "parent-identifier": "3.3.4",
                    "identifier": "(9)",
                    "content": "Aşağıdaki deri taklitleri (yedekleri) sadece yanık tedavisinde kullanılması halinde ödenir",
                }
            ),
            # Medical items as articles
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="a) Dermis iskeleti: dermisin tam kat hasar gördüğü üçüncü derece yanık bölgelerinin tedavisinde, %40'ı (0-12 yaş için %20) geçen yanıklarda sağlık kurulu raporu ile Kurumca karşılanır",
                attributes={
                    "parent-identifier": "3.3.4",
                    "identifier": "a)",
                    "content": "Dermis iskeleti: dermisin tam kat hasar gördüğü üçüncü derece yanık bölgelerinin tedavisinde, %40'ı (0-12 yaş için %20) geçen yanıklarda sağlık kurulu raporu ile Kurumca karşılanır",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="b) Deri benzerleri: en az derin ikinci derece yanıkların tedavisinde, yüz, boyun, el, ayak, perine, eklem bölgelerini içeren veya %40'ı (0-12 yaş için %20) geçen yanıklarda sağlık kurulu raporu ile Kurumca karşılanır",
                attributes={
                    "parent-identifier": "3.3.4",
                    "identifier": "b)",
                    "content": "Deri benzerleri: en az derin ikinci derece yanıkların tedavisinde, yüz, boyun, el, ayak, perine, eklem bölgelerini içeren veya %40'ı (0-12 yaş için %20) geçen yanıklarda sağlık kurulu raporu ile Kurumca karşılanır",
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
            (1) Ayaktan tedavide, bir reçeteye en fazla dört kalem ve her kalem ilaçtan bir kutunun miktarı kadar ilaç yazılabilir.
            (2) Kronik hastalıklarda üç aya kadar tedavi dozunda ilaç yazılabilir. Ancak tedaviye yeni başlanan hastalarda ilk reçete en fazla bir aylık dozda düzenlenir.
            (3) Ayakta tedavide antibiyotikler için en fazla 10 günlük doz yazılabilir."""),
        extractions=[
            # FIRST: Extract the section header
            lx.data.Extraction(
                extraction_class="level-2-title",
                extraction_text="4.1.4 - Reçetelere yazılabilecek ilaç miktarı",
                attributes={
                    "identifier": "4.1.4",
                    "parent-identifier": "4.1",
                    "content": "Reçetelere yazılabilecek ilaç miktarı",
                }
            ),
            # Prescription rules as articles
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="(1) Ayaktan tedavide, bir reçeteye en fazla dört kalem ve her kalem ilaçtan bir kutunun miktarı kadar ilaç yazılabilir.",
                attributes={
                    "parent-identifier": "4.1.4",
                    "identifier": "(1)",
                    "content": "bir reçeteye en fazla dört kalem ve her kalem ilaçtan bir kutunun miktarı kadar ilaç yazılabilir",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="(2) Kronik hastalıklarda üç aya kadar tedavi dozunda ilaç yazılabilir. Ancak tedaviye yeni başlanan hastalarda ilk reçete en fazla bir aylık dozda düzenlenir.",
                attributes={
                    "parent-identifier": "4.1.4",
                    "identifier": "(2)",
                    "content": "Kronik hastalıklarda üç aya kadar tedavi dozunda ilaç yazılabilir. Ancak tedaviye yeni başlanan hastalarda ilk reçete en fazla bir aylık dozda düzenlenir.",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="(3) Ayakta tedavide antibiyotikler için en fazla 10 günlük doz yazılabilir.",
                attributes={
                    "parent-identifier": "4.1.4",
                    "identifier": "(3)",
                    "content": "Ayakta tedavide antibiyotikler için en fazla 10 günlük doz yazılabilir.",
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
                extraction_class="level-4-title",
                extraction_text="1.5.1.A-2 - Hasta sevk işlemleri",
                attributes={
                    "identifier": "1.5.1.A-2",
                    "parent-identifier": "1.5.1.A",
                    "content": "1.5.1.A-2 - Hasta sevk işlemleri",
                }
            ),
            # Extract the general condition/scope
            lx.data.Extraction(
                extraction_class="paragraph",
                extraction_text="Tedavinin sağlanamaması halinde",
                attributes={
                    "parent-identifier": "1.5.1.A-2",
                    "identifier": "(1)",
                    "content": "Tedavinin sağlanamaması halinde",
                }
            ),
            # Referral rules as articles
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Birinci basamak sağlık hizmeti sunucularınca; sevkler aynı yerleşim yeri içindeki Sağlık Bakanlığı ikinci veya üçüncü basamak sağlık hizmeti sunucusuna yapılabilir",
                attributes={
                    "parent-identifier": "1.5.1.A-2-(1)",
                    "identifier": "a)",
                    "content": "Birinci basamak sağlık hizmeti sunucularınca; sevkler aynı yerleşim yeri içindeki Sağlık Bakanlığı ikinci veya üçüncü basamak sağlık hizmeti sunucusuna yapılabilir",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="Kişiler, aynı yerleşim yeri içindeki Sağlık Bakanlığı ikinci veya üçüncü basamak sağlık hizmeti sunucusuna sevk edilebilir",
                attributes={
                    "parent-identifier": "1.5.1.A-2-(1)",
                    "identifier": "b)-1)",
                    "content": "Kişiler, aynı yerleşim yeri içindeki Sağlık Bakanlığı ikinci veya üçüncü basamak sağlık hizmeti sunucusuna sevk edilebilir",
                }
            ),
            lx.data.Extraction(
                extraction_class="article",
                extraction_text="resmi sağlık hizmeti sunucularında uygun yoğun bakım yatağının bulunmaması halinde özel sağlık hizmeti sunucularına sevk edilebilir",
                attributes={
                    "parent-identifier": "1.5.1.A-2-(1)",
                    "identifier": "b)-2)",
                    "content": "resmi sağlık hizmeti sunucularında uygun yoğun bakım yatağının bulunmaması halinde özel sağlık hizmeti sunucularına sevk edilebilir",
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
                extraction_class="level-3-title",
                extraction_text="1.9.1 - İlave ücret alınması",
                attributes={
                    "identifier": "1.9.1",
                    "parent-identifier": "1.9",
                    "content": "1.9.1 - İlave ücret alınması",
                }
            ),
            # Extract the scope
            lx.data.Extraction(
                extraction_class="paragraph",
                extraction_text="Özel sağlık hizmeti sunucuları tarafından",
                attributes={
                    "parent-identifier": "1.9.1",
                    "identifier": "(1)",
                    "content": "Özel sağlık hizmeti sunucuları tarafından",
                }
            ),
            # Additional fee rules as articles
            lx.data.Extraction(
                extraction_class="paragraph",
                extraction_text="acil hallerde verilen sağlık hizmetleri için ilave ücret alınamaz",
                attributes={
                    "parent-identifier": "1.9.1",
                    "identifier": "(2)",
                    "content": "acil hallerde verilen sağlık hizmetleri için ilave ücret alınamaz",
                }
            ),
        ]
    ),

    # ==========================================================================
    # Example 10: Procedure codes and specific medical procedures
    # ==========================================================================
    lx.data.ExampleData(
        text=textwrap.dedent("""2.2.1.B-1 (11) - Özel sağlık hizmet sunucularında SUT eki EK-2/B Listesindeki 700610 kodlu "Transözefajiyal ekokardiyografi" ve 700611 kodlu "Transözefajiyal ekokardiyografi, çocuk" işlemlerinin yapılması durumunda her bir işlem için muayene sayısından bir muayene sayısı düşülerek yeni günlük muayene sayısı hesaplanır."""),
        extractions=[
            # Extract the scope/context
            lx.data.Extraction(
                extraction_class="paragraph",
                extraction_text="Özel sağlık hizmet sunucularında",
                attributes={
                    "parent-identifier": "2.2.1.B-1",
                    "identifier": "(11)",
                    "content": "Özel sağlık hizmet sunucularında SUT eki EK-2/B Listesindeki 700610 kodlu "Transözefajiyal ekokardiyografi" ve 700611 kodlu Transözefajiyal ekokardiyografi, çocuk işlemlerinin yapılması durumunda her bir işlem için muayene sayısından bir muayene sayısı düşülerek yeni günlük muayene sayısı hesaplanır.",
                }
            ),
        ]
    ),

    # ==========================================================================
    # Example 11: Daily examination limits
    # ==========================================================================
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            2.2.1.B-1 (11) - Ayaktan başvurularda ikinci ve üçüncü basamak özel sağlık hizmeti sunucuları için günlük muayene sınırı acil servis/polikliniğe başvurular hariç olmak üzere, sağlık hizmeti sunucusundaki sözleşme kapsamında çalışan hekimlerin çalışma saatlerinin 6 ile çarpılması ile bulunur. Her bir hekim için günlük muayene sayısı her halükarda 60'ı geçemez. Acil servis/polikliniğine başvurularda ise bir acil servis doktoru için günlük muayene sayısı 90'ı geçemez."""),
        extractions=[
            # Extract the scope
            lx.data.Extraction(
                extraction_class="paragraph",
                extraction_text="Ayaktan başvurularda ikinci ve üçüncü basamak özel sağlık hizmeti sunucuları için",
                attributes={
                    "parent-identifier": "2.2.1.B-1",
                    "identifier": "(11)",
                    "content": "Ayaktan başvurularda ikinci ve üçüncü basamak özel sağlık hizmeti sunucuları için günlük muayene sınırı acil servis/polikliniğe başvurular hariç olmak üzere, sağlık hizmeti sunucusundaki sözleşme kapsamında çalışan hekimlerin çalışma saatlerinin 6 ile çarpılması ile bulunur. Her bir hekim için günlük muayene sayısı her halükarda 60'ı geçemez. Acil servis/polikliniğine başvurularda ise bir acil servis doktoru için günlük muayene sayısı 90'ı geçemez.",
                }
            ),
        ]
    ),
]