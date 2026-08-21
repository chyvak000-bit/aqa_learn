from main.api.foundation.endpoint import Endpoint
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
