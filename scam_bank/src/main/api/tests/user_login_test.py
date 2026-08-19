import pytest

from main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager):
        login_admin_request = LoginUserRequest(username="admin", password="123456")
        login_admin_response = api_manager.admin_steps.login_user(login_admin_request)

        assert login_admin_request.username == login_admin_response.user.username
        assert login_admin_response.user.role == "ROLE_ADMIN"

    def test_login_user(self, api_manager, create_user_request):
        create_user_response = api_manager.admin_steps.login_user(create_user_request)

        assert create_user_request.username == create_user_response.user.username
        assert create_user_response.user.role == "ROLE_USER"
