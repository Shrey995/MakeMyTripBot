import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.support.ui import Select

class TestFlightBooking(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def remove_first_popup(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "webklipper-publisher-widget-container-notification-frame"))
            )
            self.driver.switch_to.frame("webklipper-publisher-widget-container-notification-frame")
            close_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@class='close']"))
            )
            close_button.click()
            self.driver.switch_to.default_content()
            self.take_screenshot("Remove_First_Popup")
        except Exception as e:
            pass

    def remove_second_popup(self):
        try:
            # Scroll to the imageSlideContainer element
            image_slide_container = self.driver.find_element(By.CLASS_NAME, "imageSlideContainer")
            self.driver.execute_script("arguments[0].scrollIntoView();", image_slide_container)

            # Click on the top-left part of the imageSlideContainer
            self.driver.execute_script("arguments[0].click();", image_slide_container)

            self.take_screenshot("Top_Left_of_imageSlideContainer_Clicked")
        except Exception as e:
            self.fail(f"An error occurred while clicking on the top-left part of imageSlideContainer: {str(e)}")

    def take_screenshot(self, name):
        self.driver.save_screenshot(f"reports/{self.__class__.__name__}/{name}.png")

    def test_flight_booking(self):
        # Navigate to the flight booking page
        self.driver.get("https://www.makemytrip.com/")

        # Remove the first popup
        self.remove_first_popup()

        # Remove the second popup
        self.remove_second_popup()

        # Search for a single flight by date, origin, and destination
        try:
            # Select origin from the combo box
            # Send keys to the origin input field (example: Mumbai)
            origin_input = WebDriverWait(self.driver, 10).until(
              EC.element_to_be_clickable((By.ID, "fromCity"))
            )
            origin_input.send_keys("Mumbai")
            time.sleep(3)

            # Wait for the autosuggestion to appear and select the first option
            origin_suggestion = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "react-autowhatever-1-section-0-item-0"))
            )
            origin_suggestion.click()

            # Send keys to the destination input field (example: Bengaluru)
            destination_input = WebDriverWait(self.driver, 10).until(
             EC.element_to_be_clickable((By.ID, "toCity"))
            )
            destination_input.send_keys("Bengaluru")
            time.sleep(3)

            # Wait for the autosuggestion to appear and select the first option
            destination_suggestion = WebDriverWait(self.driver, 10).until(
             EC.element_to_be_clickable((By.ID, "react-autowhatever-1-section-0-item-0"))
            )
            destination_suggestion.click()

            # Clear the date input field
            date_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "departure"))
            )
            date_input.clear()

            # Select the desired date from the date picker
            date_select = Select(self.driver.find_element(By.ID, "departure"))
            date_select.select_by_visible_text("20")

            # search_button = WebDriverWait(self.driver, 10).until(
            #     EC.element_to_be_clickable((By.CSS_SELECTOR, ".widgetSearchBtn"))
            # )
            # search_button.click()
            time.sleep(10)
            self.take_screenshot("Search_Flight")
        except Exception as e:
            self.fail(f"An error occurred during flight search: {str(e)}")

        # Select the first flight
        try:
            first_flight = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "(//li[@class='flight_item'])[1]"))
            )
            first_flight.click()
            self.take_screenshot("Select_Flight")
        except Exception as e:
            self.fail(f"An error occurred while selecting the first flight: {str(e)}")

        # Skip Seats & Food (Ancillaries)
        try:
            skip_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".skip_button"))
            )
            skip_button.click()
            self.take_screenshot("Skip_Ancillaries")
        except Exception as e:
            self.fail(f"An error occurred while skipping ancillaries: {str(e)}")

        # Fill checkout information
        try:
            passenger_name = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "name"))
            )
            passenger_name.send_keys("John Doe")

            email = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "email"))
            )
            email.send_keys("johndoe@example.com")

            phone = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "phone"))
            )
            phone.send_keys("1234567890")

            self.take_screenshot("Fill_Checkout_Info")
        except Exception as e:
            self.fail(f"An error occurred while filling checkout information: {str(e)}")

        # Reach till Payment screen
        try:
            proceed_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btnReviewContinue"))
            )
            proceed_button.click()
            self.take_screenshot("Payment_Screen")
        except Exception as e:
            self.fail(f"An error occurred while proceeding to the payment screen: {str(e)}")

if __name__ == "__main__":
    unittest.main()
