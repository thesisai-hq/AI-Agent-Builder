-- ============================================================================
-- COMPLETE MOCK DATABASE - All Tables with SEC Filing Text Content
-- Save to database/mock_data.sql (replace existing file)
-- ============================================================================

-- Drop existing tables
DROP TABLE IF EXISTS mock_sec_filings CASCADE;
DROP TABLE IF EXISTS mock_insider_trades CASCADE;
DROP TABLE IF EXISTS mock_analyst_ratings CASCADE;
DROP TABLE IF EXISTS mock_news CASCADE;
DROP TABLE IF EXISTS mock_prices CASCADE;
DROP TABLE IF EXISTS mock_options CASCADE;
DROP TABLE IF EXISTS mock_macro_indicators CASCADE;
DROP TABLE IF EXISTS mock_fundamentals CASCADE;

-- ============================================================================
-- FUNDAMENTALS
-- ============================================================================
CREATE TABLE mock_fundamentals (
    ticker VARCHAR(10) PRIMARY KEY,
    company_name VARCHAR(200),
    sector VARCHAR(100),
    industry VARCHAR(100),
    market_cap BIGINT,
    enterprise_value BIGINT,
    pe_ratio DECIMAL(10,2),
    forward_pe DECIMAL(10,2),
    peg_ratio DECIMAL(10,2),
    price_to_book DECIMAL(10,2),
    price_to_sales DECIMAL(10,2),
    ev_to_revenue DECIMAL(10,2),
    ev_to_ebitda DECIMAL(10,2),
    profit_margin DECIMAL(10,2),
    operating_margin DECIMAL(10,2),
    roe DECIMAL(10,2),
    roa DECIMAL(10,2),
    roic DECIMAL(10,2),
    revenue_growth DECIMAL(10,2),
    earnings_growth DECIMAL(10,2),
    revenue_per_share_growth DECIMAL(10,2),
    current_ratio DECIMAL(10,2),
    quick_ratio DECIMAL(10,2),
    debt_to_equity DECIMAL(10,2),
    debt_to_assets DECIMAL(10,2),
    interest_coverage DECIMAL(10,2),
    dividend_yield DECIMAL(10,2),
    payout_ratio DECIMAL(10,2),
    dividend_growth_5y DECIMAL(10,2),
    beta DECIMAL(10,2),
    shares_outstanding BIGINT,
    float_shares BIGINT,
    short_ratio DECIMAL(10,2),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO mock_fundamentals VALUES
('AAPL', 'Apple Inc.', 'Technology', 'Consumer Electronics', 
 2800000000000, 2750000000000, 28.5, 26.2, 2.8, 42.5, 7.2, 7.0, 20.5,
 25.3, 30.2, 150.5, 25.8, 32.5, 8.5, 12.3, 5.2,
 1.05, 0.85, 1.75, 0.45, 12.5, 0.52, 15.2, 8.5,
 1.15, 15500000000, 15400000000, 2.1, CURRENT_TIMESTAMP),

('TSLA', 'Tesla Inc.', 'Automotive', 'Electric Vehicles',
 850000000000, 845000000000, 65.2, 55.8, 3.5, 15.8, 8.5, 8.2, 42.5,
 15.2, 18.5, 28.5, 8.2, 15.8, 35.8, 42.5, 12.5,
 1.85, 1.25, 0.85, 0.25, 18.5, 0.0, 0.0, 0.0,
 2.15, 3200000000, 2800000000, 4.5, CURRENT_TIMESTAMP),

('MSFT', 'Microsoft Corporation', 'Technology', 'Software',
 2500000000000, 2480000000000, 32.5, 28.8, 2.2, 11.5, 10.5, 10.2, 18.5,
 35.2, 42.5, 38.5, 15.2, 28.5, 15.5, 18.2, 8.5,
 2.15, 1.85, 0.45, 0.15, 22.5, 0.85, 25.8, 10.2,
 0.95, 7500000000, 7400000000, 1.5, CURRENT_TIMESTAMP),

('GOOGL', 'Alphabet Inc.', 'Technology', 'Internet Services',
 1800000000000, 1750000000000, 24.5, 22.2, 1.8, 5.8, 5.2, 5.0, 15.2,
 28.5, 32.2, 25.8, 12.5, 22.5, 12.5, 15.8, 6.5,
 2.85, 2.45, 0.12, 0.05, 45.5, 0.0, 0.0, 0.0,
 1.05, 12500000000, 12000000000, 1.2, CURRENT_TIMESTAMP),

('NVDA', 'NVIDIA Corporation', 'Technology', 'Semiconductors',
 1200000000000, 1180000000000, 85.5, 65.2, 2.5, 45.8, 32.5, 28.5, 55.2,
 52.5, 58.5, 110.5, 45.2, 75.5, 85.5, 125.8, 35.2,
 3.25, 2.85, 0.25, 0.08, 65.5, 0.15, 8.5, 25.5,
 1.85, 2500000000, 2400000000, 3.8, CURRENT_TIMESTAMP);

-- ============================================================================
-- PRICES
-- ============================================================================
CREATE TABLE mock_prices (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10),
    date DATE,
    open DECIMAL(12,2),
    high DECIMAL(12,2),
    low DECIMAL(12,2),
    close DECIMAL(12,2),
    volume BIGINT,
    sma_20 DECIMAL(12,2),
    sma_50 DECIMAL(12,2),
    sma_200 DECIMAL(12,2),
    ema_12 DECIMAL(12,2),
    ema_26 DECIMAL(12,2),
    rsi_14 DECIMAL(10,2),
    macd DECIMAL(10,2),
    macd_signal DECIMAL(10,2),
    bb_upper DECIMAL(12,2),
    bb_middle DECIMAL(12,2),
    bb_lower DECIMAL(12,2),
    UNIQUE(ticker, date)
);

