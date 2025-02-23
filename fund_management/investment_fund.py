from datetime import date

class InvestmentFund:
    def __init__(self, fund_name: str, manager_name: str, description: str, nav: float, creation_date: date, performance: float):
        self.fund_name = fund_name
        self.manager_name = manager_name
        self.description = description
        self.nav = nav
        self.creation_date = creation_date
        self.performance = performance
    
    def update_nav(self, new_nav: float):
        """Update the Net Asset Value (NAV) of the fund."""
        self.nav = new_nav
    
    def update_performance(self, new_performance: float):
        """Update the fund's performance percentage."""
        self.performance = new_performance
    
    def get_fund_details(self):
        """Return a dictionary containing the fund details."""
        print(self.creation_date, 'creation_date')
        return {
            "Fund Name": self.fund_name,
            "Fund Manager": self.manager_name,
            "Description": self.description,
            "Net Asset Value (NAV)": self.nav,
            "Date of Creation": self.creation_date,
            "Performance (%)": self.performance
        }
    
    def __str__(self):
        return f"Fund {self.fund_name} managed by {self.manager_name}, NAV: {self.nav}, Performance: {self.performance}%"
