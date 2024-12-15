from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, time
import re


class AppPillPositionValidator:
    def __init__(self, driver):
        """
        Initialize validator with Appium driver

        Parameters:
        driver: Appium WebDriver instance
        """
        self.driver = driver
        self.graph_bounds = None

    def get_graph_bounds(self, graph_element_id):
        """Get the graph container boundaries."""
        graph_element = self.driver.find_element(By.ID, graph_element_id)
        self.graph_bounds = graph_element.rect
        return self.graph_bounds

    def get_pill_position(self, pill_element_id):
        """
        Get the pill icon's position relative to the graph

        Returns:
        tuple: (x_coordinate, y_coordinate) relative to graph bounds
        """
        pill_element = self.driver.find_element(By.ID, pill_element_id)
        pill_location = pill_element.rect

        if not self.graph_bounds:
            raise ValueError(
                "Graph bounds not initialized. Call get_graph_bounds first."
            )

        # Calculate relative position
        relative_x = pill_location["x"] - self.graph_bounds["x"]
        relative_y = pill_location["y"] - self.graph_bounds["y"]

        return (relative_x, relative_y)

    def convert_position_to_time(self, x_position):
        """
        Convert x-position to time value

        Parameters:
        x_position: x-coordinate relative to graph

        Returns:
        time object representing the position
        """
        if not self.graph_bounds:
            raise ValueError("Graph bounds not initialized")

        # Calculate time based on position
        # Assuming graph shows 24 hours (00:00 to 23:59)
        time_in_hours = (x_position / self.graph_bounds["width"]) * 24

        # Convert to time object
        hours = int(time_in_hours)
        minutes = int((time_in_hours - hours) * 60)
        return time(hours, minutes)

    def validate_pill_position(
        self, pill_element_id, expected_time_str, tolerance_minutes=5
    ):
        """
        Validate if pill is in correct position

        Parameters:
        pill_element_id: ID of pill element in app
        expected_time_str: Expected time in format "HH:MM AM/PM"
        tolerance_minutes: Acceptable deviation in minutes

        Returns:
        tuple: (is_valid, message)
        """
        # Parse expected time
        expected_time = datetime.strptime(expected_time_str, "%I:%M %p").time()

        # Get actual pill position
        pill_position = self.get_pill_position(pill_element_id)
        actual_time = self.convert_position_to_time(pill_position[0])

        # Calculate time difference in minutes
        expected_minutes = expected_time.hour * 60 + expected_time.minute
        actual_minutes = actual_time.hour * 60 + actual_time.minute
        difference = abs(expected_minutes - actual_minutes)

        # Validate y-position (should be near top of graph)
        y_valid = (
            pill_position[1] <= self.graph_bounds["height"] * 0.15
        )  # Top 15% of graph

        # Check if position is valid within tolerance
        time_valid = difference <= tolerance_minutes
        is_valid = time_valid and y_valid

        message = f"""
        Time position: {"Valid" if time_valid else "Invalid"}
        Expected time: {expected_time_str}
        Actual time: {actual_time.strftime("%I:%M %p")}
        Difference: {difference} minutes
        Y-position: {"Valid" if y_valid else "Invalid"}
        """

        return is_valid, message


# Example usage
def setup_appium():
    """Set up Appium driver with desired capabilities."""
    desired_caps = {
        "platformName": "Android",  # or 'iOS'
        "automationName": "UiAutomator2",  # or 'XCUITest' for iOS
        "deviceName": "Your Device Name",
        "appPackage": "your.app.package",
        "appActivity": "your.app.MainActivity",
    }
    return webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)


def validate_app_pill_position():
    try:
        # Initialize Appium
        driver = setup_appium()
        validator = AppPillPositionValidator(driver)

        # Get graph boundaries
        validator.get_graph_bounds("graph_container_id")

        # Validate pill position
        is_valid, message = validator.validate_pill_position(
            pill_element_id="pill_icon_id",
            expected_time_str="8:00 PM",
            tolerance_minutes=5,
        )

        print(f"Validation result: {'Valid' if is_valid else 'Invalid'}")
        print(message)

    finally:
        driver.quit()


if __name__ == "__main__":
    validate_app_pill_position()
