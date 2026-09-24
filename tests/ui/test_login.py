import pytest
import allure
from pages.login_page import LoginPage
from utils.config import Config

@allure.epic("Web UI Test Suite")
@allure.feature("Authentication Engine")
@pytest.mark.ui
@pytest.mark.smoke
class TestLogin:

    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Verify that standard users can authenticate successfully and reach the inventory dashboard.")
    def test_successful_login(self, page):
        login_page = LoginPage(page).open()
        login_page.login(Config.STANDARD_USER, Config.PASSWORD)
        
        assert login_page.is_login_successful(), "Expected user to land on inventory page after valid login."

    @allure.story("Invalid Login Credentials")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Verify that login fails with appropriate error prompt when using invalid password.")
    def test_invalid_password_login(self, page):
        login_page = LoginPage(page).open()
        login_page.login(Config.STANDARD_USER, "invalid_pass_123")
        
        error_msg = login_page.get_error_message()
        assert "Username and password do not match" in error_msg

    @allure.story("Locked Out User Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Verify that locked out accounts are blocked from authenticating.")
    def test_locked_out_user(self, page):
        login_page = LoginPage(page).open()
        login_page.login(Config.LOCKED_USER, Config.PASSWORD)
        
        error_msg = login_page.get_error_message()
        assert "Sorry, this user has been locked out" in error_msg
