from datetime import datetime, timedelta
from time import sleep
from bs4 import BeautifulSoup
import requests
from selenium import webdriver


URL = 'https://www.buytickets.greateranglia.co.uk/book/results?origin=8c369975256e3aa119e38f1c02da8192&destination=2144c4ddc11461cf9b03af198933e8df&outwardDate=2023-05-11T06%3A00%3A00&outwardDateType=departAfter&journeySearchType=return&passengers%5B%5D=1993-05-03&directSearch=false&inwardDate=2023-05-13T06%3A00%3A00&inwardDateType=departAfter&selectedOutward=%2F%2FJeOEpjXxs%3D%3A49IZGBXvksA%3D&selectedInward=NUbxbzhbV34%3D%3AOXpK%2Bq80Nx4%3D'
# Initialize a new Selenium webdriver instance
driver = webdriver.Chrome()

# Load the URL in the browser
driver.get(URL)
sleep(10)
# Get the page source and parse it with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find all elements with the specified class
price_outbound = soup.find_all("div", {"class": "_1q2fjk2"})
duration_outbound = soup.find_all("span", {"aria-label": ""})

for price in price_outbound:
    print(price.text.strip())
