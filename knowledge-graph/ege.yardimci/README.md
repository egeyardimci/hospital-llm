# SGK Health Document Relation Extraction

Extract structured relations from Turkish SGK health documents using LangExtract patterns and Groq's Llama 3 models.

## 🚀 Features

- **PDF Processing**: Robust PDF text extraction using PyMuPDF
- **Smart Chunking**: Intelligent text splitting with overlap for context preservation
- **LangExtract Pattern**: Structured relation extraction following LangExtract methodology
- **Groq Integration**: Fast inference using Groq's Llama 3 models
- **Turkish Support**: Handles Turkish SGK document formats and terminology
- **Relation Types**:
  - Patient Information
  - Diagnoses
  - Medical Procedures
  - Medications
  - Healthcare Facilities
  - Appointments
  - Insurance Details
  - Cost Information

## 📋 Prerequisites

- Python 3.8+
- Groq API key (Get it from [https://console.groq.com](https://console.groq.com))
- SGK health document in PDF format

## 🔧 Installation

### 1. Clone or download the code

```bash
# Create a working directory
mkdir sgk-extraction
cd sgk-extraction
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install pymupdf groq langchain langchain-groq chromadb
```

### 3. Set up your Groq API key

```bash
export GROQ_API_KEY='your-groq-api-key-here'
```

Or add it to your `.bashrc` / `.zshrc`:

```bash
echo 'export GROQ_API_KEY="your-groq-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

## 🎯 Usage

### Basic Usage

```python
from sgk_relation_extraction import SGKRelationExtractor

# Initialize extractor
extractor = SGKRelationExtractor(
    groq_api_key="your-groq-api-key",
    model="llama3-70b-8192"
)

# Extract relations from PDF
results = extractor.extract_relations(
    pdf_path="path/to/sgk_document.pdf",
    output_path="output/relations.json"
)

# Access results
print(f"Found {results['total_relations']} relations")
print(f"Relation types: {results['relations_by_type']}")
```

### Command Line Usage

```bash
python sgk_relation_extraction.py
```

Make sure to update the PDF_PATH in the script or modify the main() function.

### Advanced Usage

```python
# Use different Groq model
extractor = SGKRelationExtractor(
    groq_api_key="your-api-key",
    model="llama-3.1-70b-versatile"  # or "llama-3.1-8b-instant"
)

# Custom chunking parameters
from langchain.text_splitter import RecursiveCharacterTextSplitter

extractor.text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,      # Smaller chunks
    chunk_overlap=150,     # Less overlap
    length_function=len
)

# Extract and process
results = extractor.extract_relations("document.pdf")

# Filter specific relation types
diagnoses = [r for r in results['all_relations'] if r['type'] == 'DIAGNOSIS']
medications = [r for r in results['all_relations'] if r['type'] == 'MEDICATION']
```

## 📊 Output Format

The extraction produces a JSON file with the following structure:

```json
{
  "document": "path/to/sgk_document.pdf",
  "model": "llama3-70b-8192",
  "total_chunks": 15,
  "total_relations": 47,
  "relations_by_type": {
    "PATIENT_INFO": 1,
    "DIAGNOSIS": 8,
    "MEDICATION": 12,
    "PROCEDURE": 6,
    "FACILITY": 3,
    "APPOINTMENT": 5,
    "INSURANCE": 2,
    "COST": 10
  },
  "all_relations": [
    {
      "type": "DIAGNOSIS",
      "fields": {
        "diagnosis_code": "J06.9",
        "diagnosis_name": "Akut üst solunum yolu enfeksiyonu",
        "date": "2024-10-15",
        "severity": "hafif"
      },
      "confidence": 0.92,
      "source_text": "Tanı: J06.9 - Akut üst solunum yolu enfeksiyonu",
      "chunk_id": 3
    }
  ]
}
```

## 🔍 Relation Types Explained

### PATIENT_INFO
Patient demographic and identification information
- **Fields**: name, TC_ID, birth_date, gender, address

### DIAGNOSIS
Medical diagnoses and conditions
- **Fields**: diagnosis_code, diagnosis_name, date, severity

### PROCEDURE
Medical procedures and treatments performed
- **Fields**: procedure_code, procedure_name, date, provider

### MEDICATION
Prescribed medications and drugs
- **Fields**: drug_name, drug_code, dosage, frequency, duration, prescriber

### FACILITY
Healthcare facilities and institutions
- **Fields**: facility_name, facility_code, facility_type, location

### APPOINTMENT
Medical appointments and visits
- **Fields**: appointment_date, appointment_time, facility, doctor, purpose

### INSURANCE
Insurance and coverage information
- **Fields**: policy_number, coverage_type, validity_period, institution

### COST
Cost and payment details
- **Fields**: amount, currency, payment_type, coverage_status

## ⚙️ Configuration Options

### Chunk Size Tuning

```python
# For shorter documents or when you want more precision
extractor.text_splitter.chunk_size = 1000
extractor.text_splitter.chunk_overlap = 100

# For longer documents or when you want more context
extractor.text_splitter.chunk_size = 3000
extractor.text_splitter.chunk_overlap = 300
```

### Model Selection

```python
# Fastest (good for testing)
model="llama-3.1-8b-instant"

# Balanced (recommended for production)
model="llama3-70b-8192"

# Most capable
model="llama-3.1-70b-versatile"
```

### Temperature Settings

```python
# In extract_relations_from_chunk(), modify:
temperature=0.0   # Most deterministic
temperature=0.1   # Default (recommended)
temperature=0.3   # More creative
```

## 🐛 Troubleshooting

### PDF Extraction Issues

If PDF extraction fails:

```python
# Try alternative PDF library
import PyPDF2

def extract_with_pypdf2(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text
```

### API Rate Limiting

If you hit Groq rate limits:

```python
import time

# Add delay between chunks
for chunk in chunks:
    result = extractor.extract_relations_from_chunk(chunk['text'])
    time.sleep(1)  # 1 second delay
```

### JSON Parsing Errors

The script handles most JSON parsing issues automatically, but if you encounter persistent errors:

1. Check the model's raw output in the error message
2. Adjust the prompt to be more explicit about JSON formatting
3. Increase temperature slightly (0.15-0.2)
4. Try a different model

## 📈 Performance Tips

1. **Batch Processing**: Process multiple documents in parallel
2. **Caching**: Save extracted text to avoid re-processing PDFs
3. **Model Selection**: Use `llama-3.1-8b-instant` for faster processing
4. **Chunk Size**: Larger chunks = fewer API calls but may miss details
5. **Error Handling**: Implement retry logic for failed chunks

## 🔒 Privacy & Security

- Never commit your Groq API key to version control
- Use environment variables for sensitive data
- Be cautious with patient data - ensure HIPAA/GDPR compliance
- Consider local LLM alternatives for sensitive documents

## 📚 LangExtract Integration

This implementation follows LangExtract principles:

1. **Schema Definition**: Clear relation types and fields
2. **Prompt Engineering**: Structured extraction instructions
3. **Few-shot Learning**: Template-based examples in prompts
4. **Validation**: Confidence scores and source text tracking
5. **Aggregation**: Combining results from multiple chunks

For the official LangExtract library, see: https://github.com/google/langextract

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Add more SGK-specific relation types
- [ ] Implement relation linking across chunks
- [ ] Add OCR support for scanned documents
- [ ] Create visualization dashboard
- [ ] Add batch processing CLI
- [ ] Implement validation rules for extracted data

## 📄 License

MIT License - Feel free to use and modify as needed.

## 🙏 Acknowledgments

- [LangExtract](https://github.com/google/langextract) for relation extraction methodology
- [Groq](https://groq.com) for fast LLM inference
- [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF processing
- Turkish healthcare community for SGK document formats
