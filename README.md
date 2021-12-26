# WoolyPortal
A scraper for the wollplatz.de website using **Selenium**, **Beautifulsoup** and **Sqlalchemy**. The scraper takes as a input a meta file, that contains the information about the desired products and it automaticly search for them on the website and return their different properties:

1. Current Price
2. Composition
3. Needle Size

# Usage

### Requirements
    
1. Python = 3.0, Chrome browser = 96.0, Sqlite = 3.0
2. `pip install -r requirements.txt`

### How to run
Firstly, make sure that the `meta_data.json` file is availabe in the working directory, then you can simply run the scraper by typing: \
    `python main.py`
    
# Author
@DRMALEK
