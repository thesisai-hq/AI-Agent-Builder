"""Tests for context compression.

Tests both selective (free) and semantic (LLM-based) compression.
"""

import pytest
from agent_framework.compression import (
    SelectiveCompressor,
    SemanticCompressor,
    HybridCompressor,
    CompressionMetrics,
    CompressionQualityChecker,
    estimate_tokens,
    should_compress,
    calculate_monthly_savings
)


# ============================================================================
# Selective Compression Tests
# ============================================================================


def test_selective_compression_value():
    """Test selective compression for value investing."""
    compressor = SelectiveCompressor()
    
    # Full data with 25 fields
    full_data = {
        'ticker': 'AAPL',
        'company_name': 'Apple Inc.',
        'pe_ratio': 28.5,
        'pb_ratio': 45.2,
        'roe': 147.0,
        'profit_margin': 25.8,
        'revenue_growth': 11.2,
        'debt_to_equity': 2.1,
        'dividend_yield': 0.5,
        'current_ratio': 1.07,
        'quick_ratio': 0.85,
        'operating_margin': 30.1,
        'industry': 'Technology',
        'sector': 'Consumer Electronics',
        'ceo': 'Tim Cook',
        'founded': 1976,
        'employees': 164000,
        'market_cap': 2800000000000,
        # ... more fields
    }
    
    # Compress for value investing
    compressed = compressor.compress_fundamentals(full_data, focus='value')
    
    # Should have much fewer fields
    assert len(compressed) < len(full_data)
    
    # Should include value-relevant fields
    assert 'pe_ratio' in compressed
    assert 'pb_ratio' in compressed
    assert 'dividend_yield' in compressed
    assert 'debt_to_equity' in compressed
    
    # Should NOT include irrelevant fields
    assert 'ceo' not in compressed
    assert 'founded' not in compressed
    assert 'employees' not in compressed
    
    # Should preserve ticker
    assert 'ticker' in compressed
    
    # Calculate stats
    stats = compressor.get_compression_stats(full_data, compressed)
    assert stats['reduction_pct'] >= 50  # At least 50% reduction (use >= not >)
    print(f"Selective compression: {stats['reduction_pct']:.0f}% reduction")


def test_selective_compression_growth():
    """Test selective compression for growth investing."""
    compressor = SelectiveCompressor()
    
    data = {
        'ticker': 'TSLA',
        'revenue_growth': 45.0,
        'earnings_growth': 55.0,
        'roe': 28.0,
        'profit_margin': 15.0,
        'pe_ratio': 55.0,
        'dividend_yield': 0.0,  # Zero - should be excluded
        'founded': 2003,
        'ceo': 'Elon Musk',
    }
    
    compressed = compressor.compress_fundamentals(data, focus='growth')
    
    # Growth-relevant fields
    assert 'revenue_growth' in compressed
    assert 'earnings_growth' in compressed
    assert 'roe' in compressed
    
    # Irrelevant fields
    assert 'founded' not in compressed
    assert 'ceo' not in compressed
    
    # Zero dividend should be excluded
    assert 'dividend_yield' not in compressed


def test_estimate_token_reduction():
    """Test token reduction estimation."""
    compressor = SelectiveCompressor()
    
    full_data = {f'field_{i}': i * 10 for i in range(25)}  # 25 fields
    compressed = compressor.compress_fundamentals(full_data, focus='value')
    
    token_est = compressor.estimate_token_reduction(full_data, compressed)
    
    assert token_est['original_tokens_estimate'] == 500  # 25 * 20
    assert token_est['compressed_tokens_estimate'] < 500
    assert token_est['reduction_pct'] > 0


# ============================================================================
# Semantic Compression Tests
# ============================================================================


@pytest.mark.asyncio
@pytest.mark.skipif(
    "OPENAI_API_KEY" not in __import__('os').environ,
    reason="Requires OPENAI_API_KEY environment variable"
)
async def test_semantic_compress_fundamentals():
    """Test semantic compression of fundamentals."""
    compressor = SemanticCompressor(provider='openai', compression_model='gpt-4o-mini')
    
    # Sample data
    data = {
        'ticker': 'AAPL',
        'pe_ratio': 28.5,
        'roe': 147.0,
        'profit_margin': 25.8,
        'revenue_growth': 11.2,
        'debt_to_equity': 2.1,
        'current_ratio': 1.07,
        'dividend_yield': 0.5,
        'industry': 'Technology',
        'sector': 'Consumer Electronics',
    }
    
    # Compress for value investing
    compressed = await compressor.compress_fundamentals(
        data,
        analysis_focus="value investing with focus on margin of safety",
        target_tokens=150
    )
    
    # Verify compression worked
    assert len(compressed) > 0
    assert len(compressed) < 800  # Should be much shorter
    
    # Should mention key value metrics
    compressed_lower = compressed.lower()
    assert any(term in compressed_lower for term in ['pe', 'ratio', 'debt', 'roe', 'margin'])


