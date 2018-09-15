from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import random
import time
import pyautogui
import os
import re
import sys
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot

#limit of comments is 60 per hour
#limit of liking photos is 60 per hour
#followers limit is 7500 and 20-30 per hour

class InstagramBot:


    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome('C:/chromedriver')
        #self.driver.set_window_size(700, 900)

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

    # Not the best solutions, only liking all photos
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

    def writeComment(self,text):
        try:
            button = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/span[2]/button/span')
            button.click()
        except NoSuchElementException:
            pass
        try:
            commentBox = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[3]/div/form/textarea')
            commentBox.send_keys('')
            commentBox.clear()
            for letter in text:
                commentBox.send_keys(letter)
                time.sleep((random.randint(1,7)/30))
            return commentBox
        except StaleElementReferenceException and NoSuchElementException as e:
            print(e)
            return False

    def postComment(self,commentText):
        time.sleep(random.randint(1, 5))
        commentBox = self.writeComment(commentText)
        if commentText in self.driver.page_source:
            commentBox.send_keys(Keys.ENTER)
            try:
                postButton = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[3]/div/form/button')
                postButton.click()
                print("Clicked button")
            except NoSuchElementException:
                pass
        time.sleep(random.randint(4,6))
        self.driver.refresh()
        if commentText in self.driver.page_source:
            return True
        return False

    #taking comments from photo page
    def getComments(self):
        #we can load more comments if button exists
        time.sleep(3)
        try:
            # comments_block = self.driver.find_element_by_class_name('Xl2Pu')
            # comments_in_block = comments_block.find_elements_by_class_name('gElp9')
            # comments = [x.find_element_by_tag_name('span') for x in comments_in_block]
            # user_comment = re.sub(r'#.\w*', '', comments[0].text)
            user_comment = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/li[1]/div/div/div/span')
        except NoSuchElementException:
            return ''
        return user_comment.text
    def commentPicture(self):
        bot = ChatBot('YouTubeChatBot')
        bot.set_trainer(ListTrainer)
        picComment = self.getComments()
        response = bot.get_response(picComment).__str__()
        print("User: ",picComment)
        print("Bot: ",response)
        return  self.postComment(response)

if __name__ == '__main__':
    ig = InstagramBot('xxx','xxxx')
    ig.login()
    ig.driver.get('xxxxx')
    #m = ig.collectLinksOfPhotos('car',4)
    #ig.likePhotos(m)
    time.sleep(2)
    #print(ig.postComment('Nice Photo Man'))
    print(ig.commentPicture())
