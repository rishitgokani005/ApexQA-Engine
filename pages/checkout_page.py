import allure
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    """Page Object for Swag Labs Inventory, Shopping Cart & Checkout Process."""

    # Locators
    ADD_BACKPACK_BTN = "[data-test='add-to-cart-sauce-labs-backpack']"
    ADD_BIKE_LIGHT_BTN = "[data-test='add-to-cart-sauce-labs-bike-light']"
    CART_BADGE = ".shopping_cart_badge"
    CART_LINK = ".shopping_cart_link"
    CHECKOUT_BTN = "#checkout"
    
    # Checkout Step One (User Details)
    FIRST_NAME_INPUT = "#first-name"
    LAST_NAME_INPUT = "#last-name"
    POSTAL_CODE_INPUT = "#postal-code"
    CONTINUE_BTN = "#continue"
    
    # Checkout Step Two (Overview & Complete)
    FINISH_BTN = "#finish"
    COMPLETE_HEADER = ".complete-header"
    INVENTORY_ITEM_NAME = ".inventory_item_name"

    def __init__(self, page):
        super().__init__(page)

    @allure.step("Add backpack and bike light to shopping cart")
    def add_standard_items_to_cart(self):
        self.click(self.ADD_BACKPACK_BTN)
        self.click(self.ADD_BIKE_LIGHT_BTN)

    @allure.step("Get item count from shopping cart badge")
    def get_cart_count(self) -> int:
        if self.is_visible(self.CART_BADGE):
            text = self.get_text(self.CART_BADGE)
            return int(text)
        return 0

    @allure.step("Open shopping cart and proceed to checkout")
    def navigate_to_checkout_form(self):
        self.click(self.CART_LINK)
        self.click(self.CHECKOUT_BTN)

    @allure.step("Fill shipping details: {first_name} {last_name}, Zip: {postal_code}")
    def fill_shipping_information(self, first_name: str, last_name: str, postal_code: str):
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.POSTAL_CODE_INPUT, postal_code)
        self.click(self.CONTINUE_BTN)

    @allure.step("Complete purchase order")
    def complete_order(self):
        self.click(self.FINISH_BTN)

    @allure.step("Get confirmation message after checkout")
    def get_order_confirmation_text(self) -> str:
        return self.get_text(self.COMPLETE_HEADER)
