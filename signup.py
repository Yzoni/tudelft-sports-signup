#!/usr/bin/python3

import argparse
import getpass
import logging

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def main(username, password, sport, timeout=10, headless=False):
    options = Options()
    if headless:
        options.headless = True
    driver = webdriver.Firefox(options=options)

    logging.info(f'Started signup for {sport}')

    try:
        # Login
        driver.get('https://sportsandculture.tudelft.nl/en/auth/connect_tudelft')
        username_field = driver.find_element_by_id('user_id')
        password_field = driver.find_element_by_id('password')
        login_button = driver.find_element_by_class_name('login')

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()

        # Wait until login completed
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )

        logging.info('Finished signing in to TU account')

        # Open timetable iframe directly
        driver.get('https://services.sc.tudelft.nl/?lang=en')
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, "fc-sticky"))
        )

        logging.info('Loaded timetable')

        # Click on sports box in schedule
        box = driver.find_element_by_xpath(f"//*[contains(text(), '{sport}')]")
        box.click()

        logging.info('Found the item you were looking for in the timetable')

        # Wait until sign-up modal is loaded
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, "content-page-modal"))
        )

        logging.info('Proceeding signup (1) ...')

        signup_button = driver.find_element_by_xpath(f"//*[contains(text(), 'Sign up')]")
        course_view_link = signup_button.get_attribute('href')
        driver.get(course_view_link)

        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "courseView"))
        )

        logging.info('Proceeding signup (2) ...')

        booking_button = driver.find_element_by_xpath("//input[@value='Bookings']")
        booking_button.click()

        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )

        logging.info('Successful signup confirmed!')

    except TimeoutException:
        logging.error(f'Failed to signup, timeout ({timeout}) exceeded')
    finally:
        driver.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('username', type=str,
                        help='TU Delft username')
    parser.add_argument('--password', type=str,
                        help='TU Delft password')
    parser.add_argument('--sport', type=str, required=True,
                        help='Room on calendar')
    parser.add_argument('--timeout', type=int, default=10,
                        help='How long too wait on page loads')
    parser.add_argument('--headless', action='store_true', default=False,
                        help='Spawn selenium headless')
    args = parser.parse_args()

    if not args.password:
        password = getpass.getpass('Password: ')
    else:
        password = args.password

    username = args.username

    main(username, password, args.sport, args.timeout, args.headless)
