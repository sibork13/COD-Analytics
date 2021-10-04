'''
Script that contains all functions to scrape cod tracker
'''

from common import config
###
import requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

class COD_Tracker:
    def __init__(self,web_page,url):
        self._config = config()['WEBSITES'][web_page] # pass 'player_name' attribute
        self._xpath_dir = self._config['xpath_dir']
        self._driver = None
        self._visit(url)

    def _visit(self,url):
        options = webdriver.FirefoxOptions()
        options.add_argument("windows-size=1920x1080")
        options.add_argument("--headless")
        options.add_argument("--incognito")
        self._driver = webdriver.Firefox(executable_path='driver/geckodriver',options=options)
        self._driver.get(url)
        try:
        	player_name = WebDriverWait(self._driver,10)\
        			.until(
        			EC.presence_of_element_located((By.XPATH,'//span[@class="trn-ign__username"]'))
        			)
        	print("Ya se extrajo el nombre")
            # button = WebDriverWait(self._driver,10)\
        	# 		.until(
        	# 		EC.presence_of_element_located((By.XPATH,'//span[@class="trn-gamereport-list__group-more"]/a[@class="trn-button trn-button--block"]'))
        	# 		)
        	#print("Ya se extrajo el nombre")
        except TimeoutException:
        	print("nO")


    def _extract_one(self,xpath):
        return self._driver.find_element_by_xpath(xpath)

    def _extract_all(self,xpath):
        return self._driver.find_elements_by_xpath(xpath)


    def _close(self):
        self._driver.quit()


class HomePage(COD_Tracker):
    def __init__(self,web_page,url):
        super().__init__(web_page,url)

    @property
    def player_name(self):
        name = self._extract_one(self._xpath_dir['player_name_xpath']).text
        #self._close()
        return name

    @property
    def matches_list(self):
        listmatch = self._extract_all(self._xpath_dir['match_list_page'])
        #self._close()
        return listmatch
    @property
    def get_place(self):
        return self._extract_all(self._xpath_dir['place'])

    @property
    def get_game_mode(self):
        return self._extract_all(self._xpath_dir['game_mode'])

    @property
    def get_loby_kd(self):
        return self._extract_all(self._xpath_dir['loby_kd'])

    @property
    def get_kills(self):
        return self._extract_all(self._xpath_dir['kills'])

    @property
    def click_next(self):
        button = self._extract_one(self._xpath_dir['button'])
        button.click()
        time.sleep(5)


    @property
    def close_connection(self):
        self._close()
