import allure
from pages.base_page import BasePage
from utils.config import Config

class LoginPage(BasePage):
    """Page Object for Swag Labs (SauceDemo) Login Page."""
    
    # Locators
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_CONTAINER = "[data-test='error']"
    APP_LOGO = ".app_logo"

    def __init__(self, page):
        super().__init__(page)
        self.url = Config.BASE_URL

    @allure.step("Open Login Page")
    def open(self):
        self.navigate(self.url)
        return self

    @allure.step("Perform login with username: {username}")
    def login(self, username: str, password: str):
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    @allure.step("Get login error message")
    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_CONTAINER)

    @allure.step("Verify user successfully landed on Inventory page")
    def is_login_successful(self) -> bool:
        return self.is_visible(self.APP_LOGO)
