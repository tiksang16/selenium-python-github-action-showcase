import os
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Base URL for the HTML file
BASE_URL = "http://selenium-python-resolver.s3-website.us-east-2.amazonaws.com/"  

@pytest.fixture(scope="function")
def driver():
    # Set Chrome options
    chrome_options = Options()

    # Check if the script is running in CI/CD (e.g., GitHub Actions)
    if os.getenv("CI"):  # Headless mode for CI
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

    # Set up the Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()

@allure.title("Test 1: Verify Login Form Presence and Functionality")
@allure.description("This test verifies the presence of the login form and checks that the email and password fields are functional.")
def test_1_login_form(driver):
    """Test 1: Verify login form presence and functionality."""

    with allure.step("Navigate to the home page"):
        driver.get(BASE_URL)

    with allure.step("Wait for the email field to be visible and assert its presence"):
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
        )
        assert email_field.is_displayed(), "Email field is not visible on the page"

    with allure.step("Wait for the password field to be visible and assert its presence"):
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
        )
        assert password_field.is_displayed(), "Password field is not visible on the page"

    with allure.step("Wait for the sign-in button to be visible and assert its presence"):
        sign_in_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='Sign in']"))
        )
        assert sign_in_button.is_displayed(), "Sign-in button is not visible on the page"

    with allure.step("Enter email and password into the respective fields"):
        email_field.send_keys("test@example.com")
        password_field.send_keys("password123")

    with allure.step("Click the sign-in button"):
        sign_in_button.click()



# def test_2_list_group(driver):
#     """Test 2: Verify list group values."""
#     driver.get(BASE_URL)

#     # Assert there are 3 list items
#     list_items = driver.find_elements(By.XPATH, "//div[@id='test-2-div']//li")
#     assert len(list_items) == 3

#     # Assert the second list item's text and badge value
#     second_item_text = list_items[1].text
#     second_item_badge = list_items[1].find_element(By.XPATH, ".//span").text
#     assert "List Item 2" in second_item_text
#     assert second_item_badge == "6"


# def test_3_select_option(driver):
#     """Test 3: Verify default and selectable dropdown options."""
#     driver.get(BASE_URL)

#     # Assert "Option 1" is selected by default
#     dropdown = driver.find_element(By.XPATH, "//select[@id='dropdown']")
#     selected_option = dropdown.find_element(By.XPATH, ".//option[@selected]").text
#     assert selected_option == "Option 1"

#     # Select "Option 3"
#     dropdown.find_element(By.XPATH, ".//option[text()='Option 3']").click()


# def test_4_button_states(driver):
#     """Test 4: Verify button states."""
#     driver.get(BASE_URL)

#     # Assert the first button is enabled and the second button is disabled
#     first_button = driver.find_element(By.XPATH, "//div[@id='test-4-div']//button[1]")
#     second_button = driver.find_element(By.XPATH, "//div[@id='test-4-div']//button[2]")
#     assert first_button.is_enabled()
#     assert not second_button.is_enabled()


# def test_5_button_click(driver):
#     """Test 5: Verify dynamic button click and success message."""
#     driver.get(BASE_URL)

#     # Wait for the button to appear
#     button = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//div[@id='test-5-div']//button"))
#     )
#     button.click()

#     # Assert success message and button disabled
#     success_message = driver.find_element(By.XPATH, "//div[@id='test-5-div']//p").text
#     assert success_message == "You clicked a button!"
#     assert not button.is_enabled()


# def test_6_grid_coordinates(driver):
#     """Test 6: Verify grid value at coordinates (2, 2)."""
#     driver.get(BASE_URL)

#     # Find the value at cell (2, 2)
#     cell_value = driver.find_element(By.XPATH, "//div[@id='test-6-div']//tr[3]/td[3]").text
#     assert cell_value == "Ventosanzap"