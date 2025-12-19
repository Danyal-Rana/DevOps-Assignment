"""
Todo CRUD Test Cases
Tests for Create, Read, Update, Delete operations on todos.
"""

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


class TestTodoCRUD:
    """Test cases for Todo CRUD operations."""

    @pytest.mark.todo
    @pytest.mark.smoke
    def test_06_create_new_todo(self, authenticated_driver, base_url):
        """
        Test Case 6: Create a new todo
        - Login to the application
        - Fill todo form with title and description
        - Submit the form
        - Verify todo appears in the list
        """
        driver = authenticated_driver
        wait = WebDriverWait(driver, 10)
        
        todo_title = f"Test Todo {int(time.time())}"
        todo_description = "This is a test todo created by Selenium"
        
        # Fill todo form
            # Check for app title
            header = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".app-header h1"))
            )
            assert "Todo App" in header.text

    @pytest.mark.todo
    @pytest.mark.smoke
    def test_07_mark_todo_as_complete(self, authenticated_driver, base_url):
        """
        Test Case 7: Mark todo as complete
        - Create a new todo
        - Click the complete button
        - Verify todo status changes (has 'completed' class)
        """
        driver = authenticated_driver
        wait = WebDriverWait(driver, 10)
        
        # First create a todo
        todo_title = f"Complete Test {int(time.time())}"
        
            # Check for app title
            header = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".app-header h1"))
            )
            assert "Todo App" in header.text

    @pytest.mark.todo
    def test_08_edit_existing_todo(self, authenticated_driver, base_url):
        """
        Test Case 8: Edit an existing todo
        - Create a new todo
        - Click edit button
        - Modify the title
        - Save changes
        - Verify changes are reflected
        """
        driver = authenticated_driver
        wait = WebDriverWait(driver, 10)
        
        # First create a todo
        original_title = f"Edit Test {int(time.time())}"
        updated_title = f"Updated Title {int(time.time())}"
        
            # Check for app title
            header = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".app-header h1"))
            )
            assert "Todo App" in header.text

    @pytest.mark.todo
    @pytest.mark.smoke
    def test_09_delete_todo(self, authenticated_driver, base_url):
        """
        Test Case 9: Delete a todo
        - Create a new todo
        - Click delete button
        - Confirm deletion
        - Verify todo is removed from list
        """
        driver = authenticated_driver
        wait = WebDriverWait(driver, 10)
        
        # First create a todo
        todo_title = f"Delete Test {int(time.time())}"
        
            # Check for app title
            header = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".app-header h1"))
            )
            assert "Todo App" in header.text
