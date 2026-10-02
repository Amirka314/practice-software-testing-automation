from api.auth_client import AuthClient
from config.settings import TEST_USER_EMAIL, TEST_USER_PASSWORD

try:
    token = AuthClient().get_token(TEST_USER_EMAIL, TEST_USER_PASSWORD)
    print("TOKEN OK, длина:", len(token))
except Exception as e:
    print("ОШИБКА:", e)