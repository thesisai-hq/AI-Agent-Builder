"""Lightweight RAG (Retrieval Augmented Generation) service.

No database required - uses ChromaDB with file system storage.
Uses FastEmbed for embeddings - no PyTorch dependency, faster and lighter.
Each agent has its own document collection and embeddings.
"""

import logging
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
import chromadb
from chromadb.config import Settings
from chromadb import Documents, EmbeddingFunction, Embeddings
from fastembed.embedding import DefaultEmbedding
import PyPDF2
from datetime import datetime

logger = logging.getLogger(__name__)


class FastEmbedEmbeddingFunction(EmbeddingFunction):
    """ChromaDB-compatible wrapper for FastEmbed.
    
    Implements the ChromaDB EmbeddingFunction interface correctly.
    FastEmbed is lighter and faster than sentence-transformers,
    and doesn't require PyTorch.
    """
    
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        """Initialize FastEmbed model.
        
        Args:
            model_name: Model to use for embeddings
                - BAAI/bge-small-en-v1.5 (default, good balance)
                - BAAI/bge-base-en-v1.5 (better quality, slower)
                - sentence-transformers/all-MiniLM-L6-v2 (fastest)
        """
        self.model = DefaultEmbedding(model_name=model_name)
        logger.info(f"Initialized FastEmbed with model: {model_name}")
    
    def __call__(self, input: Documents) -> Embeddings:
        """Generate embeddings for documents.
        
        This matches ChromaDB's EmbeddingFunction interface.
        
        Args:
            input: List of text strings (ChromaDB calls them 'Documents')
            
        Returns:
            List of embedding vectors (ChromaDB calls them 'Embeddings')
        """
        # FastEmbed returns generator, convert to list
        embeddings = list(self.model.embed(input))
        # Convert numpy arrays to lists
        return [emb.tolist() for emb in embeddings]


