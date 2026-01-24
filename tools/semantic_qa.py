"""
Semantic Q&A Tool - RAG-based question answering.
"""

from .base_tool import BaseTool


class SemanticQATool(BaseTool):
    """RAG-based semantic question answering over documents."""
    
    def __init__(self):
        super().__init__()
        self.name = "semantic_qa"
        self.description = "Answer questions based on provided documents using semantic search."
        
        self.parameters = {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["ingest", "query", "clear"],
                    "description": "Operation: ingest, query, or clear",
                    "default": "query"
                },
                "text": {
                    "type": "string",
                    "description": "Document text to ingest OR question to ask"
                },
                "top_k": {
                    "type": "integer",
                    "description": "Number of results to retrieve",
                    "default": 3
                }
            },
            "required": ["text"]
        }
        
        self._documents = []
        self._chunks = []
        self._embeddings = []
        self._model = None
        self._model_available = False
        
        self._check_model()
    
    def _check_model(self):
        try:
            from sentence_transformers import SentenceTransformer
            self._model_available = True
        except ImportError:
            self._model_available = False
    
    def _get_model(self):
        if self._model is not None:
            return self._model
        
        if not self._model_available:
            return None
        
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer("all-MiniLM-L6-v2")
            return self._model
        except Exception:
            return None
    
    def execute(self, text, operation="query", top_k=3):
        try:
            if not text or not text.strip():
                return "Please provide text."
            
            text = text.strip()
            
            if operation == "ingest":
                return self._ingest_document(text)
            elif operation == "query":
                return self._query(text, top_k)
            elif operation == "clear":
                return self._clear()
            else:
                return "Unknown operation: " + operation
                
        except Exception as e:
            return "Semantic QA error: " + str(e)
    
    def _chunk_text(self, text, chunk_size=500, overlap=50):
        words = text.split()
        chunks = []
        
        if len(words) <= chunk_size:
            return [text]
        
        start = 0
        while start < len(words):
            end = start + chunk_size
            chunk = " ".join(words[start:end])
            chunks.append(chunk)
            start = end - overlap
        
        return chunks
    
    def _ingest_document(self, text):
        model = self._get_model()
        
        chunks = self._chunk_text(text)
        
        if model is None:
            self._chunks.extend(chunks)
            self._documents.append(text[:200] + "..." if len(text) > 200 else text)
            
            result = "DOCUMENT INGESTED (Basic Mode)\n"
            result += "=" * 40 + "\n\n"
            result += "Chunks created: " + str(len(chunks)) + "\n"
            result += "Total chunks: " + str(len(self._chunks)) + "\n"
            result += "Documents: " + str(len(self._documents)) + "\n\n"
            result += "Note: Install sentence-transformers for better results:\n"
            result += "pip install sentence-transformers\n"
            return result
        
        try:
            import numpy as np
            
            new_embeddings = model.encode(chunks)
            
            self._chunks.extend(chunks)
            
            if len(self._embeddings) == 0:
                self._embeddings = new_embeddings
            else:
                self._embeddings = np.vstack([self._embeddings, new_embeddings])
            
            self._documents.append(text[:200] + "..." if len(text) > 200 else text)
            
            result = "DOCUMENT INGESTED\n"
            result += "=" * 40 + "\n\n"
            result += "Chunks created: " + str(len(chunks)) + "\n"
            result += "Total chunks: " + str(len(self._chunks)) + "\n"
            result += "Documents: " + str(len(self._documents)) + "\n\n"
            result += "You can now ask questions using operation='query'.\n"
            return result
            
        except Exception as e:
            return "Ingestion error: " + str(e)
    
    def _query(self, question, top_k=3):
        if not self._chunks:
            result = "NO DOCUMENTS\n"
            result += "=" * 40 + "\n\n"
            result += "Please ingest documents first using operation='ingest'.\n"
            return result
        
        model = self._get_model()
        
        if model is None:
            return self._query_simple(question, top_k)
        
        try:
            import numpy as np
            
            question_embedding = model.encode([question])[0]
            
            similarities = []
            for i, chunk_emb in enumerate(self._embeddings):
                dot_product = np.dot(question_embedding, chunk_emb)
                norm1 = np.linalg.norm(question_embedding)
                norm2 = np.linalg.norm(chunk_emb)
                similarity = dot_product / (norm1 * norm2)
                similarities.append((i, similarity))
            
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            result = "SEMANTIC SEARCH RESULTS\n"
            result += "=" * 40 + "\n\n"
            result += "Question: " + question + "\n\n"
            result += "Top " + str(min(top_k, len(similarities))) + " Results:\n"
            result += "-" * 30 + "\n\n"
            
            for rank, (i, sim) in enumerate(similarities[:top_k]):
                chunk = self._chunks[i]
                preview = chunk[:300] + "..." if len(chunk) > 300 else chunk
                
                result += "[" + str(rank + 1) + "] Score: " + str(round(sim, 3)) + "\n"
                result += preview + "\n\n"
            
            result += "-" * 30 + "\n"
            result += "Searched " + str(len(self._chunks)) + " chunks.\n"
            
            return result
            
        except Exception as e:
            return "Query error: " + str(e)
    
    def _query_simple(self, question, top_k=3):
        import re
        
        question_words = set(re.findall(r"\b[a-zA-Z]{3,}\b", question.lower()))
        
        scored_chunks = []
        for i, chunk in enumerate(self._chunks):
            chunk_words = set(re.findall(r"\b[a-zA-Z]{3,}\b", chunk.lower()))
            overlap = len(question_words & chunk_words)
            if overlap > 0:
                scored_chunks.append((chunk, overlap, i))
        
        if not scored_chunks:
            result = "NO MATCHES\n"
            result += "=" * 40 + "\n\n"
            result += "Question: " + question + "\n\n"
            result += "No relevant information found.\n"
            result += "Try different keywords or ingest more documents.\n"
            return result
        
        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        
        result = "SEARCH RESULTS (Basic Mode)\n"
        result += "=" * 40 + "\n\n"
        result += "Question: " + question + "\n\n"
        result += "Top " + str(min(top_k, len(scored_chunks))) + " Results:\n"
        result += "-" * 30 + "\n\n"
        
        for rank, (chunk, score, idx) in enumerate(scored_chunks[:top_k]):
            preview = chunk[:300] + "..." if len(chunk) > 300 else chunk
            
            result += "[" + str(rank + 1) + "] Match score: " + str(score) + "\n"
            result += preview + "\n\n"
        
        result += "-" * 30 + "\n"
        result += "Note: Install sentence-transformers for semantic search.\n"
        
        return result
    
    def _clear(self):
        doc_count = len(self._documents)
        chunk_count = len(self._chunks)
        
        self._documents = []
        self._embeddings = []
        self._chunks = []
        
        result = "KNOWLEDGE BASE CLEARED\n"
        result += "=" * 40 + "\n\n"
        result += "Removed:\n"
        result += "- " + str(doc_count) + " document(s)\n"
        result += "- " + str(chunk_count) + " chunk(s)\n"
        
        return result