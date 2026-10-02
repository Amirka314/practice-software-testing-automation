import allure
import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.product_page import ProductPage

@allure.feature("Catalog")
class TestSearch:
    @allure.story("Search")
    @allure.title("Поиск по запросу: {query}")
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.parametrize("query", ["Pliers", "Hammer", "Wrench"])
    def test_search_returns_matching_products(self, home_page: HomePage, query):
        with allure.step("Открыть главную"):
            home_page.open()
        with allure.step(f"Искать '{query}'"):
            home_page.search(query)
        with allure.step("Проверить, что есть результаты и хотя бы один содержит запрос"):
            expect(home_page.product_cards.first).to_be_visible()
            names = home_page.get_product_names()
            assert names, "Список результатов пуст"
            assert any(query.lower() in n.lower() for n in names), f"Ни один товар из {names} не содержит '{query}'"

    @allure.story("Search")
    @allure.title("Поиск несуществующего товара")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_search_no_results(self, home_page: HomePage):
        home_page.open()
        home_page.search("qwertyuiopasdf")
        expect(home_page.no_results).to_be_visible()
        expect(home_page.product_cards).to_have_count(0)

@allure.feature("Catalog")
class TestSorting:
    @allure.story("Sorting")
    @allure.title("Сортировка: {label}")
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
    def test_sort(self, home_page: HomePage, label, key, reverse):
        home_page.open()
        expect(home_page.product_cards.first).to_be_visible()
        home_page.sort_by(label)
        expect(home_page.product_cards.first).to_be_visible()
        values = (
            home_page.get_product_names() if key == "names" else home_page.get_product_prices()
        )
        if key == "names":
            expected = sorted(values, key=str.lower, reverse=reverse)
        else:
            expected = sorted(values, reverse=reverse)
        assert values == expected, f"Порядок не соответствует '{label}'"

@allure.feature("Catalog")
class TestFilter:
    @allure.story("Category filter")
    @allure.title("Фильтр по категории: {category}")
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.parametrize("category", ["Hammer", "Hand Tools"])
    def test_filter_by_category(self, home_page: HomePage, category):
        home_page.open()
        expect(home_page.product_cards.first).to_be_visible()
        home_page.filter_by_category(category)
        expect(home_page.product_cards.first).to_be_visible()
        assert home_page.get_product_names(), "После фильтра список пуст"

@allure.feature("Catalog")
class TestProductPage:
    @allure.story("Product details")
    @allure.title("Открытие карточки товара из каталога")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_open_product_from_catalog(self, home_page: HomePage, product_page: ProductPage, page: Page):
        home_page.open()
        expect(home_page.product_cards.first).to_be_visible()
        name = home_page.get_product_names()[0]
        home_page.open_product(name)
        expect(product_page.name).to_contain_text(name)
        expect(product_page.price).to_be_visible()
        expect(product_page.add_to_cart_button).to_be_enabled()