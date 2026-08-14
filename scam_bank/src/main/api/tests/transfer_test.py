import pytest

from main.api.models.create_user_request import CreateUserRequest
from main.api.models.deposit_request import DepositRequest
from main.api.models.login_user_request import LoginUserRequest
from main.api.models.transfer_request import TransferRequest
from main.api.requests.create_account_requester import CreateAccountRequester
from main.api.requests.create_user_requester import CreateUserRequester
from main.api.requests.deposit_requester import DepositRequester
from main.api.requests.login_user_requester import LoginUserRequester
from main.api.requests.transfer_requester import TransferRequester
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestDeposit:
    def test_deposit(self):
        create_user_request = CreateUserRequest(username="User5", password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        login_user_request = LoginUserRequest(username="User5", password="Pas!sw0rd")

        LoginUserRequester(
            request_spec=RequestSpecs.unauth_headers(),
            response_spec=ResponseSpecs.request_ok()
        ).post(login_user_request)

        create_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="User5", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        account_id_1 = create_account_response.id

        create_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="User5", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        account_id_2 = create_account_response.id

        deposit_request = DepositRequest(accountId=account_id_1, amount=5000)

        DepositRequester(
            request_spec=RequestSpecs.auth_headers(username="User5", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_request)

        transfer_request = TransferRequest(fromAccountId=account_id_1, toAccountId=account_id_2, amount=2000)

        transfer_response = TransferRequester(
            request_spec=RequestSpecs.auth_headers(username="User5", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(transfer_request)

        assert transfer_response.fromAccountIdBalance == 3000
