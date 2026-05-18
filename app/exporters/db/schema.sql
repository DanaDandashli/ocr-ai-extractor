CREATE TABLE IF NOT EXISTS documents (
    id            SERIAL PRIMARY KEY,
    document_type VARCHAR(100),
    data          JSONB,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);