import requests
from time import sleep
from selenium import webdriver


def find_train_tickets(from_train,from_day,from_time,ticket_type,to_train,to_day = None,to_time= None):
    #Find website
    driver = webdriver.Chrome()
    URL = 'https://www.greateranglia.co.uk/'
    driver.get(URL)
    sleep(2)
    # Allow cookies
    click_allow_cookies = '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]'
    driver.find_element_by_xpath(click_allow_cookies).click()

    sleep(2)

    # Buy tickets
    click_buy_tickets = '//*[@id="tbt-buy-tickets"]'
    driver.find_element_by_xpath(click_buy_tickets).click()

    sleep(2)
    # More options
    more_options = '//*[@id="act-a"]/i[1]'
    driver.find_element_by_xpath(more_options).click()
    sleep(2)

    # From train
    from_train_xpath = '//*[@id="from-buytlbf"]'
    from_train = driver.find_element_by_xpath(from_train_xpath)
    from_train.send_keys(from_train)
    sleep(2)

    # Click on first option
    first_option_xpath = '//*[@id="listbox_from-buytlbf_container"]/li[1]'
    driver.find_element_by_xpath(first_option_xpath).click()

    sleep(2)
    # To train
    to_train_xpath = '//*[@id="totlbf"]'
    to_train = driver.find_element_by_xpath(to_train_xpath)
    to_train.send_keys(to_train)
    sleep(2)

    # Click on first option
    first_option_xpath = '//*[@id="listbox_totlbf_container"]/li[1]'
    driver.find_element_by_xpath(first_option_xpath).click()

    # single ticket
    if ticket_type == 'single':
        single_ticket = '//*[@id="chip-single"]'
        driver.find_element_by_xpath(single_ticket).click()
        sleep(2)

    # return ticket
    elif ticket_type == 'return':
        return_ticket = '//*[@id="chip-return"]'
        driver.find_element_by_xpath(return_ticket).click()
        sleep(2)




#


# def cheapest_ticket(arrival_train, return_train, arrival_time, return_time,
#                     arrival_day, return_day):
#     # Buy Ticket Nav
#
#     # Input search details
#     # Search with details
#     # Get details of found tickets
#
#     return
#
# def get_request(url):
#     r = requests.get(url)
#     return r.text
#
#
# def post_request(url):
#     r = requests.get(url)
#     return r.text
