from datetime import datetime, timedelta
from time import sleep
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup
import requests
from selenium import webdriver


class FindTicket:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.openURL()

    def openURL(self):
        # Find website
        URL = 'https://www.nationalrail.co.uk/'
        self.driver.get(URL)
        sleep(2)
        self.allow_cookies()

    def allow_cookies(self):
        # Allow cookies
        click_allow_cookies = '//*[@id="onetrust-accept-btn-handler"]'
        self.driver.find_element_by_xpath(click_allow_cookies).click()
        sleep(2)
    def input_from_train(self, from_train):
        # To train
        to_train_xpath = '//*[@id="txtFrom"]'
        to_train_element = self.driver.find_element_by_xpath(to_train_xpath)
        to_train_element.send_keys(from_train)
        sleep(2)

        # Selection of dropdown menu
        match = False
        station_dropDown_xpath = '//*[@id="p2"]'
        station_dropDown = self.driver.find_elements_by_xpath(station_dropDown_xpath)

        # Match with exact train
        for eachStation in station_dropDown:
            if from_train.lower() == eachStation.text.strip().lower():
                eachStation.click()
                match = True
                print("match")
                break

        # Choose first choice
        if not match:
            first_option_xpath = '//*[@id="p2"]/li[1]'
            self.driver.find_element_by_xpath(first_option_xpath).click()
            print("first option chosen")
            sleep(2)

        # Ask user to try another train
    def input_to_train(self, to_train):
        # To train
        to_train_xpath = '//*[@id="txtTo"]'
        to_train_element = self.driver.find_element_by_xpath(to_train_xpath)
        to_train_element.send_keys(to_train)
        sleep(2)

        # Selection of dropdown menu
        match = False
        station_dropDown_xpath = '//*[@id="p2"]'
        station_dropDown = self.driver.find_elements_by_xpath(station_dropDown_xpath)

        # Match with exact train
        for eachStation in station_dropDown:
            if to_train.lower() == eachStation.text.strip().lower():
                eachStation.click()
                match = True
                print("match")
                break

        # Choose first choice
        if not match:
            first_option_xpath = '//*[@id="p2"]/li[1]'
            self.driver.find_element_by_xpath(first_option_xpath).click()
            print("first option chosen")
            sleep(2)

    def round_time(self, time):
        delta = timedelta(minutes=15)
        rounded_time = datetime.min + round((time - datetime.min) / delta) * delta
        return rounded_time.strftime("%H:%M")

    def month_to_table(self, month):
        # Get the current month number (1-12)
        current_month = datetime.now().month

        # Calculate the difference between the current month and the input month
        month_diff = (month - current_month) % 12  # Use modulus to handle year rollover

        # Convert the month difference to a table number (1-4)
        table_num = month_diff + 1

        return table_num
    def from_train_day_time(self, from_day):

        # Click on calendar
        calender_xpath = '//*[@id="jp-out"]/div/span[1]/a'
        calender_element = self.driver.find_element_by_xpath(calender_xpath).click()

        # Change format of date
        year, month, day = map(int, from_day.split('-'))

        # Convert the month to a table number
        table_num = self.month_to_table(month)

        # xpath of the current + 3 months tables
        tables_xpath = '//*[@id="dp"]/div/table[{table_num}]'

        # Try to find the table
        tables = self.driver.find_element_by_xpath(tables_xpath)

        while True:
            # If table class is not 'hidden' then find day
            if 'hidden' not in tables.get_attribute('class'):
                # If the table is visible, select the date
                # Find the tbody within the table
                tbody = tables.find_element_by_xpath(f'//*[@id="dp"]/div/table[{table_num}]/tbody')
                self.driver.find_element_by_link_text(day).click
                break
            else:
                for _ in range(table_num - 1):
                    next_button_xpath = '//*[@id="dp"]/img[2]'
                    next_button_element = self.driver.find_element_by_xpath(next_button_xpath).click()
                    next_button_element.click()
                    sleep(2)
                self.driver.find_element_by_link_text(day).click
                break

ticket = FindTicket()
ticket.from_train_day_time("24-05-2023")

# Xpath
# for time list
#     time_list_chosen_xpath = '//*[@id="out_time_modaltlbf_chosen"]/div/ul'
#     time_list_chosen = self.driver.find_elements_by_xpath(time_list_chosen_xpath)
#     time = datetime.strptime(from_time, "%H:%M")
#     formatted_time = self.round_time(time)
#
#     for eachTime in time_list_chosen:
#         if formatted_time in eachTime.text:
#             eachTime.click()
#             break
#     sleep(10)