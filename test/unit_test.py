import unittest
import Legoscraper
from selenium.webdriver.common.by import By

class Test_Legoscraper(unittest.Testcase):
    def setup(self):
        self.bot = Legoscraper.Scraper('Minions')
    #def test_accept_cookies(self):
        #self.bot.accept_cookies('//*[@id="root"]/div[5]/div/div/div[1]/div[1]/div/button')
        #self.bot.driver.find_element(By.XPATH,'/html/body/div[6]/div/aside/div')
        
    def teardown(self):
        pass

if __name__ == '__main__':
    unittest.main()

