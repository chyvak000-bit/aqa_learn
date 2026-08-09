import requests


class TestTransfer:
    # Вспомогательные методы (можно вынести в отдельный класс-помощник, но для начала оставим здесь)

    def login(self, username: str, password: str) -> str:
        """Логин под пользователем и возврат токена."""
        response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={"username": username, "password": password},
            headers={"Content-Type": "application/json", "accept": "application/json"}
        )
        assert response.status_code == 200, f"Login failed for {username}"
        return response.json().get("token")

    def create_user(self, admin_token: str, username: str, password: str, role: str = "ROLE_USER"):
        """Создание пользователя админом."""
        response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={"username": username, "password": password, "role": role},
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200, f"User creation failed for {username}"
        return response

    def create_account(self, user_token: str) -> int:
        """Создание счёта для пользователя и возврат его ID."""
        response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={"accept": "application/json", "Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == 201, "Account creation failed"
        assert response.json().get("balance") == 0, "Initial balance should be 0"
        return response.json().get("id")

    def deposit(self, account_id: int, amount: float, user_token: str) -> float:
        """Пополнение счёта, возвращает новый баланс."""
        response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={"accountId": account_id, "amount": amount},
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {user_token}",
                "Content-Type": "application/json",
            }
        )
        assert response.status_code == 200, "Deposit failed"
        return response.json().get("balance")

    def transfer(self, from_id: int, to_id: int, amount: float, user_token: str) -> dict:
        """Выполняет перевод, возвращает JSON ответ."""
        response = requests.post(
            url="http://localhost:4111/api/account/transfer",
            json={"fromAccountId": from_id, "toAccountId": to_id, "amount": amount},
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {user_token}",
                "Content-Type": "application/json",
            }
        )
        assert response.status_code == 200, "Transfer failed"
        return response.json()

    # Сам тест
    def test_transfer(self):
        # 1. Логин под админом
        admin_token = self.login("admin", "123456")

        # 2. Создаём двух пользователей
        self.create_user(admin_token, "user5", "Pas!sw0rd")
        self.create_user(admin_token, "user6", "Pas!sw0rd")

        # 3. Логинимся под каждым пользователем и создаём по счёту
        token_user5 = self.login("user5", "Pas!sw0rd")
        token_user6 = self.login("user6", "Pas!sw0rd")

        account_id_1 = self.create_account(token_user5)
        account_id_2 = self.create_account(token_user6)

        # 4. Пополняем счёт первого пользователя
        initial_balance = self.deposit(account_id_1, 2500, token_user5)

        # 5. Выполняем перевод с первого счёта на второй
        transfer_data = self.transfer(account_id_1, account_id_2, 500, token_user5)

        # 6. Проверяем баланс отправителя
        assert transfer_data.get("fromAccountIdBalance") == initial_balance - 500
