from typing import Dict, List
from scenarios.base import Scenario
from utils.helpers import extract_day, is_account_closed, is_device_closed

class BalanceDueScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        cardholder_type = data.get("cardHolderType", "").upper()
        spend_limit_flag = data.get("deviceSpendLimitInd", True)
        
        if cardholder_type in {"P", "O", "U"}:
            responses.extend(self._process_pou(data))
        elif cardholder_type == "A" and spend_limit_flag is True:
            responses.extend(self._process_a_no_spend(data))
        elif cardholder_type == "E" and spend_limit_flag is True:
            responses.extend(self._process_e_no_spend(data))
        elif cardholder_type in {"A", "E"} and spend_limit_flag is False:
            responses.extend(self._process_a_e_spend_limit(data))
        else:
            responses.append("Unable to determine response for the given cardholder type.")
        return "\n".join(responses)
    
    def _process_pou(self, data: Dict) -> List[str]:
        responses: List[str] = []
        balance = data.get("adjustedBalanceAmount", 0)
        account_status = data.get("accountStatusCode", 0)
        pending_auth = data.get("accountOutstandingAuthAmt", 0)
        over_credit = data.get("overTheCreditLimit", 0)
        min_due = data.get("totalDueAmount", 0)
        payment_due_date = data.get("paymentDueDate", "")
        day_portion = extract_day(payment_due_date)
        past_due = data.get("totalDeliquencyAmount", 0)
        flex_loan = data.get("flexLoanPayment", 0)
        is_closed = is_account_closed(account_status)
        
        if balance < 0:
            # Balance < $0
            if is_closed:
                responses.append(f"You have a credit balance of {balance} and your account is closed.")
            else:
                responses.append(f"You have a credit balance of {balance}.")
        elif balance > 0:
            has_pending = pending_auth > 0
            has_ocl = over_credit > 0
            if has_ocl and has_pending:
                if is_closed:
                    responses.append(f"Your balance is {balance} which is over your credit limit and does not include some pending charges. Also, your account is closed")
                else:
                    responses.append(f"Your balance is {balance} which is over your credit limit and does not include some pending charges.")
            elif has_ocl:
                if is_closed:
                    responses.append(f"Your balance is {balance} which is over your credit limit and your account is closed")
                else:
                    responses.append(f"Your balance is {balance} which is over your credit limit.")
            elif has_pending:
                if is_closed:
                    responses.append(f"Your balance is {balance} not including some pending charges and your account is closed")
                else:
                    responses.append(f"Your balance is {balance} not including some pending charges.")
            else:
                if is_closed:
                    responses.append(f"Your balance is {balance} and your account is closed.")
                else:
                    responses.append(f"Your balance is {balance}.")
        
        if min_due == 0:
            responses.append(f"No payment is due at this time. As a reminder, your payment due date is the {day_portion} of every month.")
        elif min_due > 0:
            if flex_loan > 0:
                if past_due > 0:
                    responses.append(f"Your minimum payment of {min_due} is due on {day_portion}. This includes a past due amount of {past_due}. Your Citi Flex Plan Payment Amount is included in your Minimum Payment Due.")
                else:
                    responses.append(f"Your minimum payment of {min_due} is due on {day_portion}. Your Citi Flex Plan Payment Amount is included in your Minimum Payment Due.")
            else:
                if past_due > 0:
                    responses.append(f"Your minimum payment of {min_due} is due on {day_portion}. This includes a past due amount of {past_due}.")
                else:
                    responses.append(f"Your minimum payment of {min_due} is due on {day_portion}.")
        
        if data.get("memopostedPayment", False):
            responses.append("We received your most recent payment which is currently pending. Details will be available on the next business day.")
        return responses
    
    def _process_a_no_spend(self, data: Dict) -> List[str]:
        responses: List[str] = []
        balance = data.get("adjustedBalanceAmount", 0)
        device_status = data.get("deviceStatusCode", 0)
        pending_auth = data.get("cardOutstandingAuthorizedAmt", 0)
        over_credit = data.get("overTheCreditLimit", 0)
        min_due = data.get("totalDueAmount", 0)
        payment_due_date = data.get("paymentDueDate", "")
        day_portion = extract_day(payment_due_date)
        past_due = data.get("totalDeliquencyAmount", 0)
        flex_loan = data.get("flexLoanPayment", 0)
        is_dev_closed = is_device_closed(device_status)
        
        if balance < 0:
            # Balance < $0
            if is_dev_closed:
                responses.append(f"You have a credit balance of {balance} and your card is not active.")
            else:
                responses.append(f"You have a credit balance of {balance}.")
        elif balance > 0:
            has_pending = pending_auth > 0
            has_ocl = over_credit > 0
            if has_ocl and has_pending:
                if is_dev_closed:
                    responses.append(f"Your balance is {balance} which is over your credit limit and does not include some pending charges. Also, your card is not active.")
                else:
                    responses.append(f"Your balance is {balance} which is over your credit limit and does not include some pending charges.")
            elif has_ocl:
                if is_dev_closed:
                    responses.append(f"Your balance is {balance} which is over your credit limit and your card is not active.")
                else:
                    responses.append(f"Your balance is {balance} which is over your credit limit.")
            elif has_pending:
                if is_dev_closed:
                    responses.append(f"Your balance is {balance} not including some pending charges and your card is not active.")
                else:
                    responses.append(f"Your balance is {balance} not including some pending charges.")
            else:
                if is_dev_closed:
                    responses.append(f"Your balance is {balance} and your card is not active.")
                else:
                    responses.append(f"Your balance is {balance}.")
        
        if min_due == 0:
            responses.append(f"No payment is due at this time. As a reminder, your payment due date is the {day_portion} of every month.")
        elif min_due > 0:
            if flex_loan > 0:
                if past_due > 0:
                    responses.append(f"Your minimum payment of {min_due} is due on {day_portion}. This includes a past due amount of {past_due}. Your Citi Flex Plan Payment Amount is included in your Minimum Payment Due.")
                else:
                    responses.append(f"Your minimum payment of {min_due} is due on {day_portion}. Your Citi Flex Plan Payment Amount is included in your Minimum Payment Due.")
            else:
                if past_due > 0:
                    responses.append(f"Your minimum payment of {min_due} is due on {day_portion}. This includes a past due amount of {past_due}.")
                else:
                    responses.append(f"Your minimum payment of {min_due} is due on {day_portion}.")
        
        if data.get("memopostedPayment", False):
            responses.append("We received your most recent payment which is currently pending. Details will be available on the next business day.")
        return responses

    def _process_e_no_spend(self, data: Dict) -> List[str]:
        responses: List[str] = []
        balance = data.get("adjustedBalanceAmount", 0)
        device_status = data.get("deviceStatusCode", 0)
        pending_auth = data.get("cardOutstandingAuthorizedAmt", 0)
        over_credit = data.get("overTheCreditLimit", 0)
        min_due = data.get("totalDueAmount", 0)
        payment_due_date = data.get("paymentDueDate", "")
        day_portion = extract_day(payment_due_date)
        past_due = data.get("totalDeliquencyAmount", 0)
        flex_loan = data.get("flexLoanPayment", 0)
        is_dev_closed = is_device_closed(device_status)
        
        # Replicating A no spend logic for E no spend
        if balance < 0:
            if is_dev_closed:
                responses.append(f"You have a credit balance of {balance} and your card is not active.")
            else:
                responses.append(f"You have a credit balance of {balance}.")
        elif balance > 0:
            has_pending = pending_auth > 0
            has_ocl = over_credit > 0
            if has_ocl and has_pending:
                if is_dev_closed:
                    responses.append(f"Your balance is {balance} which is over your credit limit and does not include some pending charges. Also, your card is not active.")
                else:
                    responses.append(f"Your balance is {balance} which is over your credit limit and does not include some pending charges.")
            elif has_ocl:
                if is_dev_closed:
                    responses.append(f"Your balance is {balance} which is over your credit limit and your card is not active.")
                else:
                    responses.append(f"Your balance is {balance} which is over your credit limit.")
            elif has_pending:
                if is_dev_closed:
                    responses.append(f"Your balance is {balance} not including some pending charges and your card is not active.")
                else:
                    responses.append(f"Your balance is {balance} not including some pending charges.")
            else:
                if is_dev_closed:
                    responses.append(f"Your balance is {balance} and your card is not active.")
                else:
                    responses.append(f"Your balance is {balance}.")
        
        if min_due == 0:
            responses.append(f"No payment is due at this time. As a reminder, your payment due date is the {day_portion} of every month.")
        elif min_due > 0:
            if flex_loan > 0:
                if past_due > 0:
                    responses.append(f"Your minimum payment of {min_due} is due on {day_portion}. This includes a past due amount of {past_due}. Your Citi Flex Plan Payment Amount is included in your Minimum Payment Due.")
                else:
                    responses.append(f"Your minimum payment of {min_due} is due on {day_portion}. Your Citi Flex Plan Payment Amount is included in your Minimum Payment Due.")
            else:
                if past_due > 0:
                    responses.append(f"Your minimum payment of {min_due} is due on {day_portion}. This includes a past due amount of {past_due}.")
                else:
                    responses.append(f"Your minimum payment of {min_due} is due on {day_portion}.")
        
        if data.get("memopostedPayment", False):
            responses.append("We received your most recent payment which is currently pending. Details will be available on the next business day.")
        return responses
    
    def _process_a_e_spend_limit(self, data: Dict) -> List[str]:
        responses: List[str] = []
        ctd_spend = data.get("ctdPurchaseBalanceAmount", 0)
        device_status = data.get("deviceStatusCode", 0)
        pending_auth = data.get("cardOutstandingAuthorizedAmt", 0)
        is_dev_closed = is_device_closed(device_status)
        
        if is_dev_closed:
            if pending_auth > 0:
                responses.append(f"Your Cycle-To-Date spend balance is {ctd_spend}, not including some pending charges and your card is not active.")
            else:
                responses.append(f"Your Cycle-To-Date spend balance is {ctd_spend} and your card is not active.")
        else:
            if pending_auth > 0:
                responses.append(f"Your Cycle-To-Date spend balance is {ctd_spend}, not including some pending charges.")
            else:
                responses.append(f"Your Cycle-To-Date spend balance is {ctd_spend}.")
        return responses

