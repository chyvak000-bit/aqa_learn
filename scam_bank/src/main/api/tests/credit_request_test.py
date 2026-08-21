import pytest

from main.api.models.credit_request import CreditRequest
from main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestCreditRequest:
    def test_credit_request(self, api_manager, login_credit_user_request: LoginUserRequest):
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

        assert credit_response.amount == credit_amount
        assert credit_response.termMonths == credit_term
        assert credit_response.balance == credit_amount
