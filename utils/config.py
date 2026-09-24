import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Central configuration class for ApexQA-Engine test suite."""
    
    # UI Configurations
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10000")) # ms
    VIEWPORT = {"width": 1280, "height": 720}
    
    # Credentials (SauceDemo public demo user)
    STANDARD_USER = os.getenv("STANDARD_USER", "standard_user")
    LOCKED_USER = os.getenv("LOCKED_USER", "locked_out_user")
    PASSWORD = os.getenv("PASSWORD", "secret_sauce")
    
    # API Configurations
    API_BASE_URL = os.getenv("API_BASE_URL", "https://reqres.in/api")
    # reqres.in now requires an x-api-key header on every request (free signup at https://reqres.in)
    REQRES_API_KEY = os.getenv("REQRES_API_KEY", "")
    
    # Notifications & Reporting
    SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")
    ALLURE_REPORT_URL = os.getenv("ALLURE_REPORT_URL", "https://your-username.github.io/ApexQA-Engine/")
