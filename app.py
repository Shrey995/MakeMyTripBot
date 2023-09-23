from test import test_booking
import json
from flask import Flask, request, jsonify
import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

app = Flask(__name__)

def get_next_test_case_count():
    # You can implement this function based on your requirements,
    # for example, by checking existing folders or a database.
    # For now, let's assume a simple incrementing counter.
 return 1  # You can replace this with your implementation
@app.route("/flight-booking", methods=["POST"])
def flight_booking_route():
    try:
        inputs = request.get_json()
        
        # Get the next test case count from the test_booking module
        test_case_count = get_next_test_case_count()


        # Initialize WebDriver and other necessary resources
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.implicitly_wait(10)
        driver.maximize_window()
        
        # Create the folder name with zero-padding
        folder_name = f"test{test_case_count:02}_screenshots"
        test_dir = os.path.join("reports", folder_name)

        # Perform flight booking steps here using 'driver' and 'inputs'
        test = test_booking.TestFlightBooking(driver,test_case_count, inputs,test_dir)
        result = test.test_flight_booking()
        
        return result

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)
