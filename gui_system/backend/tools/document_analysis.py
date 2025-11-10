"""Document analysis tool using RAG system.

Queries uploaded documents for relevant investment information.
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


def document_analysis(
    ticker: str,
    agent_id: Optional[str] = None,
    query: Optional[str] = None,
    n_results: int = 5
) -> str:
    """Analyze documents using RAG system.
    
    Args:
        ticker: Stock ticker symbol
        agent_id: Agent ID (required to access agent's documents)
        query: Optional specific query (defaults to ticker-based query)
        n_results: Number of relevant chunks to retrieve
        
    Returns:
        Relevant context from uploaded documents
    """
    if not agent_id:
        return """
=== DOCUMENT ANALYSIS ERROR ===

Error: agent_id is required for document analysis.

This tool queries your uploaded documents for relevant information.
To use it, you must:
1. Upload documents via the agent configuration UI
2. Ensure agent_id is provided when executing the tool

Status: Missing agent_id
"""
    
    try:
        # Import here to avoid circular dependency
        from ..rag_service import rag_service
        
        # Build query if not provided
        if not query:
            query = f"What information is relevant for analyzing {ticker} as an investment?"
        
        logger.info(f"Querying RAG for agent {agent_id}, ticker {ticker}")
        
        # Query RAG system
        context = rag_service.query(agent_id, query, n_results)
        
        # Add header with query context
        output = f"=== DOCUMENT ANALYSIS FOR {ticker.upper()} ===\n"
        output += f"Query: {query}\n\n"
        output += context
        
        logger.info(f"Successfully retrieved RAG context for {ticker}")
        return output
        
    except Exception as e:
        error_msg = f"Error in document analysis for {ticker}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return f"""
=== DOCUMENT ANALYSIS ERROR ===

Error: {str(e)}

This could mean:
1. No documents have been uploaded for this agent
2. The RAG system encountered an error
3. The agent's document storage is not accessible

Please ensure documents are uploaded before using this tool.
"""
