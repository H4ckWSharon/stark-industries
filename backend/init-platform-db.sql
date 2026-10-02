-- STARK INDUSTRIES SQL — Platform DB initialization
-- This runs on first start of the postgres-platform container

-- (Tables are created by SQLAlchemy on startup via init_db())
-- This file can hold seed data or extensions

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Verify setup
SELECT version();
