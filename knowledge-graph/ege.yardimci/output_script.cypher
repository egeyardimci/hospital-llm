// --- BASE SETUP ---
MERGE (p1_base:ProviderType {level: 'birinci basamak'});
MERGE (p2_base:ProviderType {level: 'ikinci basamak'});
MERGE (p3_base:ProviderType {level: 'üçüncü basamak'});

MERGE (n_e3fe9d56127aebd1b57dd4d888f54614:Rule:BillingRule {uid: 'e3fe9d56127aebd1b57dd4d888f54614'})
SET n_e3fe9d56127aebd1b57dd4d888f54614 += {uid: 'e3fe9d56127aebd1b57dd4d888f54614', text: 'tem belgesine dayanılarak kişilere ödenir ve sevk/istem belgesini düzenleyen sözleşmeli sağlık hizmeti sunucusunun alacağından mahsup edilir. Sağlık Bakanlığına bağlı sağlık hizmeti sunucuları için Bakanlığa yapılan global bütçe ödemesinden mahsup edilir', paragraph: '9', rule_type: 'payment_offset', condition: 'sevk/istem belgesine dayanılarak kişilere ödeme yapıldığında', billable_items: 'kişilere yapılan ödemeler', offset_from: 'sevk/istem belgesini düzenleyen sözleşmeli sağlık hizmeti sunucusunun alacağı,Sağlık Bakanlığına bağlı sağlık hizmeti sunucuları için global bütçe ödemesi'}
;

MERGE (n_7ee2748019c13f45c0dccf68abc7c7d5:Rule:BillingRule {uid: '7ee2748019c13f45c0dccf68abc7c7d5'})
SET n_7ee2748019c13f45c0dccf68abc7c7d5 += {uid: '7ee2748019c13f45c0dccf68abc7c7d5', text: 'Kurumla sözleşmeli sağlık hizmeti sunucuları, bir başka sağlık hizmeti sunucusundan hizmet alımı yoluyla sağladıkları ... tetkik ve/veya tahlil dışındaki tedavilere ait giderleri Kuruma faturalandıramazlar', paragraph: '10', rule_type: 'prohibition', condition: 'hizmet alımı yoluyla başka sağlık hizmeti sunucusundan sağlanan, ruhsat/faaliyet/uygunluk belgesinde yer alan tetkik ve/veya tahlil dışındaki tedaviler', non_billable_items: 'tetkik ve/veya tahlil dışındaki tedavi giderleri (gastroskopi, kolonoskopi, rektosigmoidoskopi, rektoskopi, bronkoskopi, anjiyografi gibi işlemler dahil)', exception: 'hekim veya diş hekimlerinin özel sağlık hizmeti sunucusu bünyesinde çalışması halinde bu hekimler tarafından fatura düzenlenerek alınan/sunulan sağlık hizmetleri'}
;

MERGE (n_d84536d357939297c1f28b0b5e5741e2:Rule:BillingRule {uid: 'd84536d357939297c1f28b0b5e5741e2'})
SET n_d84536d357939297c1f28b0b5e5741e2 += {uid: 'd84536d357939297c1f28b0b5e5741e2', text: 'Başka bir sağlık hizmeti sunucusundan laboratuvar hizmeti alınması durumunda, hasta hastane dışına numune almak için gönderilmez, alınan numunenin transferi veya sonucu hasta veya yakını aracılığı ile istenilemez', paragraph: '11', rule_type: 'prohibition', condition: 'başka bir sağlık hizmeti sunucusundan laboratuvar hizmeti alınması', billable_items: 'laboratuvar hizmeti', provider_obligation: 'hasta hastane dışına numune almak için gönderilmez; numune transferi veya sonucu hasta/yakını aracılığı ile istenilemez'}
;

MERGE (n_b6a65b119357532fb258791ce742de5a:Rule:CoverageRule {uid: 'b6a65b119357532fb258791ce742de5a'})
SET n_b6a65b119357532fb258791ce742de5a += {uid: 'b6a65b119357532fb258791ce742de5a', text: 'Görüntüleme hizmetlerinin hizmet alımı yoluyla sağlanması halinde acil ve yatan hastaların transferi sağlık hizmeti sunucuları tarafından yapılacaktır', paragraph: '11', item_category: 'görüntüleme hizmetleri', usage_condition: 'hizmet alımı yoluyla sağlanması', coverage_status: 'conditional', provider_obligation: 'acil ve yatan hastaların transferi sağlık hizmeti sunucuları tarafından yapılır'}
;

MERGE (n_d102131e1e7feef409271e56c06859d3:Rule:BillingRule {uid: 'd102131e1e7feef409271e56c06859d3'})
SET n_d102131e1e7feef409271e56c06859d3 += {uid: 'd102131e1e7feef409271e56c06859d3', text: 'Kurum ile sözleşmeli sağlık hizmeti sunucuları tetkik, tahlil ve tedaviye ait her türlü bilgi, belge ve raporu istenildiğinde Kuruma ibraz edeceklerdir. İbraz edilememesi durumunda Kuruma faturalandırılan ilgili tetkik, tahlil ve/veya tedavi bedelleri Kurumca karşılanmaz', paragraph: '12', rule_type: 'prohibition', condition: 'istenen bilgi, belge ve raporun Kuruma ibraz edilememesi', billable_items: 'tetkik, tahlil ve/veya tedavi bedelleri (ibraz edilenler için)', non_billable_items: 'ibraz edilemeyen tetkik, tahlil ve/veya tedavi bedelleri'}
;

MERGE (n_085a2c18a7c1e9485fba2cf825f06c3e:Rule:BillingRule {uid: '085a2c18a7c1e9485fba2cf825f06c3e'})
SET n_085a2c18a7c1e9485fba2cf825f06c3e += {uid: '085a2c18a7c1e9485fba2cf825f06c3e', text: 'Kişilere sağlanan sağlık hizmetlerine ilişkin düzenlenen sağlık raporu bedelleri, SUT eki EK-2/B Listesinde yer alan rapor puanları esas alınarak sadece bir adet olarak faturalandırılır', paragraph: '13', rule_type: 'restriction', condition: 'kişilere sağlanan sağlık hizmetlerine ilişkin sağlık raporu düzenlenmesi', billable_items: 'sağlık raporu bedeli', list_reference: 'EK-2/B', quantity_restriction: 'sadece bir adet olarak faturalandırılır', calculation_basis: 'EK-2/B Listesindeki rapor puanları esas alınır'}
MERGE (l_EK_2_B_085a2c18a7c1e9485fba2cf825f06c3e_0:RegulatoryList {code: 'EK-2/B'})
MERGE (n_085a2c18a7c1e9485fba2cf825f06c3e)-[:REFERENCES_LIST]->(l_EK_2_B_085a2c18a7c1e9485fba2cf825f06c3e_0)
;

MERGE (n_8e185bffd1c883e2afa889998d18d512:RegulatoryList {code: 'EK-2/B'})
SET n_8e185bffd1c883e2afa889998d18d512 += {uid: '8e185bffd1c883e2afa889998d18d512', text: 'SUT eki EK-2/B Listesinde yer alan rapor puanları esas alınarak', paragraph: '13', list_code: 'EK-2/B', billing_status: 'billable', condition: 'sağlık raporu bedellerinin faturalandırılması; rapor puanları esas alınır'}
;

MERGE (n_b917b3b50edecba9e89f7d52795ee262:Rule:BillingRule {uid: 'b917b3b50edecba9e89f7d52795ee262'})
SET n_b917b3b50edecba9e89f7d52795ee262 += {uid: 'b917b3b50edecba9e89f7d52795ee262', text: 'Kurum birimlerince sevk belgesi düzenlenmek suretiyle sevk edilen kişiler için düzenlenen bazı rapor ve işlemlerin Kurumca karşılanmaması', rule_type: 'prohibition', condition: 'Kurum birimlerince sevk belgesi ile sevk edilen kişilerde, tedavi amacı dışındaki özel amaçlı rapor ve işlemler', billable_items: 'maluliyet, meslek hastalığı ve kontrol muayeneleri vb nedenlerle tedavi amacıyla düzenlenen sağlık raporları ile ilaç ve tıbbi malzeme temini de dâhil sağlık raporları', non_billable_items: 'engellilik raporu, adli rapor, ehliyet raporu, vasi tayini raporu, portör muayeneleri ve işlemleri, tarama amaçlı muayene ve işlemler, özel amaçla kullanılacak durum belirtir raporlar ve bu durumların tespitine yönelik işlem bedelleri', exception: 'maluliyet, meslek hastalığı ve kontrol muayeneleri vb nedenlerle düzenlenen ve tedavi amacı taşıyan sağlık raporları ile ilaç ve tıbbi malzeme teminine yönelik sağlık raporları'}
;

MERGE (n_1aa82529fbf6085aae7fad1b647651b8:Rule:CoverageRule {uid: '1aa82529fbf6085aae7fad1b647651b8'})
SET n_1aa82529fbf6085aae7fad1b647651b8 += {uid: '1aa82529fbf6085aae7fad1b647651b8', text: 'engellilik, adli, ehliyet vb özel amaçlı rapor ve işlemlerin Kurumca karşılanmaması', item_category: 'özel amaçlı sağlık kurulu raporları ve bunlara yönelik işlemler', usage_condition: 'engellilik, adli süreç, ehliyet, vasi tayini, portör muayenesi, tarama amaçlı muayene/işlem ve benzeri özel amaçlarla kullanılması', coverage_status: 'not_covered', document_requirement: 'sevk belgesi olsa dahi bu kapsamdaki rapor ve işlemler için Kurum ödeme yapmaz'}
;

MERGE (n_b0ba5ec967adba2324e7646afcdb5a80:Rule:BillingRule {uid: 'b0ba5ec967adba2324e7646afcdb5a80'})
SET n_b0ba5ec967adba2324e7646afcdb5a80 += {uid: 'b0ba5ec967adba2324e7646afcdb5a80', text: 'SUT gereği düzenlenmesi gereken sağlık kurulu raporu için sadece bir adet muayene bedelinin faturalandırılabilmesi', paragraph: '14', rule_type: 'restriction', condition: 'kişilere sağlanan tıbbi malzeme, ilaç, tedavi vb sağlık hizmetleri için SUT gereği sağlık kurulu raporu düzenlenmesi gerektiğinde', billable_items: 'sadece bir adet muayene bedeli', non_billable_items: 'aynı sağlık kurulu raporu için ilave muayene bedelleri'}
;

MERGE (n_582564dadf225ff224c067cc3e3f854d:Limit {uid: '582564dadf225ff224c067cc3e3f854d'})
SET n_582564dadf225ff224c067cc3e3f854d += {uid: '582564dadf225ff224c067cc3e3f854d', text: 'SUT gereği sağlık kurulu raporu başına bir muayene bedeli sınırı', paragraph: '14', limit_type: 'absolute_maximum', metric: 'faturalandırılabilir muayene sayısı', max_value: '1', per: 'sağlık kurulu raporu', context: 'tıbbi malzeme, ilaç, tedavi vb sağlık hizmetleri için gereken sağlık kurulu raporu düzenlenmesi'}
;

MERGE (n_a9c53289673ed2cd9981d34a4876b2de:Rule:BillingRule {uid: 'a9c53289673ed2cd9981d34a4876b2de'})
SET n_a9c53289673ed2cd9981d34a4876b2de += {uid: 'a9c53289673ed2cd9981d34a4876b2de', text: 'kurula katılan her bir uzmanlık dalı için muayene bedeli faturalandırılabilir', parent_section: '2.2.1.B-1', rule_type: 'permission', condition: 'Kurum birimlerince sevk belgesi düzenlenmek suretiyle maluliyet, meslek hastalığı ve kontrol muayeneleri vb nedenlerle sağlık hizmeti sunucusuna sevk edilen kişiler için düzenlenen sağlık kurulu raporları', billable_items: 'kurula katılan her bir uzmanlık dalı için muayene bedeli'}
MERGE (s_2_2_1_B_1_a9c53289673ed2cd9981d34a4876b2de:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_a9c53289673ed2cd9981d34a4876b2de)-[:CONTAINS]->(n_a9c53289673ed2cd9981d34a4876b2de)
;

MERGE (n_35d9fbce3509617945316bffee2003de:Rule:ReferralRule {uid: '35d9fbce3509617945316bffee2003de'})
SET n_35d9fbce3509617945316bffee2003de += {uid: '35d9fbce3509617945316bffee2003de', text: 'Kurum birimlerince sevk belgesi düzenlenmek suretiyle sevk edilen kişiler', parent_section: '2.2.1.B-1', condition: 'maluliyet, meslek hastalığı ve kontrol muayeneleri vb nedenlerle Kurum birimlerince sevk belgesi düzenlenmesi', service_type: 'sağlık kurulu muayenesi'}
MERGE (s_2_2_1_B_1_35d9fbce3509617945316bffee2003de:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_35d9fbce3509617945316bffee2003de)-[:CONTAINS]->(n_35d9fbce3509617945316bffee2003de)
;

MERGE (n_a893be1feaeb68a4eefcd9c1219410da:Rule:CoverageRule {uid: 'a893be1feaeb68a4eefcd9c1219410da'})
SET n_a893be1feaeb68a4eefcd9c1219410da += {uid: 'a893be1feaeb68a4eefcd9c1219410da', text: 'Kurumca finansmanı sağlanan sağlık hizmetleri için Sağlık Hizmetleri Fiyatlandırma Komisyonu tarafından belirlenen bedeller SUT ve eki listelerde yer almaktadır', parent_section: '2.2.1.B-1', paragraph: '15', item_category: 'Kurumca finansmanı sağlanan sağlık hizmetleri', usage_condition: 'genel', coverage_status: 'covered', document_requirement: 'SUT ve eki listelerde yer alma'}
MERGE (s_2_2_1_B_1_a893be1feaeb68a4eefcd9c1219410da:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_a893be1feaeb68a4eefcd9c1219410da)-[:CONTAINS]->(n_a893be1feaeb68a4eefcd9c1219410da)
;

MERGE (n_ae25ace72a02a35d4718b96cd4dbf1dc:RegulatoryList {code: 'SUT ve eki listeler'})
SET n_ae25ace72a02a35d4718b96cd4dbf1dc += {uid: 'ae25ace72a02a35d4718b96cd4dbf1dc', text: 'SUT ve eki listelerde yer almaktadır', parent_section: '2.2.1.B-1', paragraph: '15', list_name: 'SUT ve eki listeler', billing_status: 'billable', condition: 'Sağlık Hizmetleri Fiyatlandırma Komisyonu tarafından belirlenen bedeller'}
MERGE (s_2_2_1_B_1_ae25ace72a02a35d4718b96cd4dbf1dc:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_ae25ace72a02a35d4718b96cd4dbf1dc)-[:CONTAINS]->(n_ae25ace72a02a35d4718b96cd4dbf1dc)
;

MERGE (n_e5d2341080853aa18bc1d1040d2d4ee4:RegulatoryList {code: 'EK-2/B'})
SET n_e5d2341080853aa18bc1d1040d2d4ee4 += {uid: 'e5d2341080853aa18bc1d1040d2d4ee4', text: 'Komisyonca SUT eki EK-2/B, EK-2/C ve EK-2/Ç listelerinde yer alan işlemler için ödemeye esas puanlar belirlenmiştir', parent_section: '2.2.1.B-1', paragraph: '15', list_code: 'EK-2/B, EK-2/C, EK-2/Ç', billing_status: 'billable', condition: 'ödemeye esas puan ve katsayı ile fiyatlandırma'}
MERGE (s_2_2_1_B_1_e5d2341080853aa18bc1d1040d2d4ee4:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_e5d2341080853aa18bc1d1040d2d4ee4)-[:CONTAINS]->(n_e5d2341080853aa18bc1d1040d2d4ee4)
MERGE (l_EK_2_B_e5d2341080853aa18bc1d1040d2d4ee4_0:RegulatoryList {code: 'EK-2/B'})
MERGE (n_e5d2341080853aa18bc1d1040d2d4ee4)-[:REFERENCES_LIST]->(l_EK_2_B_e5d2341080853aa18bc1d1040d2d4ee4_0)
MERGE (l_EK_2_C_e5d2341080853aa18bc1d1040d2d4ee4_1:RegulatoryList {code: 'EK-2/C'})
MERGE (n_e5d2341080853aa18bc1d1040d2d4ee4)-[:REFERENCES_LIST]->(l_EK_2_C_e5d2341080853aa18bc1d1040d2d4ee4_1)
MERGE (l_EK_2_e5d2341080853aa18bc1d1040d2d4ee4_2:RegulatoryList {code: 'EK-2/Ç'})
MERGE (n_e5d2341080853aa18bc1d1040d2d4ee4)-[:REFERENCES_LIST]->(l_EK_2_e5d2341080853aa18bc1d1040d2d4ee4_2)
;

MERGE (n_f6e67791c3410f5bbcb7c028cfd4a632:Rule:PaymentRule {uid: 'f6e67791c3410f5bbcb7c028cfd4a632'})
SET n_f6e67791c3410f5bbcb7c028cfd4a632 += {uid: 'f6e67791c3410f5bbcb7c028cfd4a632', text: 'EK-2/B, EK-2/C ve EK-2/Ç listelerindeki işlemler için işlem bedeli puan × katsayı olarak hesaplanır', parent_section: '2.2.1.B-1', paragraph: '15', payment_type: 'per_procedure', currency: 'TL', condition: 'SUT eki EK-2/B, EK-2/C ve EK-2/Ç listelerinde yer alan işlemler'}
MERGE (s_2_2_1_B_1_f6e67791c3410f5bbcb7c028cfd4a632:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_f6e67791c3410f5bbcb7c028cfd4a632)-[:CONTAINS]->(n_f6e67791c3410f5bbcb7c028cfd4a632)
;

