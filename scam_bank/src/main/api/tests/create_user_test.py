import pytest
from sqlalchemy.orm import Session

from main.api.classes.api_manager import ApiManager
from main.api.generators.model_generator import RandomModelGenerator
from main.api.models.create_user_request import CreateUserRequest
from main.api.db.crud.user_crud import UserCrudDb


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize("create_user_request", [RandomModelGenerator.generate(CreateUserRequest)])
    def test_create_user_valid(
            self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session
    ):
        create_user_response = api_manager.admin_steps.create_user(create_user_request)

        # Проверяем ответ API
        assert create_user_request.username == create_user_response.username, "Неверное имя пользователя в ответе API"
        assert create_user_request.role == create_user_response.role, "Неверная роль пользователя в ответе API"

        user_from_db = UserCrudDb.get_user_by_username(db_session, create_user_request.username)

        # Проверяем сохранение пользователя в БД
        assert user_from_db is not None, "Созданного пользователя нет в БД"
        assert user_from_db.username == create_user_request.username, "Неверное имя пользователя в БД"
        assert user_from_db.role == create_user_request.role, "Неверная роль пользователя в БД"

    # Негативный тест
    @pytest.mark.parametrize(
        "username,password",
        [
            ("Максим", "Pass!sw0rd"),
            ("Ма", "Pas!sw0rd"),
            ("Maksimiliannnnnn", "Pas!sw0rd"),
            ("Maksim!", "Pas!sw0rd"),
            ("Maksim1", "Pas!sw0rд"),
            ("Maksim2", "Pas!sw0"),
            ("Maksim3", "pas!sw0rd"),
            ("Maksim4", "PAS!SW0RD"),
            ("Maksim5", "PASSW0RD"),
            ("Maksim6", "PAS!SWRRD"),
        ],
        ids=[
            "В имени пользователя использована кириллица",
            "Имя пользователя содержит менее 3-х символов",
            "Имя пользователя содержит более 15-ти символов",
            "В имени пользователя использованы спецсимволы",
            "В пароле пользователя использована кириллица ",
            "Пароль пользователя содержит меньше 8-ми символов",
            "Пароль пользователя не содержит заглавных букв",
            "Пароль пользователя не содержит строчных букв",
            "Пароль пользователя не содержит спецсимвол",
            "Пароль пользователя не содержит цифры",
        ]
    )
    def test_create_user_invalid(self, username: str, password: str, api_manager: ApiManager, db_session: Session):
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_invalid_user(create_user_request)

        user_from_db = UserCrudDb.get_user_by_username(db_session, create_user_request.username)

        assert user_from_db is None, "Был создан невалидный пользователь в БД"
