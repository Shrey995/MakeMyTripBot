import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

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

            # self.take_screenshot("Top_Left_of_imageSlideContainer_Clicked")
        except Exception as e:
            self.fail(f"An error occurred while clicking on the top-left part of imageSlideContainer: {str(e)}")

    def remove_third_popup(self):
        try:
            # Scroll to the imageSlideContainer element
            image_slide_container = self.driver.find_element(By.CLASS_NAME, "overlayBg")
            self.driver.execute_script("arguments[0].scrollIntoView();", image_slide_container)

            # Click on the top-left part of the imageSlideContainer
            self.driver.execute_script("arguments[0].click();", image_slide_container)

            # self.take_screenshot("Top_Left_of_imageSlideContainer_Clicked")
        except Exception as e:
            self.fail(f"An error occurred while clicking on the top-left part of imageSlideContainer: {str(e)}")

    def take_screenshot(self, name):
        # Create a directory for this class's screenshots
        class_dir = f"reports/{self.__class__.__name__}"
        os.makedirs(class_dir, exist_ok=True)
        self.driver.save_screenshot(f"{class_dir}/{name}.png")

    def select_date(self, target_date):
        try:
            date_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[aria-label^="Sun "]'))
            )
            for date_element in date_elements:
                date_label = date_element.get_attribute("aria-label")
                if date_label == target_date:
                    # Click on the date element to select it
                    date_element.click()
                    return True
        except Exception as e:
            self.fail(f"An error occurred while selecting the date: {str(e)}")

        return False  # Date not found

    def select_departure_and_return_dates(self, departure_date, return_date):
        try:
            # Click the departure date input
            # departure_input = WebDriverWait(self.driver, 10).until(
            #     EC.element_to_be_clickable((By.ID, "departure")))
            # departure_input.click()

            # Select the departure date
            if not self.select_date(departure_date):
                self.fail(f"Departure date '{departure_date}' not found in the date picker")

            # Click the return date input
            # departure_input = WebDriverWait(self.driver, 10).until(
            #     EC.element_to_be_clickable((By.ID, "departure")))
            # departure_input.click()

            # # Select the return date
            # if not self.select_date(return_date):
            #     self.fail(f"Return date '{return_date}' not found in the date picker")

        except Exception as e:
            self.fail(f"An error occurred while selecting departure and return dates: {str(e)}")

    def test_flight_booking(self):
        # Navigate to the flight booking page
        self.driver.get("https://www.makemytrip.com/")

        # Remove the first popup
        self.remove_first_popup()

        # Remove the second popup
        self.remove_second_popup()

        # Search for a flight with a date range, origin, and destination
        try:
            # Select origin from the combo box
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

            # Select destination from the combo box
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

            # Select departure and return dates
            self.select_departure_and_return_dates("Sun Oct 08 2023", "Sun Oct 15 2023")

            # Scroll to the "Search" button
            search_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[text()='Search']"))
            )
            actions = ActionChains(self.driver)
            actions.move_to_element(search_button).perform()

            # Click the "Search" button
            search_button.click()
            time.sleep(20)
                    # Remove the second popup
            self.remove_third_popup()
            self.driver.execute_script("window.scrollBy(0, 200);")
            # Locate and click the button by its ID
            view_button = WebDriverWait(self.driver, 10).until(
              EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'appendRight8')]"))
             )
            view_button.click()
            self.driver.execute_script("window.scrollBy(0, 200);")
            book_button = WebDriverWait(self.driver, 10).until(
              EC.element_to_be_clickable((By.XPATH, "//button[text()='Book Now']"))
             )
            book_button.click()
            time.sleep(300)
            # self.take_screenshot("Search_Flight")
        except Exception as e:
            self.fail(f"An error occurred during flight search: {str(e)}")

        # Select the first flight
        try:
            first_flight = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "(//li[@class='flight_item'])[1]"))
            )
            first_flight.click()
            # self.take_screenshot("Select_Flight")

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

        # Reach the Payment screen
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
