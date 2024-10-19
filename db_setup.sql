-- db_setup.sql
CREATE TABLE rules (
    id SERIAL PRIMARY KEY,
    rule_name VARCHAR(100),
    rule_ast JSONB,  -- Stores the AST as a JSON structure
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
