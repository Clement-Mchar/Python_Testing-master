from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def test_user_journey():
    driver = webdriver.Chrome()

    driver.get("http://127.0.0.1:5000/")
    assert "Welcome to the GUDLFT Registration Portal" in driver.page_source

    email_input = driver.find_element(By.NAME, "email")
    email_input.send_keys("john@simplylift.co")
    email_input.send_keys(Keys.RETURN)
    time.sleep(2)
    assert "Welcome, john@simplylift.co" in driver.page_source

    driver.get("http://127.0.0.1:5000/book/Fall Classic/Simply Lift")
    assert "Booking for Fall Classic" in driver.page_source

    places_input = driver.find_element(By.NAME, "places")
    places_input.send_keys("1")
    driver.find_element(By.CSS_SELECTOR, "form button").click()
    time.sleep(2)
    assert "Great-booking complete !" in driver.page_source
    assert "You have booked 1 places to the Fall Classic competition !" in driver.page_source

    driver.get("http://127.0.0.1:5000/logout")
    time.sleep(2)
    assert "Welcome to the GUDLFT Registration Portal" in driver.page_source

    driver.quit()

if __name__ == "__main__":
    test_user_journey()
