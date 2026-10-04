import allure
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.product_page import ProductPage


@allure.feature("Catalog")
class TestSearch:

    @allure.story("Search")
    @allure.title("Поиск по запросу: {query}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.parametrize("query", ["Pliers", "Hammer", "Wrench"])
    def test_search_returns_matching_products(self, home_page: HomePage, query: str):
        with allure.step("Открыть главную и дождаться каталога"):
            home_page.open()
            expect(home_page.product_names.first).to_be_visible()
        with allure.step(f"Искать '{query}'"):
            backend_names = home_page.search(query)
        with allure.step("Проверить, что UI показывает ответ бэкенда"):
            assert backend_names, "Поиск вернул пустой список"
            expect(home_page.product_cards).to_have_count(len(backend_names))
            expect(home_page.product_names).to_have_text(backend_names)

    @allure.story("Search")
    @allure.title("Поиск несуществующего товара")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_search_no_results(self, home_page: HomePage):
        with allure.step("Открыть главную и дождаться каталога"):
            home_page.open()
            expect(home_page.product_names.first).to_be_visible()
        with allure.step("Искать несуществующий товар"):
            backend_names = home_page.search("qwertyuiopasdf")
        with allure.step("Проверить отсутствие результатов"):
            assert backend_names == []
            expect(home_page.no_results).to_be_visible()
            expect(home_page.product_cards).to_have_count(0)


@allure.feature("Catalog")
class TestSorting:

    @allure.story("Sorting")
    @allure.title("Сортировка: {label}")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.parametrize(
        "label,key,reverse",
        [
            ("Name (A - Z)", "names", False),
            ("Name (Z - A)", "names", True),
            ("Price (Low - High)", "prices", False),
            ("Price (High - Low)", "prices", True),
        ],
        ids=["name_asc", "name_desc", "price_asc", "price_desc"],
    )
    def test_sort(self, home_page: HomePage, label: str, key: str, reverse: bool):
        with allure.step("Открыть главную и дождаться каталога"):
            home_page.open()
            expect(home_page.product_names.first).to_be_visible()
        with allure.step(f"Выбрать сортировку: {label}"):
            old_names = home_page.sort_by(label)
            expect(home_page.product_names).not_to_have_text(old_names)
        with allure.step("Проверить порядок"):
            if key == "names":
                values = home_page.get_product_names()
                expected = sorted(values, key=str.lower, reverse=reverse)
            else:
                values = home_page.get_product_prices()
                expected = sorted(values, reverse=reverse)
            assert values == expected, f"Порядок не соответствует '{label}'"


@allure.feature("Catalog")
class TestFilter:

    @allure.story("Category filter")
    @allure.title("Фильтр по категории: {category}")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.parametrize("category", ["Hand Tools", "Pliers"])
    def test_filter_by_category(self, home_page: HomePage, category: str):
        with allure.step("Открыть главную и дождаться каталога"):
            home_page.open()
            expect(home_page.product_names.first).to_be_visible()
        with allure.step(f"Выбрать категорию {category}"):
            backend_names = home_page.filter_by_category(category)
        with allure.step("Проверить, что UI показывает ответ бэкенда"):
            assert backend_names, "Фильтр вернул пустой список"
            expect(home_page.product_cards).to_have_count(len(backend_names))
            expect(home_page.product_names).to_have_text(backend_names)


@allure.feature("Catalog")
class TestProductPage:

    @allure.story("Product details")
    @allure.title("Открытие карточки товара из каталога")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_open_product_from_catalog(self, home_page: HomePage, product_page: ProductPage):
        with allure.step("Открыть главную и взять первый товар"):
            home_page.open()
            expect(home_page.product_names.first).to_be_visible()
            name = home_page.get_product_names()[0]
        with allure.step(f"Открыть товар '{name}'"):
            home_page.open_product(name)
        with allure.step("Проверить страницу товара"):
            expect(product_page.name).to_contain_text(name)
            expect(product_page.price).to_be_visible()
            expect(product_page.add_to_cart_button).to_be_enabled()