@pytest.mark.asyncio
@pytest.mark.skipif(
    "OPENAI_API_KEY" not in __import__('os').environ,
    reason="Requires OPENAI_API_KEY environment variable"
)
async def test_semantic_compress_text():
    """Test semantic compression of arbitrary text."""
    compressor = SemanticCompressor()
    
    long_text = """
    Apple Inc. reported strong quarterly results with revenue of $97.5 billion,
    up 8% year-over-year. The company saw particularly strong growth in Services,
    which grew 16% to $24.2 billion. iPhone sales remained steady at $51.3 billion.
    
    The company announced new environmental initiatives, including a commitment
    to carbon neutrality by 2030 across its entire supply chain. This includes
    transitioning to 100% renewable energy for manufacturing.
    
    Management also discussed competitive pressures in the smartphone market,
    particularly from Samsung and emerging Chinese manufacturers. The company
    maintains it has a strong competitive moat through its ecosystem.
    
    Financial position remains strong with $162 billion in cash and marketable
    securities, though total debt has increased to $111 billion. The company
    continues to return capital to shareholders through dividends and buybacks.
    """  # ~200 tokens
    
    # Compress for ESG focus
    compressed = await compressor.compress_text(
        long_text,
        query="What are the ESG and environmental initiatives?",
        target_tokens=50
    )
    
    # Should be much shorter
    assert len(compressed) < len(long_text) / 2
    
    # Should focus on ESG
    compressed_lower = compressed.lower()
    assert any(term in compressed_lower for term in ['carbon', 'environmental', 'renewable', 'neutral', 'esg'])
    
    # Should NOT focus heavily on revenue (not relevant to ESG query)
    # (Though it might mention it briefly)


@pytest.mark.asyncio
@pytest.mark.skipif(
    "OPENAI_API_KEY" not in __import__('os').environ,
    reason="Requires OPENAI_API_KEY environment variable"
)
async def test_semantic_compress_rag_chunks():
    """Test RAG chunk compression."""
    compressor = SemanticCompressor()
    
    # Simulate retrieved chunks
    chunks = [
        "The company reported strong financial performance with revenue growth of 15% year-over-year.",
        "Management announced new ESG initiatives including carbon neutrality by 2030 and 100% renewable energy.",
        "Competitive landscape analysis shows the company maintains market leadership with 35% market share.",
        "Risk factors include regulatory challenges in key markets and supply chain disruptions.",
        "The company's R&D investment increased by 20% to support innovation initiatives.",
    ]
    
    # Compress for ESG query
    compressed = await compressor.compress_rag_chunks(
        chunks,
        query="What are the ESG initiatives?",
        target_tokens=100
    )
    
    # Verify
    assert len(compressed) > 0
    
    # Should focus on ESG content
    compressed_lower = compressed.lower()
    assert any(term in compressed_lower for term in ['esg', 'carbon', 'neutral', 'renewable', 'sustainability'])
    
    # Should be much shorter than combined chunks
    combined_length = sum(len(c) for c in chunks)
    assert len(compressed) < combined_length / 3  # At least 66% reduction


@pytest.mark.asyncio
@pytest.mark.skipif(
    "OPENAI_API_KEY" not in __import__('os').environ,
    reason="Requires OPENAI_API_KEY environment variable"
)
async def test_batch_compress():
    """Test batch compression in parallel."""
    compressor = SemanticCompressor()
    
    items = [
        ("PE ratio is 15.2, ROE is 18%", "value analysis", 50),
        ("Revenue growing at 25% annually", "growth analysis", 50),
        ("Profit margins stable at 20%", "quality check", 50),
    ]
    
    compressed_list = await compressor.batch_compress(items)
    
    assert len(compressed_list) == 3
    assert all(len(c) > 0 for c in compressed_list)
    assert all(len(c) < 200 for c in compressed_list)  # All should be compressed


# ============================================================================
# Hybrid Compression Tests
# ============================================================================


