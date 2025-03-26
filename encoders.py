from typing import Dict, List
from scenarios.base import Scenario
from utils.helpers import extract_day, is_account_closed, is_device_closed

class CurrentBalanceScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        cardholder_type = data.get("cardHolderType", "").upper()
        
        if cardholder_type in {"Z", "Y", "X"}:
            responses.extend(self._process_conditions(data))
        else:
            responses.append("Unable to determine response for the given cardholder type.")
        return "\n".join(responses)

    def _process_conditions(self, data: Dict) -> List[str]:
        responses: List[str] = []
        current_balance = data.get("currentBalance", 0)
        
        # Group 1: Current Balance >= 0
        if current_balance >= 0:
            responses.append(f"Your balance is {current_balance}.")
        # Group 1: Current Balance < 0
        else:
            responses.append(f"You have a credit balance of {current_balance}.")
        
        # Group 2: Cash Access enabled
        cash_access = data.get("cashAccessEnabled", False)
        if cash_access:
            cash_balance = data.get("cashBalance", 0)
            responses.append(f"of which {cash_balance} is your cash balance.")
        
        # Group 3: Available Credit < 0
        available_credit = data.get("availableCredit", 0)
        if available_credit < 0:
            responses.append("which is over your credit limit.")
        
        # Group 4: Available Credit > 0
        if available_credit > 0:
            responses.append(f"Your available credit is {available_credit}.")
        
        # Group 5: Cash Available > 0 and Cash Access Enabled
        cash_available = data.get("cashAvailable", 0)
        if cash_available > 0 and cash_access:
            responses.append(f"of which {cash_available} may be used for cash advances.")
        
        # Group 6: Min Due Amount > 0
        min_due = data.get("minDuePayment", 0)
        if min_due > 0:
            payment_due_date = data.get("paymentDueDate", "")
            day_portion = extract_day(payment_due_date)
            responses.append(f"Your payment of {min_due} is due on {day_portion}.")
        
        return responses

from typing import Dict, List
from scenarios.base import Scenario

class StatementBalanceScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        cardholder_type = data.get("cardHolderType", "").upper()
        
        if cardholder_type in {"Z", "Y", "X"}:
            responses.extend(self._process_conditions(data))
        else:
            responses.append("Unable to determine response for the given cardholder type.")
        return "\n".join(responses)

    def _process_conditions(self, data: Dict) -> List[str]:
        responses: List[str] = []
        statement_balance = data.get("lastStatementBalance", 0)
        statement_date = data.get("lastStatementDate", "")
        
        # Group 1: Statement Balance >= 0
        if statement_balance >= 0:
            responses.append(f"Your {statement_date} statement had a balance of {statement_balance}.")
        # Group 1: Statement Balance < 0
        elif statement_balance < 0:
            responses.append(f"Your {statement_date} statement had a credit balance of {statement_balance}.")
        
        # Group 2: Statement Balance = 0
        if statement_balance == 0:
            responses.append("You did not receive a statement this month because your balance was zero dollars.")
        
        # Group 3: Minimum Payment Due
        min_due = data.get("minDuePayment", 0)
        if min_due > 0:
            payment_due_date = data.get("paymentDueDate", "")
            day_portion = extract_day(payment_due_date)
            responses.append(f"Your payment of {min_due} is due on {day_portion}.")
        
        return responses

from typing import Dict, List
from scenarios.base import Scenario

class BalanceDueScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        cardholder_type = data.get("cardHolderType", "").upper()
        
        if cardholder_type in {"Z", "Y", "X"}:
            responses.extend(self._process_conditions(data))
        else:
            responses.append("Unable to determine response for the given cardholder type.")
        return "\n".join(responses)

    def _process_conditions(self, data: Dict) -> List[str]:
        responses: List[str] = []
        balance = data.get("currentBalance", 0)
        
        # Group 1: Current Balance >= 0
        if balance >= 0:
            responses.append(f"Your balance is {balance}.")
        # Group 1: Current Balance < 0
        else:
            responses.append(f"You have a credit balance of {balance}.")
        
        # Group 2: Available Credit < 0
        available_credit = data.get("availableCredit", 0)
        if available_credit < 0:
            responses.append("which is over your credit limit.")
        
        # Group 3: Minimum Payment Due Amount > 0
        min_due = data.get("minDuePayment", 0)
        if min_due > 0:
            payment_due_date = data.get("paymentDueDate", "")
            day_portion = extract_day(payment_due_date)
            responses.append(f"Your payment of {min_due} is due on {day_portion}.")
        
        return responses

