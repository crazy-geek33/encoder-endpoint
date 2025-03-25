from typing import Dict, List
from scenarios.base import Scenario
from utils.helpers import extract_day, is_account_closed, is_device_closed

class CurrentBalanceScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        balance = data.get("currentBalance", 0)
        caller_type = data.get("callerType", "").upper()
        
        if balance >= 0:
            responses.append(f"Your balance is {balance}.")
        else:
            responses.append(f"You have a credit balance of {balance}.")
        
        # Additional scenarios based on available credit and cash balance
        available_credit = data.get("availableCredit", 0)
        if available_credit > 0:
            responses.append(f"Your available credit is {available_credit}.")
        
        cash_balance = data.get("cashBalance", 0)
        cash_access_enabled = data.get("cashAccessEnabled", False)
        
        if cash_access_enabled and cash_balance > 0:
            responses.append(f"of which {cash_balance} is your cash balance.")
        elif not cash_access_enabled:
            responses.append("DO NOT SCRIPT")

        # Check account status
        account_status = data.get("accountStatus", "")
        if is_account_closed(account_status):
            responses.append("Your account is closed.")
        elif account_status == "Inactive":
            responses.append("Your account is not active.")
        
        # Check card status
        card_status = data.get("cardStatus", "")
        if card_status == "Inactive":
            responses.append("Your card is not active.")
        elif card_status == "Closed":
            responses.append("Your card is closed.")
        
        return "\n".join(responses)

from typing import Dict, List
from scenarios.base import Scenario
from utils.helpers import is_account_closed, is_device_closed

class StatementBalanceScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        last_statement_balance = data.get("lastStatementBalance", 0)
        last_statement_date = data.get("lastStatementDate", "")
        
        if last_statement_balance >= 0:
            responses.append(f"Your {last_statement_date} statement had a balance of {last_statement_balance}.")
        else:
            responses.append(f"Your {last_statement_date} statement had a credit balance of {last_statement_balance}.")
        
        # Check account status
        account_status = data.get("accountStatus", "")
        if is_account_closed(account_status):
            responses.append("Your account is closed.")
        elif account_status == "Inactive":
            responses.append("Your account is not active.")
        
        # Check card status
        card_status = data.get("cardStatus", "")
        if card_status == "Inactive":
            responses.append("Your card is not active.")
        elif card_status == "Closed":
            responses.append("Your card is closed.")
        
        return "\n".join(responses)


from typing import Dict, List
from scenarios.base import Scenario
from utils.helpers import is_account_closed, is_device_closed

class BalanceDueScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        balance = data.get("currentBalance", 0)
        min_due = data.get("minDuePayment", 0)
        past_due_amount = data.get("pastDueAmount", 0)
        
        if balance >= 0:
            responses.append(f"Your balance is {balance}.")
        else:
            responses.append(f"You have a credit balance of {balance}.")
        
        if min_due > 0:
            payment_due_date = data.get("paymentDueDate", "")
            responses.append(f"Your minimum payment of {min_due} is due on {payment_due_date}.")
        
        if past_due_amount > 0:
            responses.append(f"which includes a {past_due_amount} past due amount.")
        
        # Check account status
        account_status = data.get("accountStatus", "")
        if is_account_closed(account_status):
            responses.append("Your account is closed.")
        elif account_status == "Inactive":
            responses.append("Your account is not active.")
        
        # Check card status
        card_status = data.get("cardStatus", "")
        if card_status == "Inactive":
            responses.append("Your card is not active.")
        elif card_status == "Closed":
            responses.append("Your card is closed.")
        
        return "\n".join(responses)


from typing import Dict, List
from scenarios.base import Scenario
from utils.helpers import is_account_closed, is_device_closed

class NegativeBalanceScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        balance = data.get("currentBalance", 0)
        
        if balance < 0:
            responses.append(f"You have a credit balance of {balance}.")
        else:
            responses.append(f"Your balance is {balance}.")
        
        # Check account status
        account_status = data.get("accountStatus", "")
        if is_account_closed(account_status):
            responses.append("Your account is closed.")
        elif account_status == "Inactive":
            responses.append("Your account is not active.")
        
        # Check card status
        card_status = data.get("cardStatus", "")
        if card_status == "Inactive":
            responses.append("Your card is not active.")
        elif card_status == "Closed":
            responses.append("Your card is closed.")
        
        return "\n".join(responses)


