import pytest
from sqlalchemy.orm import Session

from main.api.classes.api_manager import ApiManager
from main.api.db.crud.account_crud import AccountCrudDb
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

        transaction_from_db = TransactionCrudDb.get_deposit(db_session, deposit_response.id)

        # Проверяем сохранение депозита в БД
        assert transaction_from_db is not None, "Депозит отсутствует в БД"
        assert transaction_from_db.to_account_id == create_account_response.id, "Неверный ID аккаунта в БД"
        assert transaction_from_db.amount == deposit_amount, "Неверная сумма депозита в БД"
        assert transaction_from_db.transaction_type == "deposit", "Неверный тип транзакции в БД"

    # Негативные тесты
    def test_deposit_money_invalid_amount(
            self, api_manager: ApiManager, login_user_request: LoginUserRequest, db_session: Session
    ):
        create_account_response = api_manager.user_steps.create_account(login_user_request)

        deposits_from_db_before = TransactionCrudDb.get_deposits_by_account_id(db_session, create_account_response.id)

        deposit_amount = 10000

        deposit_request = DepositRequest(accountId=create_account_response.id, amount=deposit_amount)

        api_manager.user_steps.deposit_money_invalid(login_user_request, deposit_request)

        deposits_from_db_after = TransactionCrudDb.get_deposits_by_account_id(db_session, create_account_response.id)

        assert len(deposits_from_db_before) == len(deposits_from_db_after), \
            "В БД была создана транзакция для невалидного пополнения"

    def test_deposit_money_negative_account_id(
            self, api_manager: ApiManager, login_user_request: LoginUserRequest, db_session: Session
    ):
        create_account_response = api_manager.user_steps.create_account(login_user_request)

        deposits_from_db_before = TransactionCrudDb.get_deposits_by_account_id(db_session, create_account_response.id)

        deposit_amount = 5000

        deposit_request = DepositRequest(accountId=-1, amount=deposit_amount)

        api_manager.user_steps.deposit_money_invalid(login_user_request, deposit_request)

        deposits_from_db_after = TransactionCrudDb.get_deposits_by_account_id(db_session, create_account_response.id)

        assert len(deposits_from_db_before) == len(deposits_from_db_after), \
            "В БД была создана транзакция для несуществующего аккаунта"

    def test_deposit_money_invalid_account_id(
            self, api_manager: ApiManager, login_user_request: LoginUserRequest, db_session: Session
    ):
        create_account_response = api_manager.user_steps.create_account(login_user_request)

        deposits_from_db_before = TransactionCrudDb.get_deposits_by_account_id(db_session, create_account_response.id)

        deposit_amount = 5000

        deposit_request = DepositRequest(accountId=999999999, amount=deposit_amount)

        api_manager.user_steps.deposit_money_invalid_account_id(login_user_request, deposit_request)

        deposits_from_db_after = TransactionCrudDb.get_deposits_by_account_id(db_session, create_account_response.id)

        assert len(deposits_from_db_before) == len(deposits_from_db_after), \
            "В БД была создана транзакция для несуществующего аккаунта"
