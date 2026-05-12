CREATE TABLE IF NOT EXISTS invoices (
    id                  SERIAL PRIMARY KEY,
    invoice_number      VARCHAR(50) UNIQUE NOT NULL,
    invoice_date        DATE,
    vendor_name         VARCHAR(255),
    vendor_address      VARCHAR(255),
    customer_name       VARCHAR(255),
    customer_address    VARCHAR(255),
    subtotal            DECIMAL(12, 2) DEFAULT 0.00,
    discount            DECIMAL(12, 2) DEFAULT 0.00,
    shipping            DECIMAL(12, 2) DEFAULT 0.00,
    tax                 DECIMAL(12, 2) DEFAULT 0.00,
    total               DECIMAL(12, 2) DEFAULT 0.00,
    currency            VARCHAR(10) DEFAULT 'USD',
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS invoice_items (
    id           SERIAL PRIMARY KEY,
    invoice_id   INT NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
    name         VARCHAR(255) NOT NULL,
    quantity     INT DEFAULT 1,
    unit_price   DECIMAL(12, 2) DEFAULT 0.00,
    total        DECIMAL(12, 2) DEFAULT 0.00
);