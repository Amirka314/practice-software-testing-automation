import allure
import pytest

from api.auth_client import AuthClient
from models.product import LoginResponse


@allure.feature("Auth API")
class TestLoginApi:

    @allure.title("Успешный логин возвращает токен")
    @pytest.mark.smoke
    @pytest.mark.api
    def test_login_success(self, test_user):
        response = AuthClient().login(test_user["email"], test_user["password"])
        assert response.status_code == 200
        token = LoginResponse.model_validate(response.json()).access_token
        assert token.count(".") == 2, "Ожидался JWT из трёх частей"

    @allure.title("Логин несуществующего пользователя: 401")
    @pytest.mark.regression
    @pytest.mark.api
    def test_login_unknown_user(self):
        response = AuthClient().login("nouser3@example.com", "wrong_password")
        assert response.status_code == 401
        assert response.json() == {"error": "Unauthorized"}