import pytest

from main.api.classes.api_manager import ApiManager
from main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager: ApiManager):
        login_admin_request = LoginUserRequest(username="admin", password="123456")

        login_admin_response = api_manager.admin_steps.login_user(login_admin_request)

        # Проверяем ответ API
        assert login_admin_request.username == login_admin_response.user.username
        assert login_admin_response.user.role == "ROLE_ADMIN"

    def test_login_user(self, api_manager: ApiManager, login_user_request: LoginUserRequest):
        login_user_response = api_manager.admin_steps.login_user(login_user_request)

        # Проверяем ответ API
        assert login_user_request.username == login_user_response.user.username
        assert login_user_response.user.role == "ROLE_USER"

    # Негативные тесты
    @pytest.mark.parametrize(
        "username,password",
        [
            ("admin", ""),
            ("", "123456"),
        ],
        ids=[
            "Отсутствует  пароль",
            "Отсутствует имя пользователя",
        ]
    )
    def test_login_user_invalid(self, username: str, password: str, api_manager: ApiManager):
        login_user_request = LoginUserRequest(username=username, password=password)

        api_manager.admin_steps.login_invalid_user(login_user_request)

    @pytest.mark.parametrize(
        "username,password",
        [
            ("admin", "111111"),
            ("non_admin", "123456"),
        ],
        ids=[
            "Неверный пароль",
            "Неверный логин",
        ]
    )
    def test_login_user_invalid_credentials(self, username: str, password: str, api_manager: ApiManager):
        login_user_request = LoginUserRequest(username=username, password=password)

        api_manager.admin_steps.login_invalid_credentials(login_user_request)