INSERT INTO mock_prices (ticker, date, open, high, low, close, volume, sma_20, sma_50, sma_200, rsi_14) VALUES
('AAPL', CURRENT_DATE - 9, 175.50, 178.20, 174.80, 177.50, 65000000, 172.50, 168.50, 155.20, 58.5),
('AAPL', CURRENT_DATE - 8, 177.80, 179.50, 176.50, 178.20, 62000000, 172.80, 168.70, 155.40, 60.2),
('AAPL', CURRENT_DATE - 7, 178.50, 180.20, 177.20, 179.80, 68000000, 173.20, 169.00, 155.60, 62.5),
('AAPL', CURRENT_DATE - 6, 179.50, 181.50, 178.50, 180.50, 70000000, 173.60, 169.30, 155.80, 64.2),
('AAPL', CURRENT_DATE - 5, 180.80, 182.50, 179.80, 181.20, 72000000, 174.00, 169.60, 156.00, 65.8),
('AAPL', CURRENT_DATE - 4, 181.50, 183.20, 180.50, 182.50, 74000000, 175.20, 170.50, 157.20, 67.2),
('AAPL', CURRENT_DATE - 3, 182.80, 184.50, 181.80, 183.80, 76000000, 176.50, 171.50, 158.50, 68.5),
('AAPL', CURRENT_DATE - 2, 184.20, 186.50, 183.20, 185.50, 78000000, 178.20, 173.20, 160.20, 70.2),
('AAPL', CURRENT_DATE - 1, 185.80, 188.20, 184.80, 187.20, 80000000, 180.50, 175.50, 162.50, 72.5),
('AAPL', CURRENT_DATE, 187.50, 190.20, 186.50, 189.50, 85000000, 183.50, 178.20, 165.20, 75.8),

('TSLA', CURRENT_DATE - 9, 235.50, 242.20, 233.80, 240.50, 115000000, 228.50, 215.20, 185.50, 62.5),
('TSLA', CURRENT_DATE - 8, 240.80, 245.50, 238.50, 243.20, 118000000, 230.80, 217.70, 187.40, 64.2),
('TSLA', CURRENT_DATE - 7, 243.50, 248.20, 241.20, 246.80, 120000000, 233.20, 220.00, 189.60, 66.5),
('TSLA', CURRENT_DATE - 6, 246.50, 250.50, 244.50, 248.50, 122000000, 235.60, 222.30, 191.80, 68.2),
('TSLA', CURRENT_DATE - 5, 248.80, 252.50, 246.80, 250.20, 124000000, 238.00, 224.60, 194.00, 69.8),
('TSLA', CURRENT_DATE - 4, 250.50, 254.20, 248.50, 252.50, 126000000, 240.20, 226.50, 196.20, 71.2),
('TSLA', CURRENT_DATE - 3, 252.80, 256.50, 250.80, 254.80, 128000000, 242.50, 228.50, 198.50, 72.5),
('TSLA', CURRENT_DATE - 2, 255.20, 259.50, 253.20, 257.50, 130000000, 245.20, 231.20, 201.20, 74.2),
('TSLA', CURRENT_DATE - 1, 257.80, 262.20, 255.80, 260.20, 132000000, 248.50, 234.40, 204.50, 76.5),
('TSLA', CURRENT_DATE, 260.50, 265.20, 258.50, 263.50, 135000000, 252.50, 238.40, 208.20, 78.8),

