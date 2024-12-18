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



@allure.title("Test 2: Verify List Group Values in Test 2 Div")
@allure.description("This test verifies the list group in the Test 2 div. It checks the number of items, the text of the second list item, and its badge value.")
def test_2_list_group(driver):
    """Test 2: Verify List Group Values in Test 2 Div."""

    with allure.step("Navigate to the home page"):
        driver.get(BASE_URL)

    with allure.step("Locate the Test 2 div and assert there are three list items"):
        # Locate all list items in the Test 2 div
        list_items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@id='test-2-div']//li"))
        )

        # Extract the text values of the list items
        list_texts = [item.text for item in list_items]

        # Log the extracted texts for debugging
        print(f"List Items Text: {list_texts}")
        allure.attach("\n".join(list_texts), name="List Items Text", attachment_type=allure.attachment_type.TEXT)

        # Assert the number of items in the list
        assert len(list_items) == 3, f"Expected 3 list items, but found {len(list_items)}"

    with allure.step("Assert that the second list item's text is 'List Item 2'"):
        # Locate the second <li> element
        second_list_item = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='test-2-div']//li[2]"))
        )

        # Get the full text of the <li> element
        full_text = second_list_item.text  # Includes 'List Item 2 6'

        # Get the text of the <span> element inside the <li>
        badge_text = second_list_item.find_element(By.XPATH, ".//span").text  # '6'

        # Subtract the badge text from the full text to get the desired value
        second_item_text = full_text.replace(badge_text, "").strip()  # 'List Item 2'

        # Log and assert the text
        print(f"Second item text: {second_item_text}")
        allure.attach(second_item_text, name="Second List Item Text", attachment_type=allure.attachment_type.TEXT)
        assert second_item_text == "List Item 2", f"Expected 'List Item 2', but found '{second_item_text}'"

    with allure.step("Assert that the second list item's badge value is '6'"):
        # Assert the badge value
        print(f"Second item badge value: {badge_text}")
        allure.attach(badge_text, name="Second List Item Badge Value", attachment_type=allure.attachment_type.TEXT)
        assert badge_text == "6", f"Expected badge value '6', but found '{badge_text}'"

@allure.title("Test 3: Verify default selection and change dropdown value in Test 3 div")
@allure.description("This test verifies that 'Option 1' is the default selected value in the Test 3 dropdown and then selects 'Option 3'")
def test_3_dropdown(driver):
    """Test 3: Verify default selection and select Option 3 in Test 3 div."""

    with allure.step("Navigate to the home page"):
        driver.get(BASE_URL)

    with allure.step("Locate the Test 3 dropdown button"):
        # Locate the dropdown button
        dropdown_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dropdownMenuButton"))
        )

        # Verify the default selected option is "Option 1"
        default_option = dropdown_button.text.strip()
        print(f"Default selected option: {default_option}")
        assert default_option == "Option 1", f"Expected 'Option 1', but found '{default_option}'"

    with allure.step("Open the dropdown menu"):
        # Click the dropdown button to open the menu
        dropdown_button.click()

        # Wait until the dropdown menu is visible
        dropdown_menu = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "dropdown-menu"))
        )
        assert dropdown_menu.is_displayed(), "Dropdown menu is not visible"

    with allure.step("Select 'Option 3' from the dropdown"):
        # Locate and click the "Option 3" item within the visible dropdown menu
        option_3 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'dropdown-menu') and contains(@class, 'show')]//a[normalize-space()='Option 3']"))
        )
        option_3.click()

        # Verify the dropdown button now shows "Option 3"
        updated_option = dropdown_button.text.strip()
        print(f"Updated selected option: {updated_option}")
        assert updated_option == "Option 3", f"Expected 'Option 3', but found '{updated_option}'"

        # Attach the updated option to the Allure report
        allure.attach(updated_option, name="Updated Selected Option", attachment_type=allure.attachment_type.TEXT)

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