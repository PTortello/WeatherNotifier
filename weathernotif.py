"""
weathernotif.py
Pedro Tortello - 08/2020
Temperature and time Win10 notifier
"""

# TODO:
#     - location selector
#     - user settings (interval, duration, forecast)
#     - forecast info
#     - icon change by climate


from win10toast import ToastNotifier
from bs4 import BeautifulSoup
from requests import get
import time


def temperature_scraper():
    """Returns location current temperature"""

    # CAUTION: Hard coded file name containing url address
    source = "sorocaba.dat"
    with open(source, 'r') as data:
        address = data.read()

    # Web scraping url address
    req = get(address).text
    soup = BeautifulSoup(req, 'lxml')

    # Searching current temperature
    match = soup.find('div', id='mainContent')
    match = match.find_all('span')
    match = match[7].text[1:3]

    return match + '\xb0C'


def win_notifier(temperature):
    """Shows notification with current temperature and time"""

    # CAUTION: Hard coded city name
    toaster = ToastNotifier()
    toaster.show_toast("Sorocaba", temperature + time.strftime(" - %H:%M"), threaded=True,
    icon_path='weather.ico', duration=5)


# Notifies every 15 minutes (900 seconds)
interval = 900
while True:
    temperature = temperature_scraper()
    win_notifier(temperature)
    time.sleep(interval)
