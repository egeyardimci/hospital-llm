import langextract as lx
import textwrap
from pypdf import PdfReader
from collections import Counter, defaultdict
import os
from dotenv import load_dotenv

load_dotenv(override=True)

# Set your API key here or via environment variable LANGEXTRACT_API_KEY
# You can get a free Gemini API key from: https://aistudio.google.com/app/apikey
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")  # Option 2: Directly set your API key here
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not OPEN_AI_API_KEY:
    print("ERROR: Please set your Gemini API key!")
    print("Option 1: Set environment variable: export LANGEXTRACT_API_KEY='your-api-key'")
    print("Option 2: Edit the script and set GEMINI_API_KEY = 'your-api-key'")
    print("Get a free API key from: https://aistudio.google.com/app/apikey")
    exit(1)

# Define comprehensive prompt and examples for extracting entities from Turkish legal/medical text
prompt = textwrap.dedent("""\
    Extract important entities, regulations, and relationships from the given Turkish legal/medical text.

    Provide meaningful attributes for every entity to add context and depth.

    Important: Use exact text from the input for extraction_text. Do not paraphrase.
    Extract entities in order of appearance with no overlapping text spans.
    
    Focus on: legal terms, medical terms, institutions, regulations, dates, and relationships between entities.""")

examples = [
    # Example 1: Patient rights and informed consent
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            Madde 15 - Sağlık hizmeti sunucuları, SGK'nın ödeme kapsamı dışında kalan 
            ilaç ve tıbbi malzemeleri kullanmadan önce hastadan veya yakınlarından 
            yazılı onay almak zorundadır."""),
        extractions=[
            lx.data.Extraction(
                extraction_class="regulation",
                extraction_text="Madde 15",
                attributes={"type": "article", "topic": "informed_consent"}
            ),
            lx.data.Extraction(
                extraction_class="obligation",
                extraction_text="hastadan veya yakınlarından yazılı onay almak zorundadır",
                attributes={
                    "obligated_party": "sağlık hizmeti sunucuları",
                    "action": "yazılı onay alma",
                    "condition": "SGK ödeme kapsamı dışı",
                    "requirement_type": "mandatory"
                }
            ),
            lx.data.Extraction(
                extraction_class="relationship",
                extraction_text="SGK'nın ödeme kapsamı dışında kalan ilaç",
                attributes={
                    "type": "coverage_exclusion",
                    "payer": "SGK",
                    "item": "ilaç ve tıbbi malzemeler"
                }
            ),
        ]
    ),
    
    # Example 2: Payment responsibility
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            Yazılı onay alınmadan uygulanan tedavi ve kullanılan malzemelerin 
            bedeli sağlık hizmeti sunucusu tarafından hastaya fatura edilemez."""),
        extractions=[
            lx.data.Extraction(
                extraction_class="rule",
                extraction_text="bedeli sağlık hizmeti sunucusu tarafından hastaya fatura edilemez",
                attributes={
                    "condition": "yazılı onay alınmadan",
                    "prohibited_action": "fatura etme",
                    "responsible_party": "sağlık hizmeti sunucusu",
                    "protected_party": "hasta"
                }
            ),
            lx.data.Extraction(
                extraction_class="relationship",
                extraction_text="Yazılı onay alınmadan uygulanan tedavi",
                attributes={
                    "type": "prevents",
                    "cause": "yazılı onay yokluğu",
                    "effect": "fatura edilemez"
                }
            ),
        ]
    ),
    
    # Example 3: SGK coverage scope
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            SGK, Sağlık Uygulama Tebliği ekinde yer alan ilaçların bedelini karşılar. 
            Ek listede bulunmayan ilaçlar kapsam dışıdır."""),
        extractions=[
            lx.data.Extraction(
                extraction_class="institution",
                extraction_text="SGK",
                attributes={"role": "payer", "type": "government_insurance"}
            ),
            lx.data.Extraction(
                extraction_class="coverage_rule",
                extraction_text="Sağlık Uygulama Tebliği ekinde yer alan ilaçların bedelini karşılar",
                attributes={
                    "payer": "SGK",
                    "covered_items": "tebliğ ekindeki ilaçlar",
                    "coverage_status": "covered"
                }
            ),
            lx.data.Extraction(
                extraction_class="coverage_rule",
                extraction_text="Ek listede bulunmayan ilaçlar kapsam dışıdır",
                attributes={
                    "covered_items": "listede olmayan ilaçlar",
                    "coverage_status": "not_covered"
                }
            ),
        ]
    ),
    
    # Example 4: Hospital obligations
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            Özel sağlık kuruluşları, SGK kapsamı dışı uygulamalar için tedaviye 
            başlamadan önce hasta veya yakınlarını bilgilendirmeli ve yazılı 
            onay belgesi almalıdır."""),
        extractions=[
            lx.data.Extraction(
                extraction_class="entity",
                extraction_text="Özel sağlık kuruluşları",
                attributes={"type": "private_healthcare_provider"}
            ),
            lx.data.Extraction(
                extraction_class="procedure",
                extraction_text="tedaviye başlamadan önce hasta veya yakınlarını bilgilendirmeli",
                attributes={
                    "timing": "before_treatment",
                    "action": "inform_patient",
                    "requirement": "mandatory"
                }
            ),
            lx.data.Extraction(
                extraction_class="procedure",
                extraction_text="yazılı onay belgesi almalıdır",
                attributes={
                    "timing": "before_treatment",
                    "action": "obtain_written_consent",
                    "requirement": "mandatory",
                    "document_type": "yazılı onay belgesi"
                }
            ),
        ]
    ),
    
    # Example 5: Patient protection scenario
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            Hasta, önceden bilgilendirilmeden uygulanan SGK kapsam dışı tedavi 
            için ödeme yapmakla yükümlü değildir."""),
        extractions=[
            lx.data.Extraction(
                extraction_class="patient_right",
                extraction_text="ödeme yapmakla yükümlü değildir",
                attributes={
                    "condition": "önceden bilgilendirilmemiş",
                    "subject": "hasta",
                    "right_type": "payment_exemption",
                    "context": "SGK kapsam dışı tedavi"
                }
            ),
            lx.data.Extraction(
                extraction_class="relationship",
                extraction_text="önceden bilgilendirilmeden uygulanan",
                attributes={
                    "type": "causes",
                    "cause": "bilgilendirme eksikliği",
                    "effect": "ödeme yükümlülüğü yok"
                }
            ),
        ]
    ),
    
    # Example 6: Legal consequence
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            Bilgilendirme ve yazılı onay olmaksızın fatura edilen tutarlar 
            için hasta SGK'ya şikayette bulunabilir."""),
        extractions=[
            lx.data.Extraction(
                extraction_class="patient_right",
                extraction_text="hasta SGK'ya şikayette bulunabilir",
                attributes={
                    "action": "file_complaint",
                    "authority": "SGK",
                    "trigger": "unauthorized_billing"
                }
            ),
            lx.data.Extraction(
                extraction_class="violation",
                extraction_text="Bilgilendirme ve yazılı onay olmaksızın fatura edilen",
                attributes={
                    "violation_type": "unauthorized_billing",
                    "missing_requirement": "bilgilendirme ve yazılı onay"
                }
            ),
        ]
    ),
]

