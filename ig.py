import random
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

class IGBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome('C:/chromedriver')
        self.comments = ['Really nice.', 'I like this.', 'Nice.', 'Great capture.', 'OMG.', 'Great feed!',
                         'Reminds me of something ...', 'Yes.', 'Exellent.', 'Love it.', 'Good eye.']

    def closeBroweser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(2)
        elem = driver.find_element_by_name('username')
        elem.send_keys(self.username)
        elem = driver.find_element_by_name('password')
        elem.send_keys(self.password)
        time.sleep(3)
        elem.submit()
        time.sleep(5)
        driver.get("https://www.instagram.com")

    def collectLinksOfPhotos(self, hashtag, numberOfScrolls):
        driver = self.driver

        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)
        links = set()
        for i in range(numberOfScrolls):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                for x in range(1, 3):
                    for y in range(1, 3):
                        currentLink = driver.find_element_by_xpath(
                            '//*[@id="react-root"]/section/main/article/div[2]/div/div[' + str(x) + ']/div[' + str(
                                y) + ']/a')
                        links.add(currentLink.get_attribute('href'))
            except Exception:
                continue
        return links

    def likePhoto(self, link):
        driver = self.driver
        time.sleep(3)
        driver.get(link)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            time.sleep(random.randint(2, 4))
            like = driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/span[1]/button')
            like.click()
            time.sleep(random.randint(2, 4))
        except Exception as e:
            time.sleep(2)

    def commentPhoto(self, text):
        try:
            button = self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/span[2]/button/span')
            button.click()
        except NoSuchElementException:
            pass
        try:
            commentBox = self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[3]/div/form/textarea')
            commentBox.send_keys('')
            commentBox.clear()
            for letter in text:
                commentBox.send_keys(letter)
                time.sleep((random.randint(1, 7) / 30))
            return commentBox
        except StaleElementReferenceException and NoSuchElementException as e:
            print(e)
            return False

    def postComment(self, commentText):
        time.sleep(random.randint(1, 5))
        commentBox = self.commentPhoto(commentText)
        time.sleep(random.randint(1, 3))
        commentBox.send_keys(Keys.ENTER)
        time.sleep(random.randint(1, 3))

    def like_and_comment_photos(self, links):
        driver = self.driver
        for link in links:
            try:
                self.likePhoto(link)
                self.postComment(random.choices(self.comments))
            except:
                continue


def Bot1(loginIG, passIG):
    ig = IGBot(loginIG, passIG)
    ig.login()
    links = ig.collectLinksOfPhotos('dogs', 1)
    ig.like_and_comment_photos(links)
    time.sleep(2)
    ig.closeBroweser()


if __name__ == '__main__':
    Bot1('xxx', 'xxx')
