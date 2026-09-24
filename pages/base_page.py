import allure
from playwright.sync_api import Page, Locator, expect
from typing import Optional

class BasePage:
    """
    Base Page class establishing standard UI interaction wrappers with 
    built-in Allure step logging and explicit wait strategies.
    """
    
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Navigate to URL: {url}")
    def navigate(self, url: str) -> None:
        """Navigates to the specified URL."""
        self.page.goto(url)

    @allure.step("Click element: {selector}")
    def click(self, selector: str) -> None:
        """Clicks an element specified by CSS selector or XPath."""
        self.page.locator(selector).click()

    @allure.step("Type text into element: {selector}")
    def fill(self, selector: str, value: str) -> None:
        """Fills input field with text."""
        self.page.locator(selector).fill(value)

    @allure.step("Get text content from: {selector}")
    def get_text(self, selector: str) -> str:
        """Retrieves visible text from an element."""
        return self.page.locator(selector).text_content().strip()

    @allure.step("Check visibility of element: {selector}")
    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """Checks if an element is visible within timeout."""
        try:
            return self.page.locator(selector).is_visible(timeout=timeout)
        except Exception:
            return False

    @allure.step("Wait for element to be visible: {selector}")
    def wait_for_element(self, selector: str, timeout: int = 10000) -> Locator:
        """Waits for an element to be visible and returns locator."""
        locator = self.page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout)
        return locator

    @allure.step("Attach explicit screenshot to report: {name}")
    def capture_screenshot(self, name: str) -> None:
        """Takes a screenshot and attaches it directly to Allure report."""
        screenshot = self.page.screenshot(full_page=True)
        allure.attach(
            screenshot,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
