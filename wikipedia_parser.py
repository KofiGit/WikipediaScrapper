from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class WikipediaParser:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))     # Driver what we will use
        self.init_page = 'https://cs.wikipedia.org/wiki/Hlavn%C3%AD_strana'
        self.already_looked_up = []
        self.go_to_initPage()

    def go_to_initPage(self):
        self.driver.get(self.init_page)

    def read_page(self):
        content = self.driver.page_source
        soup = BeautifulSoup(content, "html.parser")
        return soup

    def is_wikipedia_page(self):
        # correct wikipedia page contains mw-content-text where search result or paragraphs are stored
        return True if len(self.driver.find_elements(By.ID, 'mw-content-text')) > 0 else False

    def get_page_type(self):
        # decide what parsing function will be used
        return 'Article' if len(self.driver.find_elements(By.CLASS_NAME, 'searchresults')) == 0 else 'Search'

    def search_site(self, keyword):
        search_input = self.driver.find_element(By.ID, 'searchInput')
        search_input.send_keys(keyword)
        search_input.send_keys(Keys.RETURN)
        self.already_looked_up.append(keyword)

    def end_driver(self):
        self.driver.quit()
