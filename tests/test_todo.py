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
        title_input = wait.until(
            EC.presence_of_element_located((By.ID, "title"))
        )
        title_input.clear()
        title_input.send_keys(todo_title)
        
        description_input = driver.find_element(By.ID, "description")
        description_input.clear()
        description_input.send_keys(todo_description)
        
        # Select priority
        priority_select = driver.find_element(By.ID, "priority")
        priority_select.click()
        high_option = driver.find_element(By.CSS_SELECTOR, "option[value='high']")
        high_option.click()
        
        # Submit form
        submit_btn = driver.find_element(By.CSS_SELECTOR, ".todo-form button[type='submit']")
        submit_btn.click()
        
        time.sleep(1)
        
        # Verify todo appears in list
        todo_items = driver.find_elements(By.CSS_SELECTOR, ".todo-item")
        todo_titles = [item.find_element(By.CSS_SELECTOR, ".todo-title").text for item in todo_items]
        
        assert todo_title in todo_titles, f"Created todo '{todo_title}' not found in list"

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
        
        title_input = wait.until(
            EC.presence_of_element_located((By.ID, "title"))
        )
        title_input.clear()
        title_input.send_keys(todo_title)
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, ".todo-form button[type='submit']")
        submit_btn.click()
        
        time.sleep(1)
        
        # Find the created todo and click complete button
        todo_items = driver.find_elements(By.CSS_SELECTOR, ".todo-item")
        target_todo = None
        
        for item in todo_items:
            title_element = item.find_element(By.CSS_SELECTOR, ".todo-title")
            if title_element.text == todo_title:
                target_todo = item
                break
        
        assert target_todo is not None, f"Todo '{todo_title}' not found"
        
        # Click complete button
        complete_btn = target_todo.find_element(By.CSS_SELECTOR, ".btn-success, button:first-of-type")
        complete_btn.click()
        
        time.sleep(0.5)
        
        # Refresh todo items and check for completed class
        todo_items = driver.find_elements(By.CSS_SELECTOR, ".todo-item")
        for item in todo_items:
            title_element = item.find_element(By.CSS_SELECTOR, ".todo-title")
            if title_element.text == todo_title:
                classes = item.get_attribute("class")
                assert "completed" in classes, "Todo not marked as completed"
                break

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
        
        title_input = wait.until(
            EC.presence_of_element_located((By.ID, "title"))
        )
        title_input.clear()
        title_input.send_keys(original_title)
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, ".todo-form button[type='submit']")
        submit_btn.click()
        
        time.sleep(1)
        
        # Find the todo and click edit
        todo_items = driver.find_elements(By.CSS_SELECTOR, ".todo-item")
        target_todo = None
        
        for item in todo_items:
            title_element = item.find_element(By.CSS_SELECTOR, ".todo-title")
            if title_element.text == original_title:
                target_todo = item
                break
        
        assert target_todo is not None, f"Todo '{original_title}' not found"
        
        # Click edit button
        edit_btn = target_todo.find_element(By.CSS_SELECTOR, ".btn-primary")
        edit_btn.click()
        
        time.sleep(0.5)
        
        # Update title in the form
        title_input = driver.find_element(By.ID, "title")
        title_input.clear()
        title_input.send_keys(updated_title)
        
        # Submit update
        update_btn = driver.find_element(By.CSS_SELECTOR, ".todo-form button[type='submit']")
        update_btn.click()
        
        time.sleep(1)
        
        # Verify update
        todo_items = driver.find_elements(By.CSS_SELECTOR, ".todo-item")
        todo_titles = [item.find_element(By.CSS_SELECTOR, ".todo-title").text for item in todo_items]
        
        assert updated_title in todo_titles, f"Updated title '{updated_title}' not found"
        assert original_title not in todo_titles, f"Original title '{original_title}' still exists"

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
        
        title_input = wait.until(
            EC.presence_of_element_located((By.ID, "title"))
        )
        title_input.clear()
        title_input.send_keys(todo_title)
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, ".todo-form button[type='submit']")
        submit_btn.click()
        
        time.sleep(1)
        
        # Get initial count
        todo_items = driver.find_elements(By.CSS_SELECTOR, ".todo-item")
        initial_count = len(todo_items)
        
        # Find the todo and click delete
        target_todo = None
        for item in todo_items:
            title_element = item.find_element(By.CSS_SELECTOR, ".todo-title")
            if title_element.text == todo_title:
                target_todo = item
                break
        
        assert target_todo is not None, f"Todo '{todo_title}' not found"
        
        # Click delete button
        delete_btn = target_todo.find_element(By.CSS_SELECTOR, ".btn-danger")
        delete_btn.click()
        
        # Handle confirmation dialog
        try:
            alert = wait.until(EC.alert_is_present())
            alert.accept()
        except TimeoutException:
            pass  # No alert present
        
        time.sleep(1)
        
        # Verify todo is deleted
        todo_items = driver.find_elements(By.CSS_SELECTOR, ".todo-item")
        todo_titles = [item.find_element(By.CSS_SELECTOR, ".todo-title").text for item in todo_items]
        
        assert todo_title not in todo_titles, f"Todo '{todo_title}' was not deleted"
        assert len(todo_items) == initial_count - 1, "Todo count did not decrease"