('MSFT', CURRENT_DATE - 5, 375.50, 380.20, 373.80, 378.50, 23000000, 368.50, 358.20, 325.50, 62.5),
('MSFT', CURRENT_DATE - 4, 378.80, 382.50, 376.50, 380.20, 24000000, 370.20, 360.50, 328.20, 64.2),
('MSFT', CURRENT_DATE - 3, 380.50, 384.20, 378.20, 382.80, 25000000, 372.50, 363.50, 331.50, 66.5),
('MSFT', CURRENT_DATE - 2, 383.20, 387.50, 381.20, 385.50, 26000000, 375.20, 366.20, 335.20, 68.5),
('MSFT', CURRENT_DATE - 1, 385.80, 390.20, 383.80, 388.20, 27000000, 378.50, 369.40, 339.50, 70.5),
('MSFT', CURRENT_DATE, 388.50, 393.20, 386.50, 391.50, 28000000, 382.50, 373.50, 344.20, 72.8),

('GOOGL', CURRENT_DATE - 5, 135.50, 138.20, 134.80, 137.50, 25000000, 131.50, 128.20, 118.50, 60.5),
('GOOGL', CURRENT_DATE - 4, 137.80, 140.50, 136.50, 139.20, 26000000, 133.20, 130.50, 120.20, 62.2),
('GOOGL', CURRENT_DATE - 3, 139.50, 142.20, 138.20, 141.80, 27000000, 135.50, 133.50, 122.50, 64.5),
('GOOGL', CURRENT_DATE - 2, 142.20, 145.50, 140.20, 143.50, 28000000, 138.20, 136.20, 125.20, 66.5),
('GOOGL', CURRENT_DATE - 1, 143.80, 147.20, 142.80, 145.20, 29000000, 141.50, 139.40, 128.50, 68.5),
('GOOGL', CURRENT_DATE, 145.50, 149.20, 144.50, 147.50, 30000000, 145.50, 143.50, 132.20, 70.8),

('NVDA', CURRENT_DATE - 5, 475.50, 482.20, 473.80, 480.50, 42000000, 458.50, 438.20, 368.50, 70.5),
('NVDA', CURRENT_DATE - 4, 480.80, 486.50, 478.50, 484.20, 43000000, 462.20, 442.50, 372.20, 72.2),
('NVDA', CURRENT_DATE - 3, 484.50, 490.20, 482.20, 488.80, 44000000, 466.50, 447.50, 376.50, 74.5),
('NVDA', CURRENT_DATE - 2, 489.20, 495.50, 487.20, 493.50, 45000000, 471.20, 453.20, 381.20, 76.5),
('NVDA', CURRENT_DATE - 1, 493.80, 500.20, 491.80, 498.20, 46000000, 476.50, 459.40, 386.50, 78.5),
('NVDA', CURRENT_DATE, 498.50, 505.20, 496.50, 502.50, 48000000, 482.50, 466.50, 392.20, 80.8);

-- ============================================================================
-- NEWS
-- ============================================================================
CREATE TABLE mock_news (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10),
    headline TEXT,
    summary TEXT,
    source VARCHAR(100),
    sentiment VARCHAR(20),
    sentiment_score DECIMAL(5,2),
    published_at TIMESTAMP,
    url TEXT,
    keywords TEXT[],
    entities TEXT[],
    category VARCHAR(50)
);

INSERT INTO mock_news (ticker, headline, summary, source, sentiment, sentiment_score, published_at, keywords, category) VALUES
('AAPL', 'Apple Reports Record Q4 Earnings, Beats Expectations', 
 'Apple Inc. announced record quarterly earnings with revenue of $89.5B, surpassing analyst estimates.',
 'Reuters', 'positive', 0.85, CURRENT_TIMESTAMP - INTERVAL '2 hours',
 ARRAY['earnings', 'revenue', 'iPhone'], 'Earnings'),

