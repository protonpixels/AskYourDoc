import PyPDF2
import pdfplumber
from docx import Document
import re
from typing import List, Dict, Any, Tuple
import os

class TextProcessor:
    def __init__(self):
        self.supported_formats = {
            'application/pdf': self._extract_from_pdf,
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': self._extract_from_docx,
            'application/msword': self._extract_from_docx,
            'text/plain': self._extract_from_txt
        }
    
    def extract_text_with_metadata(self, file_path: str, mime_type: str) -> Dict[str, Any]:
        """Extract text with paragraph-level metadata and page numbers"""
        if mime_type not in self.supported_formats:
            raise ValueError(f"Unsupported file type: {mime_type}")
        
        return self.supported_formats[mime_type](file_path)
    
    def _extract_from_pdf(self, file_path: str) -> Dict[str, Any]:
        """Extract text from PDF with page numbers and paragraph positioning"""
        paragraphs = []
        full_text = ""
        
        try:
            # Use pdfplumber for better text extraction with coordinates
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n"
                        # Split into paragraphs (simple approach)
                        page_paragraphs = self._split_into_paragraphs(text, page_num)
                        paragraphs.extend(page_paragraphs)
        except Exception as e:
            # Fallback to PyPDF2
            print(f"pdfplumber failed, using PyPDF2: {e}")
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n"
                        page_paragraphs = self._split_into_paragraphs(text, page_num)
                        paragraphs.extend(page_paragraphs)
        
        return {
            'full_text': full_text.strip(),
            'paragraphs': paragraphs,
            'total_pages': len(paragraphs) and max(p['page'] for p in paragraphs) or 0
        }
    
    def _extract_from_docx(self, file_path: str) -> Dict[str, Any]:
        """Extract text from DOCX with paragraph metadata"""
        doc = Document(file_path)
        paragraphs = []
        full_text = ""
        
        # DOCX doesn't have page numbers, so we'll use paragraph indices
        for para_num, paragraph in enumerate(doc.paragraphs, 1):
            text = paragraph.text.strip()
            if text and len(text) > 10:  # Minimum paragraph length
                full_text += text + "\n"
                paragraphs.append({
                    'text': text,
                    'page': para_num,  # Using paragraph number as pseudo-page
                    'paragraph_index': para_num,
                    'start_position': len(full_text) - len(text),
                    'end_position': len(full_text)
                })
        
        return {
            'full_text': full_text.strip(),
            'paragraphs': paragraphs,
            'total_pages': len(paragraphs)
        }
    
    def _extract_from_txt(self, file_path: str) -> Dict[str, Any]:
        """Extract text from TXT files"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            full_text = file.read()
        
        paragraphs = []
        # Split by double newlines (common paragraph separator)
        raw_paragraphs = re.split(r'\n\s*\n', full_text)
        
        for para_num, para_text in enumerate(raw_paragraphs, 1):
            text = para_text.strip()
            if text and len(text) > 10:
                paragraphs.append({
                    'text': text,
                    'page': 1,  # TXT files don't have pages
                    'paragraph_index': para_num,
                    'start_position': full_text.find(text),
                    'end_position': full_text.find(text) + len(text)
                })
        
        return {
            'full_text': full_text,
            'paragraphs': paragraphs,
            'total_pages': 1
        }
    
    def _split_into_paragraphs(self, text: str, page_num: int) -> List[Dict[str, Any]]:
        """Split text into paragraphs with metadata"""
        paragraphs = []
        
        # Multiple strategies for paragraph detection
        paragraph_separators = [
            r'\n\s*\n',  # Double newlines
            r'\n(?=\s*[A-Z])',  # Newline followed by capital letter
            r'(?<=[.!?])\s+\n',  # End of sentence followed by newline
        ]
        
        combined_pattern = '|'.join(paragraph_separators)
        raw_paragraphs = re.split(combined_pattern, text)
        
        current_position = 0
        for para_num, para_text in enumerate(raw_paragraphs, 1):
            text = para_text.strip()
            if text and len(text) > 20:  # Minimum character count for a paragraph
                paragraphs.append({
                    'text': text,
                    'page': page_num,
                    'paragraph_index': para_num,
                    'start_position': current_position,
                    'end_position': current_position + len(text)
                })
            current_position += len(para_text) + 1  # +1 for the separator
        
        return paragraphs
    
    def get_first_sentence(self, text: str, max_length: int = 100) -> str:
        """Extract first sentence for document identification"""
        # Simple sentence extraction
        sentences = re.split(r'[.!?]+', text)
        first_sentence = sentences[0].strip() if sentences else text[:max_length].strip()
        
        # Clean up and limit length
        first_sentence = re.sub(r'\s+', ' ', first_sentence)
        if len(first_sentence) > max_length:
            first_sentence = first_sentence[:max_length] + '...'
        
        return first_sentence