from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#exceptions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException

import sys
import os
import time

options = Options()
options.headless = False
options.add_argument("--window-size=1920,1200")
DRIVER_PATH = 'C:/Users/danie/AppData/Roaming/ChromeDriver/chromedriver.exe'
URL = "https://music.youtube.com/"
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

metadata_path = "C:/Users/danie/Documents/Youtube_Lyrics/"
DESTINATION_DIRECTORY = "C:/Users/danie/Documents/Youtube_Lyrics/"
path_to_list = metadata_path + "song_name_list.txt"

#helper functions
#Fixes song names to be valid syntax on windows
def fix_title(song):
    fixed_song_name = song.replace("?","").replace("*", "").replace("<","").replace(">","").replace(":","").replace('"',"").replace("/","").replace("\\","").replace("|","").replace(".","").replace("é","e")
    return fixed_song_name

#Goes onto youtube music and returns the most popular song's name and lyrics in a text file
def yt_song_search(entered_song_name):
    driver.get(URL)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, "ytmusic-search-box")))
    driver.find_element_by_tag_name("ytmusic-search-box").click()
    search_box = driver.find_element_by_xpath("//input[@class='style-scope ytmusic-search-box']")
    search_box.send_keys(Keys.DELETE)
    search_box.send_keys(entered_song_name)
    search_box.send_keys(Keys.RETURN)
    time.sleep(1)
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-search-page/ytmusic-tabbed-search-results-renderer/div[2]/ytmusic-section-list-renderer/div[2]/ytmusic-shelf-renderer[2]/div[2]/ytmusic-responsive-list-item-renderer[1]/div[1]/ytmusic-item-thumbnail-overlay-renderer/div/ytmusic-play-button-renderer/div/yt-icon")))
    top_song = driver.find_element_by_xpath("/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-search-page/ytmusic-tabbed-search-results-renderer/div[2]/ytmusic-section-list-renderer/div[2]/ytmusic-shelf-renderer[2]/div[2]/ytmusic-responsive-list-item-renderer[1]/div[1]/ytmusic-item-thumbnail-overlay-renderer/div/ytmusic-play-button-renderer/div/yt-icon")
    time.sleep(1.5)       
    top_song.click()
    time.sleep(2)

    #Finds the song name and the lyrics elements 
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='layout']/ytmusic-player-bar/div[2]/div[2]/yt-formatted-string")))
    song_name = driver.find_element_by_xpath("//*[@id='layout']/ytmusic-player-bar/div[2]/div[2]/yt-formatted-string").text 
    song_name = fix_title(song_name)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='contents']/ytmusic-description-shelf-renderer/yt-formatted-string[3]")))
    lyrics = driver.find_element_by_xpath("//*[@id='contents']/ytmusic-description-shelf-renderer/yt-formatted-string[3]").text
    
    #write lyrics to a text file
    f = open(DESTINATION_DIRECTORY + song_name + ".txt", "a")
    f.write(lyrics)
    f.close()

#finds lyrics for each song name in a text file
def search_from_file():
    file = open(path_to_list, "r")
    for line in file:
        yt_song_search(line)
    file.close()

if __name__ == '__main__':
    search_from_file()
    driver.quit()
    exit(0)    