@pytest.mark.asyncio
@pytest.mark.skipif(
    "OPENAI_API_KEY" not in __import__('os').environ,
    reason="Requires OPENAI_API_KEY environment variable"
)
async def test_hybrid_compression():
    """Test hybrid compression (selective + semantic)."""
    compressor = HybridCompressor()
    
    # Full data
    data = {
        'ticker': 'MSFT',
        'pe_ratio': 35.0,
        'pb_ratio': 12.5,
        'roe': 42.0,
        'profit_margin': 36.0,
        'revenue_growth': 18.0,
        'debt_to_equity': 0.5,
        'dividend_yield': 0.8,
        'current_ratio': 2.5,
        'industry': 'Software',
        'sector': 'Technology',
        'founded': 1975,
        'ceo': 'Satya Nadella',
        # ... more fields
    }
    
    # Hybrid compress
    compressed = await compressor.compress_fundamentals(
        data,
        focus='value',
        analysis_query='looking for quality companies at reasonable prices',
        target_tokens=100
    )
    
    # Should be very compressed
    assert len(compressed) > 0
    assert len(compressed) < 500  # Highly compressed
    
    # Should mention value-relevant info
    compressed_lower = compressed.lower()
    assert any(term in compressed_lower for term in ['pe', 'roe', 'debt', 'ratio', 'margin'])


# ============================================================================
# Metrics Tests
# ============================================================================


def test_compression_metrics():
    """Test compression metrics tracking."""
    metrics = CompressionMetrics()
    
    # Log some compressions
    stats1 = metrics.log_compression(
        original_tokens=800,
        compressed_tokens=200,
        method='semantic'
    )
    
    # Verify stats
    assert stats1['tokens_saved'] == 600
    assert stats1['reduction_pct'] == 75.0
    assert stats1['roi'] > 10  # Should be ~19x
    assert stats1['net_savings_usd'] > 0
    
    # Log another
    stats2 = metrics.log_compression(
        original_tokens=1000,
        compressed_tokens=250,
        method='semantic'
    )
    
    # Check summary
    summary = metrics.get_summary()
    assert summary['total_compressions'] == 2
    assert summary['total_original_tokens'] == 1800
    assert summary['total_compressed_tokens'] == 450
    assert summary['average_reduction_pct'] == 75.0


def test_compression_metrics_selective():
    """Test metrics for free selective compression."""
    metrics = CompressionMetrics()
    
    stats = metrics.log_compression(
        original_tokens=800,
        compressed_tokens=150,
        method='selective'
    )
    
    # Selective is free
    assert stats['compression_cost_usd'] == 0.0
    # All savings, no cost
    assert stats['roi'] == 'infinite'
    assert stats['net_savings_usd'] > 0


# ============================================================================
# Quality Checker Tests
# ============================================================================


def test_quality_checker():
    """Test compression quality checker."""
    from agent_framework import Signal
    
    checker = CompressionQualityChecker()
    
    # Signals that match
    original = Signal(direction='bullish', confidence=0.80, reasoning='Strong fundamentals')
    compressed = Signal(direction='bullish', confidence=0.75, reasoning='Good metrics')
    
    quality = checker.check_quality(original, compressed)
    
    assert quality['direction_match'] is True
    assert quality['confidence_diff'] == 0.05
    assert quality['quality_maintained'] is True  # Same direction, <10% diff
    
    # Signals that don't match
    original2 = Signal(direction='bullish', confidence=0.80, reasoning='Strong fundamentals')
    compressed2 = Signal(direction='bearish', confidence=0.70, reasoning='Weak outlook')
    
    quality2 = checker.check_quality(original2, compressed2)
    
    assert quality2['direction_match'] is False
    assert quality2['quality_maintained'] is False
    
    # Get summary
    summary = checker.get_quality_summary()
    assert summary['total_checks'] == 2
    assert summary['direction_match_rate'] == 0.5  # 1 of 2 matched


# ============================================================================
# Utility Function Tests
# ============================================================================


def test_estimate_tokens():
    """Test token estimation."""
    text = "Hello, world!"  # 13 characters
    tokens = estimate_tokens(text)
    assert tokens == 3  # 13 / 4 = 3
    
    long_text = "x" * 400
    tokens = estimate_tokens(long_text)
    assert tokens == 100  # 400 / 4 = 100


def test_should_compress():
    """Test compression threshold logic."""
    short_text = "x" * 100  # ~25 tokens
    assert should_compress(short_text, threshold_tokens=300) is False
    
    long_text = "x" * 2000  # ~500 tokens
    assert should_compress(long_text, threshold_tokens=300) is True


