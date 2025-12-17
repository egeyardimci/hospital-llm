import langextract as lx
import textwrap
from pypdf import PdfReader
from collections import Counter
import os
import time
from dotenv import load_dotenv

load_dotenv(override=True)

# ---------------------------
# ENV
# ---------------------------
AI_API_KEY = os.getenv("OPENAI_API_KEY") 
if not AI_API_KEY:
    raise ValueError("Missing API key. Set AI_API_KEY or GEMINI_API_KEY in your .env")

AI_MODEL = os.getenv("OPENAI_MODEL")
FALLBACK_MODEL = os.getenv("FALLBACK_MODEL", "gemini-2.5-flash-lite")

INPUT_PATH = os.getenv("INPUT_PATH", "1.5.1_example.txt")
OUTPUT_JSONL = "output.jsonl"
OUTPUT_HTML = "output.html"

MAX_RETRIES = int(os.getenv("MAX_RETRIES", "6"))
BASE_SLEEP_SEC = float(os.getenv("BASE_SLEEP_SEC", "2.0"))

print(f"Using AI Model: {AI_MODEL}")
print(f"Fallback Model: {FALLBACK_MODEL}")
print(f"Reading input: {INPUT_PATH}")

# ---------------------------
# PROMPT
# ---------------------------
prompt = textwrap.dedent("""\
You are an expert extraction system for Turkish healthcare regulations (SUT).

TASK:
Extract structured entities from the given Turkish regulatory text.
- Only extract entities that appear in the text.
- Prefer canonical / official naming when possible.
- Keep attributes short and factual.

Return entities with sensible classes such as:
Institution, System, Regulation, Law, Article, Document, MedicalProcedure, HealthCondition, TimeConstraint, Location, ServiceProviderType.
""")

# ---------------------------
# EXAMPLES (keyword args only - compatible across versions)
# ---------------------------
examples = [
    lx.data.ExampleData(
        text=(
            "5510 sayılı Kanunun 60 ıncı maddesi gereği genel sağlık sigortası kapsamına alınan kişilerin "
            "MEDULA sistemi üzerinden müstahaklık sorgulaması yapılır."
        ),
        extractions=[
            lx.data.Extraction(
                extraction_class="Law",
                extraction_text="5510 sayılı Kanun",
                attributes={"law_number": "5510"},
            ),
            lx.data.Extraction(
                extraction_class="Article",
                extraction_text="60 ıncı maddesi",
                attributes={"article_no": "60"},
            ),
            lx.data.Extraction(
                extraction_class="System",
                extraction_text="MEDULA sistemi",
                attributes={"aliases": ["MEDULA"]},
            ),
            lx.data.Extraction(
                extraction_class="SystemAction",
                extraction_text="müstahaklık sorgulaması",
                attributes={},
            ),
            lx.data.Extraction(
                extraction_class="System",
                extraction_text="genel sağlık sigortası",
                attributes={"aliases": ["GSS"]},
            ),
        ],
    ),
    lx.data.ExampleData(
        text=(
            "Acil haller dışında sözleşmesiz özel sağlık hizmeti sunucularından alınan sağlık hizmeti bedelleri "
            "Kurumca ödenmez."
        ),
        extractions=[
            lx.data.Extraction(
                extraction_class="HealthCondition",
                extraction_text="Acil haller",
                attributes={},
            ),
            lx.data.Extraction(
                extraction_class="ServiceProviderType",
                extraction_text="sözleşmesiz özel sağlık hizmeti sunucuları",
                attributes={},
            ),
            # align to the exact surface form in the example sentence: "Kurumca"
            lx.data.Extraction(
                extraction_class="Institution",
                extraction_text="Kurumca",
                attributes={"aliases": ["SGK", "Sosyal Güvenlik Kurumu"]},
            ),
        ],
    ),
    lx.data.ExampleData(
        text=(
            "Hasta naklinin 112 Komuta Kontrol Merkezi koordinasyonunda gerçekleştirilmesi koşuluyla "
            "yoğun bakım tedavisi için özel sağlık hizmeti sunucularına sevk edilebilir."
        ),
        extractions=[
            lx.data.Extraction(
                extraction_class="Institution",
                extraction_text="112 Komuta Kontrol Merkezi",
                attributes={"role": "coordination"},
            ),
            lx.data.Extraction(
                extraction_class="MedicalProcedure",
                extraction_text="yoğun bakım tedavisi",
                attributes={},
            ),
            lx.data.Extraction(
                extraction_class="Process",
                extraction_text="sevk",
                attributes={},
            ),
            lx.data.Extraction(
                extraction_class="ServiceProviderType",
                extraction_text="özel sağlık hizmeti sunucuları",
                attributes={},
            ),
        ],
    ),
    lx.data.ExampleData(
        text=(
            "Sevk belgesi ile sevkin düzenlendiği tarih dahil 5 işgünü içinde sevk edildikleri "
            "sağlık hizmeti sunucusuna müracaat edeceklerdir."
        ),
        extractions=[
            lx.data.Extraction(
                extraction_class="Document",
                extraction_text="Sevk belgesi",
                attributes={"aliases": ["Hasta Sevk Formu", "EK-2/F"]},
            ),
            lx.data.Extraction(
                extraction_class="TimeConstraint",
                extraction_text="5 işgünü",
                attributes={"value": 5, "unit": "işgünü"},
            ),
        ],
    ),
]

