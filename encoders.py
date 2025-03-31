from typing import Dict, List
from scenarios.base import Scenario
from utils.helpers import extract_day

class CurrentBalanceScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        # Grouping 1: Current Balance
        current_balance = data.get("currentBalance", 0.0)
        if current_balance >= 0:
            responses.append(f"Your balance is {current_balance}.")
        else:
            responses.append(f"You have a credit balance of {current_balance}.")
        
        # Grouping 2: Cash Balance if cashAccessEnabled = True
        if data.get("cashAccessEnabled", False):
            cash_balance = data.get("cashBalance", 0.0)
            responses.append(f"of which {cash_balance} is your cash balance.")
        
        # Grouping 3: Available Credit OCL Advisory
        available_credit = data.get("availableCredit", 0.0)
        if available_credit < 0:
            responses.append("which is over your credit limit.")
        
        # Grouping 4: Available Credit message
        if available_credit > 0:
            responses.append(f"Your available credit is {available_credit}.")
        elif available_credit <= 0:
            responses.append("You have no available credit.")
        
        # Grouping 5: Cash Available condition
        if data.get("cashAccessEnabled", False):
            cash_available = data.get("cashAvailable", 0.0)
            if cash_available > 0:
                responses.append("of which I may be used for cash advances.")
        
        # Grouping 6: Minimum Payment Due Amount
        min_due = data.get("minDuePayment", 0.0)
        payment_due = data.get("paymentDueDate", "")
        day_portion = extract_day(payment_due)
        if min_due > 0:
            responses.append(f"Your payment of {min_due} is due on {day_portion}.")
        else:
            responses.append(f"No payment is due at this time. As a reminder, your payment due date is the {day_portion} of every month.")
        
        # Grouping 7: Account/Card status
        if data.get("accountStatus", "Active") == "Closed":
            responses.append("Your account is closed.")
        if data.get("cardStatus", "Active") == "InActive":
            responses.append("Your card is not active.")
        
        return "\n".join(responses)
from typing import Dict, List
from scenarios.base import Scenario
from utils.helpers import extract_day

class StatementBalanceScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        # Grouping 1: Last Statement Balance response
        last_stmt_balance = data.get("lastStatementBalance", 0.0)
        last_stmt_date = data.get("lastStatementDate", "")
        if last_stmt_balance > 0:
            responses.append(f"Your {last_stmt_date} statement had a balance of {last_stmt_balance}.")
        elif last_stmt_balance < 0:
            responses.append(f"Your {last_stmt_date} statement had a credit balance of {last_stmt_balance}.")
        else:
            responses.append("You did not receive a statement this month because your balance was zero dollars.")
        
        # Grouping 3: Minimum Payment Due Amount
        min_due = data.get("minDuePayment", 0.0)
        payment_due = data.get("paymentDueDate", "")
        day_portion = extract_day(payment_due)
        if min_due > 0:
            responses.append(f"Your payment of {min_due} is due on {day_portion}.")
        else:
            responses.append(f"No payment is due at this time. As a reminder, your payment due date is the {day_portion} of every month.")
        
        # Grouping 4: Account/Card status
        if data.get("accountStatus", "Active") == "Closed":
            responses.append("Your account is closed.")
        if data.get("cardStatus", "Active") == "InActive":
            responses.append("Your card is not active.")
        
        return "\n".join(responses)
from typing import Dict, List
from scenarios.base import Scenario
from utils.helpers import extract_day

class BalanceDueScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        # Grouping 1: Current Balance message
        current_balance = data.get("currentBalance", 0.0)
        if current_balance >= 0:
            responses.append(f"Your balance is {current_balance}.")
        else:
            responses.append(f"You have a credit balance of {current_balance}.")
        
        # Grouping 2: Available Credit check
        available_credit = data.get("availableCredit", 0.0)
        if available_credit < 0:
            responses.append("which is over your credit limit.")
        
        # Grouping 3: Minimum Payment Due Amount
        min_due = data.get("minDuePayment", 0.0)
        payment_due = data.get("paymentDueDate", "")
        day_portion = extract_day(payment_due)
        if min_due > 0:
            responses.append(f"Your payment of {min_due} is due on {day_portion}.")
        else:
            responses.append(f"No payment is due at this time. As a reminder, your payment due date is the {day_portion} of every month.")
        
        # Grouping 4: Past Due Amount
        past_due = data.get("pastDueAmount", 0.0)
        if past_due > 0:
            responses.append(f"which includes a {past_due} past due amount.")
        
        # Grouping 5: Recurring/Pending Payments conditions
        one_time = data.get("anyOneTimePymts", False)
        recur = data.get("anyRecurPymts", False)
        if one_time and recur:
            responses.append("Your account is currently set up for recurring payments, and you have one or more pending payment that have not yet posted.")
        elif (not one_time) and recur:
            responses.append("Your account is currently set up for recurring payments.")
        elif one_time and (not recur):
            responses.append("You have one or more pending payments that have not yet posted.")
        
        # Grouping 6: Account/Card status
        if data.get("accountStatus", "Active") == "Closed":
            responses.append("Your account is closed.")
        if data.get("cardStatus", "Active") == "InActive":
            responses.append("Your card is not active.")
        
        return "\n".join(responses)
