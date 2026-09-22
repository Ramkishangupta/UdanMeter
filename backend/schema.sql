-- ==============================================================================
-- MoSPI Real-time Airfare Price Index (APIx) - PostgreSQL DDL Schema
-- Compatible with PostgreSQL 14+, Neon, Supabase, AWS RDS, Render Postgres
-- ==============================================================================

-- 1. Raw Airfare Quotes Table
CREATE TABLE IF NOT EXISTS raw_airfare_quotes (
    id SERIAL PRIMARY KEY,
    scraped_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
    source VARCHAR(100) NOT NULL,
    origin VARCHAR(10) NOT NULL,
    destination VARCHAR(10) NOT NULL,
    flight_number VARCHAR(50),
    carrier VARCHAR(100) NOT NULL,
    departure_date TIMESTAMP WITHOUT TIME ZONE,
    advance_days INTEGER NOT NULL,
    raw_fare DOUBLE PRECISION NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    scraped_status VARCHAR(50) DEFAULT 'SUCCESS'
);

CREATE INDEX IF NOT EXISTS idx_raw_scraped_at ON raw_airfare_quotes (scraped_at);
CREATE INDEX IF NOT EXISTS idx_raw_route ON raw_airfare_quotes (origin, destination);
CREATE INDEX IF NOT EXISTS idx_raw_carrier ON raw_airfare_quotes (carrier);
CREATE INDEX IF NOT EXISTS idx_raw_source ON raw_airfare_quotes (source);
CREATE INDEX IF NOT EXISTS idx_raw_advance ON raw_airfare_quotes (advance_days);

-- 2. Cleaned Airfare Quotes Table (Outliers Filtered & Decomposed)
CREATE TABLE IF NOT EXISTS cleaned_airfare_quotes (
    id SERIAL PRIMARY KEY,
    raw_quote_id INTEGER REFERENCES raw_airfare_quotes(id) ON DELETE SET NULL,
    scraped_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
    source VARCHAR(100) NOT NULL,
    carrier VARCHAR(100) NOT NULL,
    origin VARCHAR(10) NOT NULL,
    destination VARCHAR(10) NOT NULL,
    advance_days INTEGER NOT NULL,
    base_fare DOUBLE PRECISION NOT NULL,
    taxes_fees DOUBLE PRECISION NOT NULL,
    convenience_fee DOUBLE PRECISION NOT NULL,
    total_fare DOUBLE PRECISION NOT NULL,
    fare_class VARCHAR(50) DEFAULT 'Economy Standard',
    is_outlier BOOLEAN DEFAULT FALSE,
    z_score DOUBLE PRECISION DEFAULT 0.0
);

CREATE INDEX IF NOT EXISTS idx_clean_scraped_at ON cleaned_airfare_quotes (scraped_at);
CREATE INDEX IF NOT EXISTS idx_clean_route ON cleaned_airfare_quotes (origin, destination);
CREATE INDEX IF NOT EXISTS idx_clean_carrier ON cleaned_airfare_quotes (carrier);
CREATE INDEX IF NOT EXISTS idx_clean_advance ON cleaned_airfare_quotes (advance_days);
CREATE INDEX IF NOT EXISTS idx_clean_is_outlier ON cleaned_airfare_quotes (is_outlier);

-- 3. APIx Daily Indices Table (Fisher Ideal, Laspeyres, Paasche, Jevons)
CREATE TABLE IF NOT EXISTS apix_daily_indices (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP WITHOUT TIME ZONE UNIQUE NOT NULL,
    apix_national DOUBLE PRECISION NOT NULL,
    laspeyres_index DOUBLE PRECISION NOT NULL,
    paasche_index DOUBLE PRECISION NOT NULL,
    jevons_index DOUBLE PRECISION NOT NULL,
    cpi_transport_benchmark DOUBLE PRECISION NOT NULL,
    pct_change_daily DOUBLE PRECISION DEFAULT 0.0,
    pct_change_monthly DOUBLE PRECISION DEFAULT 0.0,
    pct_change_annual DOUBLE PRECISION DEFAULT 0.0
);

CREATE INDEX IF NOT EXISTS idx_apix_date ON apix_daily_indices (date);

-- 4. Route Weights Table (DGCA Passenger Traffic Weights)
CREATE TABLE IF NOT EXISTS route_weights (
    id SERIAL PRIMARY KEY,
    origin VARCHAR(10) NOT NULL,
    destination VARCHAR(10) NOT NULL,
    route_name VARCHAR(100) NOT NULL,
    dgca_passenger_share DOUBLE PRECISION NOT NULL,
    weight_factor DOUBLE PRECISION NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_rw_origin_dest ON route_weights (origin, destination);

-- 5. DGCA Benchmarks Table (Historical Validation)
CREATE TABLE IF NOT EXISTS dgca_benchmarks (
    id SERIAL PRIMARY KEY,
    month_year VARCHAR(20) NOT NULL,
    route VARCHAR(20) NOT NULL,
    dgca_published_avg_fare DOUBLE PRECISION NOT NULL,
    apix_backtested_avg_fare DOUBLE PRECISION NOT NULL,
    variance_pct DOUBLE PRECISION NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_dgca_month_route ON dgca_benchmarks (month_year, route);

-- ==============================================================================
-- Seed Primary DGCA Route Traffic Weights (Initial Baseline)
-- ==============================================================================
INSERT INTO route_weights (origin, destination, route_name, dgca_passenger_share, weight_factor)
VALUES
    ('DEL', 'BOM', 'Delhi - Mumbai', 0.18, 0.18),
    ('DEL', 'BLR', 'Delhi - Bengaluru', 0.14, 0.14),
    ('BOM', 'BLR', 'Mumbai - Bengaluru', 0.12, 0.12),
    ('DEL', 'CCU', 'Delhi - Kolkata', 0.09, 0.09),
    ('BLR', 'HYD', 'Bengaluru - Hyderabad', 0.08, 0.08),
    ('MAA', 'DEL', 'Chennai - Delhi', 0.08, 0.08),
    ('CCU', 'BLR', 'Kolkata - Bengaluru', 0.07, 0.07),
    ('DEL', 'HYD', 'Delhi - Hyderabad', 0.07, 0.07),
    ('BOM', 'GOI', 'Mumbai - Goa', 0.06, 0.06),
    ('BLR', 'MAA', 'Bengaluru - Chennai', 0.04, 0.04),
    ('DEL', 'PNQ', 'Delhi - Pune', 0.04, 0.04),
    ('BOM', 'AMD', 'Mumbai - Ahmedabad', 0.03, 0.03)
ON CONFLICT DO NOTHING;
