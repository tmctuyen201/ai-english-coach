-- AI English Coach — Database Init Script
-- This runs automatically when PostgreSQL container starts for the first time

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create tables (will be created by SQLAlchemy, but this provides backup)
-- See backend/app/models/models.py for full schema
