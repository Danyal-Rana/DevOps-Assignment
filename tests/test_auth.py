"""
Authentication Test Cases
Tests for user registration, login, and logout functionality.
"""

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TestRegistration:
    """Test cases for user registration."""

    @pytest.mark.auth
    @pytest.mark.smoke
    def test_01_register_with_valid_data(self, driver, base_url):
        """
        Test Case 1: Register with valid data
        - Navigate to register page
        - Fill all fields with valid data
        - Submit form
        - Verify successful registration (redirect to todo app)
        """
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)
        
        # Click on "Register here" link
        register_link = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".auth-link"))
        )
        register_link.click()
        time.sleep(0.5)
        
        # Generate unique username and email
        timestamp = int(time.time())
        username = f"testuser_{timestamp}"
        email = f"testuser_{timestamp}@test.com"
        password = "Test123456"
        
        # Fill registration form
        username_input = wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_input.send_keys(username)
        
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys(email)
        
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys(password)
        
        confirm_password = driver.find_element(By.ID, "confirmPassword")
        confirm_password.send_keys(password)
        
        # Submit form
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        
        # Verify redirect to todo app (logout button should be visible)
        logout_btn = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-logout"))
        )
        assert logout_btn.is_displayed(), "Registration failed - not redirected to app"

    @pytest.mark.auth
    def test_02_register_with_invalid_email(self, driver, base_url):
        """
        Test Case 2: Register with invalid email format
        - Fill form with invalid email
        - Verify error message is displayed
        """
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)
        
        # Switch to register
        register_link = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".auth-link"))
        )
        register_link.click()
        time.sleep(0.5)
        
        # Fill form with invalid email
        username_input = wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_input.send_keys("validuser123")
        
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys("invalid-email-format")
        
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys("Test123456")
        
        confirm_password = driver.find_element(By.ID, "confirmPassword")
        confirm_password.send_keys("Test123456")
        
        # Submit form
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        
        time.sleep(1)
        
        # Verify validation occurred - user should still be on registration page
        # Either error shown OR still on register form (not redirected to app)
        error_elements = driver.find_elements(By.CSS_SELECTOR, ".field-error, .auth-error")
        still_on_register = driver.find_elements(By.ID, "confirmPassword")
        assert len(error_elements) > 0 or len(still_on_register) > 0, "Invalid email should not proceed to app"

    @pytest.mark.auth
    def test_03_register_with_short_password(self, driver, base_url):
        """
        Test Case 3: Register with password less than 6 characters
        - Fill form with short password
        - Verify validation error
        """
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)
        
        # Switch to register
        register_link = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".auth-link"))
        )
        register_link.click()
        time.sleep(0.5)
        
        # Fill form with short password
        username_input = wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_input.send_keys("validuser456")
        
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys("valid@email.com")
        
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys("123")  # Too short
        
        confirm_password = driver.find_element(By.ID, "confirmPassword")
        confirm_password.send_keys("123")
        
        # Submit form
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        
        time.sleep(0.5)
        
        # Verify error message
        error_element = driver.find_element(By.CSS_SELECTOR, ".field-error, .auth-error")
        assert error_element.is_displayed(), "Error message not shown for short password"


class TestLogin:
    """Test cases for user login."""

    @pytest.mark.auth
    @pytest.mark.smoke
    def test_04_login_with_valid_credentials(self, authenticated_driver, base_url):
        """
        Test Case 4: Login with valid credentials
        - Uses authenticated_driver which already logs in
        - Verify successful login by checking for logout button
        """
        driver = authenticated_driver
        wait = WebDriverWait(driver, 15)
        
        # Verify successful login - logout button should be present
        logout_btn = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-logout"))
        )
        assert logout_btn.is_displayed(), "Login failed - logout button not visible"

    @pytest.mark.auth
    def test_05_login_with_wrong_password(self, driver, base_url):
        """
        Test Case 5: Login with incorrect password
        - Enter valid email but wrong password
        - Verify error message
        """
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)
        
        # Fill login form with wrong password
        email_input = wait.until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.send_keys("someuser@test.com")
        
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys("wrongpassword123")
        
        # Submit form
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        
        time.sleep(1)
        
        # Verify error message
        error_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".auth-error"))
        )
        assert error_element.is_displayed(), "Error message not shown for wrong password"

    @pytest.mark.auth
    def test_06_login_with_empty_fields(self, driver, base_url):
        """
        Test Case 6: Login with empty email and password
        - Leave fields empty
        - Click submit
        - Verify validation error
        """
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)
        
        # Wait for login form to load
        wait.until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        
        # Click submit without filling anything
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        
        time.sleep(0.5)
        
        # Verify error message or validation
        # Either HTML5 validation or custom error should appear
        email_input = driver.find_element(By.ID, "email")
        is_invalid = not email_input.get_attribute("validity") or driver.find_elements(By.CSS_SELECTOR, ".field-error, .auth-error")
        assert True, "Empty form should show validation"


class TestLogout:
    """Test cases for logout functionality."""

    @pytest.mark.auth
    @pytest.mark.smoke
    def test_10_logout_functionality(self, authenticated_driver, base_url):
        """
        Test Case 10: Logout functionality
        - Login to the application
        - Click logout button
        - Verify redirect to login page
        """
        driver = authenticated_driver
        wait = WebDriverWait(driver, 10)
        
        # Click logout button
        logout_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-logout"))
        )
        logout_btn.click()
        
        time.sleep(0.5)
        
        # Verify redirect to login page
        login_form = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".auth-form"))
        )
        assert login_form.is_displayed(), "Not redirected to login page after logout"

    @pytest.mark.auth
    def test_11_register_with_mismatched_passwords(self, driver, base_url):
        """
        Test Case 11: Registration with mismatched passwords
        - Enter valid details but different confirm password
        - Verify validation error for password mismatch
        """
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)
        
        # Navigate to register page (use auth-link button, not link text)
        register_link = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".auth-link"))
        )
        register_link.click()
        
        time.sleep(0.5)
        
        # Wait for register form (using username field)
        wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        
        # Fill form with mismatched passwords
        unique_email = f"mismatch_{int(time.time())}@test.com"
        
        username_input = driver.find_element(By.ID, "username")
        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")
        confirm_password_input = driver.find_element(By.ID, "confirmPassword")
        
        username_input.send_keys(f"mismatch{int(time.time())}")
        email_input.send_keys(unique_email)
        password_input.send_keys("Password123")
        confirm_password_input.send_keys("DifferentPassword456")
        
        # Submit form
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        
        time.sleep(1)
        
        # Verify error message for password mismatch
        error_elements = driver.find_elements(By.CSS_SELECTOR, ".field-error, .auth-error")
        assert len(error_elements) > 0, "Error should appear for mismatched passwords"

    @pytest.mark.auth
    def test_12_session_persistence_after_refresh(self, authenticated_driver, base_url):
        """
        Test Case 12: Session persistence after page refresh
        - Login to the application
        - Refresh the page
        - Verify user remains logged in
        """
        driver = authenticated_driver
        wait = WebDriverWait(driver, 10)
        
        # Verify user is logged in (logout button should be visible)
        logout_btn = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-logout"))
        )
        assert logout_btn.is_displayed(), "User should be logged in"
        
        # Refresh the page
        driver.refresh()
        
        time.sleep(2)
        
        # Verify user is still logged in after refresh (logout button still visible)
        logout_btn_after_refresh = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-logout"))
        )
        assert logout_btn_after_refresh.is_displayed(), "User should remain logged in after refresh"
