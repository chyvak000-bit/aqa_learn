import pytest
from sqlalchemy.orm import Session

from main.api.classes.api_manager import ApiManager
from main.api.generators.model_generator import RandomModelGenerator
from main.api.models.create_user_request import CreateUserRequest
from main.api.db.crud.user_crud import UserCrudDb


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_create_user_valid(
            self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session
    ):
        create_user_response = api_manager.admin_steps.create_user(
            create_user_request
        )

        assert create_user_request.username == create_user_response.username
        assert create_user_request.role == create_user_response.role

        user_from_db = UserCrudDb.get_user_by_username(
            db_session, create_user_request.username
        )

        assert user_from_db is not None, "Созданного пользователя нет в базе данных"
        assert user_from_db.username == create_user_request.username

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
    def test_create_user_invalid(self, db_session: Session, username: str, password: str, api_manager: ApiManager):
        create_user_request = CreateUserRequest(
            username=username, password=password, role="ROLE_USER"
        )
        api_manager.admin_steps.create_invalid_user(
            create_user_request
        )

        user_from_db = UserCrudDb.get_user_by_username(
            db_session, create_user_request.username
        )

        assert user_from_db is None, "Пользователь создан, ошибка"
