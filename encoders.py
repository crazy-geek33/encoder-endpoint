from datetime import datetime
from pydantic import BaseModel, ValidationError, validator

class Account(BaseModel):
    accountNumber: int
    uniqueId: str
    accountStatus: str
    deviceStatus: str

class Balance(BaseModel):
    currentBalance: float
    availableCredit: float
    paymentDueDate: datetime
    minDuePayment: float
    cycletoDateSpend: float
    cashAvailable: float
    pastDueAmount: float
    creditLimit: float
    lastStatementDate: datetime
    lastStatementBalance: float
    callerType: str
    deviceSpendLimitlnd: bool
    overTheCreditLimit: float
    accountOutstandingAuthAmt: float
    cardOutstandingAuthorizedAmt: float
    cashAccessInd: bool
    flexLoanPayment: float
    memopostedPayment: bool
    cycleToDateSpendAvaialable: float
    spendLimit: float
    cashLine: float

    @validator('paymentDueDate', 'lastStatementDate', pre=True, always=True)
    def parse_datetime(cls, value):
        if isinstance(value, datetime):
            return value
        try:
            # Convert using ISO 8601 format; adjust if necessary
            return datetime.fromisoformat(value)
        except Exception:
            raise ValueError(f"Invalid datetime format: {value}")

# Example usage with sample data:
data = {
    'account': {
        'accountNumber': '123456',  # Automatically converted to int
        'uniqueId': 'ABC123',
        'accountStatus': 'Active',
        'deviceStatus': 'Active'
    },
    'balance': {
        'currentBalance': '1000.50',         # Automatically converted to float
        'availableCredit': '5000.00',          # Automatically converted to float
        'paymentDueDate': '2025-04-10T00:00:00',  # Converted to datetime
        'minDuePayment': '50.0',               # Automatically converted to float
        'cycletoDateSpend': '200.0',           # Automatically converted to float
        'cashAvailable': '100.0',              # Automatically converted to float
        'pastDueAmount': '0.0',                # Automatically converted to float
        'creditLimit': '6000.00',              # Automatically converted to float
        'lastStatementDate': '2025-03-10T00:00:00',  # Converted to datetime
        'lastStatementBalance': '900.50',      # Automatically converted to float
        'callerType': 'U',
        'deviceSpendLimitlnd': 'true',         # Automatically converted to bool
        'overTheCreditLimit': '0.0',           # Automatically converted to float
        'accountOutstandingAuthAmt': '0.0',    # Automatically converted to float
        'cardOutstandingAuthorizedAmt': '0.0', # Automatically converted to float
        'cashAccessInd': 'false',              # Automatically converted to bool
        'flexLoanPayment': '0.0',              # Automatically converted to float
        'memopostedPayment': 'false',          # Automatically converted to bool
        'cycleToDateSpendAvaialable': '200.0',  # Automatically converted to float
        'spendLimit': '1000.0',                # Automatically converted to float
        'cashLine': '150.0'                    # Automatically converted to float
    }
}

try:
    account_obj = Account(**data['account'])
    balance_obj = Balance(**data['balance'])
    print("Validation passed! Data has been successfully validated and converted.")
except ValidationError as e:
    print("Validation failed:", e)