class RAGService:
    """Lightweight RAG system using ChromaDB and file storage."""
    
    def __init__(self, storage_path: str = "storage"):
        """Initialize RAG service.
        
        Args:
            storage_path: Base storage directory path
        """
        self.storage_path = Path(storage_path)
        
        # Use FastEmbed - lightweight, no PyTorch
        try:
            self.embedding_function = FastEmbedEmbeddingFunction()
            logger.info("RAG service initialized with FastEmbed (no PyTorch)")
        except Exception as e:
            logger.warning(f"Could not initialize FastEmbed: {e}. RAG features will be limited.")
            self.embedding_function = None
    
    def add_document(
        self,
        agent_id: str,
        file_content: bytes,
        filename: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Add document to agent's RAG system.
        
        Args:
            agent_id: Agent ID
            file_content: File content as bytes
            filename: Original filename
            metadata: Optional additional metadata
            
        Returns:
            Document metadata including chunk count
        """
        try:
            logger.info(f"Adding document {filename} to agent {agent_id}")
            
            # Create agent document directory
            agent_dir = self.storage_path / "agents" / agent_id
            doc_dir = agent_dir / "documents"
            doc_dir.mkdir(parents=True, exist_ok=True)
            
            # Save document
            doc_path = doc_dir / filename
            with open(doc_path, 'wb') as f:
                f.write(file_content)
            
            # Extract text
            text = self._extract_text(doc_path, filename)
            
            if not text or len(text.strip()) < 10:
                raise ValueError(f"No text could be extracted from {filename}")
            
            # Split into chunks
            chunks = self._split_text(text)
            
            logger.info(f"Extracted {len(text)} chars, split into {len(chunks)} chunks")
            
            # Get or create ChromaDB collection
            collection = self._get_collection(agent_id)
            
            # Prepare metadata for each chunk
            chunk_metadata = []
            for i in range(len(chunks)):
                meta = {
                    "filename": filename,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "upload_date": datetime.now().isoformat(),
                }
                if metadata:
                    meta.update(metadata)
                chunk_metadata.append(meta)
            
            # Generate unique IDs
            chunk_ids = [f"{filename}_{i}" for i in range(len(chunks))]
            
            # Add to vector store with embeddings
            collection.add(
                documents=chunks,
                metadatas=chunk_metadata,
                ids=chunk_ids
            )
            
            result = {
                "filename": filename,
                "chunks": len(chunks),
                "characters": len(text),
                "path": str(doc_path),
                "status": "success",
                "upload_date": datetime.now().isoformat()
            }
            
            logger.info(f"Successfully added {filename} to agent {agent_id}")
            return result
            
        except Exception as e:
            error_msg = f"Error adding document {filename}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise Exception(error_msg)
    
    def query(
        self,
        agent_id: str,
        query: str,
        n_results: int = 5
    ) -> str:
        """Query agent's RAG system for relevant context.
        
        Args:
            agent_id: Agent ID
            query: Search query
            n_results: Number of results to return
            
        Returns:
            Formatted context from relevant documents
        """
        try:
            logger.info(f"Querying RAG for agent {agent_id}: {query}")
            
            collection = self._get_collection(agent_id)
            
            # Check if collection has any documents
            count = collection.count()
            if count == 0:
                logger.warning(f"No documents found for agent {agent_id}")
                return "No documents have been uploaded to this agent's knowledge base."
            
            # Query vector store
            results = collection.query(
                query_texts=[query],
                n_results=min(n_results, count)
            )
            
            if not results['documents'] or not results['documents'][0]:
                return "No relevant information found in uploaded documents."
            
            # Format results
            context = "=== RELEVANT INFORMATION FROM YOUR DOCUMENTS ===\n\n"
            
            seen_content = set()  # Avoid duplicate chunks
            
            for i, (doc, metadata, distance) in enumerate(
                zip(results['documents'][0], results['metadatas'][0], results['distances'][0])
            ):
                # Skip duplicate content
                if doc in seen_content:
                    continue
                seen_content.add(doc)
                
                filename = metadata.get('filename', 'Unknown')
                chunk_idx = metadata.get('chunk_index', 0)
                
                # Relevance score (0-1, where 1 is most relevant)
                # ChromaDB uses L2 distance, so smaller is better
                relevance = max(0, 1 - distance)
                
                context += f"[Document: {filename}, Chunk {chunk_idx + 1}, Relevance: {relevance:.2f}]\n"
                context += f"{doc}\n\n"
            
            context += f"Total documents in knowledge base: {count} chunks"
            
            logger.info(f"Retrieved {len(results['documents'][0])} relevant chunks")
            return context
            
        except Exception as e:
            error_msg = f"Error querying RAG: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return f"Error retrieving information from documents: {str(e)}"
    
    def list_documents(self, agent_id: str) -> List[Dict[str, Any]]:
        """List all documents for an agent.
        
        Args:
            agent_id: Agent ID
            
        Returns:
            List of document metadata
        """
        try:
            doc_dir = self.storage_path / "agents" / agent_id / "documents"
            
            if not doc_dir.exists():
                return []
            
            documents = []
            for file_path in doc_dir.iterdir():
                if file_path.is_file() and not file_path.name.startswith('.'):
                    stat = file_path.stat()
                    documents.append({
                        "filename": file_path.name,
                        "size": stat.st_size,
                        "size_mb": round(stat.st_size / (1024 * 1024), 2),
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "path": str(file_path)
                    })
            
            # Sort by modification time (newest first)
            documents.sort(key=lambda x: x['modified'], reverse=True)
            
            return documents
            
        except Exception as e:
            logger.error(f"Error listing documents for agent {agent_id}: {e}")
            return []
    
    def delete_document(self, agent_id: str, filename: str) -> bool:
        """Delete a document and its embeddings.
        
        Args:
            agent_id: Agent ID
            filename: Document filename
            
        Returns:
            True if deleted successfully
        """
        try:
            logger.info(f"Deleting document {filename} from agent {agent_id}")
            
            doc_path = self.storage_path / "agents" / agent_id / "documents" / filename
            
            if not doc_path.exists():
                logger.warning(f"Document {filename} not found for agent {agent_id}")
                return False
            
            # Remove from vector store
            collection = self._get_collection(agent_id)
            
            # Get all chunk IDs for this file
            # ChromaDB query to find all chunks with this filename
            results = collection.get(where={"filename": filename})
            
            if results['ids']:
                collection.delete(ids=results['ids'])
                logger.info(f"Deleted {len(results['ids'])} chunks from vector store")
            
            # Delete file
            doc_path.unlink()
            
            logger.info(f"Successfully deleted {filename} from agent {agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting document {filename}: {e}", exc_info=True)
            return False
    
    def get_stats(self, agent_id: str) -> Dict[str, Any]:
        """Get statistics about agent's RAG system.
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Statistics dictionary
        """
        try:
            collection = self._get_collection(agent_id)
            count = collection.count()
            documents = self.list_documents(agent_id)
            
            return {
                "total_chunks": count,
                "total_documents": len(documents),
                "documents": documents
            }
        except Exception as e:
            logger.error(f"Error getting stats for agent {agent_id}: {e}")
            return {
                "total_chunks": 0,
                "total_documents": 0,
                "documents": []
            }
    
    def _get_collection(self, agent_id: str):
        """Get or create ChromaDB collection for agent.
        
        Args:
            agent_id: Agent ID
            
        Returns:
            ChromaDB collection
        """
        embeddings_dir = self.storage_path / "agents" / agent_id / "embeddings"
        embeddings_dir.mkdir(parents=True, exist_ok=True)
        
        # Create persistent ChromaDB client
        client = chromadb.PersistentClient(
            path=str(embeddings_dir),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection with embedding function
        # Use the ChromaDB-compatible FastEmbed wrapper
        collection = client.get_or_create_collection(
            name=f"agent_{agent_id}",
            embedding_function=self.embedding_function if self.embedding_function else None,
            metadata={"hnsw:space": "cosine"}
        )
        
        return collection
    
    def _extract_text(self, file_path: Path, filename: str) -> str:
        """Extract text from various file formats.
        
        Args:
            file_path: Path to file
            filename: Original filename
            
        Returns:
            Extracted text
        """
        ext = filename.lower().split('.')[-1]
        
        if ext == 'pdf':
            return self._extract_pdf(file_path)
        elif ext == 'txt':
            return self._extract_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}. Supported: PDF, TXT")
    
    def _extract_pdf(self, file_path: Path) -> str:
        """Extract text from PDF.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text
        """
        text = ""
        try:
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- Page {page_num + 1} ---\n"
                        text += page_text
                
            return text.strip()
        except Exception as e:
            raise Exception(f"PDF extraction error: {str(e)}")
    
    def _extract_txt(self, file_path: Path) -> str:
        """Extract text from TXT file.
        
        Args:
            file_path: Path to text file
            
        Returns:
            File contents
        """
        try:
            # Try UTF-8 first
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Fallback to latin-1
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
    
    def _split_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks.
        
        Simple implementation without external dependencies.
        
        Args:
            text: Text to split
            chunk_size: Target chunk size in characters
            overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            # Get chunk
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary if not at end
            if end < len(text):
                # Look for sentence endings
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                last_break = max(last_period, last_newline)
                
                if last_break > chunk_size * 0.5:  # Don't break too early
                    chunk = chunk[:last_break + 1]
                    end = start + last_break + 1
            
            chunks.append(chunk.strip())
            
            # Move to next chunk with overlap
            start = end - overlap
        
        return chunks


# Global RAG service instance
rag_service = RAGService()
