from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, JavascriptException
from util import getFollowers
from util import getFollowing
from util import getNonfollowers
from util import unfollowUsers
from util import likePosts
from util import follow
from util import likeHashtagPosts
import sys

from logger_util import get_logger

from datetime import date
from time import sleep
import os
from subprocess import Popen

excludes = ["dziecko", "hotel", "hotelspa", "spa", "zabiegi", "butik", "fashionblogger", 
"mama", "nails", "studio", "kosmetyki", "krem", "fryzjer", "wellhair", "moda", "paznokcie", "salon", "sklep", 
"mum", "maluch", "420", "memes", "memy", "clinic", "klinika", "polskichlopak", "brwi", "brows", "suchar", "fajne"]

like_code = 'sqdOP yWX7d     _8A5w5   ZIAjV '
exit_code = 'wpO6b '
button_exit_class = '                   Igw0E     IwRSH      eGOV_         _4EzTm                                                                                  BI4qX            qJPeX            fm1AK   TxciK yiMZG'

# open chrome command
# chrome.exe -remote-debugging-port=9014 --user-data-dir="C:\Users\aro\Documents\ChromeProfile" --headless


# def init():
# command = 'chrome.exe -remote-debugging-port=9014 --user-data-dir="C:/Users/aro/Documents/ChromeProfile"'
# proc=Popen(command)

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "localhost:9014")
chrome_options.add_argument('headless')
#Change chrome driver path accordingly
chrome_driver = "C:/Users/aro/Documents/chromedriver/chromedriver.exe"
browser = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)

# browser.get("https://www.instagram.com/")

# close popup
# prob need to send keys "enter" to get that
# browser.find_elements_by_class_name('aOOlW   HoLwm ')[0].click()
# browser.find_element_by_xpath('//div[4]/div/div/div[3]/button[2]').click()

log = get_logger()

# browser.execute_script("window.scrollBy(0, {})".format(1000))

# likePosts(browser, log, int(sys.argv[1]))
# likeHashtagPosts(browser, log, 45, 35)

# like = browser.find_elements_by_class_name(like_code)[0]
# print(like.getTagName())
# like.click()

# likeHashtagPosts(43, 18)
# browser.find_elements_by_class_name(like_code)[0].click()

follow(browser, log, 5)


# getFollowers(browser)
# getFollowing(browser)

# getNonfollowers()

# unfollowUsers(browser, log)