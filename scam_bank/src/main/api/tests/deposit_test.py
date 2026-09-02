import pytest
from sqlalchemy.orm import Session

from main.api.classes.api_manager import ApiManager
from main.api.db.crud.transaction_crud import TransactionCrudDb
from main.api.models.deposit_request import DepositRequest
from main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestDeposit:
    def test_deposit(self, api_manager: ApiManager, login_user_request: LoginUserRequest, db_session: Session):
        create_account_response = api_manager.user_steps.create_account(login_user_request)

        deposit_amount = 5000

        deposit_request = DepositRequest(accountId=create_account_response.id, amount=deposit_amount)

        deposit_response = api_manager.user_steps.deposit_money(login_user_request, deposit_request)

        # Проверяем ответ API
        assert deposit_response.balance == deposit_amount, "Неверный баланс в ответе API"

        transaction_from_db = TransactionCrudDb.get_transaction_by_id(db_session, deposit_response.id)

        # Проверяем сохранение депозита в БД
        assert transaction_from_db is not None, "Депозит отсутствует в БД"
        assert transaction_from_db.to_account_id == create_account_response.id, "Неверный ID аккаунта в БД"
        assert transaction_from_db.amount == deposit_amount, "Неверная сумма депозита в БД"
        assert transaction_from_db.transaction_type == "deposit", "Неверный тип транзакции в БД"
