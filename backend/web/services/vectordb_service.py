import re
from pathlib import Path
from typing import List, Dict, Any
from backend.common.paths import CHROMA_DB_DIR
from backend.common.constants import VECTOR_DB_EMBEDDING_MODELS
from backend.ai.vectordb.main import GLOBAL_VECTOR_DB
from backend.web.dtos import VectorDBInfo

class VectorDBService:
    @staticmethod
    def get_available_vectordbs() -> List[Dict[str, Any]]:
        """
        Get list of available vector databases from the ChromaDB directory.
        
        Returns:
            List of dictionaries containing vector DB information
        """
        vectordbs_info = []
        chroma_path = Path(CHROMA_DB_DIR)
        
        # Pattern to match names ending with one or more digits
        number_pattern = re.compile(r'\d+$')
        # Pattern to match UUID-like strings (optional, for extra filtering)
        uuid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
        
        for item in chroma_path.rglob("*"):
            if (item.is_dir() and 
                item != chroma_path and 
                number_pattern.search(item.name)):
                
                rel_path = item.relative_to(chroma_path)
                
                if uuid_pattern.match(item.name):
                    continue
                    
                name = item.name
                
                if name.startswith("chroma_db_"):
                    name = name[len("chroma_db_"):]
                else:
                    # Create the normalized path outside the f-string
                    normalized_path = str(rel_path).replace('\\', '/')
                    name = normalized_path[len('chroma_db_'):]

                name_parts = name.split('_')
                if len(name_parts) >= 3:
                    vectordbs_info.append({
                        "name": name_parts[0],
                        "chunk_size": name_parts[1],
                        "chunk_overlap": name_parts[2],
                    })
        
        return vectordbs_info

    @staticmethod
    def create_vectordb(request: VectorDBInfo) -> None:
        """
        Create a new vector database.
        
        Args:
            request: VectorDBInfo containing name, chunk_size, and chunk_overlap
        """
        from backend.ai.vectordb.utils import create_vectordb
        create_vectordb(
            embedding_model_name=request.name,
            chunk_size=int(request.chunk_size),
            chunk_overlap=int(request.chunk_overlap)
        )

    @staticmethod
    def load_vectordb(request: VectorDBInfo) -> None:
        """
        Load an existing vector database.
        
        Args:
            request: VectorDBInfo containing name, chunk_size, and chunk_overlap
        """
        GLOBAL_VECTOR_DB.load_db(
            embedding_model=request.name,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap
        )

    @staticmethod
    def get_available_models() -> List[str]:
        """
        Get list of available embedding models.
        
        Returns:
            List of available embedding model names
        """
        return VECTOR_DB_EMBEDDING_MODELS

    @staticmethod
    def get_current_vectordb() -> str:
        """
        Get the name of the currently loaded vector database.
        
        Returns:
            Name of the current vector database
        """
        return GLOBAL_VECTOR_DB.get_db_name()