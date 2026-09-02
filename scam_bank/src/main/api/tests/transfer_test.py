import pytest
from sqlalchemy.orm import Session

from main.api.classes.api_manager import ApiManager
from main.api.db.crud.transaction_crud import TransactionCrudDb
from main.api.models.deposit_request import DepositRequest
from main.api.models.login_user_request import LoginUserRequest
from main.api.models.transfer_request import TransferRequest


@pytest.mark.api
class TestTransfer:
    def test_transfer(self, api_manager: ApiManager, login_user_request: LoginUserRequest, db_session: Session):
        create_account_response_1 = api_manager.user_steps.create_account(login_user_request)

        deposit_amount = 5000
        deposit_request = DepositRequest(accountId=create_account_response_1.id, amount=deposit_amount)

        api_manager.user_steps.deposit_money(login_user_request, deposit_request)
        create_account_response_2 = api_manager.user_steps.create_account(login_user_request)

        transfer_amount = 2000
        transfer_request = TransferRequest(
            fromAccountId=create_account_response_1.id, toAccountId=create_account_response_2.id, amount=transfer_amount
        )

        transfer_response = api_manager.user_steps.transfer_money(login_user_request, transfer_request)

        expected_balance = deposit_amount - transfer_amount

        # Проверяем ответ API
        assert transfer_response.fromAccountIdBalance == expected_balance, "Неверный баланс в ответе API"

        transaction_from_db = TransactionCrudDb.get_transfer(
            db_session, create_account_response_1.id, create_account_response_2.id
        )

        # Проверяем сохранение трансфера в БД
        assert transaction_from_db is not None, "Перевод отсутствует в БД"
        assert transaction_from_db.from_account_id == create_account_response_1.id, "Неверный ID счёта отправителя в БД"
        assert transaction_from_db.to_account_id == create_account_response_2.id, "Неверный ID счёта получателя в БД"
        assert transaction_from_db.amount == transfer_amount, "Неверная сумма перевода в БД"
        assert transaction_from_db.transaction_type == "transfer", "Неверный тип транзакции в БД"
