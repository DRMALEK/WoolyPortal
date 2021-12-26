import logging

from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from WoolyScraper import WoolyScraper
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
scraper = WoolyScraper(driver, session, "meta_data.json")
scraper.start_parsing()