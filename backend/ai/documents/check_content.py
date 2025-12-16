import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from documents import DocumentLoader

def main():
    loader = DocumentLoader()
    
    # EK-1A dosyasını çek
    results = loader.db_manager.search_by_filename("EK-1C")
    
    if results:
        print("="*60)
        print(f"Found: {results[0]['file_name']} - {results[0]['sheet_name']}")
        print("="*60)
        print("\nContent Preview (first 2000 chars):")
        print("-"*60)
        print(results[0]['content'][:2000])
        print("-"*60)
        print(f"\nTotal content length: {len(results[0]['content'])} characters")
        print(f"Total lines: {results[0]['content'].count(chr(10))}")
    else:
        print("No results found for EK-1A")

if __name__ == "__main__":
    main()