MERGE (n_f1fbcebb0e02c3aba0b7c2e991b0bed4:Limit {uid: 'f1fbcebb0e02c3aba0b7c2e991b0bed4'})
SET n_f1fbcebb0e02c3aba0b7c2e991b0bed4 += {uid: 'f1fbcebb0e02c3aba0b7c2e991b0bed4', text: 'katsayı (0,593)', parent_section: '2.2.1.B-1', paragraph: '15', limit_type: 'calculated', metric: 'ödemeye esas katsayı', max_value: '0.593', per: 'puan', context: 'EK-2/B, EK-2/C ve EK-2/Ç listelerindeki işlemler için işlem bedelinin hesaplanması'}
MERGE (s_2_2_1_B_1_f1fbcebb0e02c3aba0b7c2e991b0bed4:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_f1fbcebb0e02c3aba0b7c2e991b0bed4)-[:CONTAINS]->(n_f1fbcebb0e02c3aba0b7c2e991b0bed4)
;

MERGE (n_0b4025ed1d5fe1e54bc596c81791ed7e:Rule:BillingRule {uid: '0b4025ed1d5fe1e54bc596c81791ed7e'})
SET n_0b4025ed1d5fe1e54bc596c81791ed7e += {uid: '0b4025ed1d5fe1e54bc596c81791ed7e', text: 'işlem bedeli ilgili puan ile katsayının çarpımı sonucu bulunacak tutardır', parent_section: '2.2.1.B-1', paragraph: '15', rule_type: 'calculation_method', condition: 'EK-2/B, EK-2/C ve EK-2/Ç listelerinde yer alan işlemler', billable_items: 'işlem bedeli', list_reference: 'EK-2/B, EK-2/C, EK-2/Ç'}
MERGE (s_2_2_1_B_1_0b4025ed1d5fe1e54bc596c81791ed7e:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_0b4025ed1d5fe1e54bc596c81791ed7e)-[:CONTAINS]->(n_0b4025ed1d5fe1e54bc596c81791ed7e)
MERGE (l_EK_2_B_0b4025ed1d5fe1e54bc596c81791ed7e_0:RegulatoryList {code: 'EK-2/B'})
MERGE (n_0b4025ed1d5fe1e54bc596c81791ed7e)-[:REFERENCES_LIST]->(l_EK_2_B_0b4025ed1d5fe1e54bc596c81791ed7e_0)
MERGE (l_EK_2_C_0b4025ed1d5fe1e54bc596c81791ed7e_1:RegulatoryList {code: 'EK-2/C'})
MERGE (n_0b4025ed1d5fe1e54bc596c81791ed7e)-[:REFERENCES_LIST]->(l_EK_2_C_0b4025ed1d5fe1e54bc596c81791ed7e_1)
MERGE (l_EK_2_0b4025ed1d5fe1e54bc596c81791ed7e_2:RegulatoryList {code: 'EK-2/Ç'})
MERGE (n_0b4025ed1d5fe1e54bc596c81791ed7e)-[:REFERENCES_LIST]->(l_EK_2_0b4025ed1d5fe1e54bc596c81791ed7e_2)
;

MERGE (n_1f45cc6a7777715e54057892e2795830:Rule:BillingRule {uid: '1f45cc6a7777715e54057892e2795830'})
SET n_1f45cc6a7777715e54057892e2795830 += {uid: '1f45cc6a7777715e54057892e2795830', text: 'işlem puanının katsayı ile çarpılması sonucu bulunacak tutar virgülden sonra iki basamak olacak şekilde alınır ve yuvarlama yapılmaz', parent_section: '2.2.1.B-1', paragraph: '15', rule_type: 'calculation_method', condition: 'ödemeye esas puanın ödemeye esas işlem bedeline çevrilmesi', billable_items: 'ödemeye esas işlem bedeli', list_reference: 'EK-2/B, EK-2/C, EK-2/Ç', exception: 'yuvarlama işlemi yapılmaz'}
MERGE (s_2_2_1_B_1_1f45cc6a7777715e54057892e2795830:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_1f45cc6a7777715e54057892e2795830)-[:CONTAINS]->(n_1f45cc6a7777715e54057892e2795830)
MERGE (l_EK_2_B_1f45cc6a7777715e54057892e2795830_0:RegulatoryList {code: 'EK-2/B'})
MERGE (n_1f45cc6a7777715e54057892e2795830)-[:REFERENCES_LIST]->(l_EK_2_B_1f45cc6a7777715e54057892e2795830_0)
MERGE (l_EK_2_C_1f45cc6a7777715e54057892e2795830_1:RegulatoryList {code: 'EK-2/C'})
MERGE (n_1f45cc6a7777715e54057892e2795830)-[:REFERENCES_LIST]->(l_EK_2_C_1f45cc6a7777715e54057892e2795830_1)
MERGE (l_EK_2_1f45cc6a7777715e54057892e2795830_2:RegulatoryList {code: 'EK-2/Ç'})
MERGE (n_1f45cc6a7777715e54057892e2795830)-[:REFERENCES_LIST]->(l_EK_2_1f45cc6a7777715e54057892e2795830_2)
;

MERGE (n_e65ec3d04a79d3cafa8f055b1d61ce33:Rule:BillingRule {uid: 'e65ec3d04a79d3cafa8f055b1d61ce33'})
SET n_e65ec3d04a79d3cafa8f055b1d61ce33 += {uid: 'e65ec3d04a79d3cafa8f055b1d61ce33', text: 'Sağlık hizmeti sunucularınca gerçekleştirilecek check-up, kampanya ya da tarama kapsamında yapılan işlemler Kuruma faturalandırılmaz', paragraph: '16', rule_type: 'prohibition', condition: 'check-up, kampanya ya da tarama kapsamında yapılan işlemler', non_billable_items: 'check-up, kampanya ya da tarama kapsamında yapılan işlemler'}
;

MERGE (n_4890015309bea9b3956f02da4db620e9:Rule:CoverageRule {uid: '4890015309bea9b3956f02da4db620e9'})
SET n_4890015309bea9b3956f02da4db620e9 += {uid: '4890015309bea9b3956f02da4db620e9', text: 'EK-2/B ve EK-2/C işlemlerinin laparoskopik, perkütan, endoskopik, endosonografik, mikrocerrahi, robotik cerrahi gibi yöntemlerle yapılması halinde SUT’ta yer alan işlem puanı esas alınarak Kurumca karşılanır', paragraph: '17', item_category: 'EK-2/B ve EK-2/C listelerindeki işlemler', usage_condition: 'laparoskopik, perkütan, endoskopik, endosonografik, mikrocerrahi, robotik cerrahi gibi yöntemlerle yapılması', coverage_status: 'covered'}
;

MERGE (n_cb5927d20c2af415bdcac0065fd6c0da:RegulatoryList {code: 'EK-2/B; EK-2/C'})
SET n_cb5927d20c2af415bdcac0065fd6c0da += {uid: 'cb5927d20c2af415bdcac0065fd6c0da', text: 'SUT eki EK-2/B ve EK-2/C listelerinde yer alan işlemler', paragraph: '17', list_code: 'EK-2/B; EK-2/C', billing_status: 'billable', condition: 'laparoskopik, perkütan, endoskopik, endosonografik, mikrocerrahi, robotik cerrahi gibi yöntemlerle yapılması halinde işlem puanı esas alınır'}
;

MERGE (n_20d6d70b74440c46f3aa6f6ff5eb1010:Rule:CoverageRule {uid: '20d6d70b74440c46f3aa6f6ff5eb1010'})
SET n_20d6d70b74440c46f3aa6f6ff5eb1010 += {uid: '20d6d70b74440c46f3aa6f6ff5eb1010', text: 'Ayrı kodu bulunan laparoskopik, perkütan, endoskopik, endosonografik, mikrocerrahi, robotik cerrahi gibi yöntemlerle yapılan işlemler kendi puanı esas alınarak Kurumca karşılanır', paragraph: '17', item_category: 'ayrı kodu bulunan laparoskopik, perkütan, endoskopik, endosonografik, mikrocerrahi, robotik cerrahi işlemler', usage_condition: 'işlemin SUT’ta ayrı kodunun bulunması', coverage_status: 'covered'}
;

MERGE (n_d97c18794939e39500cdc99478f5e074:Rule:CoverageRule {uid: 'd97c18794939e39500cdc99478f5e074'})
SET n_d97c18794939e39500cdc99478f5e074 += {uid: 'd97c18794939e39500cdc99478f5e074', text: 'Trafik kazası nedeniyle ilk müdahalenin sözleşmesiz sağlık hizmeti sunucularında sağlanması halinde bu sağlık hizmeti sunucusunda trafik kazası nedeniyle sunulan sağlık hizmetinin devamı niteliğinde olan tedaviler SUT ve ekleri esas alınarak Kurumca karşılanacaktır', paragraph: '18', item_category: 'trafik kazası nedeniyle sunulan sağlık hizmetinin devamı niteliğinde olan tedaviler', usage_condition: 'ilk müdahalenin sözleşmesiz sağlık hizmeti sunucusunda sağlanmış olması', coverage_status: 'conditional'}
;

MERGE (n_eb51d43ac90908665818f48e87b2e1d1:Limit {uid: 'eb51d43ac90908665818f48e87b2e1d1'})
SET n_eb51d43ac90908665818f48e87b2e1d1 += {uid: 'eb51d43ac90908665818f48e87b2e1d1', text: 'Bu süre trafik kazasının oluştuğu tarihten itibaren 6 ayı geçemez', paragraph: '18', limit_type: 'absolute_maximum', metric: 'trafik kazasına bağlı tedavi süresi', max_value: '6', per: 'ay', context: 'sözleşmesiz sağlık hizmeti sunucusunda, trafik kazası nedeniyle sunulan sağlık hizmetinin devamı niteliğindeki tedaviler'}
;

MERGE (n_66191d64aa2c62d7479f86feb5ebfc9e:Rule:CoverageRule {uid: '66191d64aa2c62d7479f86feb5ebfc9e'})
SET n_66191d64aa2c62d7479f86feb5ebfc9e += {uid: '66191d64aa2c62d7479f86feb5ebfc9e', text: 'Kurumca finansmanı sağlanan sağlık hizmetlerinde geri ödeme kural ve/veya kriterleri belirlenmemiş sağlık hizmetleri için güncel bilimsel klinik uygunluğun bulunması gerekir', parent_section: '2.2.1', paragraph: '19', item_category: 'geri ödeme kural ve/veya kriterleri belirlenmemiş sağlık hizmetleri', usage_condition: 'güncel bilimsel klinik uygunluğun bulunması', coverage_status: 'conditional'}
MERGE (s_2_2_1_66191d64aa2c62d7479f86feb5ebfc9e:Section {identifier: '2.2.1'})
MERGE (s_2_2_1_66191d64aa2c62d7479f86feb5ebfc9e)-[:CONTAINS]->(n_66191d64aa2c62d7479f86feb5ebfc9e)
;

MERGE (n_fefb4c5c506a18ced39d849fc472cc11:Rule:BillingRule {uid: 'fefb4c5c506a18ced39d849fc472cc11'})
SET n_fefb4c5c506a18ced39d849fc472cc11 += {uid: 'fefb4c5c506a18ced39d849fc472cc11', text: 'SUT eki EK -2/C-1 Listesinde yer alan işlemlerin SUT eki EK -2/A-1 Listesinde Sınıf -3 grubunda tanımlanan sağlık hizmeti sunucularınca yapılması halinde işlem puanlarına Listede belirtilen oranlar ilave edilerek faturalandırılır ve bu şekilde faturalandırılan işlemler için “2.2.2.B- Tanıya dayalı işlem üzerinden ödeme yöntemi” başlıklı maddenin beşinci fıkrasında yer alan hüküm uygulanmaz', parent_section: '2.2.1', paragraph: '20', rule_type: 'permission', condition: 'EK-2/C-1 Listesi işlemlerinin EK-2/A-1 Listesinde Sınıf-3 grubunda tanımlanan sağlık hizmeti sunucularınca yapılması', billable_items: 'EK-2/C-1 Listesi işlemleri, işlem puanlarına Listede belirtilen oranlar ilave edilerek', exception: '2.2.2.B maddesinin beşinci fıkrası hükmü uygulanmaz', list_reference: 'EK-2/C-1,EK-2/A-1'}
MERGE (s_2_2_1_fefb4c5c506a18ced39d849fc472cc11:Section {identifier: '2.2.1'})
MERGE (s_2_2_1_fefb4c5c506a18ced39d849fc472cc11)-[:CONTAINS]->(n_fefb4c5c506a18ced39d849fc472cc11)
MERGE (l_EK_2_C_1_fefb4c5c506a18ced39d849fc472cc11_0:RegulatoryList {code: 'EK-2/C-1'})
MERGE (n_fefb4c5c506a18ced39d849fc472cc11)-[:REFERENCES_LIST]->(l_EK_2_C_1_fefb4c5c506a18ced39d849fc472cc11_0)
MERGE (l_EK_2_A_1_fefb4c5c506a18ced39d849fc472cc11_1:RegulatoryList {code: 'EK-2/A-1'})
MERGE (n_fefb4c5c506a18ced39d849fc472cc11)-[:REFERENCES_LIST]->(l_EK_2_A_1_fefb4c5c506a18ced39d849fc472cc11_1)
;

MERGE (n_c0b47e0485fd53e63e35cba596fa40f1:RegulatoryList {code: 'EK-2/C-1'})
SET n_c0b47e0485fd53e63e35cba596fa40f1 += {uid: 'c0b47e0485fd53e63e35cba596fa40f1', text: 'SUT eki EK -2/C-1 Listesinde yer alan işlemler', parent_section: '2.2.1', paragraph: '20', list_code: 'EK-2/C-1', billing_status: 'billable', condition: 'EK-2/A-1 Listesinde Sınıf -3 grubunda tanımlanan sağlık hizmeti sunucularınca yapılması ve işlem puanlarına Listede belirtilen oranların ilavesi'}
MERGE (s_2_2_1_c0b47e0485fd53e63e35cba596fa40f1:Section {identifier: '2.2.1'})
MERGE (s_2_2_1_c0b47e0485fd53e63e35cba596fa40f1)-[:CONTAINS]->(n_c0b47e0485fd53e63e35cba596fa40f1)
;

MERGE (n_85af7129151d7c1fef79b9639673aa89:RegulatoryList {code: 'EK-2/A-1'})
SET n_85af7129151d7c1fef79b9639673aa89 += {uid: '85af7129151d7c1fef79b9639673aa89', text: 'SUT eki EK -2/A-1 Listesinde Sınıf -3 grubunda tanımlanan sağlık hizmeti sunucuları', parent_section: '2.2.1', paragraph: '20', list_code: 'EK-2/A-1', billing_status: 'billable', condition: 'Sınıf -3 grubunda tanımlanan sağlık hizmeti sunucuları tarafından EK-2/C-1 işlemlerinin yapılması'}
MERGE (s_2_2_1_85af7129151d7c1fef79b9639673aa89:Section {identifier: '2.2.1'})
MERGE (s_2_2_1_85af7129151d7c1fef79b9639673aa89)-[:CONTAINS]->(n_85af7129151d7c1fef79b9639673aa89)
;

MERGE (n_15dabcdb1ee10679c847062aa2ba7e8c:Section {identifier: '2.2.1'})
SET n_15dabcdb1ee10679c847062aa2ba7e8c += {uid: '15dabcdb1ee10679c847062aa2ba7e8c', text: '2.2.1 - Ayakta tedavilerde ödeme', identifier: '2.2.1', title: 'Ayakta tedavilerde ödeme', parent_section: '2.2', care_setting: 'ayakta tedavi'}
MERGE (s_2_2_15dabcdb1ee10679c847062aa2ba7e8c:Section {identifier: '2.2'})
MERGE (s_2_2_15dabcdb1ee10679c847062aa2ba7e8c)-[:CONTAINS]->(n_15dabcdb1ee10679c847062aa2ba7e8c)
;

MERGE (n_c5ed2bfba40d84174d1600630846c27e:Section {identifier: '2.2.1.A'})
SET n_c5ed2bfba40d84174d1600630846c27e += {uid: 'c5ed2bfba40d84174d1600630846c27e', text: '2.2.1.A - Birinci basamak sağlık kuruluşları', identifier: '2.2.1.A', title: 'Birinci basamak sağlık kuruluşları', parent_section: '2.2.1', healthcare_level: 'birinci basamak', care_setting: 'ayakta tedavi'}
MERGE (s_2_2_1_c5ed2bfba40d84174d1600630846c27e:Section {identifier: '2.2.1'})
MERGE (s_2_2_1_c5ed2bfba40d84174d1600630846c27e)-[:CONTAINS]->(n_c5ed2bfba40d84174d1600630846c27e)
MERGE (p_birinci_basamak_c5ed2bfba40d84174d1600630846c27e_0:ProviderType {level: 'birinci basamak'})
MERGE (n_c5ed2bfba40d84174d1600630846c27e)-[:APPLIES_TO]->(p_birinci_basamak_c5ed2bfba40d84174d1600630846c27e_0)
;