('AAPL', 'Apple Vision Pro Pre-Orders Exceed Expectations',
 'The new Vision Pro headset received overwhelming pre-order numbers.',
 'Bloomberg', 'positive', 0.78, CURRENT_TIMESTAMP - INTERVAL '5 hours',
 ARRAY['Vision Pro', 'AR', 'VR'], 'Product Launch'),

('AAPL', 'Apple Faces Regulatory Scrutiny in EU Markets',
 'European regulators announced investigation into Apple App Store practices.',
 'Financial Times', 'negative', -0.65, CURRENT_TIMESTAMP - INTERVAL '1 day',
 ARRAY['regulation', 'EU', 'App Store'], 'Legal'),

('TSLA', 'Tesla Deliveries Surge 40% Year-Over-Year',
 'Tesla reported delivering 435,000 vehicles in Q3.',
 'CNBC', 'positive', 0.82, CURRENT_TIMESTAMP - INTERVAL '3 hours',
 ARRAY['deliveries', 'growth'], 'Operations'),

('MSFT', 'Microsoft Azure Revenue Grows 29% in Cloud Push',
 'Microsoft Azure cloud platform continues strong growth.',
 'Wall Street Journal', 'positive', 0.88, CURRENT_TIMESTAMP - INTERVAL '4 hours',
 ARRAY['Azure', 'cloud', 'revenue'], 'Earnings'),

('GOOGL', 'Google AI Chatbot Bard Gains New Features',
 'Google enhanced Bard with multimodal capabilities.',
 'TechCrunch', 'positive', 0.72, CURRENT_TIMESTAMP - INTERVAL '6 hours',
 ARRAY['AI', 'Bard', 'features'], 'Product'),

('NVDA', 'NVIDIA AI Chip Demand Remains Strong',
 'Despite export controls, NVIDIA reports strong demand.',
 'Reuters', 'neutral', 0.15, CURRENT_TIMESTAMP - INTERVAL '7 hours',
 ARRAY['AI', 'chips', 'demand'], 'Operations');

-- ============================================================================
-- ANALYST RATINGS
-- ============================================================================
CREATE TABLE mock_analyst_ratings (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10),
    analyst_firm VARCHAR(100),
    rating VARCHAR(20),
    price_target DECIMAL(12,2),
    previous_rating VARCHAR(20),
    previous_price_target DECIMAL(12,2),
    rating_date TIMESTAMP,
    analyst_name VARCHAR(100)
);

INSERT INTO mock_analyst_ratings VALUES
(1, 'AAPL', 'Morgan Stanley', 'Overweight', 210.00, 'Overweight', 200.00, CURRENT_TIMESTAMP - INTERVAL '2 days', 'Erik Woodring'),
(2, 'AAPL', 'Goldman Sachs', 'Buy', 205.00, 'Buy', 195.00, CURRENT_TIMESTAMP - INTERVAL '5 days', 'Michael Ng'),
(3, 'AAPL', 'JP Morgan', 'Overweight', 215.00, 'Neutral', 185.00, CURRENT_TIMESTAMP - INTERVAL '1 week', 'Samik Chatterjee'),
(4, 'TSLA', 'Morgan Stanley', 'Overweight', 310.00, 'Equal-weight', 250.00, CURRENT_TIMESTAMP - INTERVAL '1 day', 'Adam Jonas'),
(5, 'TSLA', 'Wedbush', 'Outperform', 350.00, 'Outperform', 300.00, CURRENT_TIMESTAMP - INTERVAL '4 days', 'Dan Ives'),
(6, 'MSFT', 'Wedbush', 'Outperform', 450.00, 'Outperform', 425.00, CURRENT_TIMESTAMP - INTERVAL '3 days', 'Dan Ives'),
(7, 'GOOGL', 'Evercore ISI', 'Outperform', 165.00, 'Outperform', 155.00, CURRENT_TIMESTAMP - INTERVAL '5 days', 'Mark Mahaney'),
(8, 'NVDA', 'Bank of America', 'Buy', 600.00, 'Buy', 550.00, CURRENT_TIMESTAMP - INTERVAL '2 days', 'Vivek Arya');

-- ============================================================================
-- INSIDER TRADES
-- ============================================================================
CREATE TABLE mock_insider_trades (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10),
    insider_name VARCHAR(100),
    position VARCHAR(100),
    transaction_type VARCHAR(20),
    shares BIGINT,
    price_per_share DECIMAL(12,2),
    total_value BIGINT,
    shares_owned_after BIGINT,
    transaction_date DATE,
    filed_date DATE
);

