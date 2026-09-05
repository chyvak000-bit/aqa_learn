import pytest
from sqlalchemy.orm import Session

from main.api.classes.api_manager import ApiManager
from main.api.db.crud.account_crud import AccountCrudDb
from main.api.db.crud.user_crud import UserCrudDb
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

    # Негативные тесты
    def test_create_account_no_rights(self, api_manager: ApiManager, db_session: Session):
        login_admin_request = LoginUserRequest(username="admin", password="123456")

        admin_from_db = UserCrudDb.get_user_by_username(db_session, login_admin_request.username)

        assert admin_from_db is not None, "Администратор отсутствует в БД"

        accounts_from_db_before = AccountCrudDb.get_accounts_by_user_id(db_session, admin_from_db.id)

        api_manager.user_steps.create_account_no_rights(login_admin_request)

        accounts_from_db_after = AccountCrudDb.get_accounts_by_user_id(db_session, admin_from_db.id)

        assert len(accounts_from_db_before) == len(accounts_from_db_after), \
            "Количество аккаунтов администратора изменилось"

    def test_create_account_limit(
            self, api_manager: ApiManager, login_user_request: LoginUserRequest, db_session: Session
    ):
        for _ in range(2):
            api_manager.user_steps.create_account(login_user_request)

        user_from_db = UserCrudDb.get_user_by_username(db_session, login_user_request.username)

        assert user_from_db is not None, "Пользователь отсутствует в БД"

        accounts_from_db_before = AccountCrudDb.get_accounts_by_user_id(db_session, user_from_db.id)

        api_manager.user_steps.create_account_limit(login_user_request)

        accounts_from_db_after = AccountCrudDb.get_accounts_by_user_id(db_session, user_from_db.id)

        assert len(accounts_from_db_before) == 2, "Неверное количество аккаунтов перед попыткой создания третьего"
        assert len(accounts_from_db_after) == 2, "Количество аккаунтов изменилось после попытки создания третьего"
