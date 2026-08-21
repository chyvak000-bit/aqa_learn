from main.api.foundation.endpoint import Endpoint
from main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from main.api.models.credit_repay_request import CreditRepayRequest
from main.api.models.credit_request import CreditRequest
from main.api.models.login_user_request import LoginUserRequest
from main.api.specs.response_specs import ResponseSpecs
from main.api.steps.user_steps import UserSteps


class CreditSteps(UserSteps):
    def request_credit(self, login_user_request: LoginUserRequest, credit_request: CreditRequest):
        credit_response = ValidateCrudRequester(
            self.get_auth_headers(login_user_request),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_created()
        ).post(credit_request)
        return credit_response

    def repay_credit(self, login_user_request: LoginUserRequest, credit_repay_request: CreditRepayRequest):
        credit_repay_response = ValidateCrudRequester(
            self.get_auth_headers(login_user_request),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok()
        ).post(credit_repay_request)
        return credit_repay_response