INSERT INTO mock_insider_trades VALUES
(1, 'AAPL', 'Tim Cook', 'CEO', 'Sale', 500000, 185.50, 92750000, 3200000, CURRENT_DATE - 10, CURRENT_DATE - 8),
(2, 'AAPL', 'Luca Maestri', 'CFO', 'Sale', 150000, 186.20, 27930000, 850000, CURRENT_DATE - 12, CURRENT_DATE - 10),
(3, 'AAPL', 'Katherine Adams', 'General Counsel', 'Sale', 80000, 184.80, 14784000, 450000, CURRENT_DATE - 15, CURRENT_DATE - 13),
(4, 'TSLA', 'Elon Musk', 'CEO', 'Sale', 2000000, 248.50, 497000000, 411000000, CURRENT_DATE - 5, CURRENT_DATE - 3),
(5, 'TSLA', 'Zachary Kirkhorn', 'CFO', 'Purchase', 50000, 245.20, 12260000, 250000, CURRENT_DATE - 20, CURRENT_DATE - 18),
(6, 'MSFT', 'Satya Nadella', 'CEO', 'Sale', 300000, 382.50, 114750000, 1850000, CURRENT_DATE - 8, CURRENT_DATE - 6),
(7, 'GOOGL', 'Sundar Pichai', 'CEO', 'Sale', 400000, 140.80, 56320000, 2200000, CURRENT_DATE - 7, CURRENT_DATE - 5),
(8, 'NVDA', 'Jensen Huang', 'CEO', 'Sale', 120000, 475.50, 57060000, 3500000, CURRENT_DATE - 4, CURRENT_DATE - 2);

-- ============================================================================
-- SEC FILINGS (WITH FULL TEXT CONTENT)
-- ============================================================================
CREATE TABLE mock_sec_filings (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10),
    filing_type VARCHAR(20),
    filing_date DATE,
    filing_url TEXT,
    revenue BIGINT,
    net_income BIGINT,
    total_assets BIGINT,
    total_liabilities BIGINT,
    cash_and_equivalents BIGINT,
    total_debt BIGINT,
    eps DECIMAL(10,2),
    shares_outstanding BIGINT,
    risk_factors TEXT[],
    sentiment_score DECIMAL(5,2),
    fiscal_quarter VARCHAR(10),
    fiscal_year INTEGER,
    filing_text TEXT
);

INSERT INTO mock_sec_filings VALUES
(1, 'AAPL', '10-Q', CURRENT_DATE - 30, 'https://sec.gov/aapl-10q-q3-2024',
 89498000000, 22956000000, 352755000000, 290437000000, 28408000000, 106063000000,
 1.46, 15550321000,
 ARRAY['Supply chain disruptions', 'Geopolitical tensions', 'Currency fluctuations', 'Competition in smartphone market'],
 0.72, 'Q3', 2024,
 'APPLE INC. FORM 10-Q - QUARTERLY REPORT. For the fiscal quarter ended June 30, 2024. The Company designs, manufactures and markets smartphones, personal computers, tablets, wearables and accessories worldwide. Net sales for the quarter increased 8% year over year to $89.5 billion. iPhone revenue was $46.2 billion, up 5% from the prior year, driven by strong demand in emerging markets. Services revenue reached a new all-time high of $24.2 billion, up 12% year over year. Gross margin was 45.6%, up from 44.5% in the prior year quarter. Operating income was $27.4 billion with an operating margin of 30.6%. The Company returned over $28 billion to shareholders during the quarter through dividends and share repurchases. Looking forward, management expects continued strength in Services and wearables categories. The Company continues to invest heavily in research and development, with R&D expenses of $7.8 billion for the quarter. Key risks include supply chain constraints, foreign exchange headwinds, and increasing competition in key markets. The Company maintains a strong balance sheet with $166 billion in cash and marketable securities. Management remains confident in the long-term growth opportunities across the product portfolio and services ecosystem.');

