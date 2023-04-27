import requests
from bs4 import BeautifulSoup as bs

def get_request(url):
    r = requests.get(url)
    return r.text


def post_request(url):
    r = requests.get(url)
    return r.text


def cheapest_ticket(arrival_train, return_train, arrival_time, return_time,
                    arrival_day, return_day):
    # Find website
    URL = "https://www.greateranglia.co.uk/"
    # Get request of website

    # Search Ticket
    # Input search details
    # Search with details
    # Get details of found tickets

    return
