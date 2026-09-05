import allure

from typing import Optional, Callable, Any

from main.api.configs.config import Config
from main.api.foundation.endpoint import Endpoint
from main.api.foundation.http_requester import HttpRequester
from main.api.foundation.requesters.crud_requester import CrudRequester
from main.api.models.base_model import BaseModel


class ValidateCrudRequester(HttpRequester):
    def __init__(self, request_spec: dict, endpoint: Endpoint, response_spec: Callable[..., Any]):
        super().__init__(request_spec, endpoint, response_spec)
        self.crud_requester = CrudRequester(
            request_spec=request_spec,
            endpoint=endpoint,
            response_spec=response_spec,
        )

    def post(self, model: Optional[BaseModel] = None) -> BaseModel:
        response = self.crud_requester.post(model)

        with allure.step(f"POST {Config.fetch("backendUrl")}{self.endpoint.value.url} and Validated Model"):
            allure.attach(f"Validated Model response: {self.endpoint.value.response_model.__name__}")

        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())

    def delete(self, user_id: int) -> BaseModel:
        response = self.crud_requester.delete(user_id)
        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())
