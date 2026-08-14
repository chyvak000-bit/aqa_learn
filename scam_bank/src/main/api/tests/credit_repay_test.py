import pytest

from main.api.models.create_user_request import CreateUserRequest
from main.api.models.credit_repay_request import CreditRepayRequest
from main.api.models.credit_request import CreditRequest
from main.api.models.deposit_request import DepositRequest
from main.api.models.login_user_request import LoginUserRequest
from main.api.requests.create_account_requester import CreateAccountRequester
from main.api.requests.create_user_requester import CreateUserRequester
from main.api.requests.credit_repay_requester import CreditRepayRequester
from main.api.requests.credit_requester import CreditRequester
from main.api.requests.deposit_requester import DepositRequester
from main.api.requests.login_user_requester import LoginUserRequester
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self):
        create_user_request = CreateUserRequest(username="User7", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        login_user_request = LoginUserRequest(username="User7", password="Pas!sw0rd")

        LoginUserRequester(
            request_spec=RequestSpecs.unauth_headers(),
            response_spec=ResponseSpecs.request_ok()
        ).post(login_user_request)

        create_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="User7", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        account_id_1 = create_account_response.id

        credit_request = CreditRequest(accountId=account_id_1, amount=12000, termMonths=12)

        credit_response = CreditRequester(
            request_spec=RequestSpecs.auth_headers(username="User7", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post(credit_request)

        user_credit_id = credit_response.creditId

        credit_repay_request = CreditRepayRequest(creditId=user_credit_id, accountId=account_id_1, amount=12000)

        credit_repay_response = CreditRepayRequester(
            request_spec=RequestSpecs.auth_headers(username="User7", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(credit_repay_request)

        assert credit_repay_response.creditId == user_credit_id
        assert credit_repay_response.amountDeposited == 12000
