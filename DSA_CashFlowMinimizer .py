import datetime
import random

class Bank:
    def __init__(self, name):
        self.name = name
        self.net_amount = 0
        self.types = set()

class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, item):
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def peek(self):
        return self.heap[0] if self.heap else None

    def _heapify_up(self, index):
        parent = (index - 1) // 2
        while index > 0 and self.heap[index][0] < self.heap[parent][0]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent
            parent = (index - 1) // 2

    def _heapify_down(self, index):
        size = len(self.heap)
        smallest = index
        left, right = 2 * index + 1, 2 * index + 2

        if left < size and self.heap[left][0] < self.heap[smallest][0]:
            smallest = left
        if right < size and self.heap[right][0] < self.heap[smallest][0]:
            smallest = right

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

class CashFlowMinimizer:
    def __init__(self):
        self.banks = {}
        self.adj_list = {}
        self.transaction_history = []

    # [Previous methods remain the same]

    # New Risk Assessment Feature
    def assess_bank_risk(self):
        risk_scores = {}
        for bank_name, bank in self.banks.items():
            # Calculate risk based on transaction history and balance
            transactions = [t for t in self.transaction_history if t[0] == bank_name or t[1] == bank_name]
            
            # Risk factors
            total_transactions = len(transactions)
            total_amount = sum(abs(t[2]) for t in transactions)
            net_balance = abs(bank.net_amount)
            
            # Simple risk scoring algorithm
            risk_score = (
                (total_transactions * 0.3) + 
                (total_amount * 0.4) + 
                (net_balance * 0.3)
            )
            
            risk_category = (
                "Low Risk" if risk_score < 100 else
                "Medium Risk" if risk_score < 500 else
                "High Risk"
            )
            
            risk_scores[bank_name] = {
                "risk_score": risk_score,
                "risk_category": risk_category
            }
        
        print("\nBank Risk Assessment:")
        for bank, risk_data in risk_scores.items():
            print(f"{bank}: Risk Score {risk_data['risk_score']:.2f} - {risk_data['risk_category']}")

    # Fraud Detection Mechanism
    def detect_potential_fraud(self):
        fraud_indicators = []
        
        # Check for unusual transaction patterns
        for bank_name in self.banks:
            bank_transactions = [t for t in self.transaction_history if t[0] == bank_name or t[1] == bank_name]
            
            # Detect large transactions
            large_transactions = [t for t in bank_transactions if t[2] > 10000]
            if large_transactions:
                fraud_indicators.append({
                    "bank": bank_name,
                    "type": "Large Transactions",
                    "details": [f"{t[0]} -> {t[1]}: {t[2]} on {t[3]}" for t in large_transactions]
                })
            
            # Detect frequent transactions with same bank
            bank_connections = {}
            for t in bank_transactions:
                other_bank = t[1] if t[0] == bank_name else t[0]
                bank_connections[other_bank] = bank_connections.get(other_bank, 0) + 1
            
            suspicious_connections = {k: v for k, v in bank_connections.items() if v > 10}
            if suspicious_connections:
                fraud_indicators.append({
                    "bank": bank_name,
                    "type": "Suspicious Frequent Connections",
                    "details": suspicious_connections
                })
        
        if fraud_indicators:
            print("\nFraud Detection Report:")
            for indicator in fraud_indicators:
                print(f"Bank: {indicator['bank']}")
                print(f"Type: {indicator['type']}")
                print("Details:", indicator['details'])
                print("---")
        else:
            print("No potential fraud detected.")

    # Advanced Cash Flow Projection
    def advanced_cash_flow_projection(self, bank_name, months=6):
        # More sophisticated cash flow projection
        transactions = [t for t in self.transaction_history if t[0] == bank_name or t[1] == bank_name]
        
        if not transactions:
            print(f"No transaction data available for {bank_name}")
            return
        
        # Seasonal trend analysis
        monthly_trends = {}
        for t in transactions:
            month = t[3].month
            monthly_trends[month] = monthly_trends.get(month, []) + [t[2]]
        
        # Calculate monthly averages and projections
        projections = []
        current_balance = self.banks[bank_name].net_amount
        
        for i in range(1, months + 1):
            month = (datetime.datetime.now().month + i - 1) % 12 + 1
            monthly_avg = sum(monthly_trends.get(month, [0])) / len(monthly_trends.get(month, [1]))
            
            # Simple projection with some randomness
            projection = current_balance + monthly_avg * (1 + random.uniform(-0.1, 0.1))
            projections.append({
                "month": month,
                "projected_balance": projection
            })
            current_balance = projection
        
        print(f"\nCash Flow Projection for {bank_name} over {months} months:")
        for proj in projections:
            print(f"Month {proj['month']}: Projected Balance {proj['projected_balance']:.2f}")

    # Compliance and Regulatory Reporting
    def generate_regulatory_report(self):
        print("\nRegulatory Compliance Report:")
        
        # Total transaction volume
        total_transactions = len(self.transaction_history)
        total_transaction_amount = sum(t[2] for t in self.transaction_history)
        
        # Bank-wise breakdown
        bank_transaction_summary = {}
        for bank_name in self.banks:
            bank_transactions = [t for t in self.transaction_history if t[0] == bank_name or t[1] == bank_name]
            bank_transaction_summary[bank_name] = {
                "total_transactions": len(bank_transactions),
                "total_amount": sum(t[2] for t in bank_transactions)
            }
        
        print(f"Total Transactions: {total_transactions}")
        print(f"Total Transaction Volume: ${total_transaction_amount:,.2f}")
        
        print("\nBank-wise Transaction Summary:")
        for bank, summary in bank_transaction_summary.items():
            print(f"{bank}:")
            print(f"  Transactions: {summary['total_transactions']}")
            print(f"  Total Amount: ${summary['total_amount']:,.2f}")

