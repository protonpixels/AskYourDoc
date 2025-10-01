from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os

from document_manager import DocumentManager
from text_processor import TextProcessor
from similarity_search import SimilaritySearch

# Initialize components
app = FastAPI(title="AskYourDoc Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

document_manager = DocumentManager()
text_processor = TextProcessor()
similarity_search = SimilaritySearch()

# Pydantic models
class QuestionRequest(BaseModel):
    question: str
    document_id: str
    top_k: int = 5  # Number of relevant paragraphs to return
    context_paragraphs: int = 5  # Context in each direction

class ParagraphResponse(BaseModel):
    text: str
    page: int
    paragraph_index: int
    similarity_score: float

class ContextResponse(BaseModel):
    before: List[ParagraphResponse]
    after: List[ParagraphResponse]

class SearchResult(BaseModel):
    paragraph: ParagraphResponse
    context_before: List[ParagraphResponse]
    context_after: List[ParagraphResponse]

class QuestionResponse(BaseModel):
    document_id: str
    document_title: str
    original_filename: str
    results: List[SearchResult]
    total_paragraphs_searched: int

class UploadResponse(BaseModel):
    document_id: str
    document_title: str
    original_filename: str
    total_paragraphs: int
    total_pages: int
    message: str

# API endpoints
@app.get("/")
async def root():
    return {"message": "AskYourDoc Backend", "status": "running"}

@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    try:
        # Validate file type
        if file.content_type not in text_processor.supported_formats:
            raise HTTPException(400, f"Unsupported file type: {file.content_type}")
        
        # Read file
        file_content = await file.read()
        if len(file_content) == 0:
            raise HTTPException(400, "File is empty")
        
        # Save document
        document_id, file_path = document_manager.save_document(file_content, file.filename)
        
        # Extract text and metadata
        extracted_data = text_processor.extract_text_with_metadata(file_path, file.content_type)
        
        # Generate document title from first sentence
        first_sentence = text_processor.get_first_sentence(extracted_data['full_text'])
        
        # Store document metadata
        document_manager.store_document_metadata(
            document_id, file.filename, extracted_data, first_sentence
        )
        
        return UploadResponse(
            document_id=document_id,
            document_title=first_sentence,
            original_filename=file.filename,
            total_paragraphs=len(extracted_data['paragraphs']),
            total_pages=extracted_data['total_pages'],
            message="Document uploaded and processed successfully"
        )
        
    except Exception as e:
        raise HTTPException(500, f"Error processing document: {str(e)}")

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    try:
        # Get document
        document = document_manager.get_document(request.document_id)
        if not document:
            raise HTTPException(404, "Document not found")
        
        # Find relevant paragraphs
        paragraphs = document['paragraphs']
        results = similarity_search.find_relevant_paragraphs(
            query=request.question,
            paragraphs=paragraphs,
            top_k=request.top_k,
            context_paragraphs=request.context_paragraphs
        )
        
        # Format response
        formatted_results = []
        for result in results:
            formatted_results.append({
                'paragraph': {
                    'text': result['paragraph']['text'],
                    'page': result['paragraph']['page'],
                    'paragraph_index': result['paragraph']['paragraph_index'],
                    'similarity_score': result['similarity_score']
                },
                'context_before': [
                    {
                        'text': p['text'],
                        'page': p['page'],
                        'paragraph_index': p['paragraph_index'],
                        'similarity_score': 0.0  # Context paragraphs don't have similarity scores
                    }
                    for p in result['context_before']
                ],
                'context_after': [
                    {
                        'text': p['text'],
                        'page': p['page'],
                        'paragraph_index': p['paragraph_index'],
                        'similarity_score': 0.0
                    }
                    for p in result['context_after']
                ]
            })
        
        return QuestionResponse(
            document_id=request.document_id,
            document_title=document['document_title'],
            original_filename=document['original_filename'],
            results=formatted_results,
            total_paragraphs_searched=len(paragraphs)
        )
        
    except Exception as e:
        raise HTTPException(500, f"Error processing question: {str(e)}")

@app.get("/documents")
async def list_documents():
    """List all uploaded documents"""
    return document_manager.get_all_documents()

@app.get("/documents/{document_id}")
async def get_document_info(document_id: str):
    """Get document information"""
    document = document_manager.get_document(document_id)
    if not document:
        raise HTTPException(404, "Document not found")
    
    # Return minimal info (no full text)
    return {
        'document_id': document['document_id'],
        'original_filename': document['original_filename'],
        'document_title': document['document_title'],
        'upload_time': document['upload_time'],
        'total_paragraphs': document['total_paragraphs'],
        'total_pages': document['total_pages']
    }

@app.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a document"""
    success = document_manager.delete_document(document_id)
    if not success:
        raise HTTPException(404, "Document not found")
    
    return {"message": "Document deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)