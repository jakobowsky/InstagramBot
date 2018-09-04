from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import random
import time
import pyautogui
import os
import sys

#limit of comments is 60 per hour
#limit of liking photos is 60 per hour
#followers limit is 7500 and 20-30 per hour

class InstagramBot:


    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome('C:/chromedriver')

    def closeBroweser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'shift', 'i')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'shift', 'm')
        time.sleep(1)
        elem = driver.find_element_by_name('username')
        elem.send_keys(self.username)
        elem = driver.find_element_by_name('password')
        elem.send_keys(self.password)
        time.sleep(3)
        elem.submit()
        time.sleep(5)
        driver.get("https://www.instagram.com")
        pyautogui.hotkey('ctrl', 'shift', 'm')
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'shift', 'i')


    def collectLinksOfPhotos(self,hashtag,numberOfScrolls):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)
        #links to photos
        links = set()
        for i in range(numberOfScrolls):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                for x in range(1,3):
                    for y in range(1,3):
                        currentLink = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div['+str(x)+']/div['+str(y)+']/a')
                        links.add(currentLink.get_attribute('href'))
            except Exception:
                continue
        return links

    def likePhotos(self,links):
        driver = self.driver
        for link in links:
            time.sleep(3)
            driver.get(link)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                time.sleep(random.randint(2,4))
                like = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/span[1]/button')
                like.click()
                time.sleep(random.randint(2, 4))
            except Exception as e:
                time.sleep(2)





if __name__ == '__main__':
    ig = InstagramBot('login','pass')
    ig.login()
    m = ig.collectLinksOfPhotos('car',4)
    ig.likePhotos(m)