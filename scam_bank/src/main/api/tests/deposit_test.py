import pytest

from main.api.models.deposit_request import DepositRequest


@pytest.mark.api
class TestDeposit:
    def test_deposit(self, api_manager, login_user_request):
        create_account_response = api_manager.user_steps.create_account(
            login_user_request
        )

        deposit_amount = 5000

        deposit_request = DepositRequest(
            accountId=create_account_response.id,
            amount=deposit_amount
        )

        deposit_response = api_manager.user_steps.deposit_money(
            login_user_request,
            deposit_request
        )

        assert deposit_response.balance == deposit_amount
