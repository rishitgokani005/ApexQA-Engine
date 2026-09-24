import pytest
import allure
from pages.login_page import LoginPage
from pages.checkout_page import CheckoutPage
from utils.config import Config

@allure.epic("Web UI Test Suite")
@allure.feature("Order Processing & Checkout")
@pytest.mark.ui
@pytest.mark.regression
class TestCheckout:

    @allure.story("End-to-End E-Commerce Purchase Flow")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Verify complete customer journey: Authentication -> Cart Selection -> Shipping Details -> Order Finalization.")
    def test_e2e_checkout_flow(self, page):
        # 1. Login
        login_page = LoginPage(page).open()
        login_page.login(Config.STANDARD_USER, Config.PASSWORD)
        assert login_page.is_login_successful()

        # 2. Add products & verify cart badge count
        checkout_page = CheckoutPage(page)
        checkout_page.add_standard_items_to_cart()
        assert checkout_page.get_cart_count() == 2, "Expected 2 items in shopping cart badge."

        # 3. Proceed to checkout & fill form
        checkout_page.navigate_to_checkout_form()
        checkout_page.fill_shipping_information("Alex", "QA", "90210")

        # 4. Complete order & verify confirmation
        checkout_page.complete_order()
        confirmation = checkout_page.get_order_confirmation_text()
        assert "Thank you for your order" in confirmation, f"Unexpected confirmation text: {confirmation}"
