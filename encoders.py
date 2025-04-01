import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

def generate_account_data(n=100):
    account_data = []
    for _ in range(n):
        # Using a 10-digit account number for realism
        account_number = random.randint(1000000000, 9999999999)
        unique_id = fake.uuid4()
        account_status = random.choice(["Closed", "Active"])
        device_status = random.choice(["InActive", "Active"])
        account_data.append({
            "accountNumber": account_number,
            "uniqueId": unique_id,
            "accountStatus": account_status,
            "deviceStatus": device_status
        })
    return pd.DataFrame(account_data)

def generate_balance_data(n=100):
    balance_data = []
    for _ in range(n):
        # Credit limit realistic range (e.g., for credit cards)
        credit_limit = round(random.uniform(1000, 15000), 2)
        
        # With a small chance the current balance goes over the limit (simulate overspending)
        if random.random() < 0.1:
            current_balance = round(random.uniform(credit_limit, credit_limit * 1.2), 2)
        else:
            current_balance = round(random.uniform(0, credit_limit), 2)
        
        # Available credit is what remains (or zero if over limit)
        available_credit = round(credit_limit - current_balance, 2) if current_balance <= credit_limit else 0.0
        
        # Last statement date between 30 and 60 days ago
        last_statement_date = fake.date_time_between(start_date="-60d", end_date="-30d")
        # Payment due date typically about 20 days after the statement
        payment_due_date = last_statement_date + timedelta(days=20)
        
        # Minimum due payment: at least $25 or 3% of current balance (if balance > 0)
        min_due_payment = round(max(25, current_balance * 0.03), 2) if current_balance > 0 else 0.0
        
        # Cycle-to-date spend: assume it's between 50% to 100% of the current balance
        cycle_to_date_spend = round(random.uniform(0.5 * current_balance, current_balance), 2) if current_balance > 0 else 0.0
        
        # Remaining spend available in this cycle (cannot be negative)
        cycle_to_date_spend_available = round(max(credit_limit - cycle_to_date_spend, 0.0), 2)
        
        # Cash available for cash advances: typically a fraction (e.g., 30%) of the credit limit
        cash_available = round(0.3 * credit_limit, 2)
        
        # Past due amount: a small amount, with a 20% chance of being non-zero
        past_due_amount = round(random.uniform(0, 50), 2) if random.random() < 0.2 else 0.0
        
        # Last statement balance: current balance adjusted by +/- 10%
        last_statement_balance = round(current_balance * (1 + random.uniform(-0.1, 0.1)), 2)
        
        caller_type = random.choice(["U", "P", "A", "E", "O"])
        device_spend_limit_ind = random.choice([True, False])
        
        # Calculate any amount over the credit limit
        over_the_credit_limit = round(current_balance - credit_limit, 2) if current_balance > credit_limit else 0.0
        
        # Authorized amounts: a small fraction (up to 10% of current balance)
        account_outstanding_auth_amt = round(random.uniform(0, 0.1 * current_balance), 2) if current_balance > 0 else 0.0
        card_outstanding_authorized_amt = round(random.uniform(0, 0.1 * current_balance), 2) if current_balance > 0 else 0.0
        
        cash_access_ind = random.choice([True, False])
        
        # Flex loan payment: simulate a scheduled payment, sometimes applicable
        flex_loan_payment = round(random.uniform(25, 500), 2) if random.random() < 0.5 else 0.0
        
        memoposted_payment = random.choice([True, False])
        
        # Spend limit: we assume it to be the same as the credit limit
        spend_limit = credit_limit
        
        # Cash line: usually a portion (e.g., 20%) of the credit limit
        cash_line = round(0.2 * credit_limit, 2)
        
        balance_data.append({
            "currentBalance": current_balance,
            "availableCredit": available_credit,
            "paymentDueDate": payment_due_date.isoformat(),
            "minDuePayment": min_due_payment,
            "cycletoDateSpend": cycle_to_date_spend,
            "cashAvailable": cash_available,
            "pastDueAmount": past_due_amount,
            "creditLimit": credit_limit,
            "lastStatementDate": last_statement_date.isoformat(),
            "lastStatementBalance": last_statement_balance,
            "callerType": caller_type,
            "deviceSpendLimitlnd": device_spend_limit_ind,
            "overTheCreditLimit": over_the_credit_limit,
            "accountOutstandingAuthAmt": account_outstanding_auth_amt,
            "cardOutstandingAuthorizedAmt": card_outstanding_authorized_amt,
            "cashAccessInd": cash_access_ind,
            "flexLoanPayment": flex_loan_payment,
            "memopostedPayment": memoposted_payment,
            "cycleToDateSpendAvaialable": cycle_to_date_spend_available,
            "spendLimit": spend_limit,
            "cashLine": cash_line
        })
    return pd.DataFrame(balance_data)