# ---------------------------
# INPUT: PDF or TXT
# ---------------------------
ext = os.path.splitext(INPUT_PATH)[1].lower()

if ext == ".pdf":
    print("Extracting text from PDF...")
    reader = PdfReader(INPUT_PATH)
    full_text = ""
    for page in reader.pages:
        full_text += (page.extract_text() or "")
elif ext == ".txt":
    print("Reading text from TXT...")
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        full_text = f.read()
else:
    raise ValueError("Unsupported input type. Please provide a .pdf or .txt file.")

full_text = (full_text or "").strip()
print(f"Total length: {len(full_text):,} characters")
if not full_text:
    raise ValueError("Input text is empty (check file encoding/content).")

with open("text_chunk.txt", "w", encoding="utf-8") as f:
    f.write(full_text)

print(f"Processing FULL text: {len(full_text):,} characters")

# ---------------------------
# EXTRACT with retry/backoff
# ---------------------------
def run_extract(model_id: str):
    return lx.extract(
        text_or_documents=full_text,
        prompt_description=prompt,
        examples=examples,
        model_id=model_id,
        api_key=AI_API_KEY,
        fence_output=True,
        use_schema_constraints=False,
    )

print("\nExtracting entities from text...")

last_err = None
result = None

for model_try in [AI_MODEL, FALLBACK_MODEL]:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            result = run_extract(model_try)
            break
        except Exception as e:
            last_err = e
            msg = str(e)
            sleep_s = min(BASE_SLEEP_SEC * (2 ** (attempt - 1)), 30.0)
            print(f"\n[WARN] extract failed (model={model_try}, attempt={attempt}/{MAX_RETRIES})")
            print(f"       error: {msg[:250]}")
            print(f"       retrying in {sleep_s:.1f}s...")
            time.sleep(sleep_s)
    if result is not None:
        break

if result is None:
    raise RuntimeError(f"Extraction failed after retries. Last error: {last_err}")

print(f"\nExtracted {len(result.extractions)} entities from {len(result.text):,} characters")

if result.extractions:
    print("\n--- Sample Extractions ---")
    for i, extraction in enumerate(result.extractions[:15]):
        print(f"\n{i+1}. Class: {extraction.extraction_class}")
        print(f"   Text: {extraction.extraction_text[:140]}...")
        print(f"   Attributes: {extraction.attributes}")

lx.io.save_annotated_documents([result], output_name=OUTPUT_JSONL, output_dir=".")
print(f"\nResults saved to {OUTPUT_JSONL}")

print("\nGenerating interactive visualization...")
html_content = lx.visualize(OUTPUT_JSONL)
with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content.data if hasattr(html_content, "data") else html_content)
print(f"Interactive visualization saved to {OUTPUT_HTML}")

print("\n--- Summary Statistics ---")
classes = [e.extraction_class for e in result.extractions]
counts = Counter(classes)
for entity_type, count in counts.most_common():
    print(f"  {entity_type}: {count}")