MERGE (n_693e4dc5a2ad0bd00890559a303470e6:Rule:PaymentRule {uid: '693e4dc5a2ad0bd00890559a303470e6'})
SET n_693e4dc5a2ad0bd00890559a303470e6 += {uid: '693e4dc5a2ad0bd00890559a303470e6', text: 'Birinci basamak sağlık kuruluşlarındaki ayakta tedavilerde, her başvuru için 11 (onbir) TL ödeme yapılır', parent_section: '2.2.1.A', paragraph: '1', payment_type: 'per_visit', amount: '11', amount_text: 'onbir', currency: 'TL', condition: 'birinci basamak sağlık kuruluşlarındaki ayakta tedavilerde her başvuru', healthcare_level: 'birinci basamak', care_setting: 'ayakta tedavi'}
MERGE (s_2_2_1_A_693e4dc5a2ad0bd00890559a303470e6:Section {identifier: '2.2.1.A'})
MERGE (s_2_2_1_A_693e4dc5a2ad0bd00890559a303470e6)-[:CONTAINS]->(n_693e4dc5a2ad0bd00890559a303470e6)
MERGE (p_birinci_basamak_693e4dc5a2ad0bd00890559a303470e6_0:ProviderType {level: 'birinci basamak'})
MERGE (n_693e4dc5a2ad0bd00890559a303470e6)-[:APPLIES_TO]->(p_birinci_basamak_693e4dc5a2ad0bd00890559a303470e6_0)
;

MERGE (n_6a8e0034346640dbe742a7629a5c6550:Rule:PaymentRule {uid: '6a8e0034346640dbe742a7629a5c6550'})
SET n_6a8e0034346640dbe742a7629a5c6550 += {uid: '6a8e0034346640dbe742a7629a5c6550', text: 'Hastanın diğer bir sağlık kurumuna sevk edilmesi halinde ise sadece 5 (beş) TL ödeme yapılır', parent_section: '2.2.1.A', paragraph: '1', payment_type: 'per_referral', amount: '5', amount_text: 'beş', currency: 'TL', condition: 'hastanın diğer bir sağlık kurumuna sevk edilmesi', care_setting: 'ayakta tedavi', healthcare_level: 'birinci basamak'}
MERGE (s_2_2_1_A_6a8e0034346640dbe742a7629a5c6550:Section {identifier: '2.2.1.A'})
MERGE (s_2_2_1_A_6a8e0034346640dbe742a7629a5c6550)-[:CONTAINS]->(n_6a8e0034346640dbe742a7629a5c6550)
MERGE (p_birinci_basamak_6a8e0034346640dbe742a7629a5c6550_0:ProviderType {level: 'birinci basamak'})
MERGE (n_6a8e0034346640dbe742a7629a5c6550)-[:APPLIES_TO]->(p_birinci_basamak_6a8e0034346640dbe742a7629a5c6550_0)
;

MERGE (n_a36790c075f23ff15af484bfe59400b7:Section {identifier: '2.2.1.B'})
SET n_a36790c075f23ff15af484bfe59400b7 += {uid: 'a36790c075f23ff15af484bfe59400b7', text: '2.2.1.B - İkinci ve üçüncü basamak sağlık kurumları', identifier: '2.2.1.B', title: 'İkinci ve üçüncü basamak sağlık kurumları', parent_section: '2.2.1', healthcare_level: 'ikinci basamak,üçüncü basamak', care_setting: 'ayakta tedavi'}
MERGE (s_2_2_1_a36790c075f23ff15af484bfe59400b7:Section {identifier: '2.2.1'})
MERGE (s_2_2_1_a36790c075f23ff15af484bfe59400b7)-[:CONTAINS]->(n_a36790c075f23ff15af484bfe59400b7)
MERGE (p_ikinci_basamak_a36790c075f23ff15af484bfe59400b7_0:ProviderType {level: 'ikinci basamak'})
MERGE (n_a36790c075f23ff15af484bfe59400b7)-[:APPLIES_TO]->(p_ikinci_basamak_a36790c075f23ff15af484bfe59400b7_0)
MERGE (p_nc_basamak_a36790c075f23ff15af484bfe59400b7_1:ProviderType {level: 'üçüncü basamak'})
MERGE (n_a36790c075f23ff15af484bfe59400b7)-[:APPLIES_TO]->(p_nc_basamak_a36790c075f23ff15af484bfe59400b7_1)
;

MERGE (n_2cee57e898ff7afdca15f7a09a234279:Amendment {uid: '2cee57e898ff7afdca15f7a09a234279'})
SET n_2cee57e898ff7afdca15f7a09a234279 += {uid: '2cee57e898ff7afdca15f7a09a234279', text: 'Değişik: RG- 25/08/2022- 31934/ 12-b md. Yürürlük: 03/09/2022', parent_section: '2.2.1.B', amendment_type: 'değişik', official_gazette_date: '25/08/2022', official_gazette_number: '31934', article_reference: '12-b md.', effective_date: '03/09/2022'}
MERGE (s_2_2_1_B_2cee57e898ff7afdca15f7a09a234279:Section {identifier: '2.2.1.B'})
MERGE (s_2_2_1_B_2cee57e898ff7afdca15f7a09a234279)-[:CONTAINS]->(n_2cee57e898ff7afdca15f7a09a234279)
;

MERGE (n_a2d0e9705548da7012fed201503195ec:Section {identifier: '1.B-1'})
SET n_a2d0e9705548da7012fed201503195ec += {uid: 'a2d0e9705548da7012fed201503195ec', text: '1.B-1 - Ayakta tedavilerde ödeme uygulaması', identifier: '1.B-1', title: 'Ayakta tedavilerde ödeme uygulaması', parent_section: '1.B', care_setting: 'ayakta tedavi', payment_method: 'ayakta tedavilerde ödeme'}
MERGE (s_1_B_a2d0e9705548da7012fed201503195ec:Section {identifier: '1.B'})
MERGE (s_1_B_a2d0e9705548da7012fed201503195ec)-[:CONTAINS]->(n_a2d0e9705548da7012fed201503195ec)
;

MERGE (n_70b75afa9f1a9f3348915370062e0b50:Amendment {uid: '70b75afa9f1a9f3348915370062e0b50'})
SET n_70b75afa9f1a9f3348915370062e0b50 += {uid: '70b75afa9f1a9f3348915370062e0b50', text: 'Ek:RG-09/05/2024-32541/1-a md. Yürürlük:11/05/2024', parent_section: '1.B-1', amendment_type: 'ek', official_gazette_date: '09/05/2024', official_gazette_number: '32541', article_reference: '1-a md.', effective_date: '11/05/2024'}
MERGE (s_1_B_1_70b75afa9f1a9f3348915370062e0b50:Section {identifier: '1.B-1'})
MERGE (s_1_B_1_70b75afa9f1a9f3348915370062e0b50)-[:CONTAINS]->(n_70b75afa9f1a9f3348915370062e0b50)
;

MERGE (n_79eded3fb343bf334dc58ee8ee9199a7:Rule:BillingRule {uid: '79eded3fb343bf334dc58ee8ee9199a7'})
SET n_79eded3fb343bf334dc58ee8ee9199a7 += {uid: '79eded3fb343bf334dc58ee8ee9199a7', text: 'Ayakta tedavilerde ödeme kapsamında her bir ayaktan başvuru için EK-2/A Listesi tutarları esas alınarak ödeme yapılır', parent_section: '1.B-1', paragraph: '1', rule_type: 'payment_basis', care_setting: 'ayakta tedavi', condition: 'sağlık hizmeti sunucusunda ayaktan her bir başvuru', billable_items: 'EK-2/A Listesinde yer alan tutarlar', list_reference: 'EK-2/A', calculation_basis: 'SUT eki EK-2/A Listesi', classification_basis: 'EK-2/A-1 Listesinde bulunduğu sınıf'}
MERGE (s_1_B_1_79eded3fb343bf334dc58ee8ee9199a7:Section {identifier: '1.B-1'})
MERGE (s_1_B_1_79eded3fb343bf334dc58ee8ee9199a7)-[:CONTAINS]->(n_79eded3fb343bf334dc58ee8ee9199a7)
MERGE (l_EK_2_A_79eded3fb343bf334dc58ee8ee9199a7_0:RegulatoryList {code: 'EK-2/A'})
MERGE (n_79eded3fb343bf334dc58ee8ee9199a7)-[:REFERENCES_LIST]->(l_EK_2_A_79eded3fb343bf334dc58ee8ee9199a7_0)
;

MERGE (n_2a0f2f1bf76bab2e68fa434482d77dd7:RegulatoryList {code: 'EK-2/A-1'})
SET n_2a0f2f1bf76bab2e68fa434482d77dd7 += {uid: '2a0f2f1bf76bab2e68fa434482d77dd7', text: 'Sağlık Hizmeti Sunucularının Ayakta Tedavilerde Sınıflandırılması Listesi (EK-2/A-1)', parent_section: '1.B-1', paragraph: '1', list_code: 'EK-2/A-1', list_name: 'Sağlık Hizmeti Sunucularının Ayakta Tedavilerde Sınıflandırılması Listesi', billing_status: 'billable', condition: 'hizmet sunucusunun sınıfına göre EK-2/A tutarının belirlenmesi'}
MERGE (s_1_B_1_2a0f2f1bf76bab2e68fa434482d77dd7:Section {identifier: '1.B-1'})
MERGE (s_1_B_1_2a0f2f1bf76bab2e68fa434482d77dd7)-[:CONTAINS]->(n_2a0f2f1bf76bab2e68fa434482d77dd7)
;

MERGE (n_9ac2674b4b56f876453c472a44884465:RegulatoryList {code: 'EK-2/A'})
SET n_9ac2674b4b56f876453c472a44884465 += {uid: '9ac2674b4b56f876453c472a44884465', text: 'SUT eki EK-2/A Listesinde yer alan tutarlar esas alınarak ödeme yapılır', parent_section: '1.B-1', paragraph: '1', list_code: 'EK-2/A', billing_status: 'billable', condition: 'ayaktan her bir başvuru için ödeme hesabı'}
MERGE (s_1_B_1_9ac2674b4b56f876453c472a44884465:Section {identifier: '1.B-1'})
MERGE (s_1_B_1_9ac2674b4b56f876453c472a44884465)-[:CONTAINS]->(n_9ac2674b4b56f876453c472a44884465)
;

MERGE (n_fd3b527bd02f721f15bfeedbb5703256:Rule:PaymentRule {uid: 'fd3b527bd02f721f15bfeedbb5703256'})
SET n_fd3b527bd02f721f15bfeedbb5703256 += {uid: 'fd3b527bd02f721f15bfeedbb5703256', text: 'mesai saatleri dışında sunulan poliklinik hizmetleri için EK-2/A Listesinde yer alan tutarların iki katı esas alınarak ödeme yapılır', parent_section: '1.B-1', paragraph: '1', payment_type: 'per_visit', multiplier: '2', currency: 'TL', condition: 'Sağlık Bakanlığı tarafından Kuruma bildirilen, mesai saatlerinde aynı gün randevusu dolu olan branşlarda; Sağlık Bakanlığına bağlı ikinci ve üçüncü basamak sağlık hizmeti sunucularında uzman hekimler tarafından mesai saatleri dışında sunulan poliklinik hizmetleri', care_setting: 'ayaktan tedavi', healthcare_level: 'ikinci basamak,üçüncü basamak', provider_affiliation: 'Sağlık Bakanlığı', payment_basis_list: 'EK-2/A'}
MERGE (s_1_B_1_fd3b527bd02f721f15bfeedbb5703256:Section {identifier: '1.B-1'})
MERGE (s_1_B_1_fd3b527bd02f721f15bfeedbb5703256)-[:CONTAINS]->(n_fd3b527bd02f721f15bfeedbb5703256)
MERGE (p_ikinci_basamak_fd3b527bd02f721f15bfeedbb5703256_0:ProviderType {level: 'ikinci basamak'})
MERGE (n_fd3b527bd02f721f15bfeedbb5703256)-[:APPLIES_TO]->(p_ikinci_basamak_fd3b527bd02f721f15bfeedbb5703256_0)
MERGE (p_nc_basamak_fd3b527bd02f721f15bfeedbb5703256_1:ProviderType {level: 'üçüncü basamak'})
MERGE (n_fd3b527bd02f721f15bfeedbb5703256)-[:APPLIES_TO]->(p_nc_basamak_fd3b527bd02f721f15bfeedbb5703256_1)
;

MERGE (n_84c260187f38b0b1363bc738e8928b91:RegulatoryList {code: 'EK-2/A'})
SET n_84c260187f38b0b1363bc738e8928b91 += {uid: '84c260187f38b0b1363bc738e8928b91', text: 'mesai saatleri dışında sunulan poliklinik hizmetleri için EK-2/A Listesinde yer alan tutarların iki katı esas alınır', parent_section: '1.B-1', paragraph: '1', list_code: 'EK-2/A', billing_status: 'billable', condition: 'mesai dışı, aynı gün randevusu dolu branş poliklinik hizmetleri için 2 katı esas alınır'}
MERGE (s_1_B_1_84c260187f38b0b1363bc738e8928b91:Section {identifier: '1.B-1'})
MERGE (s_1_B_1_84c260187f38b0b1363bc738e8928b91)-[:CONTAINS]->(n_84c260187f38b0b1363bc738e8928b91)
;

MERGE (n_fc9044a4b3a76090096d65499c071559:Rule:BillingRule {uid: 'fc9044a4b3a76090096d65499c071559'})
SET n_fc9044a4b3a76090096d65499c071559 += {uid: 'fc9044a4b3a76090096d65499c071559', text: 'Ayaktan Başvurularda İlave Olarak Faturalandırılabilecek İşlemler Listesi (EK-2/A-2) bedelleri Kurumca karşılanır', parent_section: '1.B-1', paragraph: '1', rule_type: 'permission', condition: 'ayaktan başvuruya ilave işlemler', billable_items: 'EK-2/A-2 Listesinde yer alan işlemler', payer: 'Kurum'}
MERGE (s_1_B_1_fc9044a4b3a76090096d65499c071559:Section {identifier: '1.B-1'})
MERGE (s_1_B_1_fc9044a4b3a76090096d65499c071559)-[:CONTAINS]->(n_fc9044a4b3a76090096d65499c071559)
;

MERGE (n_a92c448eedf93c62c4991ed4d5f0cd4e:RegulatoryList {code: 'EK-2/A-2'})
SET n_a92c448eedf93c62c4991ed4d5f0cd4e += {uid: 'a92c448eedf93c62c4991ed4d5f0cd4e', text: 'Ayaktan Başvurularda İlave Olarak Faturalandırılabilecek İşlemler Listesi (EK-2/A-2)', parent_section: '1.B-1', paragraph: '1', list_code: 'EK-2/A-2', list_name: 'Ayaktan Başvurularda İlave Olarak Faturalandırılabilecek İşlemler Listesi', billing_status: 'billable', condition: 'ayaktan başvurularda ilave olarak faturalandırılabilecek işlemler; bedelleri Kurumca karşılanır'}
MERGE (s_1_B_1_a92c448eedf93c62c4991ed4d5f0cd4e:Section {identifier: '1.B-1'})
MERGE (s_1_B_1_a92c448eedf93c62c4991ed4d5f0cd4e)-[:CONTAINS]->(n_a92c448eedf93c62c4991ed4d5f0cd4e)
;

MERGE (n_d3df67b7c473704b502e985e6335989c:Rule:BillingRule {uid: 'd3df67b7c473704b502e985e6335989c'})
SET n_d3df67b7c473704b502e985e6335989c += {uid: 'd3df67b7c473704b502e985e6335989c', text: 'Hastanın aynı sağlık hizmeti sunucusuna, acil servise başvuruları hariç olmak üzere ayaktan başvurduğu gün dahil, 10 gün içindeki aynı uzmanlık dalına diğer ayaktan başvurularında; sadece SUT eki EK-2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılabilecek olup SUT eki EK-2/A Listesinde yer alan tutar faturalandırılamaz', parent_section: '2.2.1.B-1', paragraph: '2', rule_type: 'restriction', condition: 'aynı sağlık hizmeti sunucusuna, acil servis başvuruları hariç, ayaktan başvuru günü dahil 10 gün içindeki aynı uzmanlık dalına diğer ayaktan başvurular', billable_items: 'SUT eki EK-2/A-2 Listesinde yer alan işlemler', non_billable_items: 'SUT eki EK-2/A Listesinde yer alan tutarlar', time_window: '10 gün', exception: 'acil servise başvurular', provider_scope: 'aynı sağlık hizmeti sunucusu', scope: 'aynı uzmanlık dalı'}
MERGE (s_2_2_1_B_1_d3df67b7c473704b502e985e6335989c:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_d3df67b7c473704b502e985e6335989c)-[:CONTAINS]->(n_d3df67b7c473704b502e985e6335989c)
;

MERGE (n_44421da85d5a5e5e7a710f6b8997f441:RegulatoryList {code: 'EK-2/A-2'})
SET n_44421da85d5a5e5e7a710f6b8997f441 += {uid: '44421da85d5a5e5e7a710f6b8997f441', text: 'SUT eki EK -2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılabilecek', parent_section: '2.2.1.B-1', paragraph: '2', list_code: 'EK-2/A-2', billing_status: 'billable', condition: 'aynı sağlık hizmeti sunucusuna, ayaktan başvuru günü dahil 10 gün içindeki aynı uzmanlık dalına diğer ayaktan başvurular'}
MERGE (s_2_2_1_B_1_44421da85d5a5e5e7a710f6b8997f441:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_44421da85d5a5e5e7a710f6b8997f441)-[:CONTAINS]->(n_44421da85d5a5e5e7a710f6b8997f441)
;

