import pytest
from sqlalchemy.orm import Session

from main.api.classes.api_manager import ApiManager
from main.api.db.crud.transaction_crud import TransactionCrudDb
from main.api.models.credit_repay_request import CreditRepayRequest
from main.api.models.credit_request import CreditRequest
from main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay(
            self, api_manager: ApiManager, login_credit_user_request: LoginUserRequest, db_session: Session
    ):
        create_account_response = api_manager.credit_steps.create_account(login_credit_user_request)

        credit_amount = 12000
        credit_term = 12

        credit_request = CreditRequest(
            accountId=create_account_response.id, amount=credit_amount, termMonths=credit_term
        )

        credit_response = api_manager.credit_steps.request_credit(login_credit_user_request, credit_request)

        credit_repay_request = CreditRepayRequest(
            creditId=credit_response.creditId, accountId=create_account_response.id, amount=credit_amount
        )

        credit_repay_response = api_manager.credit_steps.repay_credit(login_credit_user_request, credit_repay_request)

        # Проверяем ответ API
        assert credit_repay_response.creditId == credit_response.creditId, "Неверный ID кредита в ответе API"
        assert credit_repay_response.amountDeposited == credit_amount, "Неверная сумма выплаты кредита в ответе API"

        transaction_from_db = TransactionCrudDb.get_credit_repayment(db_session, credit_response.creditId)

        # Проверяем сохранение выплаты кредита в БД
        assert transaction_from_db is not None, "Выплата кредита отсутствует в БД"
        assert transaction_from_db.credit_id == credit_response.creditId, "Неверный ID кредита в БД"
        assert transaction_from_db.from_account_id == create_account_response.id, "Неверный ID счёта в БД"
        assert transaction_from_db.amount == credit_amount, "Неверная сумма выплаты кредита в БД"
        assert transaction_from_db.transaction_type == "credit_repayment", "Неверный тип транзакции в БД"

    # Негативные тесты
    def test_credit_repay_not_found(
            self, api_manager: ApiManager, login_credit_user_request: LoginUserRequest, db_session: Session
    ):
        create_account_response = api_manager.credit_steps.create_account(login_credit_user_request)

        credit_amount = 12000
        credit_term = 12
        invalid_credit_id = 999999999

        credit_request = CreditRequest(
            accountId=create_account_response.id, amount=credit_amount, termMonths=credit_term
        )

        api_manager.credit_steps.request_credit(login_credit_user_request, credit_request)

        credit_repay_request = CreditRepayRequest(
            creditId=invalid_credit_id, accountId=create_account_response.id, amount=credit_amount
        )

        api_manager.credit_steps.repay_credit_not_found(login_credit_user_request, credit_repay_request)

        transaction_from_db = TransactionCrudDb.get_credit_repayment(db_session, invalid_credit_id)

        # Проверяем, что выплата не была сохранена в БД
        assert transaction_from_db is None, "Выплата несуществующего кредита появилась в БД"
