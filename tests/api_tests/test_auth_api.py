import allure
import pytest

from api.auth_client import AuthClient
from models.product import LoginResponse


@allure.feature("Auth API")
class TestLoginApi:

    @allure.title("Успешный логин возвращает токен")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_login_success(self, test_user):
        with allure.step("Отправить POST /users/login"):
            response = AuthClient().login(test_user["email"], test_user["password"])
        with allure.step("Проверить код ответа"):
            assert response.status_code == 200
        with allure.step("Проверить формат токена"):
            token = LoginResponse.model_validate(response.json()).access_token
            assert token.count(".") == 2, "Ожидался JWT из трёх частей"

    @allure.title("Логин несуществующего пользователя: 401")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.api
    def test_login_unknown_user(self):
        response = AuthClient().login("nouser3@example.com", "wrong_password")
        assert response.status_code == 401
        assert response.json() == {"error": "Unauthorized"}