INSERT INTO mock_sec_filings VALUES
(2, 'TSLA', '10-Q', CURRENT_DATE - 35, 'https://sec.gov/tsla-10q-q3-2024',
 23350000000, 1853000000, 106618000000, 43009000000, 26077000000, 2857000000,
 0.58, 3178920000,
 ARRAY['Manufacturing scale-up challenges', 'Raw material price volatility', 'Competition in EV market', 'Autonomous driving regulations'],
 0.65, 'Q3', 2024,
 'TESLA INC. FORM 10-Q - QUARTERLY REPORT. For the quarter ended September 30, 2024. Tesla is accelerating the world transition to sustainable energy through increasingly affordable electric vehicles and energy solutions. Total revenues increased 35% year over year to $23.4 billion. Automotive revenues were $19.6 billion, representing 84% of total revenue. Energy generation and storage revenues grew 148% to $1.6 billion, reflecting strong Megapack deployments. Vehicle deliveries totaled 435,000 units, up 40% year over year. Gross margin was 17.9%, impacted by reduced average selling prices and increased raw material costs. The company achieved a record operating margin of 9.6% driven by improved manufacturing efficiency. Production capacity continues to expand with the Berlin and Texas factories ramping production. Full Self-Driving beta expanded to over 400,000 customers. Capital expenditures were $2.5 billion focused on increasing production capacity and developing next-generation platforms. Key challenges include battery supply constraints, logistics costs, and competitive pressures. The company maintains strong liquidity with $26.1 billion in cash. Management expects continued volume growth and margin improvement through operational efficiencies and localized production.');

INSERT INTO mock_sec_filings VALUES
(3, 'MSFT', '10-Q', CURRENT_DATE - 25, 'https://sec.gov/msft-10q-q1-2024',
 56517000000, 22291000000, 411976000000, 205753000000, 111262000000, 79625000000,
 2.99, 7446000000,
 ARRAY['Cloud competition', 'Cybersecurity risks', 'Regulatory compliance', 'AI technology risks'],
 0.82, 'Q1', 2024,
 'MICROSOFT CORPORATION FORM 10-Q - QUARTERLY REPORT. For the quarter ended September 30, 2024. Microsoft enables digital transformation for the era of an intelligent cloud and an intelligent edge. Revenue increased 13% to $56.5 billion driven by strong performance across all segments. Intelligent Cloud revenue grew 19% to $24.3 billion with Azure growing 29%. Productivity and Business Processes revenue increased 12% to $18.6 billion with Office Commercial growing 15%. More Personal Computing revenue was $13.7 billion, up 3% driven by Windows OEM and Gaming. Operating income increased 25% to $26.9 billion with operating margin expanding to 48%. The company returned $9.7 billion to shareholders through dividends and share repurchases. AI services are being rapidly adopted with over 18,000 Azure AI customers, up 60% quarter over quarter. Microsoft 365 Copilot launched to commercial customers. Gaming revenue grew with strong Xbox content and services performance. The company invested $10.7 billion in capital expenditures primarily for cloud infrastructure to support AI workloads. Key opportunities include AI-powered products and cloud migration. Risks include intense competition, cybersecurity threats, and regulatory scrutiny. Commercial bookings increased 17% demonstrating strong customer demand. Management remains focused on innovation in AI and cloud computing.');

INSERT INTO mock_sec_filings VALUES
(4, 'GOOGL', '10-Q', CURRENT_DATE - 28, 'https://sec.gov/googl-10q-q3-2024',
 76693000000, 19689000000, 402392000000, 120258000000, 115617000000, 26348000000,
 1.55, 12696000000,
 ARRAY['Advertising revenue dependency', 'Privacy regulations', 'Antitrust investigations', 'AI safety concerns'],
 0.75, 'Q3', 2024,
 'ALPHABET INC. FORM 10-Q - QUARTERLY REPORT. For the quarter ended September 30, 2024. Alphabet is a collection of businesses including Google Search, ads, YouTube, Cloud, and Other Bets. Consolidated revenues grew 11% to $76.7 billion. Google Services revenues were $67.9 billion with Google Search growing 11% and YouTube ads growing 12%. Google Cloud revenue increased 22% to $8.4 billion achieving quarterly operating income of $266 million, the first time reaching profitability. Operating income grew 26% to $21.3 billion with operating margin of 28%. The company generated $23.1 billion in operating cash flow. Paid clicks grew 16% while cost-per-click decreased 2%. Traffic acquisition costs were $12.7 billion. The company announced new AI-powered features across products including Search Generative Experience and Bard. Investment in technical infrastructure was $8.1 billion to support AI initiatives. Headcount decreased 6% year over year reflecting efficiency initiatives. Key opportunities include AI integration, Cloud growth, and YouTube monetization. Primary risks include regulatory actions, competition, and content liability. The company faces multiple antitrust investigations globally. Management emphasizes continued investment in AI and machine learning capabilities while maintaining discipline on operating expenses.');