#  scenarios/credit_limit.py 
from typing import Dict, List
from scenarios.base import Scenario
from utils.helpers import extract_day, is_account_closed, is_device_closed

class CreditLimitScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        cardholder_type = data.get("cardHolderType", "").upper()
        spend_limit_flag = data.get("deviceSpendLimitInd", True)
        
        if cardholder_type in {"P", "O", "U"}:
            responses.extend(self._process_pou(data))
        elif cardholder_type == "A" and spend_limit_flag is True:
            responses.extend(self._process_a_no_spend(data))
        elif cardholder_type == "E" and spend_limit_flag is True:
            responses.extend(self._process_e_no_spend(data))
        elif cardholder_type in {"A", "E"} and spend_limit_flag is False:
            responses.extend(self._process_a_e_spend_limit(data))
        else:
            responses.append("Unable to determine response for the given cardholder type.")
        return "\n".join(responses)
    
    # P/O/U branch
    def _process_pou(self, data: Dict) -> List[str]:
        responses: List[str] = []
        # Output credit limit (I)
        credit_limit = data.get("creditLimit", 0)
        responses.append(f"Your credit limit is {credit_limit}")
        
        account_status = data.get("accountStatusCode", 0)
        if is_account_closed(account_status):
            # Available Credit (B) with Account Closed (N)
            responses.append("You have no available credit because your account is currently closed")
        else:
            available_credit = data.get("availableCreditAmount", 0)
            cash_line = data.get("cashAdvanceLimitAmount", 0)
            cash_avail = data.get("cashAvailable", 0)
            if available_credit > 0:
                if cash_line == 0:
                    responses.append(f"Your available credit is {available_credit}.")
                elif available_credit <= cash_avail:
                    responses.append(f"Your available credit is {available_credit} all of which can be used for cash advances")
                else:
                    responses.append(f"Your available credit is {available_credit} of which {cash_avail} may be used for cash advances.")
        
        # Payment due conditions
        min_due = data.get("totalDueAmount", 0)
        payment_due_date = data.get("paymentDueDate", "")
        day_portion = extract_day(payment_due_date)
        if min_due == 0:
            responses.append(f"No payment is due at this time. As a reminder, your payment due date is the {day_portion} of every month.")
        elif min_due > 0:
            flex_loan = data.get("flexLoanPayment", 0)
            if flex_loan > 0:
                responses.append(f"Your minimum payment of {min_due} is due on {day_portion}. Your Citi Flex Plan Payment Amount is included in your Minimum Payment Due.")
            else:
                responses.append(f"Your minimum payment of {min_due} is due on {day_portion}.")
        return responses
    
    # A no spend limit branch
    def _process_a_no_spend(self, data: Dict) -> List[str]:
        responses: List[str] = []
        available_credit = data.get("availableCreditAmount", 0)
        device_status = data.get("deviceStatusCode", 0)
        if is_device_closed(device_status):
            responses.append("You have no available credit because your card is not active.")
        elif available_credit > 0:
            cash_line = data.get("cashAdvanceLimitAmount", 0)
            cash_avail = data.get("cashAvailable", 0)
            if cash_line == 0:
                responses.append(f"Your available credit is {available_credit}.")
            elif available_credit <= cash_avail:
                responses.append(f"Your available credit is {available_credit} all of which can be used for cash advances")
            else:
                responses.append(f"Your available credit is {available_credit} of which {cash_avail} may be used for cash advances.")
        # Payment due conditions
        min_due = data.get("totalDueAmount", 0)
        payment_due_date = data.get("paymentDueDate", "")
        day_portion = extract_day(payment_due_date)
        if min_due == 0:
            responses.append(f"No payment is due at this time. As a reminder, your payment due date is the {day_portion} of every month.")
        elif min_due > 0:
            flex_loan = data.get("flexLoanPayment", 0)
            if flex_loan > 0:
                responses.append(f"Your minimum payment of {min_due} is due on {day_portion}. Your Citi Flex Plan Payment Amount is included in your Minimum Payment Due.")
            else:
                responses.append(f"Your minimum payment of {min_due} is due on {day_portion}.")
        return responses

    # E no spend limit branch
    def _process_e_no_spend(self, data: Dict) -> List[str]:
        responses: List[str] = []
        available_credit = data.get("availableCreditAmount", 0)
        device_status = data.get("deviceStatusCode", 0)
        if is_device_closed(device_status):
            responses.append("You have no available credit because your card is not active.")
        elif available_credit > 0:
            cash_line = data.get("cashAdvanceLimitAmount", 0)
            cash_avail = data.get("cashAvailable", 0)
            if cash_line == 0:
                responses.append(f"Your available credit is {available_credit}.")
            elif available_credit <= cash_avail:
                responses.append(f"Your available credit is {available_credit} all of which can be used for cash advances")
            else:
                responses.append(f"Your available credit is {available_credit} of which {cash_avail} may be used for cash advances.")
        # Payment due conditions
        min_due = data.get("totalDueAmount", 0)
        payment_due_date = data.get("paymentDueDate", "")
        day_portion = extract_day(payment_due_date)
        if min_due == 0:
            responses.append(f"No payment is due at this time. As a reminder, your payment due date is the {day_portion} of every month.")
        elif min_due > 0:
            flex_loan = data.get("flexLoanPayment", 0)
            if flex_loan > 0:
                responses.append(f"Your minimum payment of {min_due} is due on {day_portion}. Your Citi Flex Plan Payment Amount is included in your Minimum Payment Due.")
            else:
                responses.append(f"Your minimum payment of {min_due} is due on {day_portion}.")
        return responses

    # A/E with Spend Limit branch
    def _process_a_e_spend_limit(self, data: Dict) -> List[str]:
        responses: List[str] = []
        # Spend Limit (W) response
        spend_limit = data.get("purchaseSpendLimitAmount", 0)
        responses.append(f"Your spend limit is {spend_limit}.")
        
        available_spend = data.get("cycleToDateSpendAvailable", 0)
        device_status = data.get("deviceStatusCode", 0)
        if is_device_closed(device_status):
            responses.append("You have no available spend because your card is not active")
        else:
            cash_access = data.get("cashAccessIndicator", False)
            cash_avail = data.get("cashAvailable", 0)
            if not cash_access:
                responses.append(f"Your available spend is {available_spend}. Your available spending limit may be affected by the overall account balance.")
            else:
                if available_spend <= cash_avail:
                    responses.append(f"Your available spend is {available_spend}, all of which can be used for cash advances. Your available spending limit may be affected by the overall account balance., leverage <cashAccessIndicator> to know if customer has cash access")
                else:
                    responses.append(f"Your available spend is {available_spend} of which {cash_avail} may be used for cash advances. Your available spending limit may be affected by the overall account balance.")
        return responses

