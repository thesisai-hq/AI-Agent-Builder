-- PostgreSQL Schema for AI Agent Framework
-- Drop tables if they exist
DROP TABLE IF EXISTS sec_filings CASCADE;
DROP TABLE IF EXISTS news CASCADE;
DROP TABLE IF EXISTS prices CASCADE;
DROP TABLE IF EXISTS fundamentals CASCADE;

-- Fundamentals table
CREATE TABLE fundamentals (
    ticker VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sector VARCHAR(100),
    market_cap BIGINT,
    pe_ratio NUMERIC(10, 2),
    pb_ratio NUMERIC(10, 2),
    roe NUMERIC(10, 2),
    profit_margin NUMERIC(10, 2),
    revenue_growth NUMERIC(10, 2),
    debt_to_equity NUMERIC(10, 2),
    current_ratio NUMERIC(10, 2),
    dividend_yield NUMERIC(10, 2),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Prices table
CREATE TABLE prices (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    open NUMERIC(10, 2),
    high NUMERIC(10, 2),
    low NUMERIC(10, 2),
    close NUMERIC(10, 2),
    volume BIGINT,
    FOREIGN KEY (ticker) REFERENCES fundamentals(ticker) ON DELETE CASCADE,
    UNIQUE(ticker, date)
);

-- News table
CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    headline TEXT NOT NULL,
    sentiment VARCHAR(20),
    source VARCHAR(100),
    FOREIGN KEY (ticker) REFERENCES fundamentals(ticker) ON DELETE CASCADE
);

-- SEC Filings table
CREATE TABLE sec_filings (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    filing_type VARCHAR(20) NOT NULL,
    filing_date DATE NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY (ticker) REFERENCES fundamentals(ticker) ON DELETE CASCADE
);

-- Indexes for better query performance
CREATE INDEX idx_prices_ticker_date ON prices(ticker, date DESC);
CREATE INDEX idx_news_ticker_date ON news(ticker, date DESC);
CREATE INDEX idx_filings_ticker_date ON sec_filings(ticker, filing_date DESC);