INSERT INTO mock_sec_filings VALUES
(5, 'NVDA', '10-Q', CURRENT_DATE - 20, 'https://sec.gov/nvda-10q-q2-2024',
 13507000000, 6188000000, 65728000000, 22407000000, 26024000000, 8463000000,
 2.48, 2500000000,
 ARRAY['Supply chain constraints', 'Export control regulations', 'Competition from alternatives', 'Demand volatility'],
 0.88, 'Q2', 2024,
 'NVIDIA CORPORATION FORM 10-Q - QUARTERLY REPORT. For the quarter ended July 30, 2024. NVIDIA pioneered accelerated computing to tackle challenges no one else can solve. Revenue surged 101% year over year to $13.5 billion, with Data Center revenue up 171% to $10.3 billion driven by generative AI and large language model adoption. Gaming revenue was $2.5 billion, up 22% reflecting strong demand for RTX 40 Series GPUs. Professional Visualization grew 28% to $379 million. Gross margin expanded to 70.1% from 57.1% in the prior year. Operating income more than tripled to $7.0 billion with operating margin of 52%. The company generated $7.2 billion in operating cash flow. Data Center compute platforms saw exceptional demand from cloud service providers and enterprises deploying AI infrastructure. NVIDIA H100 and A100 Tensor Core GPUs remain supply constrained. The company announced new products including GH200 Grace Hopper Superchip. Gaming momentum continues with over 150 RTX games released. Automotive revenue grew driven by autonomous vehicle platforms. Capital expenditures were $803 million to expand capacity. Key risks include export restrictions to China, supply constraints, and rapid technological change. Management expects continued strong demand for AI infrastructure but notes export controls as a headwind. The company maintains industry-leading position in accelerated computing and AI.');

-- ============================================================================
-- OPTIONS
-- ============================================================================
CREATE TABLE mock_options (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10),
    option_type VARCHAR(10),
    strike_price DECIMAL(12,2),
    expiration_date DATE,
    implied_volatility DECIMAL(10,2),
    open_interest INTEGER,
    volume INTEGER,
    bid DECIMAL(12,2),
    ask DECIMAL(12,2),
    last_price DECIMAL(12,2),
    delta DECIMAL(10,4),
    gamma DECIMAL(10,4),
    theta DECIMAL(10,4),
    vega DECIMAL(10,4),
    date DATE
);

INSERT INTO mock_options VALUES
(1, 'AAPL', 'CALL', 190.00, CURRENT_DATE + 30, 28.5, 15000, 2500, 3.20, 3.40, 3.30, 0.5250, 0.0125, -0.0850, 0.1250, CURRENT_DATE),
(2, 'AAPL', 'CALL', 195.00, CURRENT_DATE + 30, 30.2, 12000, 1800, 1.80, 2.00, 1.90, 0.3850, 0.0145, -0.0920, 0.1350, CURRENT_DATE),
(3, 'AAPL', 'PUT', 185.00, CURRENT_DATE + 30, 32.5, 18000, 3200, 2.50, 2.70, 2.60, -0.4250, 0.0135, -0.0780, 0.1180, CURRENT_DATE),
(4, 'AAPL', 'PUT', 180.00, CURRENT_DATE + 30, 35.8, 22000, 4500, 4.80, 5.00, 4.90, -0.5850, 0.0115, -0.0650, 0.1050, CURRENT_DATE),
(5, 'TSLA', 'CALL', 260.00, CURRENT_DATE + 30, 65.2, 25000, 5500, 8.50, 8.80, 8.65, 0.5450, 0.0095, -0.1250, 0.2150, CURRENT_DATE),
(6, 'TSLA', 'PUT', 250.00, CURRENT_DATE + 30, 68.5, 20000, 4200, 10.20, 10.50, 10.35, -0.4750, 0.0105, -0.1180, 0.2050, CURRENT_DATE),
(7, 'NVDA', 'CALL', 500.00, CURRENT_DATE + 30, 52.8, 30000, 7200, 15.20, 15.60, 15.40, 0.6150, 0.0085, -0.1450, 0.1850, CURRENT_DATE),
(8, 'NVDA', 'PUT', 490.00, CURRENT_DATE + 30, 55.2, 25000, 5800, 12.80, 13.20, 13.00, -0.4250, 0.0095, -0.1320, 0.1750, CURRENT_DATE);

