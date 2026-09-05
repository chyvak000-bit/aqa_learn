from main.api.foundation.endpoint import Endpoint
from main.api.foundation.requesters.crud_requester import CrudRequester
from main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from main.api.models.create_user_request import CreateUserRequest
from main.api.models.create_user_response import CreateUserResponse
from main.api.models.login_user_request import LoginUserRequest
from main.api.specs.response_specs import ResponseSpecs
from main.api.steps.base_steps import BaseSteps


class AdminSteps(BaseSteps):
    def get_admin_auth_headers(self):
        login_user_request = LoginUserRequest(
            username="admin",
            password="123456"
        )

        return self.get_auth_headers(login_user_request)

    def create_user(self, create_user_request: CreateUserRequest):
        create_user_response = ValidateCrudRequester(
            self.get_admin_auth_headers(),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_ok()
        ).post(create_user_request)

        self.created_obj.append(create_user_response)
        return create_user_response

    def delete_user(self, user_id: int):
        CrudRequester(
            self.get_admin_auth_headers(),
            Endpoint.ADMIN_DELETE_USER,
            ResponseSpecs.request_ok()
        ).delete(user_id)

    # Для негативных тестов
    def create_invalid_user(self, create_user_request: CreateUserRequest):
        CrudRequester(
            self.get_admin_auth_headers(),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_bad()
        ).post(create_user_request)