MERGE (n_4816e024693c77aed59b205c872d8650:RegulatoryList {code: 'EK-2/A'})
SET n_4816e024693c77aed59b205c872d8650 += {uid: '4816e024693c77aed59b205c872d8650', text: 'SUT eki EK-2/A Listesinde yer alan tutar faturalandırılamaz', parent_section: '2.2.1.B-1', paragraph: '2', list_code: 'EK-2/A', billing_status: 'not_billable', condition: 'aynı sağlık hizmeti sunucusuna, ayaktan başvuru günü dahil 10 gün içindeki aynı uzmanlık dalına diğer ayaktan başvurular'}
MERGE (s_2_2_1_B_1_4816e024693c77aed59b205c872d8650:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_4816e024693c77aed59b205c872d8650)-[:CONTAINS]->(n_4816e024693c77aed59b205c872d8650)
;

MERGE (n_8b0e996669ecee4cfdeaa50738716603:Amendment {uid: '8b0e996669ecee4cfdeaa50738716603'})
SET n_8b0e996669ecee4cfdeaa50738716603 += {uid: '8b0e996669ecee4cfdeaa50738716603', text: 'Değişik:RG- 09/05/2024-32541/1-b md. Yürürlük: 11/05/2024', parent_section: '2.2.1.B-1', amendment_type: 'değişik', official_gazette_date: '09/05/2024', official_gazette_number: '32541', article_reference: '1-b md.', effective_date: '11/05/2024'}
MERGE (s_2_2_1_B_1_8b0e996669ecee4cfdeaa50738716603:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_8b0e996669ecee4cfdeaa50738716603)-[:CONTAINS]->(n_8b0e996669ecee4cfdeaa50738716603)
;

MERGE (n_407f4eb9458c30213a7d31a647a7ae13:Rule:BillingRule {uid: '407f4eb9458c30213a7d31a647a7ae13'})
SET n_407f4eb9458c30213a7d31a647a7ae13 += {uid: '407f4eb9458c30213a7d31a647a7ae13', text: 'Hastaya SUT eki EK-2/A-2 ve EK -2/C Listelerinde yer alan işlemlerin yapılmasının gerekli görülmesi, ancak bu işlemlerin bu muayene başvurusundan sonra aynı sağlık hizmeti sunucusunda randevu verilmek suretiyle ileri bir tarihte yapılması durumunda SUT eki EK-2/A Listesinde yer alan tutarlar ikinci bir defa girilmeksizin sadece yapılan işlem faturalandırılır', parent_section: '2.2.1.B-1', paragraph: '3', rule_type: 'restriction', condition: 'SUT eki EK-2/A-2 ve EK-2/C Listesi işlemlerinin gerekli görülmesi ve aynı sağlık hizmeti sunucusunda bu muayene başvurusundan sonra randevu verilerek ileri tarihte yapılması', billable_items: 'sadece yapılan işlem', non_billable_items: 'SUT eki EK-2/A Listesinde yer alan tutarların ikinci defa girilmesi', provider_scope: 'aynı sağlık hizmeti sunucusu', note: 'EK-2/A listesi muayene tutarı ikinci kez girilemez'}
MERGE (s_2_2_1_B_1_407f4eb9458c30213a7d31a647a7ae13:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_407f4eb9458c30213a7d31a647a7ae13)-[:CONTAINS]->(n_407f4eb9458c30213a7d31a647a7ae13)
;

MERGE (n_a42204fece53eedb12271343f608f706:RegulatoryList {code: 'EK-2/A-2'})
SET n_a42204fece53eedb12271343f608f706 += {uid: 'a42204fece53eedb12271343f608f706', text: 'SUT eki EK-2/A-2 ve EK -2/C Listelerinde yer alan işlemlerin yapılmasının gerekli görülmesi', parent_section: '2.2.1.B-1', paragraph: '3', list_code: 'EK-2/A-2', billing_status: 'billable', condition: 'işlemlerin gerekli görülmesi ve bu muayene başvurusundan sonra aynı sağlık hizmeti sunucusunda randevu ile ileri tarihte yapılması'}
MERGE (s_2_2_1_B_1_a42204fece53eedb12271343f608f706:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_a42204fece53eedb12271343f608f706)-[:CONTAINS]->(n_a42204fece53eedb12271343f608f706)
;

MERGE (n_9a94fd23e54c2d5b5e9732c1c8ea5291:RegulatoryList {code: 'EK-2/C'})
SET n_9a94fd23e54c2d5b5e9732c1c8ea5291 += {uid: '9a94fd23e54c2d5b5e9732c1c8ea5291', text: 'SUT eki EK-2/A-2 ve EK -2/C Listelerinde yer alan işlemlerin yapılmasının gerekli görülmesi', parent_section: '2.2.1.B-1', paragraph: '3', list_code: 'EK-2/C', billing_status: 'billable', condition: 'işlemlerin gerekli görülmesi ve bu muayene başvurusundan sonra aynı sağlık hizmeti sunucusunda randevu ile ileri tarihte yapılması'}
MERGE (s_2_2_1_B_1_9a94fd23e54c2d5b5e9732c1c8ea5291:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_9a94fd23e54c2d5b5e9732c1c8ea5291)-[:CONTAINS]->(n_9a94fd23e54c2d5b5e9732c1c8ea5291)
;

MERGE (n_cc2d28848176e3746fd0d4c599c9a83a:RegulatoryList {code: 'EK-2/A'})
SET n_cc2d28848176e3746fd0d4c599c9a83a += {uid: 'cc2d28848176e3746fd0d4c599c9a83a', text: 'SUT eki EK-2/A Listesinde yer alan tutarlar ikinci bir defa girilmeksizin sadece yapılan işlem faturalandırılır', parent_section: '2.2.1.B-1', paragraph: '3', list_code: 'EK-2/A', billing_status: 'not_billable', condition: 'EK-2/A-2 veya EK-2/C Listesi işlemlerinin aynı sağlık hizmeti sunucusunda randevu ile ileri tarihte yapılması; muayene için EK-2/A tutarı daha önce girilmiş olması'}
MERGE (s_2_2_1_B_1_cc2d28848176e3746fd0d4c599c9a83a:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_cc2d28848176e3746fd0d4c599c9a83a)-[:CONTAINS]->(n_cc2d28848176e3746fd0d4c599c9a83a)
;

MERGE (n_9485f5e83316d6aaa7bb4361ec45ba29:Rule:BillingRule {uid: '9485f5e83316d6aaa7bb4361ec45ba29'})
SET n_9485f5e83316d6aaa7bb4361ec45ba29 += {uid: '9485f5e83316d6aaa7bb4361ec45ba29', text: 'ayaktan başvuru sonrasında aynı gün yatarak tedavi kapsamında EK-2/C işlem yapılması halinde', parent_section: 'UNKNOWN', paragraph: '4', rule_type: 'outpatient_to_inpatient_same_day', condition: 'Hastanın aynı sağlık hizmeti sunucusunda aynı uzmanlık dalına ayaktan başvurusu sonrasında aynı gün yatarak tedavi kapsamında EK-2/C Listesinde yer alan bir işlem yapılması', billable_items: 'SUT eki EK-2/C Listesinde yer alan işlem ile birlikte ayaktan yapılan işlemler', list_reference: 'EK-2/C', condition_detail: 'bu işlemler bu maddenin birinci fıkrasındaki hükümlere göre faturalandırılır'}
MERGE (l_EK_2_C_9485f5e83316d6aaa7bb4361ec45ba29_0:RegulatoryList {code: 'EK-2/C'})
MERGE (n_9485f5e83316d6aaa7bb4361ec45ba29)-[:REFERENCES_LIST]->(l_EK_2_C_9485f5e83316d6aaa7bb4361ec45ba29_0)
;

MERGE (n_4e53db4fbf93be551a8d8fb47d447671:Rule:BillingRule {uid: '4e53db4fbf93be551a8d8fb47d447671'})
SET n_4e53db4fbf93be551a8d8fb47d447671 += {uid: '4e53db4fbf93be551a8d8fb47d447671', text: 'yatarak tedavi kapsamında hizmet başına ödeme yöntemi ile bir işlem yapılması durumunda', parent_section: 'UNKNOWN', paragraph: '4', rule_type: 'outpatient_to_inpatient_same_day', condition: '“yatarak tedavi” kapsamında hizmet başına ödeme yöntemi ile bir işlem yapılması', billable_items: 'ayaktan başvurular hizmet başına ödeme yöntemine göre', non_billable_items: 'SUT eki EK-2/A Listesinde yer alan tutarlar', list_reference: 'EK-2/A', condition_detail: 'EK-2/A Listesinde yer alan tutarlar faturalandırılmayacak olup ayaktan başvurular da hizmet başına ödeme yöntemine göre faturalandırılır'}
MERGE (l_EK_2_A_4e53db4fbf93be551a8d8fb47d447671_0:RegulatoryList {code: 'EK-2/A'})
MERGE (n_4e53db4fbf93be551a8d8fb47d447671)-[:REFERENCES_LIST]->(l_EK_2_A_4e53db4fbf93be551a8d8fb47d447671_0)
;

MERGE (n_1bcfc64d8ffea9f9b1a6b1b437a356f3:RegulatoryList {code: 'EK-2/C'})
SET n_1bcfc64d8ffea9f9b1a6b1b437a356f3 += {uid: '1bcfc64d8ffea9f9b1a6b1b437a356f3', text: 'SUT eki EK-2/C Listesinde yer alan bir işlem yapılması', parent_section: 'UNKNOWN', paragraph: '4', list_code: 'EK-2/C', billing_status: 'billable', condition: 'Hastanın aynı sağlık hizmeti sunucusunda aynı uzmanlık dalına ayaktan başvurusu sonrasında aynı gün yatarak tedavi kapsamında işlem yapılması'}
;

MERGE (n_025a7840ab609e4c06f327004368fd57:RegulatoryList {code: 'EK-2/A'})
SET n_025a7840ab609e4c06f327004368fd57 += {uid: '025a7840ab609e4c06f327004368fd57', text: 'SUT eki EK-2/A Listesinde yer alan tutarlar faturalandırılmayacak', parent_section: 'UNKNOWN', paragraph: '4', list_code: 'EK-2/A', billing_status: 'not_billable', condition: '“yatarak tedavi” kapsamında hizmet başına ödeme yöntemi ile bir işlem yapılması'}
;

MERGE (n_f5ad2c95feacb6f52dd8985f38a42b97:Rule:BillingRule {uid: 'f5ad2c95feacb6f52dd8985f38a42b97'})
SET n_f5ad2c95feacb6f52dd8985f38a42b97 += {uid: 'f5ad2c95feacb6f52dd8985f38a42b97', text: 'Hastanın aynı gün içerisinde, aynı sağlık hizmeti sunucusunda; birden fazla uzmanlık dalına başvurusu sonrasında bu uzmanlık dallarından herhangi birinde aynı gün “yatarak tedavi” kapsamında SUT eki EK-2/C Listesinde yer alan bir işlem yapılması halinde bu işlem ile birlikte, o uzmanlık dalına ait ayaktan yapılan işlemler bu maddenin birinci fıkrasındaki hükümlere göre, diğer uzmanlık dallarındaki ayakta tedavi kapsamındaki başvuruları SUT eki EK-2/B Listesindeki “normal poliklinik muayenesi” bedeli ve yapılması halinde SUT eki EK-2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılacaktır.', parent_section: '2.2.1.B-1', paragraph: '5', rule_type: 'outpatient_to_inpatient_same_day', condition: 'aynı gün, aynı sağlık hizmeti sunucusunda birden fazla uzmanlık dalına başvuru; bu dallardan birinde aynı gün yatarak tedavi kapsamında EK-2/C Listesinde yer alan bir işlem yapılması', scenario: 'çoklu uzmanlık başvurusu, bir uzmanlık dalında yatarak EK-2/C işlemi', inpatient_billing: 'SUT eki EK-2/C Listesindeki işlem bedeli', outpatient_billing: 'yatarak işlemin yapıldığı uzmanlık dalına ait ayaktan işlemler birinci fıkra hükümlerine göre; diğer uzmanlık dallarındaki başvurular EK-2/B \'normal poliklinik muayenesi\' ve varsa EK-2/A-2 işlemleri üzerinden'}
MERGE (s_2_2_1_B_1_f5ad2c95feacb6f52dd8985f38a42b97:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_f5ad2c95feacb6f52dd8985f38a42b97)-[:CONTAINS]->(n_f5ad2c95feacb6f52dd8985f38a42b97)
;

MERGE (n_1083b11b2b7fdb652c4fb3d4ee77dea3:RegulatoryList {code: 'EK-2/C'})
SET n_1083b11b2b7fdb652c4fb3d4ee77dea3 += {uid: '1083b11b2b7fdb652c4fb3d4ee77dea3', text: 'SUT eki EK-2/C Listesinde yer alan bir işlem yapılması', parent_section: '2.2.1.B-1', paragraph: '5', list_code: 'EK-2/C', billing_status: 'billable', condition: 'aynı gün yatarak tedavi kapsamında yapılan işlem'}
MERGE (s_2_2_1_B_1_1083b11b2b7fdb652c4fb3d4ee77dea3:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_1083b11b2b7fdb652c4fb3d4ee77dea3)-[:CONTAINS]->(n_1083b11b2b7fdb652c4fb3d4ee77dea3)
;

MERGE (n_2d18d105cd582f162d043c40cd43a7fe:RegulatoryList {code: 'EK-2/B'})
SET n_2d18d105cd582f162d043c40cd43a7fe += {uid: '2d18d105cd582f162d043c40cd43a7fe', text: 'SUT eki EK-2/B Listesindeki “normal poliklinik muayenesi” bedeli', parent_section: '2.2.1.B-1', paragraph: '5', list_code: 'EK-2/B', billing_status: 'billable', condition: 'diğer uzmanlık dallarındaki ayakta tedavi kapsamındaki başvurular için normal poliklinik muayenesi bedeli'}
MERGE (s_2_2_1_B_1_2d18d105cd582f162d043c40cd43a7fe:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_2d18d105cd582f162d043c40cd43a7fe)-[:CONTAINS]->(n_2d18d105cd582f162d043c40cd43a7fe)
;

MERGE (n_28b44903939b491d53bdfa2fe868da95:RegulatoryList {code: 'EK-2/A-2'})
SET n_28b44903939b491d53bdfa2fe868da95 += {uid: '28b44903939b491d53bdfa2fe868da95', text: 'SUT eki EK-2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılacaktır', parent_section: '2.2.1.B-1', paragraph: '5', list_code: 'EK-2/A-2', billing_status: 'billable', condition: 'diğer uzmanlık dallarındaki ayakta tedavi başvurularında bu listede yer alan işlemlerin yapılması halinde'}
MERGE (s_2_2_1_B_1_28b44903939b491d53bdfa2fe868da95:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_28b44903939b491d53bdfa2fe868da95)-[:CONTAINS]->(n_28b44903939b491d53bdfa2fe868da95)
;

MERGE (n_e6d0a8f1b529301b54d7ea59bd1bff23:Rule:BillingRule {uid: 'e6d0a8f1b529301b54d7ea59bd1bff23'})
SET n_e6d0a8f1b529301b54d7ea59bd1bff23 += {uid: 'e6d0a8f1b529301b54d7ea59bd1bff23', text: 'yatarak tedavi kapsamında hizmet başına ödeme yöntemi ile bir işlem yapılması durumunda; SUT eki EK-2/A Listesinde yer alan tutarlar faturalandırılmayacak olup ayaktan yapılan işlemler hizmet başına ödeme yöntemine göre faturalandırılacaktır.', parent_section: '2.2.1.B-1', paragraph: '5', rule_type: 'outpatient_to_inpatient_same_day', condition: 'yatarak tedavi kapsamında hizmet başına ödeme yöntemi ile bir işlem yapılması', non_billable_items: 'SUT eki EK-2/A Listesinde yer alan tutarlar', outpatient_billing: 'hizmet başına ödeme yöntemi', note: 'ayaktan yapılan tüm işlemler hizmet başına ödeme yöntemine göre faturalandırılır'}
MERGE (s_2_2_1_B_1_e6d0a8f1b529301b54d7ea59bd1bff23:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_e6d0a8f1b529301b54d7ea59bd1bff23)-[:CONTAINS]->(n_e6d0a8f1b529301b54d7ea59bd1bff23)
;

MERGE (n_c0e2a0c1bce6d4ca146037b2131dde75:RegulatoryList {code: 'EK-2/A'})
SET n_c0e2a0c1bce6d4ca146037b2131dde75 += {uid: 'c0e2a0c1bce6d4ca146037b2131dde75', text: 'SUT eki EK-2/A Listesinde yer alan tutarlar faturalandırılmayacak', parent_section: '2.2.1.B-1', paragraph: '5', list_code: 'EK-2/A', billing_status: 'not_billable', condition: 'yatarak tedavi kapsamında hizmet başına ödeme yöntemi ile işlem yapılması'}
MERGE (s_2_2_1_B_1_c0e2a0c1bce6d4ca146037b2131dde75:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_c0e2a0c1bce6d4ca146037b2131dde75)-[:CONTAINS]->(n_c0e2a0c1bce6d4ca146037b2131dde75)
;