from typing import Dict, List
from scenarios.base import Scenario

class NegativeBalanceScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        cardholder_type = data.get("cardHolderType", "").upper()
        
        if cardholder_type in {"Z", "Y", "X"}:
            responses.extend(self._process_conditions(data))
        else:
            responses.append("Unable to determine response for the given cardholder type.")
        return "\n".join(responses)

    def _process_conditions(self, data: Dict) -> List[str]:
        responses: List[str] = []
        balance = data.get("currentBalance", 0)
        
        # Group 1: Current Balance >= 0
        if balance >= 0:
            responses.append(f"Your balance is {balance}.")
        # Group 1: Current Balance < 0
        else:
            responses.append(f"You have a credit balance of {balance}.")
        
        # Group 3: Account Status "Closed"
        account_status = data.get("accountStatus", "")
        if account_status == "Closed":
            responses.append("Your account is closed.")
        
        return responses

from typing import Dict, List
from scenarios.base import Scenario

class CreditLimitScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        cardholder_type = data.get("cardHolderType", "").upper()
        
        if cardholder_type in {"Z", "Y", "X"}:
            responses.extend(self._process_conditions(data))
        else:
            responses.append("Unable to determine response for the given cardholder type.")
        return "\n".join(responses)

    def _process_conditions(self, data: Dict) -> List[str]:
        responses: List[str] = []
        
        # Group 1: Credit Limit Information
        credit_limit = data.get("creditLimit", 0)
        if credit_limit > 0:
            responses.append(f"Your credit limit is {credit_limit}.")
        else:
            responses.append("You have no available credit limit.")
        
        # Group 2: Available Credit > 0
        available_credit = data.get("availableCredit", 0)
        if available_credit > 0:
            responses.append(f"Your available credit is {available_credit}.")
        
        # Group 3: Cash Available > 0 and Cash Access Enabled
        cash_available = data.get("cashAvailable", 0)
        cash_access_enabled = data.get("cashAccessEnabled", False)
        if cash_available > 0 and cash_access_enabled:
            responses.append(f"of which {cash_available} may be used for cash advances.")
        
        # Group 4: Account Status and Card Status
        account_status = data.get("accountStatus", "")
        card_status = data.get("cardStatus", "")
        
        if account_status == "Closed":
            responses.append("Your account is closed.")
        elif card_status == "InActive":
            responses.append("Your card is not active.")
        
        return responses

from typing import Dict, List
from scenarios.base import Scenario

class BalanceAndMakePaymentScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        cardholder_type = data.get("cardHolderType", "").upper()
        
        if cardholder_type in {"Z", "Y", "X"}:
            responses.extend(self._process_conditions(data))
        else:
            responses.append("Unable to determine response for the given cardholder type.")
        return "\n".join(responses)

    def _process_conditions(self, data: Dict) -> List[str]:
        responses: List[str] = []
        balance = data.get("currentBalance", 0)
        
        # Group 1: Current Balance >= 0
        if balance >= 0:
            responses.append(f"Your balance is {balance}.")
        # Group 1: Current Balance < 0
        else:
            responses.append(f"You have a credit balance of {balance}.")
        
        # Group 2: Cash Access enabled
        cash_access = data.get("cashAccessEnabled", False)
        if cash_access:
            cash_balance = data.get("cashBalance", 0)
            responses.append(f"of which {cash_balance} is your cash balance.")
        
        # Group 3: Available Credit < 0
        available_credit = data.get("availableCredit", 0)
        if available_credit < 0:
            responses.append("which is over your credit limit.")
        
        # Group 4: Available Credit > 0
        if available_credit > 0:
            responses.append(f"Your available credit is {available_credit}.")
        
        # Group 5: Cash Available > 0 and Cash Access Enabled
        cash_available = data.get("cashAvailable", 0)
        if cash_available > 0 and cash_access:
            responses.append(f"of which {cash_available} may be used for cash advances.")
        
        # Group 6: Min Due Amount > 0
        min_due = data.get("minDuePayment", 0)
        if min_due > 0:
            payment_due_date = data.get("paymentDueDate", "")
            day_portion = extract_day(payment_due_date)
            responses.append(f"Your payment of {min_due} is due on {day_portion}.")
        
        return responses
