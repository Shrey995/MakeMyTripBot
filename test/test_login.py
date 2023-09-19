import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

class TestLoginWithSecondGoogleAccount(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_login_with_second_google_account(self):
        self.driver.get("https://www.makemytrip.com/")

        # Switch to the iframe containing the notification close button
        try:
            WebDriverWait(self.driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, "webklipper-publisher-widget-container-notification-frame"))
            )
            
            # Find and close the notification inside the iframe
            notification_close_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@class='close']"))
            )
            notification_close_button.click()
            
            # Switch back to the default content
            self.driver.switch_to.default_content()
        except Exception as e:
            self.fail(f"An error occurred: {str(e)}")  # Fail the test if there's an exception

        # Switch to your iframe by finding it using the "#document" identifier
        try:
            # iframe = WebDriverWait(self.driver, 10).until(
            #     EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@name='#document']"))
            # )

            # Find the element with class "g_id_signin" and click it
            element_to_click = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "g_id_signin"))
            )
            element_to_click.click()
            
            # Now the Google login page should automatically open in a new window/tab
            # Switch to the newly opened window/tab
            self.driver.switch_to.window(self.driver.window_handles[-1])
            
            # Read the credentials from input.txt
            with open("inputs/input.txt", "r") as file:
                credentials = json.load(file)
            
            # Find and fill the email field
            email_field = self.driver.find_element(By.ID, "identifierId")
            email_field.send_keys(credentials["username"])
            
            # Click the "Next" button
            next_button = self.driver.find_element(By.ID, "identifierNext")
            next_button.click()
            
            # Wait for the password field to appear
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "Passwd"))
            )
            
            # Fill the password field with the app password
            password_field.send_keys(credentials["password"])
            
            # Click the "Next" button to login
            next_button = self.driver.find_element(By.ID, "passwordNext")
            next_button.click()

            # Optional: Add assertions or further test steps after logging in
            time.sleep(10)  # Adjust sleep time for further actions

            # Switch back to the original window/tab
            self.driver.switch_to.window(self.driver.window_handles[0])
        except Exception as e:
            self.fail(f"An error occurred while logging in: {str(e)}")  # Fail the test if there's an exception

if __name__ == "__main__":
    unittest.main()
