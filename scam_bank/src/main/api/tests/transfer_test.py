import pytest

from main.api.models.deposit_request import DepositRequest
from main.api.models.transfer_request import TransferRequest


@pytest.mark.api
class TestTransfer:
    def test_transfer(self, api_manager, login_user_request):
        create_account_response_1 = api_manager.user_steps.create_account(
            login_user_request
        )


        deposit_request = DepositRequest(
            accountId=create_account_response_1.id,
            amount=5000
        )

        api_manager.user_steps.deposit_money(
            login_user_request,
            deposit_request
        )

        create_account_response_2 = api_manager.user_steps.create_account(
            login_user_request
        )

        transfer_request = TransferRequest(
            fromAccountId=create_account_response_1.id,
            toAccountId=create_account_response_2.id,
            amount=2000
        )

        transfer_response = api_manager.user_steps.transfer_money(
            login_user_request,
            transfer_request
        )

        assert transfer_response.fromAccountIdBalance == 3000
