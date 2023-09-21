import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import os

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
            # Switch to the newly opened tab
            self.driver.switch_to.window(self.driver.window_handles[-1])



            self.driver.execute_script("window.scrollBy(0, 0);")
            while True:
                       try:
                         # Locate the button element with the target text
                         risk_trip_span = self.driver.find_element(By.XPATH, "//span[contains(text(), 'I will risk my trip')]")

                         # If found, break the loop
                         break
                       except NoSuchElementException:
                        # If not found, scroll down
                        self.driver.execute_script("window.scrollBy(0, 100);")

             # Click the button with the target text
            risk_trip_span.click()

            self.driver.execute_script("window.scrollBy(0, 0);")
            # Scroll down until you find the button with text "+ ADD NEW ADULT"
            target_text = "+ ADD NEW ADULT"
            while True:
                       try:
                         # Locate the button element with the target text
                         button = self.driver.find_element(By.XPATH, f"//button[text()='{target_text}']")

                         # If found, break the loop
                         break
                       except NoSuchElementException:
                        # If not found, scroll down
                        self.driver.execute_script("window.scrollBy(0, 100);")

             # Click the button with the target text
            button.click()


            # Scroll down to make the form elements visible
            self.driver.execute_script("window.scrollBy(0, 200);")

            # Find and fill the "Last Name" field
            last_name_field = self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Last Name"]')
            last_name_field.send_keys("Doe")

            # Find and fill the "First & Middle Name" field
            first_middle_name_field = self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="First & Middle Name"]')
            first_middle_name_field.send_keys("John Middle")
            your_gender = "male"  # Change this to "female" if needed

            # Find and select the gender radio button (choose either "male" or "female")

            if your_gender == "male":
                gender_radio = self.driver.find_element(By.CSS_SELECTOR, 'input[value="MALE"]')
            else:
                gender_radio = self.driver.find_element(By.CSS_SELECTOR, 'input[value="FEMALE"]')

            gender_radio.click()
            # Scroll down further if needed
            self.driver.execute_script("window.scrollBy(0, 200);")

            # Find and fill the "Mobile No" field
            mobile_field = self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Mobile No"]')
            mobile_field.send_keys("8369932133")

            # Find and fill the "Email" field
            email_field = self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Email"]')
            email_field.send_keys("johndoe@example.com")

            # Find and fill the "Your Pincode" field
            pincode_field = self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Your Pincode"]')
            pincode_field.clear()  # Clear any existing value
            pincode_field.send_keys("403512")


            # Click on the element with ID "dt_state_gst_info"
            # Locate the input element by ID
# Assuming 'state_input' is the element you want to double-click
            state_input = self.driver.find_element(By.ID, "dt_state_gst_info")

# Create an ActionChains object
            action_chains = ActionChains(self.driver)

# Double-click the element
            action_chains.double_click(state_input).perform()
            time.sleep(10)

            # Find the element with class "dropdownListWpr"
            dropdown_list = self.driver.find_element(By.XPATH, '//*[@class="dropdownListWpr"]')

             # Scroll the dropdown options until you find the right option
            desired_option_text = "Goa"  # Replace with the actual text of the option you want to select
            option_found = False

            while not option_found:
             # Locate all the options within the dropdown
             options = dropdown_list.find_elements(By.CLASS_NAME, "dropdownListWpr__liItem")

             # Check each option's text and click if it matches the desired text
             for option in options:
                  if desired_option_text in option.text:
                      option.click()
                      option_found = True
                      break

                   # If the desired option is not found, scroll the dropdown options
                  if not option_found:
                    self.driver.execute_script("arguments[0].scrollBy(0, 100);", dropdown_list)



            # Scroll down further if needed
            self.driver.execute_script("window.scrollBy(0, 200);")
            # Click the input element with ID "cb_gst_info"
            self.driver.execute_script("window.scrollBy(0, 0);")
            while True:
                       try:
                         # Locate the button element with the target text
                         risk_trip_span = self.driver.find_element(By.XPATH, "//p[contains(text(), 'Confirm and save billing details to your profile')]")

                         # If found, break the loop
                         break
                       except NoSuchElementException:
                        # If not found, scroll down
                        self.driver.execute_script("window.scrollBy(0, 100);")

             # Click the button with the target text
            risk_trip_span.click()

            # self.driver.execute_script("window.scrollBy(0, 0);")
            # while True:
            #            try:
            #              # Locate the button element with the target text
            #              risk_trip_span = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Adult 1')]")

            #              # If found, break the loop
            #              break
            #            except NoSuchElementException:
            #             # If not found, scroll down
            #             self.driver.execute_script("window.scrollBy(0, 100);")

            #  # Click the button with the target text
            # risk_trip_span.click()   

            self.driver.execute_script("window.scrollBy(0, 0);")
            while True:
                       try:
                         # Locate the button element with the target text
                         continue_button = self.driver.find_element(By.XPATH, '//button[text()="Continue"]')

                         # If found, break the loop
                         break
                       except NoSuchElementException:
                        # If not found, scroll down
                        self.driver.execute_script("window.scrollBy(0, 200);")
            
            continue_button.click()
            # Wait for the popup to appear
            popup_element = WebDriverWait(self.driver, 10).until(
             EC.presence_of_element_located((By.CSS_SELECTOR, '.commonOverlay'))
              )
    
            confirm_button = WebDriverWait(popup_element, 10).until(
              EC.element_to_be_clickable((By.XPATH, '//button[text()="Confirm"]'))
             )
            time.sleep(10)
            # Use JavaScript to prevent the default action (closing the window)
            self.driver.execute_script("arguments[0].addEventListener('click', function(e) { e.preventDefault(); }, false);", confirm_button)
            # Click the "Confirm" button
            confirm_button.click()
            # Get the handles of all open tabs/windows
            window_handles = self.driver.window_handles

            # Assuming the original tab is at index 0, switch back to it
            self.driver.switch_to.window(window_handles[0])
            time.sleep(300)
            self.take_screenshot("Search_Flight")
        except Exception as e:
            print(e)
            # self.fail(f"An error occurred during flight search: {str(e)}")

       
if __name__ == "__main__":
    unittest.main()
