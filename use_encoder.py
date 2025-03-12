from typing import Dict, List
from scenarios.base import Scenario
from utils.helpers import extract_mmdd, extract_day, is_account_closed, is_device_closed

class StatementBalanceScenario(Scenario):
    def get_response(self, data: Dict) -> str:
        responses: List[str] = []
        cardholder_type = data.get("cardHolderType", "").upper()
        spend_limit_flag = data.get("equalPurchaseAccessIndicator", True)
        
        # Process for P/O/U cardholders
        if cardholder_type in {"P", "O", "U"}:
            account_status = data.get("accountStatusCode", 0)
            if is_account_closed(account_status):
                # Account Status is closed (N)
                responses.append("Your account is closed.")
                return "\n".join(responses)
            statement_date = data.get("statementDate", "")
            statement_balance = data.get("lastStatementTotalBalance", None)
            if not statement_date:
                # Last Statement Date (J) BLANK
                responses.append("I'm sorry but I don't see a statement balance available for your account right now. Keep in mind that a statement may not print if your balance is zero and the only activity was a payment.")
            else:
                mmdd = extract_mmdd(statement_date)
                if statement_balance is not None:
                    if statement_balance < 0:
                        # Last Statement Date not BLANK and billed balance (K) < 0
                        responses.append(f"Your last statement was printed on {mmdd} and at that time, your statement balance was a credit balance of {statement_balance}.")
                    else:
                        # Last Statement Date not BLANK and billed balance (K) >= 0
                        responses.append(f"Your last statement was printed on {mmdd} and at that time, your statement balance was {statement_balance}.")
                else:
                    responses.append("Statement balance information is unavailable.")
            min_due = data.get("totalDueAmount", 0)
            payment_due_date = data.get("paymentDueDate", "")
            day_portion = extract_day(payment_due_date)
            if min_due == 0:
                # Min Due (D) = 0
                responses.append(f"No payment is due at this time. As a reminder, your payment due date is the {day_portion} of every month.")
            elif min_due > 0:
                flex_loan = data.get("lastStmtMinDueLoanAmount", 0)
                if flex_loan > 0:
                    # Min Due (D) > 0 and Flex Loan (T > $0)
                    responses.append(f"Your minimum payment of {min_due} is due on {day_portion}. Your Citi Flex Plan Payment Amount is included in your Minimum Payment.")
                else:
                    # Min Due (D) > 0 and no Flex Loan (T = $0)
                    responses.append(f"Your minimum payment of {min_due} is due on {day_portion}.")
            return "\n".join(responses)
        
        # Process for A no spend limit (M = True)
        elif cardholder_type == "A" and spend_limit_flag is True:
            statement_date = data.get("statementDate", "")
            statement_balance = data.get("lastStatementTotalBalance", None)
            if not statement_date:
                # Last Statement Date (J) BLANK
                responses.append("I'm sorry but I don't see a statement balance available for your account right now. Keep in mind that a statement may not print if your balance is zero and the only activity was a payment.")
            else:
                mmdd = extract_mmdd(statement_date)
                if statement_balance is not None:
                    if statement_balance < 0:
                        # Last Statement Date not BLANK and billed balance (K) < 0
                        responses.append(f"Your last statement was printed on {mmdd} and at that time, your statement balance was a credit balance of {statement_balance}.")
                    else:
                        # Last Statement Date not BLANK and billed balance (K) >= 0
                        responses.append(f"Your last statement was printed on {mmdd} and at that time, your statement balance was {statement_balance}.")
                else:
                    responses.append("Statement balance information is unavailable.")
            min_due = data.get("totalDueAmount", 0)
            payment_due_date = data.get("paymentDueDate", "")
            day_portion = extract_day(payment_due_date)
            if min_due == 0:
                # Min Due (D) = 0
                responses.append(f"No payment is due at this time. As a reminder, your payment due date is the {day_portion} of every month.")
            elif min_due > 0:
                flex_loan = data.get("lastStmtMinDueLoanAmount", 0)
                if flex_loan > 0:
                    # Min Due (D) > 0 and Flex Loan (T > $0)
                    responses.append(f"Your minimum payment of {min_due} is due on {day_portion}. Your Citi Flex Plan Payment Amount is included in your Minimum Payment Due.")
                else:
                    # Min Due (D) > 0 and no Flex Loan (T = $0)
                    responses.append(f"Your minimum payment of {min_due} is due on {day_portion}.")
            device_status = data.get("deviceStatusCode", 0)
            if is_device_closed(device_status):
                # Card Status is closed (0)
                responses.append("Your card is not active.")
            return "\n".join(responses)
        
        # Process for A with Spend Limit (M = False)
        elif cardholder_type == "A" and spend_limit_flag is False:
            # DO NOT HAVE ACCESS TO STATEMENT DATE or MIN DUE DATA
            return "I'm sorry, but only the primary cardholder can request statement information."
        
        # Process for E cardholder type
        elif cardholder_type == "E":
            # DO NOT HAVE ACCESS TO STATEMENT DATE or MIN DUE DATA
            return "I'm sorry, but only the owner on this account can request statement information."
        
        return "Unable to determine response for the given cardholder type."
