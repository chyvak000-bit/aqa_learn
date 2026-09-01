import pytest

from sqlalchemy.orm import Session

from main.api.classes.api_manager import ApiManager
from main.api.db.crud.account_crud import AccountCrudDb
from main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(
            self, db_session: Session, api_manager: ApiManager, login_user_request: LoginUserRequest
    ):
        create_account_response = api_manager.user_steps.create_account(
            login_user_request
        )

        assert create_account_response.balance == 0

        account_from_db = AccountCrudDb.get_account_by_id(
            db_session, create_account_response.id
        )

        assert account_from_db is not None, "Созданного аккаунта нету в базе данных"
        assert account_from_db.id == create_account_response.id
        assert account_from_db.balance is not None, "Поле баланса отсутствует в базе данных"