MERGE (n_5fd082958834346a0e247a1b10307a59:Rule:BillingRule {uid: '5fd082958834346a0e247a1b10307a59'})
SET n_5fd082958834346a0e247a1b10307a59 += {uid: '5fd082958834346a0e247a1b10307a59', text: 'Hastanın, aynı gün içinde aynı sağlık hizmeti sunucusunda ilk muayenesini takip eden diğer uzmanlık dallarındaki ayakta tedavi kapsamında yer alan başvuruları, “ayakta tedavilerde ödeme” uygulaması kapsamında değerlendirilmez', parent_section: '2.2.1.B-1', paragraph: '6', rule_type: 'restriction', condition: 'aynı gün, aynı sağlık hizmeti sunucusunda ilk muayeneyi takip eden diğer uzmanlık dallarına ayakta başvurular', care_setting: 'ayakta tedavi', non_billable_items: 'SUT eki EK-2/A Listesinde yer alan tutarlar', exception: 'EK-2/B \'normal poliklinik muayenesi\' ve EK-2/A-2 işlemleri'}
MERGE (s_2_2_1_B_1_5fd082958834346a0e247a1b10307a59:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_5fd082958834346a0e247a1b10307a59)-[:CONTAINS]->(n_5fd082958834346a0e247a1b10307a59)
;

MERGE (n_8ce279308c0d47adef159bf01eaad085:RegulatoryList {code: 'EK-2/A'})
SET n_8ce279308c0d47adef159bf01eaad085 += {uid: '8ce279308c0d47adef159bf01eaad085', text: 'SUT eki EK-2/A Listesinde yer alan tutarlar faturalandırılamaz', parent_section: '2.2.1.B-1', paragraph: '6', list_code: 'EK-2/A', billing_status: 'not_billable', condition: 'aynı gün, aynı sağlık hizmeti sunucusunda ilk muayeneyi takip eden diğer uzmanlık dallarına ayakta başvurular'}
MERGE (s_2_2_1_B_1_8ce279308c0d47adef159bf01eaad085:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_8ce279308c0d47adef159bf01eaad085)-[:CONTAINS]->(n_8ce279308c0d47adef159bf01eaad085)
;

MERGE (n_2d18d105cd582f162d043c40cd43a7fe:RegulatoryList {code: 'EK-2/B'})
SET n_2d18d105cd582f162d043c40cd43a7fe += {uid: '2d18d105cd582f162d043c40cd43a7fe', text: 'SUT eki EK-2/B Listesindeki “normal poliklinik muayenesi” bedeli ... faturalandırılacaktır', parent_section: '2.2.1.B-1', paragraph: '6', list_code: 'EK-2/B', billing_status: 'billable', condition: 'aynı gün, aynı sağlık hizmeti sunucusunda ilk muayeneyi takip eden diğer uzmanlık dallarına ayakta başvurular', list_name: 'normal poliklinik muayenesi (İlgili madde kapsamında)'}
MERGE (s_2_2_1_B_1_2d18d105cd582f162d043c40cd43a7fe:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_2d18d105cd582f162d043c40cd43a7fe)-[:CONTAINS]->(n_2d18d105cd582f162d043c40cd43a7fe)
;

MERGE (n_28b44903939b491d53bdfa2fe868da95:RegulatoryList {code: 'EK-2/A-2'})
SET n_28b44903939b491d53bdfa2fe868da95 += {uid: '28b44903939b491d53bdfa2fe868da95', text: 'SUT eki EK-2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılacaktır', parent_section: '2.2.1.B-1', paragraph: '6', list_code: 'EK-2/A-2', billing_status: 'billable', condition: 'aynı gün, aynı sağlık hizmeti sunucusunda ilk muayeneyi takip eden diğer uzmanlık dallarına ayakta başvurular'}
MERGE (s_2_2_1_B_1_28b44903939b491d53bdfa2fe868da95:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_28b44903939b491d53bdfa2fe868da95)-[:CONTAINS]->(n_28b44903939b491d53bdfa2fe868da95)
;

MERGE (n_c3547a2b3a04844c8c3f7476ee12f466:Rule:BillingRule {uid: 'c3547a2b3a04844c8c3f7476ee12f466'})
SET n_c3547a2b3a04844c8c3f7476ee12f466 += {uid: 'c3547a2b3a04844c8c3f7476ee12f466', text: 'Hastanın aynı gün içinde aynı sağlık hizmeti sunucusundaki ilk başvurusunun ana dal, sonraki başvurusunun yan dal olması durumunda yan dala olan başvuru "ayakta tedavilerde ödeme” uygulaması kapsamında faturalandırılır', parent_section: '2.2.1.B-1', paragraph: '7', rule_type: 'permission', condition: 'aynı gün, aynı sağlık hizmeti sunucusunda ilk başvuru ana dal, sonraki başvuru yan dal', care_setting: 'ayakta tedavi', billable_items: 'yan dal başvurusu, ayakta tedavilerde ödeme uygulaması kapsamında'}
MERGE (s_2_2_1_B_1_c3547a2b3a04844c8c3f7476ee12f466:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_c3547a2b3a04844c8c3f7476ee12f466)-[:CONTAINS]->(n_c3547a2b3a04844c8c3f7476ee12f466)
;

MERGE (n_9d03dac1a5084903d10ffacba0480e66:Rule:BillingRule {uid: '9d03dac1a5084903d10ffacba0480e66'})
SET n_9d03dac1a5084903d10ffacba0480e66 += {uid: '9d03dac1a5084903d10ffacba0480e66', text: 'Ana dala başvuru ise, SUT eki EK-2/A Listesinde yer alan tutarlar girilmeksizin, SUT eki EK-2/B Listesindeki “normal poliklinik muayenesi” bedeli ve yapılması halinde SUT eki EK-2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılabilir', parent_section: '2.2.1.B-1', paragraph: '7', rule_type: 'restriction', condition: 'aynı gün, aynı sağlık hizmeti sunucusunda ilk başvuru ana dal, sonraki başvuru yan dal', non_billable_items: 'EK-2/A Listesi tutarları (ana dal başvurusu için)', billable_items: 'EK-2/B \'normal poliklinik muayenesi\' bedeli ve EK-2/A-2 Listesi işlemleri (ana dal başvurusu için)'}
MERGE (s_2_2_1_B_1_9d03dac1a5084903d10ffacba0480e66:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_9d03dac1a5084903d10ffacba0480e66)-[:CONTAINS]->(n_9d03dac1a5084903d10ffacba0480e66)
;

MERGE (n_9ae6cef89c561399cdff573e0b39ec91:RegulatoryList {code: 'EK-2/A'})
SET n_9ae6cef89c561399cdff573e0b39ec91 += {uid: '9ae6cef89c561399cdff573e0b39ec91', text: 'SUT eki EK -2/A Listesinde yer alan tutarlar girilmeksizin', parent_section: '2.2.1.B-1', paragraph: '7', list_code: 'EK-2/A', billing_status: 'not_billable', condition: 'aynı gün, aynı sağlık hizmeti sunucusunda ilk başvuru ana dal olup, ana dala başvuru için faturalandırma'}
MERGE (s_2_2_1_B_1_9ae6cef89c561399cdff573e0b39ec91:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_9ae6cef89c561399cdff573e0b39ec91)-[:CONTAINS]->(n_9ae6cef89c561399cdff573e0b39ec91)
;

MERGE (n_dec0ce2894ef2d44a8466124a2748d2c:RegulatoryList {code: 'EK-2/B'})
SET n_dec0ce2894ef2d44a8466124a2748d2c += {uid: 'dec0ce2894ef2d44a8466124a2748d2c', text: 'SUT eki EK -2/B Listesindeki “normal poliklinik muayenesi” bedeli', parent_section: '2.2.1.B-1', paragraph: '7', list_code: 'EK-2/B', billing_status: 'billable', condition: 'aynı gün, aynı sağlık hizmeti sunucusunda ilk başvuru ana dal, sonraki başvuru yan dal; ana dal başvurusu için', list_name: 'normal poliklinik muayenesi (İlgili madde kapsamında)'}
MERGE (s_2_2_1_B_1_dec0ce2894ef2d44a8466124a2748d2c:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_dec0ce2894ef2d44a8466124a2748d2c)-[:CONTAINS]->(n_dec0ce2894ef2d44a8466124a2748d2c)
;

MERGE (n_a92a53a51f71c3dd5c15199be9cb462c:RegulatoryList {code: 'EK-2/A-2'})
SET n_a92a53a51f71c3dd5c15199be9cb462c += {uid: 'a92a53a51f71c3dd5c15199be9cb462c', text: 'SUT eki EK-2/A-2 Listesinde yer alan işlemlerin bedelleri faturalandırılabilir', parent_section: '2.2.1.B-1', paragraph: '7', list_code: 'EK-2/A-2', billing_status: 'billable', condition: 'aynı gün, aynı sağlık hizmeti sunucusunda ilk başvuru ana dal, sonraki başvuru yan dal; ana dal başvurusu için'}
MERGE (s_2_2_1_B_1_a92a53a51f71c3dd5c15199be9cb462c:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_a92a53a51f71c3dd5c15199be9cb462c)-[:CONTAINS]->(n_a92a53a51f71c3dd5c15199be9cb462c)
;

MERGE (n_9127befdfc4ff4220078fc56e046a258:Rule:BillingRule {uid: '9127befdfc4ff4220078fc56e046a258'})
SET n_9127befdfc4ff4220078fc56e046a258 += {uid: '9127befdfc4ff4220078fc56e046a258', text: 'Sağlık raporu ile yapılması gerekli görülen hiperbarik oksijen tedavisi, fizik tedavi ve rehabilitasyon, ESWL ve ESWT tedavilerinde; ... bu sağlık raporu ile yapılan tedavi başvuruları "ayakta tedavilerde ödeme” uygulaması kapsamında SUT eki EK-2/A Listesinde yer alan tutarlar girilmeksizin SUT eki EK-2/C Listesi üzerinden faturalandırılır', parent_section: '2.2.1.B-1', paragraph: '8', rule_type: 'restriction', condition: 'sağlık raporu ile gerekli görülen hiperbarik oksijen tedavisi, fizik tedavi ve rehabilitasyon, ESWL, ESWT; ayaktan başvurularda rapor düzenlendikten sonraki günlerde aynı veya başka bir sağlık hizmeti sunucusunda yapılması', billable_items: 'SUT eki EK-2/C Listesi işlemleri', non_billable_items: 'SUT eki EK-2/A Listesinde yer alan tutarlar', care_setting: 'ayakta tedavi', exception: 'sağlık raporu ile yapılan bu tedavi başvurularında EK-2/A tutarları girilmez'}
MERGE (s_2_2_1_B_1_9127befdfc4ff4220078fc56e046a258:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_9127befdfc4ff4220078fc56e046a258)-[:CONTAINS]->(n_9127befdfc4ff4220078fc56e046a258)
;

MERGE (n_8ce279308c0d47adef159bf01eaad085:RegulatoryList {code: 'EK-2/A'})
SET n_8ce279308c0d47adef159bf01eaad085 += {uid: '8ce279308c0d47adef159bf01eaad085', text: 'SUT eki EK-2/A Listesinde yer alan tutarlar girilmeksizin', parent_section: '2.2.1.B-1', paragraph: '8', list_code: 'EK-2/A', billing_status: 'not_billable', condition: 'sağlık raporu ile yapılan hiperbarik oksijen, fizik tedavi ve rehabilitasyon, ESWL, ESWT tedavilerinde ayakta tedavilerde ödeme uygulaması kapsamında'}
MERGE (s_2_2_1_B_1_8ce279308c0d47adef159bf01eaad085:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_8ce279308c0d47adef159bf01eaad085)-[:CONTAINS]->(n_8ce279308c0d47adef159bf01eaad085)
;

MERGE (n_1bcfc64d8ffea9f9b1a6b1b437a356f3:RegulatoryList {code: 'EK-2/C'})
SET n_1bcfc64d8ffea9f9b1a6b1b437a356f3 += {uid: '1bcfc64d8ffea9f9b1a6b1b437a356f3', text: 'SUT eki EK-2/C Listesi üzerinden faturalandırılır', parent_section: '2.2.1.B-1', paragraph: '8', list_code: 'EK-2/C', billing_status: 'billable', condition: 'sağlık raporu ile yapılan hiperbarik oksijen, fizik tedavi ve rehabilitasyon, ESWL, ESWT tedavilerinde ayakta tedavilerde ödeme uygulaması kapsamında'}
MERGE (s_2_2_1_B_1_1bcfc64d8ffea9f9b1a6b1b437a356f3:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_1bcfc64d8ffea9f9b1a6b1b437a356f3)-[:CONTAINS]->(n_1bcfc64d8ffea9f9b1a6b1b437a356f3)
;

MERGE (n_4e1ee24ef58a08fc406798edc376b495:Rule:CoverageRule {uid: '4e1ee24ef58a08fc406798edc376b495'})
SET n_4e1ee24ef58a08fc406798edc376b495 += {uid: '4e1ee24ef58a08fc406798edc376b495', text: 'Sağlık raporu ile yapılması gerekli görülen hiperbarik oksijen tedavisi, fizik tedavi ve rehabilitasyon, ESWL ve ESWT tedavileri', parent_section: '2.2.1.B-1', paragraph: '8', item_category: 'belirli tedavi türleri', usage_condition: 'sağlık raporu ile gerekli görülmesi ve ayaktan tedavide, rapor sonrası günlerde uygulanması', coverage_status: 'conditional', document_requirement: 'sağlık raporu'}
MERGE (s_2_2_1_B_1_4e1ee24ef58a08fc406798edc376b495:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_4e1ee24ef58a08fc406798edc376b495)-[:CONTAINS]->(n_4e1ee24ef58a08fc406798edc376b495)
;

MERGE (n_c59da334d16ffdc87c07a9ee06af1736:MedicalService {uid: 'c59da334d16ffdc87c07a9ee06af1736'})
SET n_c59da334d16ffdc87c07a9ee06af1736 += {uid: 'c59da334d16ffdc87c07a9ee06af1736', text: 'hiperbarik oksijen tedavisi', parent_section: '2.2.1.B-1', paragraph: '8', name: 'hiperbarik oksijen tedavisi', service_type: 'hyperbaric_oxygen', coverage_status: 'conditional'}
MERGE (s_2_2_1_B_1_c59da334d16ffdc87c07a9ee06af1736:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_c59da334d16ffdc87c07a9ee06af1736)-[:CONTAINS]->(n_c59da334d16ffdc87c07a9ee06af1736)
;

MERGE (n_6a2b9b30505eaee90ba88aabdcc71e5b:MedicalService {uid: '6a2b9b30505eaee90ba88aabdcc71e5b'})
SET n_6a2b9b30505eaee90ba88aabdcc71e5b += {uid: '6a2b9b30505eaee90ba88aabdcc71e5b', text: 'fizik tedavi ve rehabilitasyon', parent_section: '2.2.1.B-1', paragraph: '8', name: 'fizik tedavi ve rehabilitasyon', service_type: 'physical_therapy_rehabilitation', coverage_status: 'conditional'}
MERGE (s_2_2_1_B_1_6a2b9b30505eaee90ba88aabdcc71e5b:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_6a2b9b30505eaee90ba88aabdcc71e5b)-[:CONTAINS]->(n_6a2b9b30505eaee90ba88aabdcc71e5b)
;

MERGE (n_9872261d17a486bdea15a07a30e9e007:MedicalService {uid: '9872261d17a486bdea15a07a30e9e007'})
SET n_9872261d17a486bdea15a07a30e9e007 += {uid: '9872261d17a486bdea15a07a30e9e007', text: 'ESWL tedavisi', parent_section: '2.2.1.B-1', paragraph: '8', name: 'ESWL tedavisi', service_type: 'ESWL', coverage_status: 'conditional'}
MERGE (s_2_2_1_B_1_9872261d17a486bdea15a07a30e9e007:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_9872261d17a486bdea15a07a30e9e007)-[:CONTAINS]->(n_9872261d17a486bdea15a07a30e9e007)
;

MERGE (n_3c2efa6809a2435511273dd0878b7b70:MedicalService {uid: '3c2efa6809a2435511273dd0878b7b70'})
SET n_3c2efa6809a2435511273dd0878b7b70 += {uid: '3c2efa6809a2435511273dd0878b7b70', text: 'ESWT tedavisi', parent_section: '2.2.1.B-1', paragraph: '8', name: 'ESWT tedavisi', service_type: 'ESWT', coverage_status: 'conditional'}
MERGE (s_2_2_1_B_1_3c2efa6809a2435511273dd0878b7b70:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_3c2efa6809a2435511273dd0878b7b70)-[:CONTAINS]->(n_3c2efa6809a2435511273dd0878b7b70)
;

MERGE (n_03464148a056f2a80de72da730a8cbb9:Rule:PaymentRule {uid: '03464148a056f2a80de72da730a8cbb9'})
SET n_03464148a056f2a80de72da730a8cbb9 += {uid: '03464148a056f2a80de72da730a8cbb9', text: 'Hastanın, ikinci veya üçüncü basamak sağlık hizmeti sunucusundan başka bir sağlık hizmeti sunucusuna sevk edilmesi halinde sevk eden sağlık kurumuna, SUT eki EK-2/A Listesinde yer alan tutarın %75’i ödenir', parent_section: '2.2.1.B-1', paragraph: '9', payment_type: 'per_referral', amount: '75', amount_text: '%75', condition: 'hastanın ikinci veya üçüncü basamak sağlık hizmeti sunucusundan başka bir sağlık hizmeti sunucusuna sevk edilmesi', healthcare_level: 'ikinci basamak,üçüncü basamak'}
MERGE (s_2_2_1_B_1_03464148a056f2a80de72da730a8cbb9:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_03464148a056f2a80de72da730a8cbb9)-[:CONTAINS]->(n_03464148a056f2a80de72da730a8cbb9)
MERGE (p_ikinci_basamak_03464148a056f2a80de72da730a8cbb9_0:ProviderType {level: 'ikinci basamak'})
MERGE (n_03464148a056f2a80de72da730a8cbb9)-[:APPLIES_TO]->(p_ikinci_basamak_03464148a056f2a80de72da730a8cbb9_0)
MERGE (p_nc_basamak_03464148a056f2a80de72da730a8cbb9_1:ProviderType {level: 'üçüncü basamak'})
MERGE (n_03464148a056f2a80de72da730a8cbb9)-[:APPLIES_TO]->(p_nc_basamak_03464148a056f2a80de72da730a8cbb9_1)
;

