-- Create new tables if they don’t exist
CREATE TABLE IF NOT EXISTS investors (
    investor_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT
);

CREATE TABLE IF NOT EXISTS fund_transactions (
    transaction_id INTEGER PRIMARY KEY,
    fund_id INTEGER NOT NULL,
    investor_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    transaction_date TEXT NOT NULL,
    transaction_type TEXT CHECK(transaction_type IN ('BUY', 'SELL')) NOT NULL,
    FOREIGN KEY (fund_id) REFERENCES funds (fund_id) ON DELETE CASCADE,
    FOREIGN KEY (investor_id) REFERENCES investors (investor_id) ON DELETE CASCADE
);

-- Insert existing fund data into the new schema
INSERT INTO funds (fund_id, fund_name, manager_name, description, nav, creation_date, performance)
SELECT fund_id, fund_name, manager_name, description, nav, creation_date, performance FROM old_funds;

-- Insert sample investors (since they don’t exist in the old DB)
INSERT INTO investors (name, email, phone) 
VALUES 
    ('Alice Johnson', 'alice@example.com', '123-456-7890'),
    ('Bob Smith', 'bob@example.com', '987-654-3210');

-- Insert sample transactions (this step assumes that each fund has at least one transaction)
INSERT INTO fund_transactions (fund_id, investor_id, amount, transaction_date, transaction_type)
VALUES
    (1, 1, 1000.00, '2024-02-01', 'BUY'),
    (2, 2, 500.00, '2024-02-10', 'SELL');
