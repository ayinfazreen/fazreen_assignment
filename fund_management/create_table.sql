CREATE TABLE funds (
    fund_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_name TEXT NOT NULL,
    manager_name TEXT NOT NULL,
    description TEXT,
    nav REAL NOT NULL,
    creation_date TEXT NOT NULL,
    performance REAL NOT NULL
);

CREATE TABLE investors (
    investor_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT
);

CREATE TABLE fund_transactions (
    transaction_id INTEGER PRIMARY KEY,
    fund_id INTEGER NOT NULL,
    investor_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    transaction_date TEXT NOT NULL,
    transaction_type TEXT CHECK(transaction_type IN ('BUY', 'SELL')) NOT NULL,
    FOREIGN KEY (fund_id) REFERENCES funds (fund_id) ON DELETE CASCADE,
    FOREIGN KEY (investor_id) REFERENCES investors (investor_id) ON DELETE CASCADE
);

