import pytest

from main.api.models.create_user_request import CreateUserRequest
from main.api.requests.create_user_requester import CreateUserRequester
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreateUser:
    def test_create_user_valid(self):
        create_user_request = CreateUserRequest(username="User1", password="Pas!sw0rd", role="ROLE_USER")

        create_user_response = CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        assert create_user_request.username == create_user_response.username
        assert create_user_request.role == create_user_response.role

    @pytest.mark.parametrize(
        "username,password",
        [
            ("абв", "Pass!sw0rd"),
            ("ab", "Pas!sw0rd"),
            ("abv!", "Pas!sw0rd"),
            ("Maxx1", "Pas!sw0rд"),
            ("Maxx2", "Pas!sw0"),
            ("Maxx3", "pas!sw0rd"),
            ("Maxx4", "PAS!SW0RD"),
            ("Maxx5", "PASSW0RD"),
            ("Maxx6", "PAS!SWRRD")
        ]
    )
    def test_create_user_invalid(self, username, password):
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_bad()
        ).post(create_user_request)
