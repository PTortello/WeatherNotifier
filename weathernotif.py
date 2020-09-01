"""
weathernotif.py
Pedro Tortello - 08/2020
Temperature and time Win10 notifier
"""

# TODO:
#     - user settings (interval, duration, forecast)
#     - forecast info
#     - icon change by climate


from win10toast import ToastNotifier
from bs4 import BeautifulSoup
from requests import get
import time


def temperature_scraper(cityName):
    """Returns location current temperature"""

    # Opens .DAT file containing address
    source = cityName + ".dat"
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


def win_notifier(cityName, temperature):
    """Shows notification with current temperature and time"""

    toaster = ToastNotifier()
    toaster.show_toast(cityName.capitalize(),
        temperature + time.strftime(" - %H:%M"),
        threaded=True, icon_path='weather.ico', duration=5)


# User input
cityName = input("Location name: ").lower()
interval = int(input("Time interval between alerts [minutes]: ")) * 60
print("Running...")

# Notifies every 15 minutes (900 seconds)
# interval = 900
while True:
    temperature = temperature_scraper(cityName)
    win_notifier(cityName, temperature)
    time.sleep(interval)
