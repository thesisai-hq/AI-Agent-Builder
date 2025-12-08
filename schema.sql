-- PostgreSQL Schema for AI Agent Framework
-- Compatible with thesis-data-fabric production database

-- Create schema
CREATE SCHEMA IF NOT EXISTS thesis_data;

-- Drop existing objects (in correct order for dependencies)
DROP VIEW IF EXISTS thesis_data.fundamentals CASCADE;
DROP TABLE IF EXISTS thesis_data.edgar_filing_chunks CASCADE;
DROP TABLE IF EXISTS thesis_data.edgar_filings CASCADE;
DROP TABLE IF EXISTS thesis_data.stock_news CASCADE;
DROP TABLE IF EXISTS thesis_data.prices CASCADE;
DROP TABLE IF EXISTS thesis_data.macro_indicators CASCADE;

-- =============================================================================
-- PRICES TABLE
-- Matches thesis-data-fabric: thesis_data.prices
-- =============================================================================
CREATE TABLE thesis_data.prices (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    price_date DATE NOT NULL,
    open NUMERIC(10, 2),
    high NUMERIC(10, 2),
    low NUMERIC(10, 2),
    close NUMERIC(10, 2),
    volume BIGINT,
    source VARCHAR(50) DEFAULT 'yahoo_finance',
    UNIQUE(ticker, price_date)
);

CREATE INDEX idx_prices_ticker_date ON thesis_data.prices(ticker, price_date DESC);

-- =============================================================================
-- STOCK NEWS TABLE
-- Matches thesis-data-fabric: thesis_data.stock_news
-- =============================================================================
CREATE TABLE thesis_data.stock_news (
    id SERIAL PRIMARY KEY,
    article_id VARCHAR(100),
    ticker VARCHAR(10) NOT NULL,
    headline TEXT NOT NULL,
    summary TEXT,
    url TEXT,
    published_at TIMESTAMP NOT NULL,
    source VARCHAR(100),
    sentiment_score NUMERIC(4, 3),  -- -1.000 to 1.000
    sentiment_label VARCHAR(20),     -- positive, negative, neutral
    has_earnings_keyword BOOLEAN DEFAULT FALSE,
    has_acquisition_keyword BOOLEAN DEFAULT FALSE,
    has_regulatory_keyword BOOLEAN DEFAULT FALSE,
    UNIQUE(article_id)
);

CREATE INDEX idx_news_ticker_date ON thesis_data.stock_news(ticker, published_at DESC);

-- =============================================================================
-- SEC FILINGS TABLE
-- Matches thesis-data-fabric: thesis_data.edgar_filings
-- =============================================================================
CREATE TABLE thesis_data.edgar_filings (
    id SERIAL PRIMARY KEY,
    filing_id VARCHAR(100) UNIQUE NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    cik VARCHAR(20),
    company_name VARCHAR(255),
    filing_type VARCHAR(20) NOT NULL,  -- 10-K, 10-Q, 8-K
    filing_date DATE NOT NULL,
    filing_url TEXT,
    is_xbrl BOOLEAN DEFAULT FALSE,
    sections JSONB,                     -- Available sections in filing
    financial_data JSONB                -- Extracted financial metrics
);

CREATE INDEX idx_filings_ticker_date ON thesis_data.edgar_filings(ticker, filing_date DESC);
CREATE INDEX idx_filings_type ON thesis_data.edgar_filings(filing_type);

-- =============================================================================
-- FILING CHUNKS TABLE
-- Matches thesis-data-fabric: thesis_data.edgar_filing_chunks
-- Text split into ~2000 char segments for LLM processing
-- =============================================================================
CREATE TABLE thesis_data.edgar_filing_chunks (
    id SERIAL PRIMARY KEY,
    filing_id VARCHAR(100) NOT NULL REFERENCES thesis_data.edgar_filings(filing_id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    UNIQUE(filing_id, chunk_index)
);

CREATE INDEX idx_chunks_filing ON thesis_data.edgar_filing_chunks(filing_id, chunk_index);

-- =============================================================================
-- MACRO INDICATORS TABLE
-- Matches thesis-data-fabric: thesis_data.macro_indicators
-- Federal Reserve economic data (FRED)
-- =============================================================================
CREATE TABLE thesis_data.macro_indicators (
    id SERIAL PRIMARY KEY,
    indicator_name VARCHAR(50) NOT NULL,  -- cpi, unemployment, fed_funds, 10y_yield, gdp, inflation
    series_id VARCHAR(20),                 -- FRED series ID (CPIAUCSL, UNRATE, etc.)
    date DATE NOT NULL,
    value NUMERIC(15, 4),
    units VARCHAR(50),
    year INTEGER,
    month INTEGER,
    quarter INTEGER,
    UNIQUE(indicator_name, date)
);

CREATE INDEX idx_macro_indicator_date ON thesis_data.macro_indicators(indicator_name, date DESC);

-- =============================================================================
-- FUNDAMENTALS VIEW
-- Derives fundamental metrics from edgar_filings.financial_data JSON
-- Provides backward compatibility with original schema
-- =============================================================================
CREATE VIEW thesis_data.fundamentals AS
SELECT 
    ef.ticker,
    ef.company_name AS name,
    (ef.financial_data->>'sector')::VARCHAR(100) AS sector,
    (ef.financial_data->>'market_cap')::BIGINT AS market_cap,
    (ef.financial_data->>'pe_ratio')::NUMERIC(10,2) AS pe_ratio,
    (ef.financial_data->>'pb_ratio')::NUMERIC(10,2) AS pb_ratio,
    (ef.financial_data->>'roe')::NUMERIC(10,2) AS roe,
    (ef.financial_data->>'profit_margin')::NUMERIC(10,2) AS profit_margin,
    (ef.financial_data->>'revenue_growth')::NUMERIC(10,2) AS revenue_growth,
    (ef.financial_data->>'debt_to_equity')::NUMERIC(10,2) AS debt_to_equity,
    (ef.financial_data->>'current_ratio')::NUMERIC(10,2) AS current_ratio,
    (ef.financial_data->>'dividend_yield')::NUMERIC(10,2) AS dividend_yield,
    ef.filing_date AS updated_at
FROM thesis_data.edgar_filings ef
WHERE ef.filing_type = '10-K'
  AND ef.filing_date = (
      SELECT MAX(ef2.filing_date)
      FROM thesis_data.edgar_filings ef2
      WHERE ef2.ticker = ef.ticker
        AND ef2.filing_type = '10-K'
  );

-- =============================================================================
-- HELPER COMMENTS
-- =============================================================================
COMMENT ON TABLE thesis_data.prices IS 'Daily OHLCV stock prices from Yahoo Finance';
COMMENT ON TABLE thesis_data.stock_news IS 'Company news with sentiment analysis from Finnhub';
COMMENT ON TABLE thesis_data.edgar_filings IS 'SEC filings metadata from EDGAR';
COMMENT ON TABLE thesis_data.edgar_filing_chunks IS 'Filing text chunks for LLM processing';
COMMENT ON TABLE thesis_data.macro_indicators IS 'Economic indicators from FRED';
COMMENT ON VIEW thesis_data.fundamentals IS 'Derived fundamental metrics from latest 10-K filings';