import pytest
from sqlalchemy.orm import Session

from main.api.classes.api_manager import ApiManager
from main.api.db.crud.account_crud import AccountCrudDb
from main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self, api_manager: ApiManager, login_user_request: LoginUserRequest, db_session: Session):
        create_account_response = api_manager.user_steps.create_account(login_user_request)

        # Проверяем ответ API
        assert create_account_response.balance == 0, "Неверный баланс нового аккаунта в ответе API"

        account_from_db = AccountCrudDb.get_account_by_id(db_session, create_account_response.id)

        # Проверяем сохранение аккаунта в БД
        assert account_from_db is not None, "Созданного аккаунта нет в БД"
        assert account_from_db.id == create_account_response.id, "Неверный ID аккаунта в БД"
        assert account_from_db.balance == 0, "Неверный баланс аккаунта в БД"
