import pytest

from main.api.models.credit_repay_request import CreditRepayRequest
from main.api.models.credit_request import CreditRequest
from main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay(self, api_manager, login_credit_user_request: LoginUserRequest):
        create_account_response = api_manager.credit_steps.create_account(
            login_credit_user_request
        )

        credit_amount = 12000
        credit_term = 12

        credit_request = CreditRequest(
            accountId=create_account_response.id,
            amount=credit_amount,
            termMonths=credit_term
        )

        credit_response = api_manager.credit_steps.request_credit(
            login_credit_user_request,
            credit_request
        )

        credit_repay_request = CreditRepayRequest(
            creditId=credit_response.creditId,
            accountId=create_account_response.id,
            amount=credit_amount
        )

        credit_repay_response = api_manager.credit_steps.repay_credit(
            login_credit_user_request,
            credit_repay_request
        )

        assert credit_repay_response.creditId == credit_response.creditId
        assert credit_repay_response.amountDeposited == credit_amount