from typing import Dict, List
from scenarios.base import Scenario

class NegativeBalanceScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        # Grouping 1: Current Balance message
        current_balance = data.get("currentBalance", 0.0)
        if current_balance >= 0:
            responses.append(f"Your balance is {current_balance}.")
        else:
            responses.append(f"You have a credit balance of {current_balance}.")
        
        # Grouping 3: Account/Card status
        if data.get("accountStatus", "Active") == "Closed":
            responses.append("Your account is closed.")
        if data.get("cardStatus", "Active") == "InActive":
            responses.append("Your card is not active.")
        
        return "\n".join(responses)
from typing import Dict, List
from scenarios.base import Scenario

class AvailableCreditScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        # Current Balance message
        current_balance = data.get("currentBalance", 0.0)
        if current_balance >= 0:
            responses.append(f"Your balance is {current_balance}.")
        else:
            responses.append(f"You have a credit balance of {current_balance}.")
        
        # Available Credit message
        available_credit = data.get("availableCredit", 0.0)
        if available_credit > 0:
            responses.append(f"Your available credit is {available_credit}.")
        else:
            responses.append("You have no available credit.")
        
        # Cash Available condition for cash advances
        if data.get("cashAccessEnabled", False):
            cash_available = data.get("cashAvailable", 0.0)
            if cash_available > 0:
                responses.append("of which I may be used for cash advances.")
        
        # Account/Card status
        if data.get("accountStatus", "Active") == "Closed":
            responses.append("Your account is closed.")
        if data.get("cardStatus", "Active") == "InActive":
            responses.append("Your card is not active.")
        
        return "\n".join(responses)
from typing import Dict, List
from scenarios.base import Scenario

class CreditLimitScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        # Grouping 1: Credit Limit
        credit_limit = data.get("creditLimit", 0.0)
        responses.append(f"Your credit limit is {credit_limit}.")
        
        # Grouping 2: Available Credit message
        available_credit = data.get("availableCredit", 0.0)
        if available_credit > 0:
            responses.append(f"Your available credit is {available_credit}.")
        else:
            responses.append("You have no available credit.")
        
        # Grouping 3: Cash Available for cash advances
        if data.get("cashAccessEnabled", False):
            cash_available = data.get("cashAvailable", 0.0)
            if cash_available > 0:
                responses.append("of which I may be used for cash advances.")
        
        # Grouping 4: Account/Card status
        if data.get("accountStatus", "Active") == "Closed":
            responses.append("Your account is closed.")
        if data.get("cardStatus", "Active") == "InActive":
            responses.append("Your card is not active.")
        
        return "\n".join(responses)
from typing import Dict, List
from scenarios.base import Scenario
from utils.helpers import extract_day

class BalanceAndMakeAPaymentScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        # Grouping 1: Current Balance
        current_balance = data.get("currentBalance", 0.0)
        if current_balance >= 0:
            responses.append(f"Your balance is {current_balance}.")
        else:
            responses.append(f"You have a credit balance of {current_balance}.")
        
        # Grouping 2: Cash Balance (if cashAccessEnabled true)
        if data.get("cashAccessEnabled", False):
            cash_balance = data.get("cashBalance", 0.0)
            responses.append(f"of which {cash_balance} is your cash balance.")
        
        # Grouping 3: OCL Advisory for Available Credit < 0
        available_credit = data.get("availableCredit", 0.0)
        if available_credit < 0:
            responses.append("which is over your credit limit.")
        
        # Grouping 4: Available Credit message
        if available_credit > 0:
            responses.append(f"Your available credit is {available_credit}.")
        elif available_credit <= 0:
            responses.append("You have no available credit.")
        
        # Grouping 5: Cash Available for cash advances
        if data.get("cashAccessEnabled", False):
            cash_available = data.get("cashAvailable", 0.0)
            if cash_available > 0:
                responses.append("of which I may be used for cash advances.")
        
        # Grouping 6: Minimum Payment Due Amount
        min_due = data.get("minDuePayment", 0.0)
        payment_due = data.get("paymentDueDate", "")
        day_portion = extract_day(payment_due)
        if min_due > 0:
            responses.append(f"Your payment of {min_due} is due on {day_portion}.")
        else:
            responses.append(f"No payment is due at this time. As a reminder, your payment due date is the {day_portion} of every month.")
        
        # Grouping 7: Account/Card status
        if data.get("accountStatus", "Active") == "Closed":
            responses.append("Your account is closed.")
        if data.get("cardStatus", "Active") == "InActive":
            responses.append("Your card is not active.")
        
        return "\n".join(responses)
