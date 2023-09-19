import pytest
from src.makemytrip import MakeMyTrip

@pytest.fixture
def make_my_trip(driver):
    make_my_trip = MakeMyTrip(driver)
    make_my_trip.navigate_to_website()
    return make_my_trip

def test_flight_booking(make_my_trip):
    # Add your test steps here
    # Use make_my_trip object to interact with the MakeMyTrip website
    pass
