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
            if 'handle' in url:
                print("EXTRACTING PLAYERS PAGE")
                player_name = WebDriverWait(self._driver,10).until(
                EC.presence_of_element_located(
                (By.XPATH,'//div[@class="player-header"]/div[@class="button"]')))
            else:
                print("SCRAPING HOME PAGE")
                player_name = WebDriverWait(self._driver,10).until(
                EC.presence_of_element_located(
                (By.XPATH,'//div[@class="trn-gamereport-list__group"]/span[@class="trn-gamereport-list__group-more"]/button[@class="trn-button"]')))

            print("Se accedio a la pagina")
        except TimeoutException:
        	print("nO")


    def _extract_one(self,xpath):
        return self._driver.find_element_by_xpath(xpath)

    def _extract_all(self,xpath):
        return self._driver.find_elements_by_xpath(xpath)

    def _extract_href(self,xpath):
        # print(self._driver.find_element_by_xpath(xpath))
        return [a_tag.get_attribute("href") for a_tag in self._driver.find_elements_by_xpath(xpath)]



    def _close(self):
        self._driver.quit()


class HomePage(COD_Tracker):
    def __init__(self,web_page,url):
        super().__init__(web_page,url)

    @property
    def player_name(self):
        name = self._extract_one(self._xpath_dir['player_name_xpath']).text
        return name


    def matches_list(self,allowed_game_mode_list):
        # list of all data will be stored ordenated
        list = []
        #List of every match link
        match_List = []
        #getting bloc of matches per date
        matches_per_date = self._extract_all(self._xpath_dir['match_per_date'])
        for date in matches_per_date:
            listmatch = date.find_elements_by_xpath(self._xpath_dir['listmatch'])
            for match in listmatch:
                place = match.find_elements_by_xpath(self._xpath_dir['place'])[0]
                game_mode = match.find_elements_by_xpath(self._xpath_dir['game_mode'])[0]
                loby_kd = match.find_elements_by_xpath(self._xpath_dir['loby_kd'])
                kills = match.find_elements_by_xpath(self._xpath_dir['kills'])[0]
                match_link = [a_tag.get_attribute("href") for a_tag in match.find_elements_by_xpath('.//a[@class="match-row__link"]')][0]
                # print(len(place))
                # print(loby_kd)
                if game_mode.text in allowed_game_mode_list:
                    # somethmes kd doesn exist
                    if len(loby_kd) == 0 :
                        loby_kd = 'NA'
                    else:
                        loby_kd = loby_kd[0]
                    #here will separate data for match
                    match_List.append(match_link)
                    list.append(place.text)
                    list.append(game_mode.text)
                    list.append(loby_kd.text)
                    list.append(kills.text)
        return list,match_List

    @property
    def click_next(self):
        button = self._extract_one(self._xpath_dir['button'])
        button.click()
        time.sleep(5)


    @property
    def close_connection(self):
        self._close()


class MatchPage(COD_Tracker):
    def __init__(self,web_page,url):
        super().__init__(web_page,url)


    @property
    def extract_butons(self):
        return self._extract_all(self._xpath_dir['b_stats'])


    def click_open_stats(self,button):
        button.click()

    @property
    def extract_enemy_name(self):
        return self._extract_all(self._xpath_dir['enemy_name'])

    @property
    def close_connection(self):
        self._close()

    @property
    def test_get_player_block(self):
        allowed_metrics =['Kills','Deaths','Assists','Damage','Score']
        bloc = self._extract_all(self._xpath_dir['test_block_player'])
        stats_list = []
        test_enemies = []
        for i_bloc in bloc:
            # Is time to extract every player bloc from team block
            team_players = i_bloc.find_elements_by_xpath(self._xpath_dir['test_team_plaers'])
            team_placement = i_bloc.find_element_by_xpath(self._xpath_dir['test_placement']).text
            for player in team_players:
                test_enemies = []
                try:
                    enemy_name = player.find_element_by_xpath(self._xpath_dir['enemy_name']).text
                except:
                    enemy_name = 'NA'
                # Adding player name
                test_enemies.append(enemy_name)
                # Adding team place
                test_enemies.append(team_placement)
                # Extracting stats for player
                enemy_stats = player.find_elements_by_xpath(self._xpath_dir['player'])
                # Iterating returned list to take only important metrics
                for j in range(0,len(enemy_stats)):
                    if enemy_stats[j].text in allowed_metrics:
                        test_enemies.append(enemy_stats[j].text)
                        test_enemies.append(enemy_stats[j+1].text)
                stats_list.append(test_enemies)
        return stats_list