MERGE (n_4dc9b8c69c38040856ddfcdbf45abe8d:Rule:BillingRule {uid: '4dc9b8c69c38040856ddfcdbf45abe8d'})
SET n_4dc9b8c69c38040856ddfcdbf45abe8d += {uid: '4dc9b8c69c38040856ddfcdbf45abe8d', text: 'sevk eden sağlık kurumuna, SUT eki EK-2/A Listesinde yer alan tutarın %75’i ödenir', parent_section: '2.2.1.B-1', paragraph: '9', rule_type: 'payment_sharing', condition: 'ikinci veya üçüncü basamak sağlık hizmeti sunucusundan başka bir sağlık hizmeti sunucusuna sevk', billable_items: 'SUT eki EK-2/A Listesindeki işlem tutarının %75’i sevk eden kuruma ödenir', list_reference: 'EK-2/A'}
MERGE (s_2_2_1_B_1_4dc9b8c69c38040856ddfcdbf45abe8d:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_4dc9b8c69c38040856ddfcdbf45abe8d)-[:CONTAINS]->(n_4dc9b8c69c38040856ddfcdbf45abe8d)
MERGE (l_EK_2_A_4dc9b8c69c38040856ddfcdbf45abe8d_0:RegulatoryList {code: 'EK-2/A'})
MERGE (n_4dc9b8c69c38040856ddfcdbf45abe8d)-[:REFERENCES_LIST]->(l_EK_2_A_4dc9b8c69c38040856ddfcdbf45abe8d_0)
;

MERGE (n_39969530ca9c77a9f074a81874353dc1:RegulatoryList {code: 'EK-2/A'})
SET n_39969530ca9c77a9f074a81874353dc1 += {uid: '39969530ca9c77a9f074a81874353dc1', text: 'SUT eki EK-2/A Listesinde yer alan tutarın %75’i ödenir', parent_section: '2.2.1.B-1', paragraph: '9', list_code: 'EK-2/A', billing_status: 'billable', condition: 'ikinci veya üçüncü basamak sağlık hizmeti sunucusundan başka bir sağlık hizmeti sunucusuna sevk edilen hasta için sevk eden kuruma ödeme'}
MERGE (s_2_2_1_B_1_39969530ca9c77a9f074a81874353dc1:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_39969530ca9c77a9f074a81874353dc1)-[:CONTAINS]->(n_39969530ca9c77a9f074a81874353dc1)
;

MERGE (n_eceed23bec2e5e8ed5e562ced60b2332:Rule:BillingRule {uid: 'eceed23bec2e5e8ed5e562ced60b2332'})
SET n_eceed23bec2e5e8ed5e562ced60b2332 += {uid: 'eceed23bec2e5e8ed5e562ced60b2332', text: 'Ayakta tedavilerde ödeme uygulamasında, SUT eki EK-2/A-2 Listesinde yer alan işlemlerin faturalandırılmasında aşağıdaki hususlara uyulur', parent_section: '2.2.1.B-1', paragraph: '10', rule_type: 'restriction', condition: 'ayakta tedavilerde EK-2/A-2 Listesi işlemlerinin faturalandırılması', list_reference: 'EK-2/A-2'}
MERGE (s_2_2_1_B_1_eceed23bec2e5e8ed5e562ced60b2332:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_eceed23bec2e5e8ed5e562ced60b2332)-[:CONTAINS]->(n_eceed23bec2e5e8ed5e562ced60b2332)
MERGE (l_EK_2_A_2_eceed23bec2e5e8ed5e562ced60b2332_0:RegulatoryList {code: 'EK-2/A-2'})
MERGE (n_eceed23bec2e5e8ed5e562ced60b2332)-[:REFERENCES_LIST]->(l_EK_2_A_2_eceed23bec2e5e8ed5e562ced60b2332_0)
;

MERGE (n_b25c57cf1c8825759d1e180c1a8bee32:RegulatoryList {code: 'EK-2/A-2'})
SET n_b25c57cf1c8825759d1e180c1a8bee32 += {uid: 'b25c57cf1c8825759d1e180c1a8bee32', text: 'SUT eki EK-2/A-2 Listesinde yer alan işlemler', parent_section: '2.2.1.B-1', paragraph: '10', list_code: 'EK-2/A-2', billing_status: 'billable', condition: 'ayakta tedavilerde ödeme uygulaması kapsamında, (10) uncu fıkradaki kurallara göre'}
MERGE (s_2_2_1_B_1_b25c57cf1c8825759d1e180c1a8bee32:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_b25c57cf1c8825759d1e180c1a8bee32)-[:CONTAINS]->(n_b25c57cf1c8825759d1e180c1a8bee32)
;

MERGE (n_387c162c0cadd73ac73f4a3aa8c65f3c:Rule:BillingRule {uid: '387c162c0cadd73ac73f4a3aa8c65f3c'})
SET n_387c162c0cadd73ac73f4a3aa8c65f3c += {uid: '387c162c0cadd73ac73f4a3aa8c65f3c', text: 'İşlemin SUT eki EK-2/C Listesinde yer alması halinde bedelleri tanıya dayalı işlem üzerinden ödeme yöntemi ile faturalandırılır', parent_section: '2.2.1.B-1', paragraph: '10', item: 'a', rule_type: 'permission', condition: 'işlemin EK-2/C Listesinde yer alması', billable_items: 'EK-2/C Listesindeki işlemin bedeli', list_reference: 'EK-2/C', payment_method: 'tanıya dayalı işlem üzerinden ödeme'}
MERGE (s_2_2_1_B_1_387c162c0cadd73ac73f4a3aa8c65f3c:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_387c162c0cadd73ac73f4a3aa8c65f3c)-[:CONTAINS]->(n_387c162c0cadd73ac73f4a3aa8c65f3c)
MERGE (l_EK_2_C_387c162c0cadd73ac73f4a3aa8c65f3c_0:RegulatoryList {code: 'EK-2/C'})
MERGE (n_387c162c0cadd73ac73f4a3aa8c65f3c)-[:REFERENCES_LIST]->(l_EK_2_C_387c162c0cadd73ac73f4a3aa8c65f3c_0)
;

MERGE (n_0187ccfd1b690ec5103846d45ec451c3:RegulatoryList {code: 'EK-2/C'})
SET n_0187ccfd1b690ec5103846d45ec451c3 += {uid: '0187ccfd1b690ec5103846d45ec451c3', text: 'SUT eki EK-2/C Listesinde yer alması halinde bedelleri tanıya dayalı işlem üzerinden ödeme yöntemi ile faturalandırılır', parent_section: '2.2.1.B-1', paragraph: '10', item: 'a', list_code: 'EK-2/C', billing_status: 'billable', condition: 'EK-2/A-2 Listesindeki işlemin ayrıca EK-2/C Listesinde yer alması'}
MERGE (s_2_2_1_B_1_0187ccfd1b690ec5103846d45ec451c3:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_0187ccfd1b690ec5103846d45ec451c3)-[:CONTAINS]->(n_0187ccfd1b690ec5103846d45ec451c3)
;

MERGE (n_bf41ee17cda2049b5babcd5fbffe5d2c:Rule:BillingRule {uid: 'bf41ee17cda2049b5babcd5fbffe5d2c'})
SET n_bf41ee17cda2049b5babcd5fbffe5d2c += {uid: 'bf41ee17cda2049b5babcd5fbffe5d2c', text: 'Bu işleme ilişkin tanıya dayalı işlem üzerinden ödeme yöntemine dâhil olmayan tıbbi malzeme ve ilaç bedelleri ayrıca faturalandırılabilir', parent_section: '2.2.1.B-1', paragraph: '10', item: 'a', rule_type: 'permission', condition: 'EK-2/C kapsamında tanıya dayalı işlem üzerinden ödeme yöntemi kullanılması', billable_items: 'tanıya dayalı işleme dahil olmayan tıbbi malzeme ve ilaç bedelleri', payment_method: 'ayrıca faturalandırma'}
MERGE (s_2_2_1_B_1_bf41ee17cda2049b5babcd5fbffe5d2c:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_bf41ee17cda2049b5babcd5fbffe5d2c)-[:CONTAINS]->(n_bf41ee17cda2049b5babcd5fbffe5d2c)
;

MERGE (n_b89a70286daad57fb0004d1c11a00fdb:Rule:BillingRule {uid: 'b89a70286daad57fb0004d1c11a00fdb'})
SET n_b89a70286daad57fb0004d1c11a00fdb += {uid: 'b89a70286daad57fb0004d1c11a00fdb', text: 'İşlemin sadece SUT eki EK-2/B Listesinde yer alması halinde, SUT eki EK-2/A Listesinde yer alan tutarlara ilave olarak işlem bedeli ve bu işlemle ilgili ilaç ve tıbbi malzeme bedelleri ayrıca faturalandırılabilir', parent_section: '2.2.1.B-1', paragraph: '10', item: 'b', rule_type: 'permission', condition: 'işlemin sadece EK-2/B Listesinde yer alması', billable_items: 'işlem bedeli, bu işlemle ilgili ilaç ve tıbbi malzeme bedelleri', list_reference: 'EK-2/B', additional_to: 'EK-2/A Listesindeki tutarlar'}
MERGE (s_2_2_1_B_1_b89a70286daad57fb0004d1c11a00fdb:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_b89a70286daad57fb0004d1c11a00fdb)-[:CONTAINS]->(n_b89a70286daad57fb0004d1c11a00fdb)
MERGE (l_EK_2_B_b89a70286daad57fb0004d1c11a00fdb_0:RegulatoryList {code: 'EK-2/B'})
MERGE (n_b89a70286daad57fb0004d1c11a00fdb)-[:REFERENCES_LIST]->(l_EK_2_B_b89a70286daad57fb0004d1c11a00fdb_0)
;

MERGE (n_561516dcf1abd76ba868c754f3b2a19c:RegulatoryList {code: 'EK-2/B'})
SET n_561516dcf1abd76ba868c754f3b2a19c += {uid: '561516dcf1abd76ba868c754f3b2a19c', text: 'SUT eki EK-2/B Listesinde yer alması', parent_section: '2.2.1.B-1', paragraph: '10', item: 'b', list_code: 'EK-2/B', billing_status: 'billable', condition: 'işlemin sadece EK-2/B Listesinde yer alması'}
MERGE (s_2_2_1_B_1_561516dcf1abd76ba868c754f3b2a19c:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_561516dcf1abd76ba868c754f3b2a19c)-[:CONTAINS]->(n_561516dcf1abd76ba868c754f3b2a19c)
;

MERGE (n_cc2d28848176e3746fd0d4c599c9a83a:RegulatoryList {code: 'EK-2/A'})
SET n_cc2d28848176e3746fd0d4c599c9a83a += {uid: 'cc2d28848176e3746fd0d4c599c9a83a', text: 'SUT eki EK-2/A Listesinde yer alan tutarlara ilave olarak', parent_section: '2.2.1.B-1', paragraph: '10', item: 'b', list_code: 'EK-2/A', billing_status: 'billable', condition: 'EK-2/B işlemlerinin işlem bedeli ve ilgili ilaç/tıbbi malzeme ile birlikte faturalandırılması'}
MERGE (s_2_2_1_B_1_cc2d28848176e3746fd0d4c599c9a83a:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_cc2d28848176e3746fd0d4c599c9a83a)-[:CONTAINS]->(n_cc2d28848176e3746fd0d4c599c9a83a)
;

MERGE (n_bc8ac410339b1c9e844198454ef204ad:Rule:BillingRule {uid: 'bc8ac410339b1c9e844198454ef204ad'})
SET n_bc8ac410339b1c9e844198454ef204ad += {uid: 'bc8ac410339b1c9e844198454ef204ad', text: 'Sağlık Bakanlığına bağlı eğitim ve araştırma hastaneleri ile tıp fakülteleri bulunan üniversite sağlık uygulama ve araştırma merkezleri tarafından EK-2/A-2 Listesinde yer alan işlemler işlem puanlarına %10 oranında ilave edilerek faturalandırılır', parent_section: '2.2.1.B-1', paragraph: '10', item: 'c', rule_type: 'quota_adjustment', condition: 'Sağlık Bakanlığı eğitim ve araştırma hastaneleri, Tıp Fakülteleri Bulunan Devlet/Vakıf Üniversiteleri Sağlık Uygulama ve Araştırma Merkezleri tarafından yapılması', billable_items: 'EK-2/A-2 Listesindeki işlemler', adjustment: '%10 artış', affected_metric: 'işlem puanı', per: 'işlem'}
MERGE (s_2_2_1_B_1_bc8ac410339b1c9e844198454ef204ad:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_bc8ac410339b1c9e844198454ef204ad)-[:CONTAINS]->(n_bc8ac410339b1c9e844198454ef204ad)
;

MERGE (n_918fb1e45b1012897a58c96f235d40d1:Scope {uid: '918fb1e45b1012897a58c96f235d40d1'})
SET n_918fb1e45b1012897a58c96f235d40d1 += {uid: '918fb1e45b1012897a58c96f235d40d1', text: 'Sağlık Bakanlığına bağlı eğitim ve araştırma hastaneler, Tıp Fakülteleri Bulunan Devlet Üniversiteleri Sağlık Uygulama ve Araştırma Merkezleri, Tıp Fakülteleri Bulunan Vakıf Üniversiteleri Sağlık Uygulama ve Araştırma Merkezleri', parent_section: '2.2.1.B-1', paragraph: '10', item: 'c', applicable_level: 'ikinci basamak,üçüncü basamak', provider_type: 'eğitim ve araştırma hastaneleri ile üniversite sağlık uygulama ve araştırma merkezleri'}
MERGE (s_2_2_1_B_1_918fb1e45b1012897a58c96f235d40d1:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_918fb1e45b1012897a58c96f235d40d1)-[:CONTAINS]->(n_918fb1e45b1012897a58c96f235d40d1)
MERGE (p_ikinci_basamak_918fb1e45b1012897a58c96f235d40d1_0:ProviderType {level: 'ikinci basamak'})
MERGE (n_918fb1e45b1012897a58c96f235d40d1)-[:APPLIES_TO]->(p_ikinci_basamak_918fb1e45b1012897a58c96f235d40d1_0)
MERGE (p_nc_basamak_918fb1e45b1012897a58c96f235d40d1_1:ProviderType {level: 'üçüncü basamak'})
MERGE (n_918fb1e45b1012897a58c96f235d40d1)-[:APPLIES_TO]->(p_nc_basamak_918fb1e45b1012897a58c96f235d40d1_1)
;

MERGE (n_fd3cc4dce611fde43e4a84610b8a7d81:RegulatoryList {code: 'EK-2/A-2'})
SET n_fd3cc4dce611fde43e4a84610b8a7d81 += {uid: 'fd3cc4dce611fde43e4a84610b8a7d81', text: 'SUT eki EK-2/A-2 Listesinde yer alan işlemler, işlem puanlarına %10 oranında ilave edilerek faturalandırılır', parent_section: '2.2.1.B-1', paragraph: '10', item: 'c', list_code: 'EK-2/A-2', billing_status: 'billable', condition: 'belirtilen eğitim ve araştırma hastaneleri/üniversite merkezleri tarafından yapılması, işlem puanına %10 ilave'}
MERGE (s_2_2_1_B_1_fd3cc4dce611fde43e4a84610b8a7d81:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_fd3cc4dce611fde43e4a84610b8a7d81)-[:CONTAINS]->(n_fd3cc4dce611fde43e4a84610b8a7d81)
;

MERGE (n_87a160114ddbf657658d365505c7aa40:Amendment {uid: '87a160114ddbf657658d365505c7aa40'})
SET n_87a160114ddbf657658d365505c7aa40 += {uid: '87a160114ddbf657658d365505c7aa40', text: 'ikinci ve üçüncü basamak özel sağlık hizmeti sunucuları ibaresinin mülga olması', parent_section: '2.2.1.B-1', amendment_type: 'mülga', official_gazette_date: '16/03/2023', official_gazette_number: '32134', article_reference: '5 md.', effective_date: '24/03/2023'}
MERGE (s_2_2_1_B_1_87a160114ddbf657658d365505c7aa40:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_87a160114ddbf657658d365505c7aa40)-[:CONTAINS]->(n_87a160114ddbf657658d365505c7aa40)
;

