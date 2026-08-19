from main.api.foundation.endpoint import Endpoint
from main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from main.api.models.create_user_request import CreateUserRequest
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.response_specs import ResponseSpecs
from main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        create_account_response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return create_account_response
