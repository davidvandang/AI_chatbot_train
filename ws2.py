from datetime import datetime, timedelta
from time import sleep
from bs4 import BeautifulSoup
import requests
from selenium import webdriver


class FindTicket:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.openURL()

    def openURL(self):
        # Find website
        URL = 'https://www.greateranglia.co.uk/'
        self.driver.get(URL)
        sleep(2)
        self.allow_cookies()

    def allow_cookies(self):
        # Allow cookies
        click_allow_cookies = '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]'
        self.driver.find_element_by_xpath(click_allow_cookies).click()
        sleep(2)
        self.buy_ticket()

    def buy_ticket(self):
        # Buy tickets
        click_buy_tickets = '//*[@id="tbt-buy-tickets"]'
        self.driver.find_element_by_xpath(click_buy_tickets).click()
        sleep(2)
        self.more_option()

    def more_option(self):
        # More options
        more_options = '//*[@id="act-a"]/i[1]'
        self.driver.find_element_by_xpath(more_options).click()
        sleep(2)

    def input_from_train(self, from_train):
        # To train
        to_train_xpath = '//*[@id="from-buytlbf"]'
        to_train_element = self.driver.find_element_by_xpath(to_train_xpath)
        to_train_element.send_keys(from_train)
        sleep(2)

        # Selection of dropdown menu
        match = False
        station_dropDown_xpath = '//*[@id="listbox_from-buytlbf_container"]'
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
            first_option_xpath = '//*[@id="listbox_from-buytlbf_container"]/li[1]'
            self.driver.find_element_by_xpath(first_option_xpath).click()
            print("first option chosen")
            sleep(2)

        # Ask user to try another train

    def input_to_train(self, to_train):
        # To train
        to_train_xpath = '//*[@id="totlbf"]'
        to_train_element = self.driver.find_element_by_xpath(to_train_xpath)
        to_train_element.send_keys(to_train)
        sleep(2)

        # Selection of dropdown menu
        match = False
        station_dropDown_xpath = '//*[@id="listbox_totlbf_container"]'
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
            first_option_xpath = '//*[@id="listbox_totlbf_container"]/li[1]'
            self.driver.find_element_by_xpath(first_option_xpath).click()
            print("first option chosen")
            sleep(2)



    def ticket_type_selection(self, ticket_type):
        # single ticket
        if ticket_type == 'single':
            single_ticket = '//*[@id="chip-single"]'
            self.driver.find_element_by_xpath(single_ticket).click()
            sleep(2)

        # return ticket
        elif ticket_type == 'return':
            return_ticket = '//*[@id="chip-return"]'
            self.driver.find_element_by_xpath(return_ticket).click()
            sleep(2)

    # Round time to nearest 15 minute interval
    def round_time(self, time):
        delta = timedelta(minutes=15)
        rounded_time = datetime.min + round((time - datetime.min) / delta) * delta
        return rounded_time.strftime("%H:%M")

    def from_train_day_time(self, from_day, from_time):
        # Click on outbound
        outbound_xpath = '//*[@id="tls-bkf-tlbf"]/div[3]/div[1]/div[2]/div/div/div[1]/div/a'
        outbound = self.driver.find_element_by_xpath(outbound_xpath).click()
        sleep(6)

        date = datetime.strptime(from_day, '%Y-%m-%d')
        formatted_date = date.strftime('%a %b %d %Y')

        # Search calendar id
        for d in range(12):
            month = self.driver.find_element_by_xpath().text



        calendar_xpath = '//*[@id="dp1683120358003"]/div/div[1]/table/tbody/tr/td/a'

        calendar = self.driver.find_element_by_xpath(calendar_xpath)

        for dateElement in calendar:
            dates = calendar.get_attribute("aria-label")
            if formatted_date in dates:
                dateElement.click
                break


        # Xpath for time list
        time_list_chosen_xpath = '//*[@id="out_time_modaltlbf_chosen"]/div/ul'
        time_list_chosen = self.driver.find_elements_by_xpath(time_list_chosen_xpath)
        time = datetime.strptime(from_time, "%H:%M")
        formatted_time = self.round_time(time)

        for eachTime in time_list_chosen:
            if formatted_time in eachTime.text:
                eachTime.click()
                break
        sleep(10)

        return








# def find_train_tickets(from_train, from_day, from_time, ticket_type, to_train, to_day=None, to_time=None):


# def test_from_train():
#     # Create an object of FindTicket class
#     find_ticket = FindTicket()
#
#     # Call the input_from_train method with a sample input
#     find_ticket.input_to_train('london')
#
#     # Sleep for some time to observe the results
#     sleep(10)
#
#     # Close the browser window
#     find_ticket.driver.quit()
#
#
# Run the test function
def test_from_train_day_time():
    # Create an instance of your class (replace YourClassName with the actual class name)
    find_ticket = FindTicket()

    # Call the function with some sample data
    from_day = "2023-05-20"
    from_time = "01:22"

    find_ticket.from_train_day_time(from_day, from_time)

    # Add some assertions or checks here if needed
    # For example, you can check if the correct date and time are selected on the website

#test_from_train_day_time()
find = FindTicket()
find.input_to_train("london bridge")