MERGE (n_9e767754aa4fc60cda299a6842135557:Rule:QuotaRule {uid: '9e767754aa4fc60cda299a6842135557'})
SET n_9e767754aa4fc60cda299a6842135557 += {uid: '9e767754aa4fc60cda299a6842135557', text: 'günlük muayene sınırı acil servis/polikliniğe başvurular hariç olmak üzere çalışma saatlerinin 6 ile çarpılması ile bulunur', parent_section: '2.2.1.B-1', paragraph: '11', rule_type: 'daily_examination_limit', provider_type: 'özel sağlık hizmeti sunucuları', healthcare_level: 'ikinci basamak,üçüncü basamak', calculation_formula: 'hekim çalışma saati × 6', care_setting: 'ayaktan başvuru', exception: 'acil servis/poliklinik başvuruları', note: 'metinde geçen ikinci ve üçüncü basamak özel sağlık hizmeti sunucuları ibaresi mülga edilmiştir'}
MERGE (s_2_2_1_B_1_9e767754aa4fc60cda299a6842135557:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_9e767754aa4fc60cda299a6842135557)-[:CONTAINS]->(n_9e767754aa4fc60cda299a6842135557)
MERGE (p_ikinci_basamak_9e767754aa4fc60cda299a6842135557_0:ProviderType {level: 'ikinci basamak'})
MERGE (n_9e767754aa4fc60cda299a6842135557)-[:APPLIES_TO]->(p_ikinci_basamak_9e767754aa4fc60cda299a6842135557_0)
MERGE (p_nc_basamak_9e767754aa4fc60cda299a6842135557_1:ProviderType {level: 'üçüncü basamak'})
MERGE (n_9e767754aa4fc60cda299a6842135557)-[:APPLIES_TO]->(p_nc_basamak_9e767754aa4fc60cda299a6842135557_1)
;

MERGE (n_1cdb16734759aa5e7997785ae9a66e57:Limit {uid: '1cdb16734759aa5e7997785ae9a66e57'})
SET n_1cdb16734759aa5e7997785ae9a66e57 += {uid: '1cdb16734759aa5e7997785ae9a66e57', text: 'Her bir hekim için günlük muayene sayısı her halükarda 60’ı geçemez', parent_section: '2.2.1.B-1', paragraph: '11', limit_type: 'absolute_maximum', metric: 'günlük muayene sayısı', max_value: '60', per: 'hekim', context: 'genel poliklinik, ayaktan başvuru'}
MERGE (s_2_2_1_B_1_1cdb16734759aa5e7997785ae9a66e57:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_1cdb16734759aa5e7997785ae9a66e57)-[:CONTAINS]->(n_1cdb16734759aa5e7997785ae9a66e57)
;

MERGE (n_3c021528530792242665c3b3d4c7342d:Limit {uid: '3c021528530792242665c3b3d4c7342d'})
SET n_3c021528530792242665c3b3d4c7342d += {uid: '3c021528530792242665c3b3d4c7342d', text: 'bir acil servis doktoru için günlük muayene sayısı 90’ı geçemez', parent_section: '2.2.1.B-1', paragraph: '11', limit_type: 'absolute_maximum', metric: 'günlük muayene sayısı', max_value: '90', per: 'acil servis doktoru', context: 'acil servis/poliklinik', note: 'sağlık hizmeti sunucusu ifadesinde geçen ikinci ve üçüncü basamak özel sağlık hizmeti sunucuları ibaresi mülga edilmiştir'}
MERGE (s_2_2_1_B_1_3c021528530792242665c3b3d4c7342d:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_3c021528530792242665c3b3d4c7342d)-[:CONTAINS]->(n_3c021528530792242665c3b3d4c7342d)
;

MERGE (n_75a729dc11d57fa53de3e95a118e1efe:Limit {uid: '75a729dc11d57fa53de3e95a118e1efe'})
SET n_75a729dc11d57fa53de3e95a118e1efe += {uid: '75a729dc11d57fa53de3e95a118e1efe', text: 'Kırmızı alan tarifine giren başvurular olması halinde günlük muayene sayısı 90’ı geçebilir ancak 100’ü geçemez', parent_section: '2.2.1.B-1', paragraph: '11', limit_type: 'absolute_maximum', metric: 'günlük muayene sayısı', max_value: '100', per: 'acil servis doktoru', context: 'acil servis/poliklinik, kırmızı alan triyajı dahil toplam günlük sayı', condition: 'Sağlık Bakanlığının “Yataklı Sağlık Tesislerinde Acil Servis Hizmetlerinin Uygulama Usul ve Esasları Hakkında Tebliğ”e göre triyaj uygulamasında Kırmızı alan tarifine giren acil servis/polikliniğine başvuruların olması', note: 'kırmızı alan başvuruları nedeniyle 90 sınırı aşılabilir, ancak toplam 100’ü geçemez'}
MERGE (s_2_2_1_B_1_75a729dc11d57fa53de3e95a118e1efe:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_75a729dc11d57fa53de3e95a118e1efe)-[:CONTAINS]->(n_75a729dc11d57fa53de3e95a118e1efe)
;

MERGE (n_2849424b291e584bb88590e1e6ba40e0:Scope {uid: '2849424b291e584bb88590e1e6ba40e0'})
SET n_2849424b291e584bb88590e1e6ba40e0 += {uid: '2849424b291e584bb88590e1e6ba40e0', text: 'Sağlık Bakanlığının Acil Servis Hizmetleri Tebliği uyarınca kırmızı alan tanımına giren başvurular', parent_section: '2.2.1.B-1', paragraph: '11', applicable_level: 'ikinci basamak,üçüncü basamak', provider_type: 'özel sağlık hizmeti sunucuları acil servis/poliklinik', geographic_scope: 'Türkiye', note: 'kapsam, Sağlık Bakanlığının “Yataklı Sağlık Tesislerinde Acil Servis Hizmetlerinin Uygulama Usul ve Esasları Hakkında Tebliğ”deki kırmızı alan tanımına atıf yapmaktadır'}
MERGE (s_2_2_1_B_1_2849424b291e584bb88590e1e6ba40e0:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_2849424b291e584bb88590e1e6ba40e0)-[:CONTAINS]->(n_2849424b291e584bb88590e1e6ba40e0)
MERGE (p_ikinci_basamak_2849424b291e584bb88590e1e6ba40e0_0:ProviderType {level: 'ikinci basamak'})
MERGE (n_2849424b291e584bb88590e1e6ba40e0)-[:APPLIES_TO]->(p_ikinci_basamak_2849424b291e584bb88590e1e6ba40e0_0)
MERGE (p_nc_basamak_2849424b291e584bb88590e1e6ba40e0_1:ProviderType {level: 'üçüncü basamak'})
MERGE (n_2849424b291e584bb88590e1e6ba40e0)-[:APPLIES_TO]->(p_nc_basamak_2849424b291e584bb88590e1e6ba40e0_1)
;

MERGE (n_566a399767e590bcfd82d5394af1ff5e:Rule:BillingRule {uid: '566a399767e590bcfd82d5394af1ff5e'})
SET n_566a399767e590bcfd82d5394af1ff5e += {uid: '566a399767e590bcfd82d5394af1ff5e', text: 'Transözefajiyal ekokardiyografi işlemlerinin yapılması durumunda her bir işlem için muayene sayısından bir muayene sayısı düşülerek yeni günlük muayene sayısı hesaplanır', parent_section: '2.2.1.B-1', rule_type: 'quota_adjustment', provider_type: 'özel sağlık hizmeti sunucuları', condition: 'SUT eki EK-2/B Listesindeki 700610 ve 700611 kodlu işlemlerin yapılması', adjustment: '-1 muayene sayısı', per: 'her bir işlem', affected_metric: 'günlük muayene sayısı'}
MERGE (s_2_2_1_B_1_566a399767e590bcfd82d5394af1ff5e:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_566a399767e590bcfd82d5394af1ff5e)-[:CONTAINS]->(n_566a399767e590bcfd82d5394af1ff5e)
;

MERGE (n_8e706a8af4d8bcabc3a6bee3e62aa494:MedicalProcedure {uid: '8e706a8af4d8bcabc3a6bee3e62aa494'})
SET n_8e706a8af4d8bcabc3a6bee3e62aa494 += {uid: '8e706a8af4d8bcabc3a6bee3e62aa494', text: 'Transözefajiyal ekokardiyografi', parent_section: '2.2.1.B-1', code: '700610', name: 'Transözefajiyal ekokardiyografi', list_reference: 'EK-2/B', specialty: 'kardiyoloji', patient_group: 'adult'}
MERGE (s_2_2_1_B_1_8e706a8af4d8bcabc3a6bee3e62aa494:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_8e706a8af4d8bcabc3a6bee3e62aa494)-[:CONTAINS]->(n_8e706a8af4d8bcabc3a6bee3e62aa494)
MERGE (l_EK_2_B_8e706a8af4d8bcabc3a6bee3e62aa494_0:RegulatoryList {code: 'EK-2/B'})
MERGE (n_8e706a8af4d8bcabc3a6bee3e62aa494)-[:REFERENCES_LIST]->(l_EK_2_B_8e706a8af4d8bcabc3a6bee3e62aa494_0)
MERGE (c_700610_8e706a8af4d8bcabc3a6bee3e62aa494:Code {value: '700610'})
MERGE (n_8e706a8af4d8bcabc3a6bee3e62aa494)-[:HAS_CODE]->(c_700610_8e706a8af4d8bcabc3a6bee3e62aa494)
;

MERGE (n_c8cbba669904fb6e0d88eb33da33729a:MedicalProcedure {uid: 'c8cbba669904fb6e0d88eb33da33729a'})
SET n_c8cbba669904fb6e0d88eb33da33729a += {uid: 'c8cbba669904fb6e0d88eb33da33729a', text: 'Transözefajiyal ekokardiyografi, çocuk', parent_section: '2.2.1.B-1', code: '700611', name: 'Transözefajiyal ekokardiyografi, çocuk', list_reference: 'EK-2/B', specialty: 'pediatrik kardiyoloji', patient_group: 'pediatric'}
MERGE (s_2_2_1_B_1_c8cbba669904fb6e0d88eb33da33729a:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_c8cbba669904fb6e0d88eb33da33729a)-[:CONTAINS]->(n_c8cbba669904fb6e0d88eb33da33729a)
MERGE (l_EK_2_B_c8cbba669904fb6e0d88eb33da33729a_0:RegulatoryList {code: 'EK-2/B'})
MERGE (n_c8cbba669904fb6e0d88eb33da33729a)-[:REFERENCES_LIST]->(l_EK_2_B_c8cbba669904fb6e0d88eb33da33729a_0)
MERGE (c_700611_c8cbba669904fb6e0d88eb33da33729a:Code {value: '700611'})
MERGE (n_c8cbba669904fb6e0d88eb33da33729a)-[:HAS_CODE]->(c_700611_c8cbba669904fb6e0d88eb33da33729a)
;

MERGE (n_bb315e9883dede9b413a8941baeaf033:Amendment {uid: 'bb315e9883dede9b413a8941baeaf033'})
SET n_bb315e9883dede9b413a8941baeaf033 += {uid: 'bb315e9883dede9b413a8941baeaf033', text: 'Mülga:RG-16/03/2023-32134/5 md. Yürürlük:24/03/2023', parent_section: '2.2.1.B-1', amendment_type: 'mülga', official_gazette_date: '16/03/2023', official_gazette_number: '32134', article_reference: '5 md.', effective_date: '24/03/2023'}
MERGE (s_2_2_1_B_1_bb315e9883dede9b413a8941baeaf033:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_bb315e9883dede9b413a8941baeaf033)-[:CONTAINS]->(n_bb315e9883dede9b413a8941baeaf033)
;

MERGE (n_0ca688155ca9012e0f6cf5cbdf26d639:Rule:BillingRule {uid: '0ca688155ca9012e0f6cf5cbdf26d639'})
SET n_0ca688155ca9012e0f6cf5cbdf26d639 += {uid: '0ca688155ca9012e0f6cf5cbdf26d639', text: 'İkinci ve üçüncü basamak özel sağlık hizmeti sunucuları her bir hekim için ayrı ayrı olmak üzere bu sınırlarda muayene fatura edebilir', parent_section: '2.2.1.B-1', rule_type: 'restriction', provider_type: 'özel sağlık hizmeti sunucuları', healthcare_level: 'ikinci basamak,üçüncü basamak', condition: 'her bir hekim için ayrı ayrı günlük muayene sınırları içinde kalınması', context: 'günlük muayene sınırları'}
MERGE (s_2_2_1_B_1_0ca688155ca9012e0f6cf5cbdf26d639:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_0ca688155ca9012e0f6cf5cbdf26d639)-[:CONTAINS]->(n_0ca688155ca9012e0f6cf5cbdf26d639)
MERGE (p_ikinci_basamak_0ca688155ca9012e0f6cf5cbdf26d639_0:ProviderType {level: 'ikinci basamak'})
MERGE (n_0ca688155ca9012e0f6cf5cbdf26d639)-[:APPLIES_TO]->(p_ikinci_basamak_0ca688155ca9012e0f6cf5cbdf26d639_0)
MERGE (p_nc_basamak_0ca688155ca9012e0f6cf5cbdf26d639_1:ProviderType {level: 'üçüncü basamak'})
MERGE (n_0ca688155ca9012e0f6cf5cbdf26d639)-[:APPLIES_TO]->(p_nc_basamak_0ca688155ca9012e0f6cf5cbdf26d639_1)
;

MERGE (n_a527de3fce846937073583d24807cf98:Rule:BillingRule {uid: 'a527de3fce846937073583d24807cf98'})
SET n_a527de3fce846937073583d24807cf98 += {uid: 'a527de3fce846937073583d24807cf98', text: 'Bu sınırlar aşıldıktan sonra kabul edilen hastalar için yapılan işlemler Kuruma faturalandırılamaz', parent_section: '2.2.1.B-1', rule_type: 'prohibition', condition: 'günlük muayene sınırlarının aşılmasından sonra kabul edilen hastalar', non_billable_items: 'sınır aşıldıktan sonra yapılan tüm işlemler', payer: 'Kurum'}
MERGE (s_2_2_1_B_1_a527de3fce846937073583d24807cf98:Section {identifier: '2.2.1.B-1'})
MERGE (s_2_2_1_B_1_a527de3fce846937073583d24807cf98)-[:CONTAINS]->(n_a527de3fce846937073583d24807cf98)
;

MERGE (n_b97c0f64ee98dcc83770d0986299acd0:Section {identifier: '2.2.1.B-2'})
SET n_b97c0f64ee98dcc83770d0986299acd0 += {uid: 'b97c0f64ee98dcc83770d0986299acd0', text: '2.2.1.B-2 - Hizmet başına ödeme yöntemi ile faturalandırılacak ayakta tedaviler', identifier: '2.2.1.B-2', title: 'Hizmet başına ödeme yöntemi ile faturalandırılacak ayakta tedaviler', parent_section: '2.2.1.B', care_setting: 'ayakta tedavi', payment_method: 'hizmet başına ödeme yöntemi'}
MERGE (s_2_2_1_B_b97c0f64ee98dcc83770d0986299acd0:Section {identifier: '2.2.1.B'})
MERGE (s_2_2_1_B_b97c0f64ee98dcc83770d0986299acd0)-[:CONTAINS]->(n_b97c0f64ee98dcc83770d0986299acd0)
;

MERGE (n_12cf7d3d673c30a485817cc9aa6ddcd1:Amendment {uid: '12cf7d3d673c30a485817cc9aa6ddcd1'})
SET n_12cf7d3d673c30a485817cc9aa6ddcd1 += {uid: '12cf7d3d673c30a485817cc9aa6ddcd1', text: 'Değişik: RG- 25/08/2022- 31934/ 12-c md. Yürürlük: 03/09/2022', parent_section: '2.2.1.B-2', amendment_type: 'değişik', official_gazette_date: '25/08/2022', official_gazette_number: '31934', article_reference: '12-c md.', effective_date: '03/09/2022'}
MERGE (s_2_2_1_B_2_12cf7d3d673c30a485817cc9aa6ddcd1:Section {identifier: '2.2.1.B-2'})
MERGE (s_2_2_1_B_2_12cf7d3d673c30a485817cc9aa6ddcd1)-[:CONTAINS]->(n_12cf7d3d673c30a485817cc9aa6ddcd1)
;

MERGE (n_cd3b452d8b3df1760bea989ff3ebe2ed:Section {identifier: ''})
SET n_cd3b452d8b3df1760bea989ff3ebe2ed += {uid: 'cd3b452d8b3df1760bea989ff3ebe2ed', text: 'unknown - paragraph (1) context'}
;

MERGE (n_f1b66a66b302734d2b30664198701f8f:Scope {uid: 'f1b66a66b302734d2b30664198701f8f'})
SET n_f1b66a66b302734d2b30664198701f8f += {uid: 'f1b66a66b302734d2b30664198701f8f', text: 'Birinci basamak sağlık hizmeti sunucularında', paragraph: '1', applicable_level: 'birinci basamak', provider_type: 'sağlık hizmeti sunucuları'}
MERGE (p_birinci_basamak_f1b66a66b302734d2b30664198701f8f_0:ProviderType {level: 'birinci basamak'})
MERGE (n_f1b66a66b302734d2b30664198701f8f)-[:APPLIES_TO]->(p_birinci_basamak_f1b66a66b302734d2b30664198701f8f_0)
;

MERGE (n_8502579767e0f4a4ee4e5c7626c30fdc:MedicalService {uid: '8502579767e0f4a4ee4e5c7626c30fdc'})
SET n_8502579767e0f4a4ee4e5c7626c30fdc += {uid: '8502579767e0f4a4ee4e5c7626c30fdc', text: '112 acil sağlık hizmeti birimince verilen hizmetler', paragraph: '1', item: 'a', name: '112 acil sağlık hizmeti birimince verilen hizmetler', service_type: 'emergency_services', coverage_status: 'covered'}
;

