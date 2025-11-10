"""Document management routes for RAG system.

Handles file uploads, listing, deletion, and querying.
"""

import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import List
from ..rag_service import rag_service
from ..storage import storage
from ..errors import AgentNotFoundError, APIError
from ..models import AgentResponse

logger = logging.getLogger(__name__)

router = APIRouter(tags=["documents"])

# Maximum file size: 10MB
MAX_FILE_SIZE = 10 * 1024 * 1024

# Allowed file extensions
ALLOWED_EXTENSIONS = {'.pdf', '.txt'}


@router.post("/agents/{agent_id}/documents", status_code=201)
async def upload_document(agent_id: str, file: UploadFile = File(...)):
    """Upload document to agent's RAG system.
    
    Args:
        agent_id: Agent ID
        file: Uploaded file (PDF or TXT)
        
    Returns:
        Document upload confirmation with metadata
    """
    # Verify agent exists
    agent = storage.get_agent(agent_id)
    if not agent:
        raise AgentNotFoundError(agent_id)
    
    # Validate file extension
    filename = file.filename or "unknown"
    ext = '.' + filename.lower().split('.')[-1] if '.' in filename else ''
    
    if ext not in ALLOWED_EXTENSIONS:
        raise APIError(
            400,
            "Invalid file type",
            {
                "filename": filename,
                "allowed": list(ALLOWED_EXTENSIONS),
                "received": ext
            }
        )
    
    # Read file content
    try:
        content = await file.read()
    except Exception as e:
        raise APIError(500, "Failed to read file", {"error": str(e)})
    
    # Check file size
    if len(content) > MAX_FILE_SIZE:
        raise APIError(
            400,
            "File too large",
            {
                "size": len(content),
                "max_size": MAX_FILE_SIZE,
                "max_size_mb": MAX_FILE_SIZE / (1024 * 1024)
            }
        )
    
    if len(content) == 0:
        raise APIError(400, "Empty file", {"filename": filename})
    
    # Add to RAG system
    try:
        result = rag_service.add_document(
            agent_id=agent_id,
            file_content=content,
            filename=filename,
            metadata={"agent_name": agent.name}
        )
        
        logger.info(f"Document {filename} uploaded for agent {agent_id}")
        return result
        
    except Exception as e:
        logger.error(f"Error uploading document: {e}", exc_info=True)
        raise APIError(500, "Failed to process document", {"error": str(e)})


@router.get("/agents/{agent_id}/documents")
async def list_documents(agent_id: str):
    """List all documents for an agent.
    
    Args:
        agent_id: Agent ID
        
    Returns:
        List of document metadata
    """
    # Verify agent exists
    agent = storage.get_agent(agent_id)
    if not agent:
        raise AgentNotFoundError(agent_id)
    
    try:
        documents = rag_service.list_documents(agent_id)
        stats = rag_service.get_stats(agent_id)
        
        return {
            "documents": documents,
            "total_documents": len(documents),
            "total_chunks": stats.get("total_chunks", 0),
            "agent_id": agent_id,
            "agent_name": agent.name
        }
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise APIError(500, "Failed to list documents", {"error": str(e)})


@router.delete("/agents/{agent_id}/documents/{filename}")
async def delete_document(agent_id: str, filename: str):
    """Delete a document from agent's RAG system.
    
    Args:
        agent_id: Agent ID
        filename: Document filename
        
    Returns:
        Deletion confirmation
    """
    # Verify agent exists
    agent = storage.get_agent(agent_id)
    if not agent:
        raise AgentNotFoundError(agent_id)
    
    success = rag_service.delete_document(agent_id, filename)
    
    if not success:
        raise APIError(404, "Document not found", {
            "agent_id": agent_id,
            "filename": filename
        })
    
    logger.info(f"Document {filename} deleted from agent {agent_id}")
    return {
        "status": "deleted",
        "filename": filename,
        "agent_id": agent_id
    }


@router.post("/agents/{agent_id}/documents/query")
async def query_documents(
    agent_id: str,
    query: str = Query(..., description="Search query"),
    n_results: int = Query(5, ge=1, le=20, description="Number of results")
):
    """Query documents for relevant context.
    
    Args:
        agent_id: Agent ID
        query: Search query
        n_results: Number of results to return (1-20)
        
    Returns:
        Relevant context from documents
    """
    # Verify agent exists
    agent = storage.get_agent(agent_id)
    if not agent:
        raise AgentNotFoundError(agent_id)
    
    try:
        context = rag_service.query(agent_id, query, n_results)
        
        return {
            "query": query,
            "context": context,
            "agent_id": agent_id,
            "n_results": n_results
        }
    except Exception as e:
        logger.error(f"Error querying documents: {e}")
        raise APIError(500, "Failed to query documents", {"error": str(e)})


@router.get("/agents/{agent_id}/documents/stats")
async def get_document_stats(agent_id: str):
    """Get statistics about agent's RAG system.
    
    Args:
        agent_id: Agent ID
        
    Returns:
        RAG system statistics
    """
    # Verify agent exists
    agent = storage.get_agent(agent_id)
    if not agent:
        raise AgentNotFoundError(agent_id)
    
    try:
        stats = rag_service.get_stats(agent_id)
        return {
            **stats,
            "agent_id": agent_id,
            "agent_name": agent.name
        }
    except Exception as e:
        logger.error(f"Error getting document stats: {e}")
        raise APIError(500, "Failed to get stats", {"error": str(e)})
