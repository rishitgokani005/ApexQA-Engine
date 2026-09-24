import os
import time
import pytest
import allure
from datetime import datetime
from playwright.sync_api import sync_playwright
from utils.config import Config

# Store test execution metrics for reporting & notifications
pytest_results = {
    "passed": 0,
    "failed": 0,
    "skipped": 0,
    "start_time": 0,
    "end_time": 0,
    "duration": 0
}

def pytest_sessionstart(session):
    """Fired at the start of pytest execution."""
    pytest_results["start_time"] = time.time()

def pytest_sessionfinish(session, exitstatus):
    """Fired when pytest execution completes. Generates Allure environment details."""
    pytest_results["end_time"] = time.time()
    pytest_results["duration"] = round(pytest_results["end_time"] - pytest_results["start_time"], 2)
    
    # Save environment information for Allure report
    results_dir = session.config.getoption("--alluredir")
    if results_dir and os.path.exists(results_dir):
        env_file = os.path.join(results_dir, "environment.properties")
        with open(env_file, "w") as f:
            f.write(f"Framework=ApexQA-Engine\n")
            f.write(f"Environment=Production Target\n")
            f.write(f"UI_Base_URL={Config.BASE_URL}\n")
            f.write(f"API_Base_URL={Config.API_BASE_URL}\n")
            f.write(f"Execution_Timestamp={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test outcome and auto-attach screenshot on failure to Allure report."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        if report.passed:
            pytest_results["passed"] += 1
        elif report.failed:
            pytest_results["failed"] += 1
            # Capture screenshot if page object is available in fixture arguments
            page = item.funcargs.get("page", None)
            if page:
                try:
                    screenshot_bytes = page.screenshot(full_page=True)
                    allure.attach(
                        screenshot_bytes,
                        name=f"Failure_Screenshot_{item.name}",
                        attachment_type=allure.attachment_type.PNG
                    )
                    # Also attach page HTML source for deep debugging
                    allure.attach(
                        page.content(),
                        name=f"Page_DOM_{item.name}",
                        attachment_type=allure.attachment_type.HTML
                    )
                except Exception as e:
                    print(f"Failed to capture failure screenshot: {e}")
        elif report.skipped:
            pytest_results["skipped"] += 1

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context arguments for Playwright."""
    return {
        **browser_context_args,
        "viewport": Config.VIEWPORT,
        "ignore_https_errors": True,
    }

@pytest.fixture(scope="function")
def page(page):
    """Function-scoped page fixture with default timeout configuration."""
    page.set_default_timeout(Config.DEFAULT_TIMEOUT)
    yield page
