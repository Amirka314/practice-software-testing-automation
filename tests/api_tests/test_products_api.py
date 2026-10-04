import allure
import pytest

from api.products_client import ProductsClient
from models.product import Product, ProductsPage


@pytest.fixture(scope="module")
def client() -> ProductsClient:
    return ProductsClient()


@allure.feature("Products API")
class TestProductsList:

    @allure.title("GET /products возвращает 200 и валидную схему")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_list_schema(self, client):
        with allure.step("Запросить первую страницу каталога"):
            response = client.get_products()
        with allure.step("Проверить код ответа"):
            assert response.status_code == 200
        with allure.step("Проверить схему ответа через pydantic"):
            page = ProductsPage.model_validate(response.json())
            assert page.current_page == 1
            assert 0 < len(page.data) <= page.per_page

    @allure.title("Пагинация согласована: сумма по страницам равна total")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_pagination_is_consistent(self, client):
        items = client.get_all_products()
        first = client.get_products().json()
        assert len(items) == first["total"]
        assert len({p["id"] for p in items}) == len(items), "Есть дубли между страницами"

    @allure.title("Страница за пределами диапазона не возвращает товары")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.api
    def test_page_out_of_range(self, client):
        last = client.get_products().json()["last_page"]
        response = client.get_products(page=last + 1)
        assert response.status_code == 200
        assert response.json()["data"] == []

    @allure.title("Сортировка по всему каталогу: {sort}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    @pytest.mark.parametrize(
        "sort,field,reverse",
        [
            ("name,asc", "name", False),
            ("name,desc", "name", True),
            ("price,asc", "price", False),
            ("price,desc", "price", True),
        ],
        ids=["name_asc", "name_desc", "price_asc", "price_desc"],
    )
    def test_sort_across_all_pages(self, client, sort, field, reverse):
        with allure.step(f"Загрузить все страницы с sort={sort}"):
            items = client.get_all_products(sort=sort)
        with allure.step("Проверить порядок по всему каталогу"):
            values = [p[field].lower() if field == "name" else p[field] for p in items]
            assert values == sorted(values, reverse=reverse)


@allure.feature("Products API")
class TestProductById:

    @allure.title("GET /products/{id} возвращает тот же товар, что и список")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_by_id(self, client):
        with allure.step("Получить первый товар из списка"):
            listed = client.get_products().json()["data"][0]
        with allure.step(f"Запросить товар {listed['id']} по id"):
            response = client.get_product(listed["id"])
        with allure.step("Проверить код и схему ответа"):
            assert response.status_code == 200
            product = Product.model_validate(response.json())
        with allure.step("Сравнить с данными из списка"):
            assert product.id == listed["id"]
            assert product.name == listed["name"]
            assert product.price == listed["price"]

    @allure.title("Несуществующий id возвращает 404")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.api
    def test_get_nonexistent(self, client):
        response = client.get_product("00000000000000000000000000")
        assert response.status_code == 404
        assert response.json() == {"message": "Requested item not found"}