if __name__ == "__main__":
    n = 100  # Number of records to generate
    accounts_df = generate_account_data(n)
    balances_df = generate_balance_data(n)
    accounts_df.to_csv("accounts.csv", index=False)
    balances_df.to_csv("balances.csv", index=False)
    print("CSV files generated: accounts.csv and balances.csv")

import csv
from neo4j import GraphDatabase

# Configure your Neo4j connection details
uri = "bolt://localhost:7687"
username = "neo4j"
password = "password"  # update with your Neo4j password

driver = GraphDatabase.driver(uri, auth=(username, password))

def create_account_and_balance(tx, account, balance):
    query = """
    MERGE (a:Account {accountNumber: $accountNumber})
      SET a.uniqueId = $uniqueId, 
          a.accountStatus = $accountStatus, 
          a.deviceStatus = $deviceStatus
    MERGE (b:Balance {
          currentBalance: $currentBalance,
          availableCredit: $availableCredit,
          paymentDueDate: datetime($paymentDueDate),
          minDuePayment: $minDuePayment,
          cycletoDateSpend: $cycletoDateSpend,
          cashAvailable: $cashAvailable,
          pastDueAmount: $pastDueAmount,
          creditLimit: $creditLimit,
          lastStatementDate: datetime($lastStatementDate),
          lastStatementBalance: $lastStatementBalance,
          callerType: $callerType,
          deviceSpendLimitlnd: $deviceSpendLimitlnd,
          overTheCreditLimit: $overTheCreditLimit,
          accountOutstandingAuthAmt: $accountOutstandingAuthAmt,
          cardOutstandingAuthorizedAmt: $cardOutstandingAuthorizedAmt,
          cashAccessInd: $cashAccessInd,
          flexLoanPayment: $flexLoanPayment,
          memopostedPayment: $memopostedPayment,
          cycleToDateSpendAvaialable: $cycleToDateSpendAvaialable,
          spendLimit: $spendLimit,
          cashLine: $cashLine
    })
    MERGE (a)-[:HAS_BALANCE]->(b)
    """
    tx.run(query, **account, **balance)

def ingest_data():
    with driver.session() as session:
        with open("accounts.csv", newline='') as account_file, open("balances.csv", newline='') as balance_file:
            account_reader = csv.DictReader(account_file)
            balance_reader = csv.DictReader(balance_file)
            for account, balance in zip(account_reader, balance_reader):
                # Convert Account types
                account["accountNumber"] = int(account["accountNumber"])
                
                # Convert Balance fields to appropriate types
                balance["currentBalance"] = float(balance["currentBalance"])
                balance["availableCredit"] = float(balance["availableCredit"])
                balance["minDuePayment"] = float(balance["minDuePayment"])
                balance["cycletoDateSpend"] = float(balance["cycletoDateSpend"])
                balance["cashAvailable"] = float(balance["cashAvailable"])
                balance["pastDueAmount"] = float(balance["pastDueAmount"])
                balance["creditLimit"] = float(balance["creditLimit"])
                balance["lastStatementBalance"] = float(balance["lastStatementBalance"])
                balance["overTheCreditLimit"] = float(balance["overTheCreditLimit"])
                balance["accountOutstandingAuthAmt"] = float(balance["accountOutstandingAuthAmt"])
                balance["cardOutstandingAuthorizedAmt"] = float(balance["cardOutstandingAuthorizedAmt"])
                balance["flexLoanPayment"] = float(balance["flexLoanPayment"])
                balance["cycleToDateSpendAvaialable"] = float(balance["cycleToDateSpendAvaialable"])
                balance["spendLimit"] = float(balance["spendLimit"])
                balance["cashLine"] = float(balance["cashLine"])
                
                # Convert boolean fields
                balance["deviceSpendLimitlnd"] = balance["deviceSpendLimitlnd"].strip().lower() == 'true'
                balance["cashAccessInd"] = balance["cashAccessInd"].strip().lower() == 'true'
                balance["memopostedPayment"] = balance["memopostedPayment"].strip().lower() == 'true'
                
                # Date fields (paymentDueDate and lastStatementDate) are already in ISO format.
                
                session.write_transaction(create_account_and_balance, account, balance)
                print(f"Inserted Account {account['accountNumber']} with its Balance.")

if __name__ == "__main__":
    ingest_data()
    print("Data ingestion completed.")

