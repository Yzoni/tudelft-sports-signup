import argparse
import getpass
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait


def main(username, password, room, slot):
    driver = webdriver.Firefox()

    # Login
    driver.get('https://sportsandculture.tudelft.nl/en/auth/connect_tudelft')
    username_field = driver.find_element_by_id('user_id')
    password_field = driver.find_element_by_id('password')
    login_button = driver.find_element_by_class_name('login')

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()

    # Wait until login completed
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
    )

    # TROUGH CALENDAR
    # # Switch to DOJO calendar
    driver.get('https://sportsandculture.tudelft.nl/en/bookings/view/new')
    time.sleep(5)  # Wait until page stupid JS is loaded
    room_selector = Select(driver.find_element_by_id('iResourceID'))
    room_selector.select_by_visible_text('{}'.format(room))

    # Wait until elements in calendar are loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "fc-event"))
    )

    # Select slot
    slot = driver.find_element_by_xpath('//*[contains(text(), "{}")]'.format(slot))
    parent = slot.find_element_by_xpath('..')
    driver.execute_script("arguments[0].scrollIntoView(true);", parent)
    ActionChains(driver).move_to_element(parent).click().perform()

    # Wait for popup
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "addBookingButton"))
    )

    # Finalize booking
    booking_button = driver.find_element_by_id('addBookingButton')
    driver.execute_script("arguments[0].click();", booking_button)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('username', type=str,
                        help='TU Delft username')
    parser.add_argument('--password', type=str,
                        help='TU Delft password')
    parser.add_argument('--room', type=str, default='DOJO',
                        help='Room on calendar')
    parser.add_argument('--slot', type=str, default='Krav Maga',
                        help='String slot can be identified with')
    args = parser.parse_args()

    if not args.password:
        password = getpass.getpass('Password: ')
    else:
        password = args.password

    username = args.username

    room = args.room
    slot = args.slot

    main(username, password, room, slot)
