import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from documents import DocumentLoader
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    print("\n" + "="*60)
    print("BULK DOCUMENT LOADER")
    print("="*60 + "\n")
    
    # Initialize loader with markdown format
    loader = DocumentLoader(format_type='markdown')
    
    # Load all files from storage directory
    script_dir = Path(__file__).parent
    storage_dir = script_dir / "storage"
    
    print(f"Loading all Excel files from: {storage_dir}\n")
    
    # Load all Excel files
    results = loader.load_directory(str(storage_dir))
    
    print("\n" + "="*60)
    print("FINAL STATISTICS")
    print("="*60)
    
    stats = loader.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\nAll files in database:")
    all_files = loader.db_manager.get_all_filenames()
    for idx, filename in enumerate(all_files, 1):
        print(f"  {idx}. {filename}")
    
    print("\nDONE!\n")

if __name__ == "__main__":
    main()