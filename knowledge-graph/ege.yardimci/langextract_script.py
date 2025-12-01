import langextract as lx
import textwrap
from pypdf import PdfReader
from collections import Counter
from examples import EXAMPLES as examples
import os
from dotenv import load_dotenv

load_dotenv(override=True)

# Set your API key here or via environment variable LANGEXTRACT_API_KEY
# You can get a free Gemini API key from: https://aistudio.google.com/app/apikey
AI_API_KEY = os.getenv("AI_API_KEY")  # Option 2: Directly set your API key here
AI_MODEL = os.getenv("AI_MODEL")

# Define comprehensive prompt and examples for extracting entities from Turkish legal/medical text
prompt = textwrap.dedent("""\
    Extract important entities, regulations, and relationships from the given Turkish legal/medical text.

    Provide meaningful attributes for every entity to add context and depth.

    Important: Use exact text from the input for extraction_text. Do not paraphrase.
    Extract entities in order of appearance with no overlapping text spans.
    
    Focus on: legal terms, medical terms, institutions, regulations, dates, and relationships between entities.""")

# Extract text from PDF
print("Extracting text from PDF...")
reader = PdfReader('./doc.pdf')

# Extract full text
full_text = ""
for page in reader.pages:
    full_text += page.extract_text()

print(f"Total PDF length: {len(full_text):,} characters")


text_chunk = full_text[100000:115000]

chunk_file = "text_chunk.txt"
with open(chunk_file, "w", encoding='utf-8') as f:
    f.write(text_chunk)
print(f"Text chunk saved to {chunk_file}")

quit()

print(f"Processing chunk of {len(text_chunk):,} characters")

# Process the text chunk
print("\nExtracting entities from PDF chunk...")

result = lx.extract(
    text_or_documents=text_chunk,
    prompt_description=prompt,
    examples=examples,
    model_id=AI_MODEL,
    api_key=AI_API_KEY,
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