import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any
import re

class SimilaritySearch:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.8
        )
    
    def find_relevant_paragraphs(self, 
                               query: str, 
                               paragraphs: List[Dict[str, Any]], 
                               top_k: int = 5,
                               context_paragraphs: int = 5) -> List[Dict[str, Any]]:
        """Find most relevant paragraphs with context"""
        if not paragraphs:
            return []
        
        # Prepare texts for vectorization
        paragraph_texts = [p['text'] for p in paragraphs]
        all_texts = [query] + paragraph_texts
        
        # Create TF-IDF matrix
        try:
            tfidf_matrix = self.vectorizer.fit_transform(all_texts)
        except ValueError:
            # Fallback to simple keyword matching if TF-IDF fails
            return self._keyword_fallback(query, paragraphs, top_k, context_paragraphs)
        
        # Calculate similarities
        query_vector = tfidf_matrix[0]
        paragraph_vectors = tfidf_matrix[1:]
        
        similarities = cosine_similarity(query_vector, paragraph_vectors).flatten()
        
        # Get top k most similar paragraphs
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Minimum similarity threshold
                paragraph = paragraphs[idx]
                
                # Get context paragraphs (before and after)
                context_before = self._get_context_paragraphs(
                    paragraphs, idx, -context_paragraphs, 0
                )
                context_after = self._get_context_paragraphs(
                    paragraphs, idx, 1, context_paragraphs + 1
                )
                
                results.append({
                    'paragraph': paragraph,
                    'similarity_score': float(similarities[idx]),
                    'context_before': context_before,
                    'context_after': context_after
                })
        
        return results
    
    def _get_context_paragraphs(self, 
                              paragraphs: List[Dict[str, Any]], 
                              center_idx: int, 
                              start_offset: int, 
                              end_offset: int) -> List[Dict[str, Any]]:
        """Get paragraphs before or after the target paragraph"""
        context = []
        
        for offset in range(start_offset, end_offset):
            context_idx = center_idx + offset
            if 0 <= context_idx < len(paragraphs):
                context.append(paragraphs[context_idx])
        
        return context
    
    def _keyword_fallback(self, 
                         query: str, 
                         paragraphs: List[Dict[str, Any]], 
                         top_k: int,
                         context_paragraphs: int) -> List[Dict[str, Any]]:
        """Fallback method using simple keyword matching"""
        query_terms = set(re.findall(r'\w+', query.lower()))
        
        scored_paragraphs = []
        for idx, paragraph in enumerate(paragraphs):
            para_terms = set(re.findall(r'\w+', paragraph['text'].lower()))
            common_terms = query_terms.intersection(para_terms)
            score = len(common_terms) / len(query_terms) if query_terms else 0
            
            if score > 0:
                context_before = self._get_context_paragraphs(
                    paragraphs, idx, -context_paragraphs, 0
                )
                context_after = self._get_context_paragraphs(
                    paragraphs, idx, 1, context_paragraphs + 1
                )
                
                scored_paragraphs.append({
                    'paragraph': paragraph,
                    'similarity_score': score,
                    'context_before': context_before,
                    'context_after': context_after
                })
        
        # Sort by score and return top k
        scored_paragraphs.sort(key=lambda x: x['similarity_score'], reverse=True)
        return scored_paragraphs[:top_k]