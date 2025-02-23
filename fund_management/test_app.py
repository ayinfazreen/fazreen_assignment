import pytest
import sqlite3
from app import app
from database import init_db, save_fund, get_fund_by_id, delete_fund
from investment_fund import InvestmentFund
from datetime import date

# Setup test database
TEST_DB = "test_funds.db"

@pytest.fixture(scope="module")
def test_client():
    app.config["TESTING"] = True
    with app.test_client() as testing_client:
        with app.app_context():
            init_db()
        yield testing_client

@pytest.fixture(scope="function")
def sample_fund():
    """Creates a sample fund for testing."""
    fund = InvestmentFund(
        fund_id=1,
        fund_name="Tech Growth Fund",
        manager_name="John Doe",
        description="A fund focused on tech startups",
        nav=150.75,
        creation_date=date.today(),
        performance=12.5
    )
    save_fund(fund)
    yield fund
    delete_fund(fund.fund_id)

def test_get_all_funds(test_client):
    """Test retrieving all funds when database is empty."""
    response = test_client.get("/funds")
    assert response.status_code == 200
    assert response.json == []

def test_create_fund(test_client):
    """Test creating a new fund."""
    fund_data = {
        "fund_id": 2,
        "fund_name": "Energy Fund",
        "manager_name": "Jane Smith",
        "description": "Focus on renewable energy",
        "nav": 200.50,
        "creation_date": str(date.today()),
        "performance": 10.0
    }
    response = test_client.post("/funds", json=fund_data)
    assert response.status_code == 201
    assert response.json["fund_name"] == "Energy Fund"

def test_get_fund_by_id(test_client, sample_fund):
    """Test retrieving a fund by ID."""
    response = test_client.get(f"/funds/{sample_fund.fund_id}")
    assert response.status_code == 200
    assert response.json["fund_name"] == sample_fund.fund_name

def test_update_fund_performance(test_client, sample_fund):
    """Test updating a fund's performance."""
    new_performance = 15.5
    response = test_client.put(f"/funds/{sample_fund.fund_id}/performance", json={"performance": new_performance})
    assert response.status_code == 200
    assert response.json["performance"] == new_performance

def test_delete_fund(test_client, sample_fund):
    """Test deleting a fund."""
    response = test_client.delete(f"/funds/{sample_fund.fund_id}")
    assert response.status_code == 200
    assert response.json == {"message": "Fund deleted"}
    
    response = test_client.get(f"/funds/{sample_fund.fund_id}")
    assert response.status_code == 404
