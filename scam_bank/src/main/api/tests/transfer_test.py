import requests


class TestTransfer:
    def test_transfer(self):
        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456"
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )

        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get("token")

        create_user_response_1 = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "user5",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_user_response_1.status_code == 200

        create_user_response_2 = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "user6",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_user_response_2.status_code == 200

        login_user_response_2 = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "user6",
                "password": "Pas!sw0rd"
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )

        assert login_user_response_2.status_code == 200
        token = login_user_response_2.json().get("token")

        create_account_response_2 = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_account_response_2.status_code == 201
        assert create_account_response_2.json().get("balance") == 0
        account_id_2 = create_account_response_2.json().get("id")

        login_user_response_1 = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "user5",
                "password": "Pas!sw0rd"
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )

        assert login_user_response_1.status_code == 200
        token = login_user_response_1.json().get("token")

        create_account_response_1 = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_account_response_1.status_code == 201
        assert create_account_response_1.json().get("balance") == 0
        account_id_1 = create_account_response_1.json().get("id")

        token = login_user_response_1.json().get("token")

        deposit_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": account_id_1,
                "amount": 2500
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
        )

        assert deposit_response.status_code == 200
        assert deposit_response.json().get("balance") == 2500
        initial_balance = deposit_response.json().get("balance")  # 2500

        token = login_user_response_1.json().get("token")

        transfer_response = requests.post(
            url="http://localhost:4111/api/account/transfer",
            json={
                "fromAccountId": account_id_1,
                "toAccountId": account_id_2,
                "amount": 500
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
        )

        assert transfer_response.status_code == 200
        assert transfer_response.json().get("fromAccountIdBalance") == initial_balance - 500
