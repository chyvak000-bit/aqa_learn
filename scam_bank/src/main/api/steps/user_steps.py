from main.api.foundation.endpoint import Endpoint
from main.api.foundation.requesters.crud_requester import CrudRequester
from main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from main.api.models.deposit_request import DepositRequest
from main.api.models.login_user_request import LoginUserRequest
from main.api.models.transfer_request import TransferRequest
from main.api.specs.response_specs import ResponseSpecs
from main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, login_user_request: LoginUserRequest):
        create_account_response = ValidateCrudRequester(
            self.get_auth_headers(login_user_request),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return create_account_response

    def deposit_money(self, login_user_request: LoginUserRequest, deposit_request: DepositRequest):
        deposit_money_response = ValidateCrudRequester(
            self.get_auth_headers(login_user_request),
            Endpoint.DEPOSIT_MONEY,
            ResponseSpecs.request_ok()
        ).post(deposit_request)
        return deposit_money_response

    def transfer_money(self, login_user_request: LoginUserRequest, transfer_request: TransferRequest):
        transfer_money_response = ValidateCrudRequester(
            self.get_auth_headers(login_user_request),
            Endpoint.TRANSFER_MONEY,
            ResponseSpecs.request_ok()
        ).post(transfer_request)
        return transfer_money_response

    # Для негативных тестов
    def create_account_no_rights(self, login_user_request: LoginUserRequest):
        CrudRequester(
            self.get_auth_headers(login_user_request),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_forbidden()
        ).post(None)

    def create_account_limit(self, login_user_request: LoginUserRequest):
        CrudRequester(
            self.get_auth_headers(login_user_request),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_conflict()
        ).post(None)

    def deposit_money_invalid(self, login_user_request: LoginUserRequest, deposit_request: DepositRequest):
        CrudRequester(
            self.get_auth_headers(login_user_request),
            Endpoint.DEPOSIT_MONEY,
            ResponseSpecs.request_bad()
        ).post(deposit_request)

    def deposit_money_invalid_account_id(self, login_user_request: LoginUserRequest, deposit_request: DepositRequest):
        CrudRequester(
            self.get_auth_headers(login_user_request),
            Endpoint.DEPOSIT_MONEY,
            ResponseSpecs.request_not_found()
        ).post(deposit_request)

    def transfer_money_invalid(self, login_user_request: LoginUserRequest, transfer_request: TransferRequest):
        CrudRequester(
            self.get_auth_headers(login_user_request),
            Endpoint.TRANSFER_MONEY,
            ResponseSpecs.request_unprocessable()
        ).post(transfer_request)