-- ============================================================================
-- MACRO INDICATORS
-- ============================================================================
CREATE TABLE mock_macro_indicators (
    id SERIAL PRIMARY KEY,
    indicator_name VARCHAR(100),
    indicator_code VARCHAR(20),
    value DECIMAL(12,2),
    previous_value DECIMAL(12,2),
    date DATE,
    frequency VARCHAR(20),
    unit VARCHAR(50),
    source VARCHAR(50)
);

INSERT INTO mock_macro_indicators VALUES
(1, 'Federal Funds Rate', 'FFR', 5.50, 5.25, CURRENT_DATE - 30, 'Monthly', 'Percent', 'Federal Reserve'),
(2, 'Consumer Price Index', 'CPI', 3.2, 3.7, CURRENT_DATE - 30, 'Monthly', 'Percent YoY', 'BLS'),
(3, 'Unemployment Rate', 'UNRATE', 3.8, 3.9, CURRENT_DATE - 30, 'Monthly', 'Percent', 'BLS'),
(4, 'GDP Growth Rate', 'GDP', 2.9, 2.1, CURRENT_DATE - 90, 'Quarterly', 'Percent', 'BEA'),
(5, '10-Year Treasury Yield', 'DGS10', 4.35, 4.28, CURRENT_DATE, 'Daily', 'Percent', 'Treasury'),
(6, 'VIX Index', 'VIX', 16.5, 18.2, CURRENT_DATE, 'Daily', 'Index', 'CBOE'),
(7, 'PMI Manufacturing', 'PMI', 48.5, 49.2, CURRENT_DATE - 30, 'Monthly', 'Index', 'ISM'),
(8, 'Consumer Confidence', 'CONF', 102.5, 99.8, CURRENT_DATE - 30, 'Monthly', 'Index', 'Conference Board'),
(9, 'Housing Starts', 'HOUST', 1.42, 1.38, CURRENT_DATE - 30, 'Monthly', 'Millions', 'Census Bureau'),
(10, 'Industrial Production', 'INDPRO', 0.5, 0.3, CURRENT_DATE - 30, 'Monthly', 'Percent Change', 'Federal Reserve');

-- ============================================================================
-- INDEXES
-- ============================================================================
CREATE INDEX idx_fundamentals_sector ON mock_fundamentals(sector);
CREATE INDEX idx_fundamentals_industry ON mock_fundamentals(industry);
CREATE INDEX idx_prices_ticker_date ON mock_prices(ticker, date DESC);
CREATE INDEX idx_news_ticker_published ON mock_news(ticker, published_at DESC);
CREATE INDEX idx_news_sentiment ON mock_news(sentiment);
CREATE INDEX idx_analyst_ticker_date ON mock_analyst_ratings(ticker, rating_date DESC);
CREATE INDEX idx_insider_ticker_date ON mock_insider_trades(ticker, transaction_date DESC);
CREATE INDEX idx_sec_ticker_date ON mock_sec_filings(ticker, filing_date DESC);
CREATE INDEX idx_sec_filing_type ON mock_sec_filings(filing_type);
CREATE INDEX idx_options_ticker_exp ON mock_options(ticker, expiration_date);
CREATE INDEX idx_macro_date ON mock_macro_indicators(date DESC);

-- ============================================================================
-- SUMMARY
-- ============================================================================
SELECT 'Database Setup Complete!' as status;

SELECT 
    'mock_fundamentals' as table_name, 
    COUNT(*) as records 
FROM mock_fundamentals
UNION ALL
SELECT 'mock_prices', COUNT(*) FROM mock_prices
UNION ALL
SELECT 'mock_news', COUNT(*) FROM mock_news
UNION ALL
SELECT 'mock_analyst_ratings', COUNT(*) FROM mock_analyst_ratings
UNION ALL
SELECT 'mock_insider_trades', COUNT(*) FROM mock_insider_trades
UNION ALL
SELECT 'mock_sec_filings', COUNT(*) FROM mock_sec_filings
UNION ALL
SELECT 'mock_options', COUNT(*) FROM mock_options
UNION ALL
SELECT 'mock_macro_indicators', COUNT(*) FROM mock_macro_indicators
ORDER BY table_name;