def test_calculate_monthly_savings():
    """Test savings calculator."""
    # Small scale
    savings = calculate_monthly_savings(
        analyses_per_day=100,
        avg_tokens_per_analysis=800,
        compression_reduction=0.75,
        compression_method='semantic'
    )
    
    assert savings['monthly_analyses'] == 3000  # 100 * 30
    assert savings['tokens_without_compression'] == 2400000  # 3000 * 800
    assert savings['tokens_with_compression'] == 600000  # 3000 * 200
    assert savings['reduction_pct'] == 75.0
    assert savings['monthly_savings_usd'] > 0
    
    # thesis-ai scale
    savings_large = calculate_monthly_savings(
        analyses_per_day=10000,  # 1000 users × 10 analyses
        compression_reduction=0.75
    )
    
    assert savings_large['monthly_savings_usd'] > 850  # Should be ~$870/month
    assert savings_large['annual_savings_usd'] > 10000  # Should be ~$10.4K/year


# ============================================================================
# Integration Tests
# ============================================================================


def test_selective_compressor_all_focus_types():
    """Test all focus types work."""
    compressor = SelectiveCompressor()
    
    data = {
        'ticker': 'TEST',
        'pe_ratio': 15,
        'roe': 20,
        'revenue_growth': 10,
        'profit_margin': 15,
        'debt_to_equity': 0.5,
        'dividend_yield': 2.5,
    }
    
    for focus in ['value', 'growth', 'quality', 'momentum', 'dividend', 'general']:
        compressed = compressor.compress_fundamentals(data, focus=focus)
        
        # Should always have some fields
        assert len(compressed) > 0
        
        # Should have ticker
        assert 'ticker' in compressed
        
        # Should be compressed
        assert len(compressed) <= len(data)


@pytest.mark.asyncio
async def test_compression_with_missing_fields():
    """Test compression handles missing fields gracefully."""
    compressor = SelectiveCompressor()
    
    # Incomplete data (missing some expected fields)
    incomplete_data = {
        'ticker': 'TEST',
        'pe_ratio': 15.0,
        # Missing: pb_ratio, dividend_yield, debt_to_equity, etc.
    }
    
    # Should not crash
    compressed = compressor.compress_fundamentals(incomplete_data, focus='value')
    
    # Should have what's available
    assert 'ticker' in compressed
    assert 'pe_ratio' in compressed
    
    # Should handle gracefully
    assert len(compressed) >= 2  # At least ticker + pe_ratio


# ============================================================================
# Edge Cases
# ============================================================================


@pytest.mark.asyncio
async def test_semantic_compression_empty_input():
    """Test semantic compression with empty input."""
    compressor = SemanticCompressor()
    
    # Empty data
    result = await compressor.compress_text("", "test query", target_tokens=100)
    
    # Should return empty or handle gracefully
    assert isinstance(result, str)


def test_metrics_with_no_data():
    """Test metrics with no compressions logged."""
    metrics = CompressionMetrics()
    
    summary = metrics.get_summary()
    
    assert summary['total_compressions'] == 0
    assert 'message' in summary


@pytest.mark.asyncio  
async def test_compression_fallback():
    """Test compression fallback on error."""
    # This will fail if OpenAI key not set, testing fallback
    compressor = SemanticCompressor(provider='openai', compression_model='gpt-4o-mini')
    
    # Even if compression fails, should return something
    text = "Some financial data"
    result = await compressor.compress_text(text, "test", target_tokens=50)
    
    # Should not be None
    assert result is not None
    assert isinstance(result, str)


# ============================================================================
# Performance Tests (Optional - only run with markers)
# ============================================================================


@pytest.mark.slow
@pytest.mark.asyncio
async def test_compression_performance():
    """Test compression performance (requires LLM access)."""
    import time
    
    compressor = SemanticCompressor()
    
    data = {
        'ticker': 'AAPL',
        'pe_ratio': 28.5,
        'roe': 147.0,
        'profit_margin': 25.8,
        'revenue_growth': 11.2,
        'debt_to_equity': 2.1,
    }
    
    start = time.time()
    compressed = await compressor.compress_fundamentals(data, "value investing", 200)
    elapsed = time.time() - start
    
    # Should be reasonably fast (< 2 seconds)
    assert elapsed < 2.0
    print(f"Compression took {elapsed:.2f}s")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
