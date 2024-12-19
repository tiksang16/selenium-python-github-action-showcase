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
    if os.getenv("CI") or os.getenv("HEADLESS"):  
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


@allure.title("Test 1: Verify Login Form Presence and Input Functionality")
@allure.description("This test verifies the presence of the login form (email, password and login button) and allows input into the fields.")
def test_1_login_form(driver):

    with allure.step("Navigate to the home page"):
        # Navigate to the base URL
        driver.get(BASE_URL)

    with allure.step("Locate and assert the presence of the email input field"):
        # Locate the email input field
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "inputEmail"))
        )
        # Assert that the email field is displayed
        assert email_field.is_displayed(), "Email input field is not visible on the page"

    with allure.step("Locate and assert the presence of the password input field"):
        # Locate the password input field
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "inputPassword"))
        )
        # Assert that the password field is displayed
        assert password_field.is_displayed(), "Password input field is not visible on the page"

    with allure.step("Locate and assert the presence of the login button"):
        # Locate the login button
        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and text()='Sign in']"))
        )
        # Assert that the login button is displayed
        assert login_button.is_displayed(), "Login button is not visible on the page"

    with allure.step("Enter email and password into the respective fields"):
        # Enter the email address
        email_field.send_keys("test@example.com")
        # Enter the password
        password_field.send_keys("password123")
    

    with allure.step("Click the login button"):
        # Click the login button
        login_button.click()


@allure.title("Test 2: Verify List Group Values in Test 2 Div")
@allure.description("This test verifies the list group in the Test 2 div. It checks the number of items, the text of the second list item and its badge value.")
def test_2_list_group(driver):

    with allure.step("Navigate to the home page"):
        driver.get(BASE_URL)

    with allure.step("Locate the Test 2 div and assert there are three list items"):
        # Locate all list items in the Test 2 div
        list_items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@id='test-2-div']//li"))
        )

        # Extract the text values of the list items
        list_texts = [item.text for item in list_items]


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
        allure.attach(second_item_text, name="Second List Item Text", attachment_type=allure.attachment_type.TEXT)
        assert second_item_text == "List Item 2", f"Expected 'List Item 2', but found '{second_item_text}'"

    with allure.step("Assert that the second list item's badge value is '6'"):
        # Assert the badge value
        allure.attach(badge_text, name="Second List Item Badge Value", attachment_type=allure.attachment_type.TEXT)
        assert badge_text == "6", f"Expected badge value '6', but found '{badge_text}'"


@allure.title("Test 3: Verify default selection and change dropdown value in Test 3 div")
@allure.description("This test verifies that 'Option 1' is the default selected value in the Test 3 dropdown and then selects 'Option 3'")
def test_3_dropdown(driver):

    with allure.step("Navigate to the home page"):
        driver.get(BASE_URL)

    with allure.step("Locate the Test 3 dropdown button"):
        # Locate the dropdown button
        dropdown_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dropdownMenuButton"))
        )

        # Verify the default selected option is "Option 1"
        default_option = dropdown_button.text.strip()
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
        assert updated_option == "Option 3", f"Expected 'Option 3', but found '{updated_option}'"

        # Attach the updated option to the Allure report
        allure.attach(updated_option, name="Updated Selected Option", attachment_type=allure.attachment_type.TEXT)


@allure.title("Test 4: Verify button states in Test 4 div")
@allure.description("This test verifies that the first button in Test 4 div is enabled and the second button is disabled")
def test_4_buttons(driver):

    with allure.step("Navigate to the home page"):
        driver.get(BASE_URL)

    with allure.step("Locate the Test 4 div"):
        # Locate the Test 4 div
        test_4_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "test-4-div"))
        )

    with allure.step("Locate the first and second buttons in Test 4 div"):
        # Locate the first button
        first_button = test_4_div.find_element(By.XPATH, ".//button[@class='btn btn-lg btn-primary']")

        # Locate the second button
        second_button = test_4_div.find_element(By.XPATH, ".//button[@class='btn btn-lg btn-secondary']")

    with allure.step("Assert that the first button is enabled"):
        # Assert that the first button is enabled
        assert first_button.is_enabled(), "The first button is not enabled"

    with allure.step("Assert that the second button is disabled"):
        # Assert that the second button is disabled
        assert not second_button.is_enabled(), "The second button is not disabled"


@allure.title("Test 5: Wait for button to appear, click it, and verify success message")
@allure.description("This test waits for a button to appear in Test 5 div, clicks it, verifies the success message, and ensures the button is disabled")
def test_5_button(driver):

    with allure.step("Navigate to the home page"):
        driver.get(BASE_URL)

    with allure.step("Locate the Test 5 div"):
        # Locate the Test 5 div
        test_5_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "test-5-div"))
        )

    with allure.step("Wait for the button to be displayed"):
        # Wait for the button to be displayed
        button = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, "test5-button"))
        )
        assert button.is_displayed(), "The button is not displayed"

    with allure.step("Click the button"):
        # Click the button
        button.click()

    with allure.step("Verify the success message is displayed"):
        # Wait for the success message to appear
        success_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "test5-alert"))
        )
        assert success_message.is_displayed(), "The success message is not displayed"
        assert success_message.text == "You clicked a button!", "Success message text is incorrect"

    with allure.step("Verify the button is now disabled"):
        # Assert that the button is disabled
        assert not button.is_enabled(), "The button is not disabled"


@allure.title("Test 6: Verify cell value in a table grid")
@allure.description("This test navigates to Test 6 grid, retrieves the value of a specific cell and verifies it")
def test_6_table_cell_value(driver):

    with allure.step("Navigate to the home page"):
        driver.get(BASE_URL)

    with allure.step("Locate the Test 6 table"):
        # Locate the Test 6 table
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#test-6-div table"))
        )

    with allure.step("Define a method to retrieve cell value by coordinates"):
        def get_table_cell_value(table_element, row, col):
            """
            Retrieve the value of a cell in a table based on row and column indices.
            :param table_element: The table WebElement
            :param row: Row index (0-based)
            :param col: Column index (0-based)
            :return: Text value of the specified cell
            """
            cell_xpath = f".//tbody/tr[{row + 1}]/td[{col + 1}]"
            cell = table_element.find_element(By.XPATH, cell_xpath)
            return cell.text.strip()

    with allure.step("Retrieve the value of the cell at coordinates (2, 2)"):
        # Get the value of the cell at row 2, column 2 
        cell_value = get_table_cell_value(table, 2, 2)

    with allure.step("Assert the value of the cell is 'Ventosanzap'"):
        # Assert the value of the cell is "Ventosanzap"
        assert cell_value == "Ventosanzap", f"Expected 'Ventosanzap', but got '{cell_value}'"