from datetime import date
from flask import Flask, jsonify, request
from database import init_db, save_fund, get_all_funds, get_fund_by_id, update_fund_performance, delete_fund
from investment_fund import InvestmentFund

app = Flask(__name__)

init_db()

def validate_fund_data(data):
    required_fields = ['fund_name', 'manager_name', 'description', 'nav', 'creation_date', 'performance']
    for field in required_fields:
        if field not in data:
            return f"Missing field: {field}"
    try:
        date.fromisoformat(data['creation_date'])
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD."
    return None

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad Request", "message": str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found", "message": str(error)}), 404

@app.route('/funds', methods=['GET'])
def get_funds():
    funds = get_all_funds()
    return jsonify([fund.get_fund_details() for fund in funds])

@app.route('/funds', methods=['POST'])
def create_fund():
    data = request.json
    error = validate_fund_data(data)
    if error:
        return jsonify({"error": error}), 400
    
    new_fund = InvestmentFund(
        fund_name=data['fund_name'],
        manager_name=data['manager_name'],
        description=data['description'],
        nav=data['nav'],
        creation_date=date.fromisoformat(data['creation_date']),
        performance=data['performance']
    )
    save_fund(new_fund)
    return jsonify(new_fund.get_fund_details()), 201

@app.route('/funds/<int:fund_id>', methods=['GET'])
def get_fund(fund_id):
    fund = get_fund_by_id(fund_id)
    if fund:
        return jsonify(fund.get_fund_details())
    return not_found("Fund not found")

@app.route('/funds/<int:fund_id>/performance', methods=['PUT'])
def update_performance(fund_id):
    data = request.json
    if "performance" not in data:
        return bad_request("Missing 'performance' field")
    
    fund = get_fund_by_id(fund_id)
    if not fund:
        return not_found("Fund not found")
    
    update_fund_performance(fund_id, data['performance'])
    fund = get_fund_by_id(fund_id)
    return jsonify(fund.get_fund_details())

@app.route('/funds/<int:fund_id>', methods=['DELETE'])
def delete_fund_route(fund_id):
    if not get_fund_by_id(fund_id):
        return not_found("Fund not found")
    
    delete_fund(fund_id)
    return jsonify({"message": "Fund deleted"})

if __name__ == '__main__':
    app.run(debug=True)
