import requests

from main.api.configs.config import Config
from main.api.models.login_user_request import LoginUserRequest
from main.api.models.login_user_response import LoginUserResponse


class RequestSpecs:
    @staticmethod
    def base_headers():
        return {
            "Content-Type": "application/json",
            "accept": "application/json"
        }

    @staticmethod
    def auth_headers(username: str, password: str):
        auth_request = LoginUserRequest(username=username, password=password)
        auth_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=auth_request.model_dump(),
            headers=RequestSpecs.base_headers()
        )

        if auth_response.status_code == 200:
            auth_response_data = LoginUserResponse(**auth_response.json())
            auth_token = auth_response_data.token
            headers = RequestSpecs.base_headers()
            headers["Authorization"] = f"Bearer {auth_token}"
            return {
                "headers": headers,
                "base_url": Config.fetch("backendUrl"),
            }
        raise Exception("Authentication failed")

    @staticmethod
    def unauth_headers():
        return {
            "headers": RequestSpecs.base_headers(),
            "base_url": Config.fetch("backendUrl"),
        }
