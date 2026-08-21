import pytest

from main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager):
        login_admin_request = LoginUserRequest(
            username="admin",
            password="123456"
        )

        login_admin_response = api_manager.admin_steps.login_user(
            login_admin_request
        )

        assert login_admin_request.username == login_admin_response.user.username
        assert login_admin_response.user.role == "ROLE_ADMIN"

    def test_login_user(self, api_manager, login_user_request):
        login_user_response = api_manager.admin_steps.login_user(
            login_user_request
        )

        assert login_user_request.username == login_user_response.user.username
        assert login_user_response.user.role == "ROLE_USER"