# Extract text from PDF
print("Extracting text from PDF...")
reader = PdfReader('./doc.pdf')

# Extract full text
full_text = ""
for page in reader.pages:
    full_text += page.extract_text()

print(f"Total PDF length: {len(full_text):,} characters")


text_chunk = full_text[100000:110000]
print(f"Processing chunk of {len(text_chunk):,} characters")

# Process the text chunk
print("\nExtracting entities from PDF chunk...")

result = lx.extract(
    text_or_documents=text_chunk,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-3-pro-preview",  # Automatically selects OpenAI provider
    api_key=GEMINI_API_KEY,
    fence_output=True,
    use_schema_constraints=False
)

print(f"\nExtracted {len(result.extractions)} entities from {len(result.text):,} characters")

# Display some sample extractions
if result.extractions:
    print("\n--- Sample Extractions ---")
    for i, extraction in enumerate(result.extractions[:10]):  # Show first 10
        print(f"\n{i+1}. Class: {extraction.extraction_class}")
        print(f"   Text: {extraction.extraction_text[:100]}...")  # Truncate long texts
        print(f"   Attributes: {extraction.attributes}")

# Save the results
output_file = "pdf_extractions.jsonl"
lx.io.save_annotated_documents([result], output_name=output_file, output_dir=".")
print(f"\nResults saved to {output_file}")

# Generate the interactive visualization
print("\nGenerating interactive visualization...")
html_content = lx.visualize(output_file)
output_html = "pdf_visualization.html"

with open(output_html, "w", encoding='utf-8') as f:
    if hasattr(html_content, 'data'):
        f.write(html_content.data)  # For Jupyter/Colab
    else:
        f.write(html_content)

print(f"Interactive visualization saved to {output_html}")

# Print summary statistics
print("\n--- Summary Statistics ---")
extraction_classes = [e.extraction_class for e in result.extractions]
class_counts = Counter(extraction_classes)
print("Entity types found:")
for entity_type, count in class_counts.most_common():
    print(f"  {entity_type}: {count}")