from typing import List, Any, cast

from main.api.foundation.endpoint import Endpoint
from main.api.foundation.requesters.crud_requester import CrudRequester
from main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from main.api.models.login_user_request import LoginUserRequest
from main.api.models.login_user_response import LoginUserResponse
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.response_specs import ResponseSpecs


class BaseSteps:
    def __init__(self, created_obj: List[Any]):
        self.created_obj = created_obj

    def login_user(self, login_user_request: LoginUserRequest) -> LoginUserResponse:
        return cast(
            LoginUserResponse,
            ValidateCrudRequester(
                RequestSpecs.unauth_headers(),
                Endpoint.LOGIN_USER,
                ResponseSpecs.request_ok()
            ).post(login_user_request)
        )

    def get_auth_headers(self, login_user_request: LoginUserRequest):
        login_user_response = self.login_user(login_user_request)

        headers = RequestSpecs.base_headers()
        headers["Authorization"] = f"Bearer {login_user_response.token}"

        return headers

    # Для негативных тестов
    def login_invalid_user(self, login_user_request: LoginUserRequest):
        CrudRequester(
            RequestSpecs.unauth_headers(),
            Endpoint.LOGIN_USER,
            ResponseSpecs.request_bad()
        ).post(login_user_request)

    def login_invalid_credentials(self, login_user_request: LoginUserRequest):
        CrudRequester(
            RequestSpecs.unauth_headers(),
            Endpoint.LOGIN_USER,
            ResponseSpecs.request_unauthorized()
        ).post(login_user_request)