#  scenarios/available_credit.py 
from typing import Dict, List
from scenarios.base import Scenario
from utils.helpers import extract_day, is_account_closed, is_device_closed

class AvailableCreditScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        cardholder_type = data.get("cardHolderType", "").upper()
        spend_limit_flag = data.get("deviceSpendLimitInd", True)
        
        if cardholder_type in {"P", "O", "U"}:
            responses.extend(self._process_pou(data))
        elif cardholder_type == "A" and spend_limit_flag is True:
            responses.extend(self._process_a_no_spend(data))
        elif cardholder_type == "E" and spend_limit_flag is True:
            responses.extend(self._process_e_no_spend(data))
        elif cardholder_type in {"A", "E"} and spend_limit_flag is False:
            responses.extend(self._process_a_e_spend_limit(data))
        else:
            responses.append("Unable to determine response for the given cardholder type.")
        return "\n".join(responses)
    
    # P/O/U branch
    def _process_pou(self, data: Dict) -> List[str]:
        responses: List[str] = []
        balance = data.get("adjustedBalanceAmount", 0)
        over_credit = data.get("overTheCreditLimit", 0)
        pending_auth = data.get("accountOutstandingAuthAmt", 0)
        
        if balance < 0:
            responses.append(f"You have a credit balance of {balance}.")
        elif balance > 0:
            if over_credit > 0 and pending_auth > 0:
                responses.append(f"Your balance is {balance} which is over your credit limit and does not include some pending charges.")
            elif over_credit > 0:
                responses.append(f"Your balance is {balance} which is over your credit limit.")
            elif pending_auth > 0:
                responses.append(f"Your balance is {balance} not including some pending charges.")
            else:
                responses.append(f"Your balance is {balance}.")
        
        # Check Available Credit conditions
        account_status = data.get("accountStatusCode", 0)
        if is_account_closed(account_status):
            responses.append("You have no available credit because your account is currently closed")
        else:
            available_credit = data.get("availableCreditAmount", 0)
            if available_credit > 0:
                cash_line = data.get("cashAdvanceLimitAmount", 0)
                cash_avail = data.get("cashAvailable", 0)
                if cash_line == 0:
                    responses.append(f"Your available credit is {available_credit}.")
                elif available_credit <= cash_avail:
                    responses.append(f"Your available credit is {available_credit} all of which can be used for cash advances")
                else:
                    responses.append(f"Your available credit is {available_credit} of which {cash_avail} may be used for cash advances.")
        return responses

    # A no spend limit branch
    def _process_a_no_spend(self, data: Dict) -> List[str]:
        responses: List[str] = []
        balance = data.get("adjustedBalanceAmount", 0)
        over_credit = data.get("overTheCreditLimit", 0)
        pending_auth = data.get("cardOutstandingAuthorizedAmt", 0)
        
        if balance < 0:
            responses.append(f"You have a credit balance of {balance}.")
        elif balance > 0:
            if over_credit > 0 and pending_auth > 0:
                responses.append(f"Your balance is {balance} which is over your credit limit and does not include some pending charges.")
            elif over_credit > 0:
                responses.append(f"Your balance is {balance} which is over your credit limit.")
            elif pending_auth > 0:
                responses.append(f"Your balance is {balance} not including some pending charges.")
            else:
                responses.append(f"Your balance is {balance}.")
        
        # Check Available Credit conditions for A no spend
        device_status = data.get("deviceStatusCode", 0)
        if is_device_closed(device_status):
            responses.append("You have no available credit because your card is not active.")
        else:
            available_credit = data.get("availableCreditAmount", 0)
            if available_credit > 0:
                cash_line = data.get("cashAdvanceLimitAmount", 0)
                cash_avail = data.get("cashAvailable", 0)
                if cash_line == 0:
                    responses.append(f"Your available credit is {available_credit}.")
                elif available_credit <= cash_avail:
                    responses.append(f"Your available credit is {available_credit} all of which can be used for cash advances")
                else:
                    responses.append(f"Your available credit is {available_credit} of which {cash_avail} may be used for cash advances.")
        return responses

    # E no spend limit branch
    def _process_e_no_spend(self, data: Dict) -> List[str]:
        responses: List[str] = []
        balance = data.get("adjustedBalanceAmount", 0)
        over_credit = data.get("overTheCreditLimit", 0)
        pending_auth = data.get("accountOutstandingAuthAmt", 0)
        
        if balance < 0:
            responses.append(f"You have a credit balance of {balance}.")
        elif balance > 0:
            if over_credit > 0 and pending_auth > 0:
                responses.append(f"Your balance is {balance} which is over your credit limit and does not include some pending charges.")
            elif over_credit > 0:
                responses.append(f"Your balance is {balance} which is over your credit limit.")
            elif pending_auth > 0:
                responses.append(f"Your balance is {balance} not including some pending charges.")
            else:
                responses.append(f"Your balance is {balance}.")
        
        # Check Available Credit conditions for E no spend
        device_status = data.get("deviceStatusCode", 0)
        if is_device_closed(device_status):
            responses.append("You have no available credit because your card is not active.")
        else:
            available_credit = data.get("availableCreditAmount", 0)
            if available_credit > 0:
                cash_line = data.get("cashAdvanceLimitAmount", 0)
                cash_avail = data.get("cashAvailable", 0)
                if cash_line == 0:
                    responses.append(f"Your available credit is {available_credit}.")
                elif available_credit <= cash_avail:
                    responses.append(f"Your available credit is {available_credit} all of which can be used for cash advances")
                else:
                    responses.append(f"Your available credit is {available_credit} of which {cash_avail} may be used for cash advances.")
        return responses

    # A/E with Spend Limit branch
    def _process_a_e_spend_limit(self, data: Dict) -> List[str]:
        responses: List[str] = []
        # Cycle-To-Date Spend responses
        cycle_spend = data.get("ctdPurchaseBalanceAmount", 0)
        pending_auth = data.get("cardOutstandingAuthorizedAmt", 0)
        device_status = data.get("deviceStatusCode", 0)
        
        if pending_auth > 0 and is_device_closed(device_status):
            responses.append(f"Your Cycle-To-Date spend balance is {cycle_spend}, not including some pending charges and your card is not active.")
        elif pending_auth > 0:
            responses.append(f"Your Cycle-To-Date spend balance is {cycle_spend}, not including some pending charges.")
        elif is_device_closed(device_status):
            responses.append(f"Your Cycle-To-Date spend balance is {cycle_spend} and your card is not active.")
        else:
            responses.append(f"Your Cycle-To-Date spend balance is {cycle_spend}.")
        
        # Available Spend conditions
        available_spend = data.get("cycleToDateSpendAvailable", 0)
        if is_device_closed(device_status):
            responses.append("You have no available credit because your card is not active.")
        else:
            cash_access = data.get("cashAccessIndicator", False)
            cash_avail = data.get("cashAvailable", 0)
            if not cash_access:
                responses.append(f"Your available spend is {available_spend}. Your available spending limit may be affected by the overall account balance.")
            else:
                if available_spend <= cash_avail:
                    responses.append(f"Your available spend is {available_spend}, all of which can be used for cash advances. Your available spending limit may be affected by the overall account balance.")
                else:
                    responses.append(f"Your available spend is {available_spend} of which {cash_avail} may be used for cash advances. Your available spending limit may be affected by the overall account balance.")
        return responses
