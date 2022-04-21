from logging import exception
from typing_extensions import Self
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException #used to debug the program
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from pandas import DataFrame
import os
import requests
from bs4 import BeautifulSoup
import uuid
from uuid import UUID
import json

class UUIDEncoder(json.JSONEncoder):
    """Class for json file to encode the UUID"""
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)

class Scraper():
    #Themes = 'Minions','Technics','DUPLO'
    #print('Themes')

    def __init__(self, selected_theme, url:str = 'https://www.lego.com/en-gb'):
        """ Initailising the theme"""
        #self.selected_theme = selected_theme
        self.selected_theme = selected_theme
        #input('Choose a Theme name(Minions,Technics,DUPLO): ')
        self.driver = Chrome(ChromeDriverManager().install())
        self.driver.get(url)
        self.driver.maximize_window()
        
          
    def lego_continue(self):
        """This function is created to click the cookie button in the Webpage"""
        xpath = '//*[@id="root"]/div[5]/div/div/div[1]/div[1]/div/button'
        try:
            time.sleep(2)
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.find_element(By.XPATH, xpath).click()
        except TimeoutException:
            print('no elements found')

    def necessary_cookies(self):
        """This method is meant to click the necessary cookies"""
        xpath = '//button[contains(@class,"Button__Base-sc-1jdmsyi-0 eCVPKR")]'
        try:
            #time.sleep(2)
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.find_element(By.XPATH,xpath).click()
        except TimeoutException:
            print('no elements found')

    def shop(self):
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

    def select_theme(self):
        """This method is used to click Theme which is initialised in the class. Here I programmed for only 3 themes Minions, DUPLO, Technics """
        if self.selected_theme == 'Technics':
            xpath = '//*[@id="root"]/div[2]/header/div[2]/div[2]/div/div[3]/nav/div/div[1]/div/div[1]/div/div[3]/div[7]/a/span'   
            try:
                time.sleep(2)
                WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, xpath)))
                self.driver.find_element(By.XPATH,xpath).click()
            except TimeoutException:
                print('oh!no Theme found')
        elif self.selected_theme == 'DUPLO':
            xpath = '//*[@id="root"]/div[2]/header/div[2]/div[2]/div/div[3]/nav/div/div[1]/div/div[1]/div/div[1]/div[14]/a/span'
            #'//*[@id="root"]/div[2]/header/div[2]/div[2]/div/div[3]/nav/div/div[1]/div/div[1]/div/div[1]/div[14]/a'      
            try:
                time.sleep(2)
                WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, xpath)))
                self.driver.find_element(By.XPATH,xpath).click()
            except TimeoutException:
                print('oh!no Theme found')
        elif self.selected_theme == 'Minions':
            xpath = '//*[@id="root"]/div[2]/header/div[2]/div[2]/div/div[3]/nav/div/div[1]/div/div[1]/div/div[2]/div[12]/a/span'   
            try:
                time.sleep(2)
                WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, xpath)))
                self.driver.find_element(By.XPATH,xpath).click()
            except TimeoutException:
                print('oh!no Theme found')

    def Availability(self):
        """Check for availablility button"""
        xpath = '//*[@id="product-facet-availability-accordion-title"]/div'
        try:
            #time.sleep(2)
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.find_element(By.XPATH,xpath).click()
        except TimeoutException:
            print('no elements found')

    def check_available_now(self):
        """Click Avaialbale now option"""
        xpath ='//*[@id="product-facet-availability-accordion-content"]/div/div/ul/li[1]/label/span'
        try:
            #time.sleep(2)
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.find_element(By.XPATH,xpath).click()
        except TimeoutException:
            print('no elements found')
    

    #def container(self):
       # self.xpath = '//ul[@class="ProductGridstyles__Grid-lc2zkx-0 gxucff"]'
        #'//*[@id="blt652ac4f846d07628"]/section/div/div/div[2]'
        #'//*[@id="blt652ac4f846d07628"]/section/div/div/div[2]/ul'
        #'//*[@id="blt441564c4a0c70d99"]/section/div/div'
        #'//*[@id="blt441564c4a0c70d99"]/section/div/div/div[2]'
        #'//div[@class ="Productsstyles__ProductsWrapper-r9qrnh-0 erhzcf"]'        
       # return self.driver.find_element(By.XPATH,self.xpath)
            
    #def find_container(self):
       # self.container = self.container(self.xpath)
        
    #def lego_products(self):
        #Scraper.find_container()
        #self.list_items =[]
       # self.list_items = self.driver.find_elements(By.XPATH,'//*[@class ="ProductGridstyles__Item-lc2zkx-1 bDqwSC"]') 
        #self.list_items = self.container.find_elements(By.XPATH,'//*[@class ="ProductGridstyles__Item-lc2zkx-1 bDqwSC"]')
        #self.list_items = self.driver.find_elements(By.XPATH,'//*[@class ="ProductGridstyles__Item-lc2zkx-1 bDqwSC"]')
       # return(self.list_items)

    def lego_product_links(self):
        """List_item = finds the list of products or container.
           Each list in the container get the href of each products of items in the container  """
        self.list_items = self.driver.find_elements(By.XPATH,'//*[@class ="ProductGridstyles__Item-lc2zkx-1 bDqwSC"]') 
        self.lego_links = []
        for legoitems_link in self.list_items[0:]:
            self.lego_links.append(legoitems_link.find_element(By.TAG_NAME,'a').get_attribute('href'))
        return self.lego_links
    
    def lego_product_info(self):
        """Click each lego product link and get the Product name , link, prices.
            Update these info in lego_dict . Create each record unique to avoid copies using UUID"""
        #self.lego_links 
        self.Lego_dict = {'Product_name':[], 'Prices':[], 'link':[], 'UUID':[]}
        
        for link in self.lego_links[0:]:
            self.driver.get(link)
            time.sleep(2)
            self.Lego_dict['link'].append(link)
            try:
                Prices = self.driver.find_element(By.XPATH,'//div[@data-test="product-leaf-price"]')
                self.Lego_dict['Prices'].append(Prices.text)
            except NoSuchElementException:
                self.Lego_dict['Prices'].append('N/A')
            try:
                Product_name = self.driver.find_element(By.XPATH,'//h1[@data-test="product-overview-name"]')#.text
                self.Lego_dict['Product_name'].append(Product_name.text)
            except NoSuchElementException:
                self.Lego_dict['Product_name'].append('N/A')
    #bot.driver.find_element(By.XPATH,'//span[@data-test="product-price"]')
            try:
                self.Lego_dict['UUID'].append(uuid.uuid4())
                #print('UUID is',uuid.uuid4())
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
                    self.Image_dict['Image_UUID'].append(uuid.uuid4())
                    print('UUID is',uuid.uuid4())
                except:
                        pass

    def Data_list(self):
        """Create a data table using panda for product info"""
        return(print(pd.DataFrame(self.Lego_dict)))
    def Image_data(self):  
        """Create a data table for immages using panda for lego images info"""
        return(print(pd.DataFrame(self.Image_dict))) 
    
    def data_JSON(self):
        """Created a JSON file in the root folder clled 'raw_data'-->data.json"""
        path = '/home/lakshmi/Documents/DS/Selenium/Lego/raw_data'
        os.mkdir(path)
        os.chdir(path)
        #L = json.dump(Lego_dict)
        #I = json.dump(Image_dict)
        #Lego_dict = MyEncoder.encode(Lego_dict)
        with open('data.json', 'w') as f:
            f.write(json.dumps(self.Lego_dict,cls = UUIDEncoder,indent=4, sort_keys=True))
            #f.write('\\n')
            #f.write(json.dumps(self.Image_dict,cls = UUIDEncoder))
            #f.write(I)


if __name__ == '__main__' : 
    bot = Scraper('Minions')
    bot.lego_continue()
    bot.necessary_cookies()
    bot.shop()
    bot.sets_by_theme()
    bot.select_theme()
    bot.Availability()
    bot.check_available_now()
    #bot.container()
    #bot.find_container()
    #bot.Container()
    #bot.lego_products()
    bot.lego_product_links()
    bot.lego_image_downloader()
    bot.lego_product_info()
    bot.Data_list()
    bot.Image_data()
    bot.data_JSON()


#print(container)
#list_items = container.find_elements(By.XPATH,'//*[@class ="ProductGridstyles__Item-lc2zkx-1 bDqwSC"]')
    
