import requests

from main.api.models.credit_request import CreditRequest
from main.api.models.credit_response import CreditResponse
from main.api.requests.requester import Requester


class CreditRequester(Requester):
    def post(self, credit_requester: CreditRequest) -> CreditResponse:
        url = f"{self.base_url}/credit/request"
        response = requests.post(
            url=url,
            json=credit_requester.model_dump(),
            headers=self.headers,
        )
        self.response_spec(response)
        return CreditResponse(**response.json())
