import requests

from main.api.models.transfer_request import TransferRequest
from main.api.models.transfer_response import TransferResponse
from main.api.requests.requester import Requester


class TransferRequester(Requester):
    def post(self, transfer_request: TransferRequest) -> TransferResponse:
        url = f"{self.base_url}/account/transfer"
        response = requests.post(
            url=url,
            json=transfer_request.model_dump(),
            headers=self.headers,
        )
        return TransferResponse(**response.json())