def main():
    cash_flow = CashFlowMinimizer()

    while True:
        print("\nOptions:")
        print("1. Add Bank")
        print("2. Add Transaction")
        print("3. Predict Cash Flow")
        print("4. Get Bank Balance")
        print("5. View Bank Details")
        print("6. View Transaction History")
        print("7. Minimize Cash Flow")
        print("8. Get Top Debtor and Creditor")
        print("9. Clear Specific Transaction")
        print("10. Calculate Interest")
        print("11. Filter Transaction History by date and amount")
        print("12. Filter Transaction History by name")
        print("13. Generate Transaction Report")
        print("14. Get Most Active Bank")
        print("15. Generate Monthly Transaction Summary")
        print("16. Generate Bank Statement")
        print("17. Assess Bank Risk")
        print("18. Detect Potential Fraud")
        print("19. Advanced Cash Flow Projection")
        print("20. Generate Regulatory Report")
        print("21. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter bank name: ")
            types = set(input(f"Enter payment types for {name} (comma-separated): ").split(","))
            cash_flow.add_bank(name, types)
        elif choice == "2":
            debtor = input("Enter debtor bank: ")
            creditor = input("Enter creditor bank: ")
            amount = int(input("Enter transaction amount: "))
            cash_flow.add_transaction(debtor, creditor, amount)
        elif choice == "3":
            bank_name = input("Enter bank name for prediction: ")
            days = int(input("Enter number of days for prediction: "))
            cash_flow.predict_cash_flow(bank_name, days)
        elif choice == "4":
            bank_name = input("Enter bank name to check balance: ")
            cash_flow.get_bank_balance(bank_name)
        elif choice == "5":
            cash_flow.view_bank_details()
        elif choice == "6":
            cash_flow.view_transaction_history()
        elif choice == "7":
            cash_flow.minimize_cash_flow()
        elif choice == "8":
            cash_flow.get_top_debtor_creditor()
        elif choice == "9":
            index = int(input("Enter transaction index to clear: "))
            cash_flow.clear_specific_transaction(index)
        elif choice == "10":
            debtor = input("Enter debtor bank: ")
            creditor = input("Enter creditor bank: ")
            rate = float(input("Enter interest rate (%): "))
            days = int(input("Enter number of days for interest calculation: "))
            cash_flow.calculate_interest(debtor, creditor, rate, days)
        elif choice == "11":
            start_date = input("Enter start date (YYYY-MM-DD) or leave blank: ")
            end_date = input("Enter end date (YYYY-MM-DD) or leave blank: ")
            min_amount = input("Enter minimum transaction amount or leave blank: ")
            max_amount = input("Enter maximum transaction amount or leave blank: ")
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
            min_amount = int(min_amount) if min_amount else None
            max_amount = int(max_amount) if max_amount else None
            cash_flow.filter_transaction_by_date_and_amount(start_date, end_date, min_amount, max_amount)
        elif choice == "12":
            criteria = input("Enter criteria to filter transactions: ")
            cash_flow.filter_transaction_by_name(criteria)
        elif choice == "13":
            cash_flow.generate_transaction_report()
        elif choice == "14":
            cash_flow.get_most_active_bank()
        elif choice == "15":
            month = int(input("Enter month: "))
            year = int(input("Enter year: "))
            cash_flow.generate_monthly_summary(month, year)
        elif choice == "16":
            bank_name = input("Enter bank name: ")
            start_date_str = input("Enter start date (YYYY-MM-DD) or leave empty: ")
            end_date_str = input("Enter end date (YYYY-MM-DD) or leave empty: ")
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None
            cash_flow.generate_bank_statement(bank_name, start_date, end_date)
        elif choice == "17":
            cash_flow.assess_bank_risk()
        elif choice == "18":
            cash_flow.detect_potential_fraud()
        elif choice == "19":
            bank_name = input("Enter bank name for projection: ")
            months = int(input("Enter number of months for projection: "))
            cash_flow.advanced_cash_flow_projection(bank_name, months)
        elif choice == "20":
            cash_flow.generate_regulatory_report()
        elif choice == "21":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