from typing import Dict, List
from scenarios.base import Scenario
from utils.helpers import is_account_closed, is_device_closed

class AvailableCreditScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        available_credit = data.get("availableCredit", 0)
        
        if available_credit > 0:
            responses.append(f"Your available credit is {available_credit}.")
        else:
            responses.append("You have no available credit.")
        
        # Check account status
        account_status = data.get("accountStatus", "")
        if is_account_closed(account_status):
            responses.append("Your account is closed.")
        elif account_status == "Inactive":
            responses.append("Your account is not active.")
        
        # Check card status
        card_status = data.get("cardStatus", "")
        if card_status == "Inactive":
            responses.append("Your card is not active.")
        elif card_status == "Closed":
            responses.append("Your card is closed.")
        
        return "\n".join(responses)


from typing import Dict, List
from scenarios.base import Scenario
from utils.helpers import is_account_closed, is_device_closed

class CreditLimitScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        credit_limit = data.get("creditLimit", 0)
        available_credit = data.get("availableCredit", 0)
        
        # If credit limit is provided
        responses.append(f"Your credit limit is {credit_limit}.")
        
        # Check Available Credit condition
        if available_credit > 0:
            responses.append(f"Your available credit is {available_credit}.")
        else:
            responses.append("You have no available credit.")
        
        # Check account status
        account_status = data.get("accountStatus", "")
        if is_account_closed(account_status):
            responses.append("Your account is closed.")
        elif account_status == "Inactive":
            responses.append("Your account is not active.")
        
        # Check card status
        card_status = data.get("cardStatus", "")
        if card_status == "Inactive":
            responses.append("Your card is not active.")
        elif card_status == "Closed":
            responses.append("Your card is closed.")
        
        return "\n".join(responses)


from typing import Dict, List
from scenarios.base import Scenario
from utils.helpers import is_account_closed, is_device_closed

class BalanceAndMakePaymentScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        balance = data.get("currentBalance", 0)
        min_due_payment = data.get("minDuePayment", 0)
        cash_balance = data.get("cashBalance", 0)
        cash_access_enabled = data.get("cashAccessEnabled", False)
        
        if balance >= 0:
            responses.append(f"Your balance is {balance}.")
        else:
            responses.append(f"You have a credit balance of {balance}.")
        
        # Cash Balance and Cash Access enabled
        if cash_access_enabled and cash_balance > 0:
            responses.append(f"of which {cash_balance} is your cash balance.")
        elif not cash_access_enabled:
            responses.append("DO NOT SCRIPT")

        # Available Credit condition
        available_credit = data.get("availableCredit", 0)
        if available_credit < 0:
            responses.append("which is over your credit limit.")
        elif available_credit > 0:
            responses.append(f"Your available credit is {available_credit}.")
        else:
            responses.append("You have no available credit.")
        
        # Minimum Payment Due condition
        if min_due_payment > 0:
            payment_due_date = data.get("paymentDueDate", "")
            responses.append(f"Your minimum payment of {min_due_payment} is due on {payment_due_date}.")
        else:
            day_due = extract_day(data.get("paymentDueDate", ""))
            responses.append(f"No payment is due at this time. As a reminder, your payment due date is the {day_due} of every month.")
        
        # Check account status
        account_status = data.get("accountStatus", "")
        if is_account_closed(account_status):
            responses.append("Your account is closed.")
        elif account_status == "Inactive":
            responses.append("Your account is not active.")
        
        # Check card status
        card_status = data.get("cardStatus", "")
        if card_status == "Inactive":
            responses.append("Your card is not active.")
        elif card_status == "Closed":
            responses.append("Your card is closed.")
        
        return "\n".join(responses)


def extract_day(date_str: str) -> str:
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%d").lstrip("0") or dt.strftime("%d")
    except Exception:
        return date_str
