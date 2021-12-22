from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from helpers import read_meta_data
from selenium import webdriver

class WoolyScraper():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        self.data = read_meta_data("meta_data.json")
        self.url = "https://www.wollplatz.de/wolle/herstellers"  # start url

    def __del__(self):
        self.driver.close()

    def get_page(self, url):
        self.driver.get(url)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        return soup

    def start_parsing(self):
        soup = self.get_page(self.url)
        # This is function parse the brands page to find the url for each qurey brand provided in the data object
        PRODUCT_BRAND_SELECTOR = ".productlistholder"
        for brand in soup.select(PRODUCT_BRAND_SELECTOR):
            PRODUCT_BRAND_TITLE_SELECTOR = ".productlist-imgholder"
            for product_brand in brand.select(PRODUCT_BRAND_TITLE_SELECTOR):
                brand_title = product_brand["title"]
                brand_url = product_brand["href"]
                for query_brand_title in self.data.keys():
                    if brand_title == query_brand_title:
                        for query_name in self.data[brand_title]:
                            self.url = brand_url
                            self.url = self.url + "?page=" + str(1)
                            product_url = self.parse_products_page(self.get_page(self.url), query_name)
                            if product_url:
                                self.url = product_url
                                product_details = self.parse_element_page(self.get_page(self.url))
                                print(product_details)
                            else:
                                print("Element not found " + query_name)


    def parse_products_page(self, response, query_name):
        PRODUCT_SELECTOR = ".productlistholder"
        for product in response.select(PRODUCT_SELECTOR):
            PRODUCT_TITLE_SELECTOR = ".productlist-imgholder"
            for product_title in product.select(PRODUCT_TITLE_SELECTOR):
                product_brand = product_title["title"].split(' ', 1)[0]  # extract the brand name from the product name
                product_name = product_title["title"].split(' ', 1)[1]  # drop the brand name from the product name
                product_url = product_title["href"]
                if product_name == query_name:
                    return product_url

        # In case that the element that we are searching for is not found
        NEXT_BUTTON_SELECTOR = "li[class=paging-volgende]"
        if response.select_one(NEXT_BUTTON_SELECTOR):
            current_page = int(self.url[-1])
            self.url = self.url[:-1] + str(current_page + 1)  # Go to the next page
            return self.parse_products_page(self.get_page(self.url), query_name)

    def parse_element_page(self, response):
        PRODUCT_PRICE_SELECTOR = "#ContentPlaceHolder1_upPricePanel > span.product-price > span.product-price-amount"
        PRODUCT_COMPOSITION_SELECTOR = "#pdetailTableSpecs > table > tbody > tr:nth-child(4) > td:nth-child(2)"
        PRODUCT_NEEDLE_SIZE_SELECTOR = "#pdetailTableSpecs > table > tbody > tr:nth-child(5) > td:nth-child(2)"

        product_price = response.select_one(PRODUCT_PRICE_SELECTOR).text \
            if response.select(PRODUCT_PRICE_SELECTOR) else ""
        product_composition = response.select_one(PRODUCT_COMPOSITION_SELECTOR).text \
            if response.select(PRODUCT_COMPOSITION_SELECTOR) else ""
        product_needle_size = response.select_one(PRODUCT_NEEDLE_SIZE_SELECTOR).text \
            if response.select(PRODUCT_NEEDLE_SIZE_SELECTOR) else ""

        return {
            "price": product_price,
            "composition": product_composition,
            "needle_size": product_needle_size
        }


scraper = WoolyScraper()
scraper.start_parsing()
