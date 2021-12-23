import logging

from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from scraper_selenium import WoolyScraper
from database.base import Base, engine, Session

# Initialize the driver
print("Initializing the chrome driver ...")
chrome_options = Options()
chrome_options.add_argument('headless')
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) # Disable logging
driver = webdriver.Chrome(ChromeDriverManager(log_level=logging.ERROR).install(), options=chrome_options)

# Initialize the database tables and create a new connection
print("Initializing the database  ...")
Base.metadata.create_all(engine)
session = Session()

# Start Scraping !
print("Start scrapping ...")
scraper = WoolyScraper("https://www.wollplatz.de/wolle/herstellers", driver, session)
scraper.start_parsing()

#TODOS
# 1- Add tests
# 3- Add logging system
# 4- Update the readmefile
# 5- Add tests
# 6- Add comments to functions