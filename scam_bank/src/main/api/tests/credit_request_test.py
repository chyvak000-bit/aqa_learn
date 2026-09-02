import pytest
from sqlalchemy.orm import Session

from main.api.classes.api_manager import ApiManager
from main.api.db.crud.credit_crud import CreditCrudDb
from main.api.models.credit_request import CreditRequest
from main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestCreditRequest:
    def test_credit_request(
            self, api_manager: ApiManager, login_credit_user_request: LoginUserRequest, db_session: Session
    ):
        create_account_response = api_manager.credit_steps.create_account(login_credit_user_request)

        credit_amount = 12000
        credit_term = 12

        credit_request = CreditRequest(
            accountId=create_account_response.id, amount=credit_amount, termMonths=credit_term
        )

        credit_response = api_manager.credit_steps.request_credit(login_credit_user_request, credit_request)

        # Проверяем ответ API
        assert credit_response.amount == credit_amount, "Неверная сумма кредита в ответе API"
        assert credit_response.termMonths == credit_term, "Неверный срок кредита в ответе API"
        assert credit_response.balance == credit_amount, "Неверный баланс кредита в ответе API"

        credit_from_db = CreditCrudDb.get_credit_by_account_id(db_session, create_account_response.id)

        # Проверяем сохранение кредита в БД
        assert credit_from_db is not None, "Кредит отсутствует в БД"
        assert credit_from_db.amount == credit_amount, "Неверная сумма кредита в БД"
        assert credit_from_db.term_months == credit_term, "Неверный срок кредита в БД"
        assert credit_from_db.account_id == create_account_response.id, "Неверный ID счёта в БД"
        assert credit_from_db.balance == credit_amount, "Неверный баланс кредита в БД"
