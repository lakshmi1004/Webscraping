from crypt import methods
import time
import pandas as pd
from pandas import DataFrame
import os
import requests
from bs4 import BeautifulSoup
import uuid
from uuid import UUID
import json
from dataclasses import dataclass
from logging import exception
from typing import Container, List
from typing_extensions import Self
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException #used to debug the program
from webdriver_manager.chrome import ChromeDriverManager


class Scraper():
    """This class is to scarpe the Lego Website"""

    def __init__(self, url:str = 'https://www.lego.com/en-gb')-> None:

        """ Initailising the Lego Website address"""
        self.driver = Chrome(ChromeDriverManager().install())
        self.driver.get(url)
        self.driver.maximize_window()
              
    def lego_continue(self)-> None:
        """This function is created to click the cookie button in the Webpage"""
        xpath = '//*[@id="root"]/div[5]/div/div/div[1]/div[1]/div/button'
        try:
            time.sleep(2)
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.find_element(By.XPATH, xpath).click()
        except TimeoutException:
            print('no elements found')

    def necessary_cookies(self)-> None:
        """This method is meant to click the necessary cookies"""
        xpath = '//button[contains(@class,"Button__Base-sc-1jdmsyi-0 eCVPKR")]'
        try:
            #time.sleep(2)
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.find_element(By.XPATH,xpath).click()
        except TimeoutException:
            print('no elements found')

    def shop(self)-> None:
        """This method is used to click the shop menu"""
        xpath ='//*[@id="blt51f52bea34c3fb01_menubutton"]'
        try:
            time.sleep(2)
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.find_element(By.XPATH,xpath).click()
        except TimeoutException:
                print('no elements found')

    
   
     
    def sets_by_theme(self):
        """This method is used to click Theme menu"""
        xpath = '//*[@id="blt6e23fc5280e75abb_submenubutton"]/div'
        try:
           time.sleep(2)
           WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, xpath)))
           self.driver.find_element(By.XPATH,xpath).click()
        except TimeoutException:
           print('no elements found')

    def _Theme_container(self)->str:
        self.container = self.driver.find_elements(
            By.XPATH,'//div[@class="SubMenustyles__ChildrenMenu-lbil4s-6 hsBVqy"]//following-sibling::div')
        print(self.container)

    def _Theme_extract_href(self)-> dict:
        
        self.Theme_href = []
        self.Theme_dict ={'Lego_theme_link':[],'Theme_name': []}
        for theme_link in self.container[0::]:
            self.Theme_name = theme_link.find_element(By.TAG_NAME,'a').get_attribute('data-analytics-title')
            self.Theme_dict['Theme_name'].append(self.Theme_name)
            self.Lego_theme_link = theme_link.find_element(By.TAG_NAME,'a').get_attribute('href')
            self.Theme_dict['Lego_theme_link'].append(self.Lego_theme_link)
            self.Theme_href.append(theme_link.find_element(By.TAG_NAME,'a').get_attribute('href'))
        
        return(self.Theme_dict)
    
    def _Extract_themewise_product_link(self)->str:
        for href in self.Theme_href[0::]:
            self.driver.get(href)
            #print(href)
            self.show_all()
            self.lego_product_links()

    def show_all(self):
        """This method clicks the 'show all' button in the page in order to display all the search result of the multile page"""
        xpath = '//a[@data-test="pagination-show-all"]'
        #'//*[@id="blt441564c4a0c70d99"]/section/div/div/div[3]/a'
        #'//*[@id="blt5881a9b7772d3176"]/section/div/div/div[3]/a'
        try:
            time.sleep(2)
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.find_element(By.XPATH,xpath).click()
        except TimeoutException:
            print("only one page lego product is available. No Show all button' is displayed")
    
    def lego_product_links(self):
        """List_item = finds the list of products or container.
           Each list in the container get the href of each products of items in the container  """

        #self. show_all()
        time.sleep(10)
        WebDriverWait(self.driver,30).until(EC.presence_of_element_located((By.XPATH, '//*[@data-test = "product-item"]')))
        self.list_items = self.driver.find_elements(By.XPATH,'//*[@data-test = "product-item"]') 
        self.lego_links = []
        for legoitems_link in self.list_items[0:]:
            self.lego_links.append(legoitems_link.find_element(By.TAG_NAME,'a').get_attribute('href'))
        return print(self.lego_links)
    
    def lego_product_info(self):
        """Click each lego product link and get the Product name , link, prices.
            Update these info in lego_dict. Create each record unique to avoid copies using UUID"""
        #self.lego_links 
        self.Lego_dict = {
            'Product_name':[],'Rating':[],'Prices':[],
            'link':[],'Flag':[],'Pieces':[],'Availability':[],
            'Item_num':[],'UUID':[]}
        
        for link in self.lego_links[0::]:
            self.driver.get(link)
            time.sleep(2)
            self.Lego_dict['link'].append(link)
            try:
                time.sleep(2)
                Prices = self.driver.find_element(By.XPATH,'//div[@data-test="product-leaf-price"]')
                self.Lego_dict['Prices'].append(Prices.text)
            #Lego_dict['UUID'].append(uuid)
            #print('UUID for prices')
            except NoSuchElementException:
                self.Lego_dict['Prices'].append('N/A')
            try:
                time.sleep(2)
                Product_name = self.driver.find_element(By.XPATH,'//h1[@data-test="product-overview-name"]')
                self.Lego_dict['Product_name'].append(Product_name.text)
            
            except NoSuchElementException:
                self.Lego_dict['Product_name'].append('N/A')
            #bot.driver.find_element(By.XPATH,'//span[@data-test="product-price"]')
            try:
                Discount = self.driver.find_element(By.XPATH,'//div[@data-test="sale-percentage"]')
                #Image_dict['lego_photos'].append(Pictures)
                self.Lego_dict['Discount'].append(Discount.text)
                print(Discount.text)
            except NoSuchElementException:
                self.Lego_dict['Discount'].append('No Discount')   
            try:
                Age = self.driver.find_element(By.XPATH,'//div[@data-test="ages-value"]')
                    #Age = Age_xpath.get_attribute('span')
                self.Lego_dict['Age'].append(Age.text)
                print(Age.text)
            
            except NoSuchElementException:
                self.Lego_dict['Age'].append('N/A')

            try:
                Pieces = self.driver.find_element(By.XPATH,'//div[@data-test="pieces-value"]')
                self.Lego_dict['Pieces'].append(Pieces.text)
                print(Pieces.text)
            except NoSuchElementException:
                self.Lego_dict['Pieces'].append('Num of Pieces not available for this product ')
            try:
                Discount_Price = self.driver.find_element(By.XPATH,'//div[@data-test="product-price-sale"]')
                self.Lego_dict['Discount_Price'].append(Discount_Price.text)
                print(Discount_Price.text)
            except NoSuchElementException:
                self.Lego_dict['Discount_Price'].append('N/A')
            try:
                rating_xpath = self.driver.find_element(By.XPATH,'//div[@class="RatingBarstyles__RatingContainer-sc-11ujyfe-2 fgbdIf"]')
                Rating = rating_xpath.get_attribute('title')
                self.Lego_dict['Ratings'].append(str(Rating))
                print(Rating)
            except NoSuchElementException:
                self.Lego_dict['Ratings'].append('N/A')

            try:
                Availability = self.driver.find_element(By.XPATH,'//p[@data-test="product-overview-availability"]')
                self.Lego_dict['Availability'].append(Availability.text)
                print(Availability.text)
            except NoSuchElementException:
                self.Lego_dict['Availability'].append('N/A')
            try:
                Item_num = self.driver.find_element(By.XPATH,'//div[@data-test="item-value"]')
                self.Lego_dict['Item_num'].append(Item_num.text)
                print(Item_num.text)
            except NoSuchElementException:
                self.Lego_dict['Item_num'].append('N/A')
            try:
                VIP_Points = self.driver.find_element(By.XPATH,'//div[@data-test="vip-points-value"]')
                self.Lego_dict['VIP_Points'].append(VIP_Points.text)
                print(VIP_Points.text)
            except NoSuchElementException:
                self.Lego_dict['VIP_Points'].append('N/A')
            try:
                self.driver.find_element(By.XPATH,'//*[@id="pdp-specifications-accordion-title"]/div/div/div[2]').click()
                Specification = self.driver.find_element(By.XPATH,'//div[@data-test="pdp-specifications-accordion-content-child"]')
                self.Lego_dict['Specification'].append(Specification.text)
                print(Specification.text)
            
            except:
                self.Lego_dict['Specification'].append('N/A')
            """ Customer Review icon click function"""
            self.driver.find_element(
                By.XPATH,'//*[@id="pdp-reviews-accordion-title"]/div/div/div[2]').click()

            try:
                Customer_Recommedation = self.driver.find_element(By.XPATH,'//span[@class="Text__BaseText-sc-178efqu-0 JTzEP"]')
                self.Lego_dict['Customer_Recommedation'].append(Customer_Recommedation.text)
                print(Specification.text)
                
            except:
                self.Lego_dict['Customer_Recommedation'].append('No reviews')

            try:
                Play_Experience = self.driver.find_element(By.XPATH,'//div[@class="Spacing-iay53v-0 dzdSmj"]').getattribute('title')
                self.Lego_dict['Play_Experience'].append(Play_Experience.text)
                print(Play_Experience.text)
            except:
                self.Lego_dict['Play_Experience'].append('No reviews')
            try:
                self.Lego_dict['UUID'].append(uuid.uuid4())
                print('UUID is',uuid.uuid4())
            
            except:
                pass

        
    def lego_image_downloader(self):
        """Download Firsts image from the lego products and update it as list in image_dict with UUID"""

        os.mkdir(os.path.join(os.getcwd(),self.selected_theme))
        os.chdir(os.path.join(os.getcwd(),self.selected_theme))

        self.Image_dict = {'Lego_images' :[],'Image_UUID':[]}

        for link in self.lego_links[0:]:
                self.driver.get(link)
                
                try:
                            
                    time.sleep(1)
                    Product_name = self.driver.find_element(By.XPATH,'//h1[@data-test="product-overview-name"]')
                    name = (Product_name.text).replace(' ','_').replace(',','').replace('-','')
                    img_container = self.driver.find_element(By.XPATH,'//picture[@class = "Picturestyles__Container-j8hf1d-0 bVuOVw LazyImagestyles__Picture-sc-1gcjd00-1 ddKWmr"]')
                    find_image = img_container.find_element(By.TAG_NAME,'img').get_attribute('src')
                    self.Image_dict['Lego_images'].append(find_image)
                        #os.mkdir(os.path.join(os.getcwd(),name))
                        #os.chdir(os.path.join(os.getcwd(),name))
                        #name = re.sub('\s+','_',(Product_name.text))
                    with open(name + '.jpg','wb') as f:
                            pict = requests.get(find_image)
                            f.write(pict.content)
                            f.close

                except NoSuchElementException:
                        print('No images found')

                try:
                    self.Image_dict['Image_UUID'].append(str(uuid.uuid4()))
                    print('UUID is',uuid.uuid4())
                except:
                        pass
    def Data_list(self):
        """Create a data table using panda for product info"""
        return(print(pd.DataFrame(self.Lego_dict)))

    def Image_data(self):  
        """Create a data table for immages using panda for lego images info"""
        return(print(pd.DataFrame(self.Image_dict))) 
    
    @staticmethod
    def data_JSON(self):
        """Created a JSON file in the root folder clled 'raw_data'-->data.json"""
        path = '/home/lakshmi/Documents/DS/Selenium/Lego/raw_data'
        os.mkdir(path)
        os.chdir(path)
        #L = json.dump(Lego_dict)
        #I = json.dump(Image_dict)
        #Lego_dict = MyEncoder.encode(Lego_dict)
        with open('data.json', 'w') as f:
            f.write(json.dumps(self.Lego_dict,indent=4, sort_keys=True))
            #f.write('\\n')
            #f.write(json.dumps(self.Image_dict,cls = UUIDEncoder))
            #f.write(I)

    def quit(self):
        self.driver.quit()

    def scrape_now(self):
        '''
        runs the various methods to accept cookies, select all themes, collect and download data and images
        '''
        try:
            self.lego_continue()
            self.necessary_cookies()
            self.shop()
            self.sets_by_theme()
            self._Theme_container()
            self._Theme_extract_href()
            self.lego_product_links()
            self.lego_product_info()
            self.Data_list()
            self.data_JSON()
            
        finally: 
            self.quit()

    def _set_by_price(self)-> None:
        """This method is used to click Theme menu"""
        xpath = '//*[@id="blte6fb96bc03e90791_submenubutton"]/div/span'
        try:
            time.sleep(2)
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.find_element(By.XPATH,xpath).click()
        except TimeoutException:
            print('no elements found')
    
    def _Price_Range_href(self) -> str:
        """This method is used to click Theme menu"""
        LPR_href = []
        price_range = {}
        
        Under_20 = self.driver.find_element(
            By.XPATH,'//a[@data-analytics-title="price-band-a"]').get_attribute('href')
        LPR_href.append(Under_20)
        price_range.update({'Under 20':Under_20})
        Between_20_50 = self.driver.find_element(
            By.XPATH,'//a[@data-analytics-title="price-band-b"]').get_attribute('href')
        LPR_href.append(Between_20_50)
        price_range.update({'Between 20 and 50':Between_20_50})

        Between_50_100 = self.driver.find_element(
            By.XPATH,'//a[@data-analytics-title="price-band-c"]').get_attribute('href')
        LPR_href.append(Between_50_100)
        price_range.update({'Between 50 and 100':Between_50_100})

        Between_100_150 = self.driver.find_element(
            By.XPATH,'//a[@data-analytics-title="price-band-d"]').get_attribute('href')
        LPR_href.append(Between_100_150)
        price_range.update({'Between 100 and 150':Between_100_150})

        Over_200 = self.driver.find_element(
            By.XPATH,'//a[@data-analytics-title="price-band-e"]').get_attribute('href')
        LPR_href.append(Over_200)
        price_range.update({'Over_200':Over_200})

        print(list(LPR_href))
        print(price_range)

        for i in LPR_href[0::]:
            self.driver.get(i)
            time.sleep(2)
            return self.lego_product_links()

if __name__ == '__main__' : 
    bot = Scraper()
    bot.scrape_now() 
