import sqlite3
from datetime import date
from investment_fund import InvestmentFund

DB_NAME = "funds.db"

def init_db():
    """Initialize the SQLite database and create the funds table if not exists."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS funds (
                fund_id INTEGER PRIMARY KEY AUTOINCREMENT,
                fund_name TEXT NOT NULL,
                manager_name TEXT NOT NULL,
                description TEXT,
                nav REAL NOT NULL,
                creation_date TEXT NOT NULL,
                performance REAL NOT NULL
            )
        ''')
        conn.commit()

def save_fund(fund: InvestmentFund):
    """Save a new fund to the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO funds (fund_name, manager_name, description, nav, creation_date, performance)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (fund.fund_name, fund.manager_name, fund.description, fund.nav, fund.creation_date.strftime("%Y-%m-%d"), fund.performance))
        conn.commit()

def get_all_funds():
    """Retrieve all funds from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM funds')
        rows = cursor.fetchall()
        #return rows
        # for row in rows:
        #     print(row[1:])
        #print(InvestmentFund(*row[5:], float(row[6])) for row in rows)
        return [InvestmentFund(*row[1:6], float(row[6])) for row in rows]

def get_fund_by_id(fund_id: int):
    """Retrieve a specific fund by ID."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM funds WHERE fund_id = ?', (fund_id,))
        row = cursor.fetchone()
        return InvestmentFund(*row[:6], float(row[6])) if row else None

def update_fund_performance(fund_id: int, new_performance: float):
    """Update the performance of an existing fund."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE funds SET performance = ? WHERE fund_id = ?', (new_performance, fund_id))
        conn.commit()

def delete_fund(fund_id: int):
    """Delete a fund from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM funds WHERE fund_id = ?', (fund_id,))
        conn.commit()

# Initialize the database when this script is run
if __name__ == "__main__":
    init_db()
