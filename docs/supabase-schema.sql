-- AI Captain Production Database Schema
-- Run this in the Supabase SQL Editor

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Routes Table
CREATE TABLE IF NOT EXISTS routes (
    id VARCHAR(36) PRIMARY KEY,
    source_port VARCHAR(100) NOT NULL,
    destination_port VARCHAR(100) NOT NULL,
    distance FLOAT NOT NULL,
    eta FLOAT NOT NULL,
    risk_score INTEGER DEFAULT 0,
    geometry JSONB NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Route History Table
CREATE TABLE IF NOT EXISTS route_history (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id),
    route_id VARCHAR(36) NOT NULL REFERENCES routes(id),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
