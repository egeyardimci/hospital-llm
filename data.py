"""
This file contains the data for the tests to be run.

llm_names: List of LLM names to be used for the tests.
embedding_model_names: List of embedding model names to be used for the tests.
system_messages: List of system messages to be used for the tests.
chunk_sizes_and_chunk_overlaps: List of tuples containing chunk sizes and chunk overlaps to be used for the tests.
similar_vector_counts: List of similar vector counts to be used for the tests.
queries: List of queries to be used for the tests.
document_name: Name of the document to be used for the tests and db creation.
"""

llm_names = [
    "deepseek-r1-distill-qwen-32b",
]

embedding_model_names = [
    "sentence-transformers/all-MiniLM-L6-v2",
]

system_messages = [
    """
You are a helpful assistant. Answer strictly based on the provided context and do NOT use any external knowledge.
Do not assume or infer information that is not explicitly stated in the context.
If the context does not contain enough information to answer, clearly state that you cannot provide an answer.
Always cite the exact phrase or section from the context that supports your response. If multiple references exist, summarize them before answering.
Use clear, structured responses with bullet points, numbered lists, or short paragraphs when applicable.
Communicate exclusively in Turkish, using formal and grammatically correct language unless the customer’s tone suggests informality.""",
]

chunk_sizes_and_chunk_overlaps = [
    (500, 50),
]

similar_vector_counts = [
    10,
]

queries_and_expected_answers= [
    {
        "query": "Bir hasta, 520.021 kodlu Yeşil Alan Muayenesi kapsamında değerlendirildi ancak şiddetli karın ağrısı şikayeti vardı. Sonrasında acil servisten yapılan tetkikler sonucu apandisit tanısı aldı. Bu durumda hastadan ilave ücret alınır mı?",
        "answer": "Başlangıçta 520.021 koduyla Yeşil Alan Muayenesi kapsamında değerlendirilen hastalar için ilave ücret alınabilir. Ancak, tetkikler sonucunda hastanın acil bir durumu (örneğin apandisit) olduğu tespit edilirse, bu durum acil sağlık hizmeti olarak kabul edilir ve ilave ücret alınamaz."
    },
    {
        "query": "Yanık ünitesinde tedavi gören 9 yaşındaki bir çocuk için, sağlık kurulu raporu ile dermis iskeleti içermeyen deri benzeri kullanıldı. Yanık alanı yüzeysel ikinci derece ve vücudunun %15’ini kapsıyor. Bu durumda SGK malzeme ücretini karşılar mı?",
        "answer": "SGK, dermis iskeleti içermeyen deri benzerlerini ancak %20’yi geçen ikinci derece veya üçüncü derece yanıklarda karşılar. Bu durumda yanık alanı %15 olduğu için geri ödeme yapılmaz ve malzeme ücreti hastaya aittir."
    },
    {
        "query": "Yüksek doz radyoterapi sonrası oluşan femur kırığı nedeniyle total femur rezeksiyon protezi takılan bir hastanın sağlam kemik miktarı 140 mm ise, SGK bu protezin masraflarını karşılar mı?",
        "answer": "Hayır, SGK total femur rezeksiyon protezini yalnızca hastanın sağlam kemik miktarı 130 mm’den az olduğunda karşılamaktadır. Eğer sağlam kemik miktarı 130 mm’den fazlaysa, SGK geri ödeme yapmaz ve protez masrafı hastaya ait olur."
    },
    {
        "query": "65 yaşındaki bir hasta, birinci basamak sağlık hizmeti sunucusu tarafından sağlık kurulu raporu alarak değerlendirildikten sonra, ileri görüntüleme yöntemlerinin (MR, BT, DSA, PET-CT) uygulanabilmesi için radyo cerrahi yöntemlerine yönelik olarak ikinci veya üçüncü basamak resmi sağlık hizmeti sunucusuna sevk edilmiştir. Bu durumda, SGK’nın ödeme politikası kapsamında, sevk edilen hastanın bu görüntüleme işlemleri için herhangi bir ek ücret ödemesi gerekir mi?",
        "answer": "Hayır, eğer hasta sağlık kurulu raporu ile sevk edilmişse, MR, BT, DSA ve PET-CT bedelleri faturalandırılamaz ve hasta herhangi bir ek ücret ödemez."
    },
]

document_name = "doc.docx"

test_results_output_file = "results.json"