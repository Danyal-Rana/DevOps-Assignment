"""
Pytest Configuration and Fixtures
This file contains shared fixtures used across all test files.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

# Configuration
BASE_URL = os.getenv("APP_URL", "http://localhost:3000")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"

# Test user credentials
TEST_USER = {
    "username": f"testuser_{int(time.time())}",
    "email": f"testuser_{int(time.time())}@test.com",
    "password": "Test123456"
}


@pytest.fixture(scope="function")
def driver():
    """
    Creates a Chrome WebDriver instance for each test.
    Uses headless mode for CI/CD pipelines.
    """
    chrome_options = Options()
    
    if HEADLESS:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
    
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    
    # Initialize driver - let Selenium Manager handle driver automatically
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    
    yield driver
    
    # Cleanup after test
    driver.quit()


@pytest.fixture(scope="function")
def base_url():
    """Returns the base URL for the application."""
    return BASE_URL


@pytest.fixture(scope="module")
def registered_user():
    """
    Returns test user credentials.
    Used for tests that require a pre-registered user.
    """
    return TEST_USER.copy()


@pytest.fixture(scope="function")
def authenticated_driver(driver, base_url, registered_user):
    """
    Returns a driver that is already logged in.
    First attempts registration, then tries login.
    Returns driver regardless of auth state to allow tests to handle it.
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    # Generate unique user for this test
    unique_user = {
        "username": f"authuser_{int(time.time())}",
        "email": f"authuser_{int(time.time())}@test.com",
        "password": "Test123456"
    }
    
    driver.get(base_url)
    wait = WebDriverWait(driver, 15)
    
    # Wait for page to load
    try:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".auth-container, .app-header, .app"))
        )
    except:
        # Page didn't load, return driver anyway
        return driver
    
    # Check if already authenticated
    try:
        driver.find_element(By.CSS_SELECTOR, ".btn-logout, .todo-form")
        return driver  # Already logged in
    except:
        pass
    
    # Try to switch to register
    try:
        register_link = driver.find_element(By.CSS_SELECTOR, ".auth-link")
        if "Register" in register_link.text:
            register_link.click()
            time.sleep(0.5)
    except:
        pass
    
    # Try registration
    try:
        username_input = wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_input.clear()
        username_input.send_keys(unique_user["username"])
        
        email_input = driver.find_element(By.ID, "email")
        email_input.clear()
        email_input.send_keys(unique_user["email"])
        
        password_input = driver.find_element(By.ID, "password")
        password_input.clear()
        password_input.send_keys(unique_user["password"])
        
        confirm_password = driver.find_element(By.ID, "confirmPassword")
        confirm_password.clear()
        confirm_password.send_keys(unique_user["password"])
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        
        # Wait briefly for response
        time.sleep(2)
        
        # Check if registration succeeded
        try:
            driver.find_element(By.CSS_SELECTOR, ".btn-logout, .todo-form, .app-header h1")
            return driver  # Registration successful
        except:
            pass
            
    except Exception as e:
        print(f"Registration attempt failed: {e}")
    
    # If registration didn't work, try login
    try:
        driver.get(base_url)
        time.sleep(1)
        
        email_input = wait.until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.clear()
        email_input.send_keys(unique_user["email"])
        
        password_input = driver.find_element(By.ID, "password")
        password_input.clear()
        password_input.send_keys(unique_user["password"])
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        
        time.sleep(1)
    except Exception as e:
        print(f"Login attempt failed: {e}")
    
    # Return driver regardless of auth state
    return driver