MERGE (n_fba05c674f528a50fb33b0130ea5dc91:MedicalService {uid: 'fba05c674f528a50fb33b0130ea5dc91'})
SET n_fba05c674f528a50fb33b0130ea5dc91 += {uid: 'fba05c674f528a50fb33b0130ea5dc91', text: 'Diş tedavisine yönelik işlemler', paragraph: '1', item: 'b', name: 'Diş tedavisine yönelik işlemler', service_type: 'dental', coverage_status: 'covered'}
;

MERGE (n_2e405481ca5cf31dfa7b412d84ed27c1:MedicalService {uid: '2e405481ca5cf31dfa7b412d84ed27c1'})
SET n_2e405481ca5cf31dfa7b412d84ed27c1 += {uid: '2e405481ca5cf31dfa7b412d84ed27c1', text: 'Enjeksiyon işlemi', paragraph: '1', item: 'c', name: 'Enjeksiyon işlemi', service_type: 'injection', coverage_status: 'covered', condition: 'başka bir sağlık hizmeti sunucusunda hizmet almış hastaların yapılan enjeksiyonları için sadece enjeksiyonun bedeli karşılanır'}
;

MERGE (n_6ce35d364a5c351714f5a56d20f4bb10:MedicalService {uid: '6ce35d364a5c351714f5a56d20f4bb10'})
SET n_6ce35d364a5c351714f5a56d20f4bb10 += {uid: '6ce35d364a5c351714f5a56d20f4bb10', text: 'Kalıtsal hemoglobinopati tanı ve tedavi merkezlerinde yapılan hemoglobin varyant analizi işlemleri', paragraph: '1', item: 'ç', name: 'Kalıtsal hemoglobinopati tanı ve tedavi merkezlerinde yapılan hemoglobin varyant analizi işlemleri', service_type: 'laboratuvar', provider_restriction: 'kalıtsal hemoglobinopati tanı ve tedavi merkezleri', coverage_status: 'covered'}
;

MERGE (n_75bb017284dc6946aaca751bb36083b3:MedicalProcedure {uid: '75bb017284dc6946aaca751bb36083b3'})
SET n_75bb017284dc6946aaca751bb36083b3 += {uid: '75bb017284dc6946aaca751bb36083b3', text: 'Hemoglobin varyant analizi (Agar jel)', paragraph: '1', code: 'L103130', name: 'Hemoglobin varyant analizi (Agar jel)', list_reference: 'EK-2/B', specialty: 'hematoloji', patient_group: 'adult'}
MERGE (l_EK_2_B_75bb017284dc6946aaca751bb36083b3_0:RegulatoryList {code: 'EK-2/B'})
MERGE (n_75bb017284dc6946aaca751bb36083b3)-[:REFERENCES_LIST]->(l_EK_2_B_75bb017284dc6946aaca751bb36083b3_0)
MERGE (c_L103130_75bb017284dc6946aaca751bb36083b3:Code {value: 'L103130'})
MERGE (n_75bb017284dc6946aaca751bb36083b3)-[:HAS_CODE]->(c_L103130_75bb017284dc6946aaca751bb36083b3)
;

MERGE (n_02508567623665adcb902a5bcd79181d:MedicalProcedure {uid: '02508567623665adcb902a5bcd79181d'})
SET n_02508567623665adcb902a5bcd79181d += {uid: '02508567623665adcb902a5bcd79181d', text: 'Hemoglobin varyant analizi (Elektroforez)', paragraph: '1', code: 'L103140', name: 'Hemoglobin varyant analizi (Elektroforez)', list_reference: 'EK-2/B', specialty: 'hematoloji', patient_group: 'adult'}
MERGE (l_EK_2_B_02508567623665adcb902a5bcd79181d_0:RegulatoryList {code: 'EK-2/B'})
MERGE (n_02508567623665adcb902a5bcd79181d)-[:REFERENCES_LIST]->(l_EK_2_B_02508567623665adcb902a5bcd79181d_0)
MERGE (c_L103140_02508567623665adcb902a5bcd79181d:Code {value: 'L103140'})
MERGE (n_02508567623665adcb902a5bcd79181d)-[:HAS_CODE]->(c_L103140_02508567623665adcb902a5bcd79181d)
;

MERGE (n_ba677b6253c25cae457775e0b5b6f46d:MedicalProcedure {uid: 'ba677b6253c25cae457775e0b5b6f46d'})
SET n_ba677b6253c25cae457775e0b5b6f46d += {uid: 'ba677b6253c25cae457775e0b5b6f46d', text: 'Hemoglobin varyant analizi (HPLC)', paragraph: '1', code: 'L103150', name: 'Hemoglobin varyant analizi (HPLC)', list_reference: 'EK-2/B', specialty: 'hematoloji', patient_group: 'adult'}
MERGE (l_EK_2_B_ba677b6253c25cae457775e0b5b6f46d_0:RegulatoryList {code: 'EK-2/B'})
MERGE (n_ba677b6253c25cae457775e0b5b6f46d)-[:REFERENCES_LIST]->(l_EK_2_B_ba677b6253c25cae457775e0b5b6f46d_0)
MERGE (c_L103150_ba677b6253c25cae457775e0b5b6f46d:Code {value: 'L103150'})
MERGE (n_ba677b6253c25cae457775e0b5b6f46d)-[:HAS_CODE]->(c_L103150_ba677b6253c25cae457775e0b5b6f46d)
;

MERGE (n_cfcc346c40715688525179fd80534b36:Rule:BillingRule {uid: 'cfcc346c40715688525179fd80534b36'})
SET n_cfcc346c40715688525179fd80534b36 += {uid: 'cfcc346c40715688525179fd80534b36', text: 'SUT eki EK-2/B ve EK-2/Ç Listesinde yer alan puanlar esas alınarak faturalandırılır', paragraph: '1', rule_type: 'permission', condition: 'birinci basamak sağlık hizmeti sunucularında (a, b, c, ç bentlerindeki hizmetler)', billable_items: 'EK-2/B ve EK-2/Ç Listelerinde yer alan işlemler', list_reference: 'EK-2/B,EK-2/Ç'}
MERGE (l_EK_2_B_cfcc346c40715688525179fd80534b36_0:RegulatoryList {code: 'EK-2/B'})
MERGE (n_cfcc346c40715688525179fd80534b36)-[:REFERENCES_LIST]->(l_EK_2_B_cfcc346c40715688525179fd80534b36_0)
MERGE (l_EK_2_cfcc346c40715688525179fd80534b36_1:RegulatoryList {code: 'EK-2/Ç'})
MERGE (n_cfcc346c40715688525179fd80534b36)-[:REFERENCES_LIST]->(l_EK_2_cfcc346c40715688525179fd80534b36_1)
;

MERGE (n_a3aa898bcb07b77de0f2300221a906df:Scope {uid: 'a3aa898bcb07b77de0f2300221a906df'})
SET n_a3aa898bcb07b77de0f2300221a906df += {uid: 'a3aa898bcb07b77de0f2300221a906df', text: 'İkinci ve üçüncü basamak sağlık hizmeti sunucularında', paragraph: '2', applicable_level: 'ikinci basamak,üçüncü basamak', provider_type: 'sağlık hizmeti sunucuları'}
MERGE (p_ikinci_basamak_a3aa898bcb07b77de0f2300221a906df_0:ProviderType {level: 'ikinci basamak'})
MERGE (n_a3aa898bcb07b77de0f2300221a906df)-[:APPLIES_TO]->(p_ikinci_basamak_a3aa898bcb07b77de0f2300221a906df_0)
MERGE (p_nc_basamak_a3aa898bcb07b77de0f2300221a906df_1:ProviderType {level: 'üçüncü basamak'})
MERGE (n_a3aa898bcb07b77de0f2300221a906df)-[:APPLIES_TO]->(p_nc_basamak_a3aa898bcb07b77de0f2300221a906df_1)
;

MERGE (n_adc6ad9c78fbcea9e25b0f86f48bbd85:Amendment {uid: 'adc6ad9c78fbcea9e25b0f86f48bbd85'})
SET n_adc6ad9c78fbcea9e25b0f86f48bbd85 += {uid: 'adc6ad9c78fbcea9e25b0f86f48bbd85', text: 'Değişik:RG-25/08/2022-31934/12-c md. Yürürlük:03/09/2022', amendment_type: 'değişik', official_gazette_date: '25/08/2022', official_gazette_number: '31934', article_reference: '12-c md.', effective_date: '03/09/2022'}
;

MERGE (n_c96bf9ffd4adc136b95b9f9944d93705:Amendment {uid: 'c96bf9ffd4adc136b95b9f9944d93705'})
SET n_c96bf9ffd4adc136b95b9f9944d93705 += {uid: 'c96bf9ffd4adc136b95b9f9944d93705', text: 'Değişik: RG- 07/10/2016- 29850/ 5 md. Yürürlük: 03/09/2016', amendment_type: 'değişik', official_gazette_date: '07/10/2016', official_gazette_number: '29850', article_reference: '5 md.', effective_date: '03/09/2016'}
;

MERGE (n_745ae9d317a902b14096e108b51a6e09:Amendment {uid: '745ae9d317a902b14096e108b51a6e09'})
SET n_745ae9d317a902b14096e108b51a6e09 += {uid: '745ae9d317a902b14096e108b51a6e09', text: 'Ek: RG- 01/08/2013- 28725/ 4 md. Yürürlük: 01/08/2013', parent_section: 'UNKNOWN', amendment_type: 'ek', official_gazette_date: '01/08/2013', official_gazette_number: '28725', article_reference: '4 md.', effective_date: '01/08/2013'}
;

MERGE (n_b9187390493a0f0cd5083f1301259156:MedicalService {uid: 'b9187390493a0f0cd5083f1301259156'})
SET n_b9187390493a0f0cd5083f1301259156 += {uid: 'b9187390493a0f0cd5083f1301259156', text: 'Acil sağlık hizmetleri', parent_section: 'UNKNOWN', item: 'a', name: 'Acil sağlık hizmetleri', service_type: 'emergency_services', payment_method: 'hizmet başına ödeme yöntemi', coverage_status: 'covered'}
;

MERGE (n_943522ac30ddbefd07032dfbf18028cb:MedicalService {uid: '943522ac30ddbefd07032dfbf18028cb'})
SET n_943522ac30ddbefd07032dfbf18028cb += {uid: '943522ac30ddbefd07032dfbf18028cb', text: 'İş kazasına yönelik sağlanan sağlık hizmetleri', parent_section: 'UNKNOWN', item: 'b', name: 'İş kazasına yönelik sağlanan sağlık hizmetleri', service_type: 'occupational_accident', payment_method: 'hizmet başına ödeme yöntemi', coverage_status: 'covered'}
;

MERGE (n_25a1021e2dd3f85ddc8bd419eaef2a21:MedicalService {uid: '25a1021e2dd3f85ddc8bd419eaef2a21'})
SET n_25a1021e2dd3f85ddc8bd419eaef2a21 += {uid: '25a1021e2dd3f85ddc8bd419eaef2a21', text: 'Meslek hastalıkları hastanelerince sağlanan meslek hastalığına yönelik sağlık hizmetleri', parent_section: 'UNKNOWN', item: 'c', name: 'Meslek hastalığına yönelik sağlık hizmetleri', service_type: 'occupational_disease', provider_restriction: 'meslek hastalıkları hastaneleri', payment_method: 'hizmet başına ödeme yöntemi', coverage_status: 'covered'}
;

MERGE (n_9cad7ce21aee14f1fe2b2d5c9dcf57d7:MedicalService {uid: '9cad7ce21aee14f1fe2b2d5c9dcf57d7'})
SET n_9cad7ce21aee14f1fe2b2d5c9dcf57d7 += {uid: '9cad7ce21aee14f1fe2b2d5c9dcf57d7', text: 'MEDULA’da tedavi tipi “onkolojik tedavi” olarak seçilmiş onkolojik ön tanı/tanı konulmuş hastalıklar ile ilgili tüm işlemler', parent_section: 'UNKNOWN', item: 'ç', name: 'Onkolojik ön tanı/tanı konulmuş hastalıklar ile ilgili tüm işlemler', service_type: 'oncology', payment_method: 'hizmet başına ödeme yöntemi', coverage_status: 'covered', system_requirement: 'MEDULA’da tedavi tipi "onkolojik tedavi" olarak seçilmiş', scope: 'tüm işlemler'}
;

MERGE (n_a60ba5e17543a9d4f4b05b4ad47d3562:MedicalService {uid: 'a60ba5e17543a9d4f4b05b4ad47d3562'})
SET n_a60ba5e17543a9d4f4b05b4ad47d3562 += {uid: 'a60ba5e17543a9d4f4b05b4ad47d3562', text: 'Organ ve doku nakline ilişkin donöre yapılan hazırlık tetkik ve tahlilleri', parent_section: 'UNKNOWN', item: 'd', name: 'Organ ve doku nakline ilişkin donöre yapılan hazırlık tetkik ve tahlilleri', service_type: 'transplant_donor_preparation', payment_method: 'hizmet başına ödeme yöntemi', coverage_status: 'covered'}
;

MERGE (n_c10f6cf3845b1755f5b53c902fd88e51:MedicalService {uid: 'c10f6cf3845b1755f5b53c902fd88e51'})
SET n_c10f6cf3845b1755f5b53c902fd88e51 += {uid: 'c10f6cf3845b1755f5b53c902fd88e51', text: 'Diş tedavilerine yönelik işlemler', parent_section: 'UNKNOWN', item: 'e', name: 'Diş tedavilerine yönelik işlemler', service_type: 'dental', payment_method: 'hizmet başına ödeme yöntemi', coverage_status: 'covered'}
;

MERGE (n_ea7b70adf0d32ed55d16e3dea2be8bc2:MedicalService {uid: 'ea7b70adf0d32ed55d16e3dea2be8bc2'})
SET n_ea7b70adf0d32ed55d16e3dea2be8bc2 += {uid: 'ea7b70adf0d32ed55d16e3dea2be8bc2', text: 'Kurum birimlerince sevk belgesi düzenlenmek suretiyle sevk edilen kişilere sunulan sağlık hizmetleri', parent_section: 'UNKNOWN', item: 'f', name: 'Kurum birimlerince sevk belgesi düzenlenmek suretiyle sağlık hizmeti sunucusuna sevk edilen kişilere sunulan sağlık hizmetleri', service_type: 'referred_services', payment_method: 'hizmet başına ödeme yöntemi', coverage_status: 'covered', referral_authority: 'Kurum birimleri', document_requirement: 'sevk belgesi', examples: 'maluliyet, meslek hastalığı ve kontrol muayeneleri vb.'}
;

MERGE (n_f5a4e8b33e6c6f8519d422e50b56a1f2:MedicalService {uid: 'f5a4e8b33e6c6f8519d422e50b56a1f2'})
SET n_f5a4e8b33e6c6f8519d422e50b56a1f2 += {uid: 'f5a4e8b33e6c6f8519d422e50b56a1f2', text: 'Enjeksiyon/pansuman', parent_section: 'UNKNOWN', item: 'g', name: 'Enjeksiyon/pansuman', service_type: 'injection_dressing', payment_method: 'hizmet başına ödeme yöntemi', coverage_status: 'covered', note: 'sadece enjeksiyon/pansuman amacıyla gelen hasta için sadece enjeksiyon/pansuman bedeli karşılanır'}
;

MERGE (n_e7bb633cce31e32c59e2d13c8c21aa4d:MedicalService {uid: 'e7bb633cce31e32c59e2d13c8c21aa4d'})
SET n_e7bb633cce31e32c59e2d13c8c21aa4d += {uid: 'e7bb633cce31e32c59e2d13c8c21aa4d', text: 'Alkol, madde bağımlılığı tedavisi', parent_section: 'UNKNOWN', item: 'ğ', name: 'Alkol, madde bağımlılığı tedavisi', service_type: 'addiction_treatment', payment_method: 'hizmet başına ödeme yöntemi', coverage_status: 'covered'}
;

MERGE (n_5c3313238a3a5541e928db0527a43319:Rule:BillingRule {uid: '5c3313238a3a5541e928db0527a43319'})
SET n_5c3313238a3a5541e928db0527a43319 += {uid: '5c3313238a3a5541e928db0527a43319', text: 'Bu durumda SUT eki EK-2/A Listesinde yer alan tutarlar faturalandırılamaz', parent_section: 'UNKNOWN', rule_type: 'prohibition', condition: 'sayılmış hizmetlerin hizmet başına ödeme yöntemi ile faturalandırılması', non_billable_items: 'SUT eki EK-2/A Listesinde yer alan tutarlar', list_reference: 'EK-2/A'}
MERGE (l_EK_2_A_5c3313238a3a5541e928db0527a43319_0:RegulatoryList {code: 'EK-2/A'})
MERGE (n_5c3313238a3a5541e928db0527a43319)-[:REFERENCES_LIST]->(l_EK_2_A_5c3313238a3a5541e928db0527a43319_0)
;

MERGE (n_2013502d9ae3a8f072ea1aff1421d84d:Amendment {uid: '2013502d9ae3a8f072ea1aff1421d84d'})
SET n_2013502d9ae3a8f072ea1aff1421d84d += {uid: '2013502d9ae3a8f072ea1aff1421d84d', text: 'Değişik: RG- 25/08/2022- 31934/ 12-c md. Yürürlük: 03/09/2022', amendment_type: 'değişik', official_gazette_date: '25/08/2022', official_gazette_number: '31934', article_reference: '12-c md.', effective_date: '03/09/2022'}
;
