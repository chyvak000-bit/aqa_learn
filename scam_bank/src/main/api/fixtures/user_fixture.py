import pytest

from main.api.generators.model_generator import RandomModelGenerator
from main.api.models.create_user_request import CreateUserRequest, CreateCreditUserRequest
from main.api.models.login_user_request import LoginUserRequest


@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_credit_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateCreditUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def login_user_request(create_user_request):
    return LoginUserRequest(
        username=create_user_request.username,
        password=create_user_request.password
    )

@pytest.fixture
def login_credit_user_request(create_credit_user_request):
    return LoginUserRequest(
        username=create_credit_user_request.username,
        password=create_credit_user_request.password
    )