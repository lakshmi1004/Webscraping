#%%
import unittest
import sys
sys.path.append("/home/blair/Desktop/Computer-Vision-Rock-Paper-Scissors/Webscraping/Lego")
from Legoscraper import Scraper
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
class TestScraper(unittest.TestCase):
    def setUp(self):
        self.new_scraper = Scraper("https://www.lego.com/en-gb")

    def test_lego_continue(self):
    
        self.new_scraper.lego_continue()

        with self.assertRaises(NoSuchElementException):
            self.new_scraper.driver.find_element_by_xpath(
                '//*[@id="root"]/div[5]/div/div/div[1]/div[1]/div/button')
        
    def test_necessary_cookies(self):
        self.new_scraper.lego_continue()
        self.new_scraper.necessary_cookies()

        with self.assertRaises(NoSuchElementException):
            self.new_scraper.driver.find_element_by_xpath(
                '//*[@id="root"]/div[5]/div/div/div[1]/div[1]/div/button')
            self.new_scraper.driver.find_element_by_xpath(
        '/html/body/div[6]/div/aside/div/div/div[3]/div[1]/button[1]')

    def test_shop(self):
        self.new_scraper.lego_continue()
        self.new_scraper.necessary_cookies()
        self.new_scraper.shop()


        with self.assertRaises(NoSuchElementException):
            self.new_scraper.driver.find_element_by_xpath(
                '//*[@id="root"]/div[5]/div/div/div[1]/div[1]/div/button')
            self.new_scraper.driver.find_element_by_xpath(
                '/html/body/div[6]/div/aside/div/div/div[3]/div[1]/button[1]')
            self.new_scraper.driver.find_element_by_xpath(
                '//*[@id="blt6e23fc5280e75abb_submenubutton"]/div')            
    def teardown(self):
        pass

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'],verbosity=2, exit=False)
# %%
