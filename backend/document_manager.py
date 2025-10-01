import os
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
import hashlib

class DocumentManager:
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = upload_dir
        self.documents = {}  # In production, use a database
        os.makedirs(upload_dir, exist_ok=True)
    
    def generate_document_id(self, file_content: bytes, original_filename: str) -> str:
        """Generate unique document ID using content hash and timestamp"""
        content_hash = hashlib.md5(file_content).hexdigest()[:8]
        timestamp = str(int(datetime.now().timestamp()))[-6:]
        return f"doc_{content_hash}_{timestamp}"
    
    def save_document(self, file_content: bytes, original_filename: str) -> str:
        """Save document and return unique ID"""
        document_id = self.generate_document_id(file_content, original_filename)
        file_extension = os.path.splitext(original_filename)[1]
        filename = f"{document_id}{file_extension}"
        file_path = os.path.join(self.upload_dir, filename)
        
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        return document_id, file_path
    
    def store_document_metadata(self, 
                              document_id: str, 
                              original_filename: str,
                              extracted_data: Dict[str, Any],
                              first_sentence: str) -> None:
        """Store document metadata and processed content"""
        self.documents[document_id] = {
            'document_id': document_id,
            'original_filename': original_filename,
            'document_title': first_sentence,  # Using first sentence as title
            'upload_time': datetime.now().isoformat(),
            'file_size': extracted_data.get('file_size', 0),
            'total_paragraphs': len(extracted_data.get('paragraphs', [])),
            'total_pages': extracted_data.get('total_pages', 0),
            'paragraphs': extracted_data.get('paragraphs', []),
            'full_text': extracted_data.get('full_text', '')
        }
    
    def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve document by ID"""
        return self.documents.get(document_id)
    
    def get_all_documents(self) -> List[Dict[str, Any]]:
        """Get list of all documents (minimal info)"""
        return [
            {
                'document_id': doc_id,
                'original_filename': doc['original_filename'],
                'document_title': doc['document_title'],
                'upload_time': doc['upload_time'],
                'total_paragraphs': doc['total_paragraphs'],
                'total_pages': doc['total_pages']
            }
            for doc_id, doc in self.documents.items()
        ]
    
    def delete_document(self, document_id: str) -> bool:
        """Delete document and its metadata"""
        if document_id in self.documents:
            # Remove physical file
            doc = self.documents[document_id]
            file_extension = os.path.splitext(doc['original_filename'])[1]
            file_path = os.path.join(self.upload_dir, f"{document_id}{file_extension}")
            
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Remove from memory
            del self.documents[document_id]
            return True
        
        return False