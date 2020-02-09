from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, JavascriptException
from util import getFollowers
from util import getFollowing
from util import getNonfollowers
from util import unfollowUsers
from util import likePosts

from logger_util import get_logger

from random import randint as r
from datetime import date
from time import sleep
import os
import re

excludes = ["dziecko", "hotel", "hotelspa", "spa", "zabiegi", "butik", "fashionblogger", 
"mama", "nails", "studio", "kosmetyki", "krem", "fryzjer", "wellhair", "moda", "paznokcie", "salon", "sklep", 
"mum", "maluch", "420", "memes", "memy", "clinic", "klinika", "polskichlopak", "brwi", "brows", "suchar", "fajne"]

exit_code = 'wpO6b '

# TODO GENERAL
# move all js scripts to constants file for easier updates
# manual fix when stuck


# TODO
# add scrolling
# add random post picking
# add check for already liked today
# add function final result
# add comments if some comments already posted
def likeHashtagPosts(amount, startOffset):
	try: 
		for postNum in range(amount):
			browser.execute_script("document.getElementsByClassName(\"KL4Bh\")[{}].click()".format(postNum + startOffset))
			sleep(r(1,100)/100.0 + r(2,4))
			
			
			# check post hashtags
			postValid = checkPostData()

			print("Post valid: {}".format(postValid))

			if not postValid:
				# post invalid, close user window
				browser.execute_script("document.getElementsByClassName(\"ckWGn\")[0].click()")
				print("Post is invalid: ")
				sleep(r(1,100)/10.0 + 1)
				return


			browser.execute_script("document.getElementsByClassName('dCJp8 afkep')[0].click()")
			sleep(r(1,7) + 1)

			# get username from post and save it in file
			# TODO add timestamp
			username = browser.execute_script("return document.getElementsByClassName('FPmhX notranslate  nJAzx')[0].href")
			with open("likedImage.txt", "a+") as users:
				users.write("%s;%s\n" % (str(date.today()), str(username)))

			users.close()

			# close user window
			browser.execute_script("document.getElementsByClassName(\"ckWGn\")[0].click()")	
			sleep(r(1,100)/100.0 + 1)


	except NoSuchElementException as exception:
		print(exception)
		browser.refresh()

	except JavascriptException as exception:
		# user deleted image, close empty window
		browser.execute_script("document.getElementsByClassName(\"ckWGn\")[0].click()")

def follow(amount):
	follow_counter = 0
	post = 0

	while follow_counter < amount:
		post += 1
		try: 
			browser.execute_script("document.getElementsByClassName('KL4Bh')[{}].click()".format(post + 9 + 3 * 9))
			sleep(r(1,100)/100.0 + r(2,4))

			buttons = browser.execute_script("return document.getElementsByClassName('{}')".format(exit_code))
			print(len(buttons))
			exit_button = buttons[-1]
			print(type(exit_button))
			
			# check post hashtags
			postValid = checkPostData()

			username = browser.execute_script("return document.getElementsByClassName('FPmhX notranslate  nJAzx')[0].href")

			print("{}. post valid: {} for user: {}".format(follow_counter, postValid, username))

			if postValid:
				# try to follow, if user already followed go next post
				try:
					print('post valid, follow n like....')
					browser.execute_script("document.getElementsByClassName('oW_lN sqdOP yWX7d    y3zKF     ')[0].click()")
					sleep(r(1,3) + 1)
					# like image
					browser.execute_script("document.getElementsByClassName('wpO6b ')[0].click()")
				except JavascriptException:
					print("already following! like and close image")
					browser.execute_script("document.getElementsByClassName('wpO6b ')[0].click()")
					
					sleep(r(1,7) + 1)
					# browser.execute_script("document.getElementsByClassName(\"ckWGn\")[0].click()")
					
					browser.execute_script("arguments[0].click()", exit_button)
					
					continue

				follow_counter += 1

				sleep(r(1,100)/10.0 + 1)

				# get username from post and save it in file
				with open("ifollow.txt", "a+") as users:
					users.write("%s;%s\n" % (str(date.today()), str(username)))

				users.close()

				# close user window
				sleep(r(1,2) + 1)
				# browser.execute_script("document.getElementsByClassName('{}')[0].click()".format(exit_code))
				exit_button.click()
				sleep(r(1,2) + 1)
				try:
					# browser.execute_script("document.getElementsByClassName('{}')[0].click()".format(exit_code))
					exit_button.click()
					print('HAD TO DOUBLE EXIT')
				except JavascriptException:
					print("[insta.py - follow] cant close window")

				sleep(r(1,100)/100.0 + 1)

				# scroll page
				if follow_counter % 3 == 0:
					browser.execute_script("window.scrollBy(0,350)")

			else:
				# post invalid, close user window
				try:
					print('click exit....')
					# browser.execute_script("document.getElementsByClassName('{}')[0].click()".format(exit_code))
					exit_button.click()
				except:
					print("cant close invalid post")
				print("Post is invalid: ")
				sleep(r(1,100)/10.0 + 1)

				continue

		except NoSuchElementException as exception:
			print(exception)
			browser.refresh()

		except JavascriptException as exception:
			# user deleted image, close empty window
			# browser.execute_script("document.getElementsByClassName('wpO6b ')[0].click()")
			exit_button.click()

# TODO
# return invalidity reason/hashtag
# fix it
# add try catch
def checkPostData():
	postValid = True
	strPost = browser.execute_script("return document.querySelector(\"body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > div.EtaWk > ul > div > li > div > div > div.C4VMK > span\").innerText")

	listPostWords = strPost.split(' ')

	for postWord in listPostWords:
		for badWord in excludes:
			if re.search(badWord, postWord):
				print("found bad word: {}".format(postWord))
				postValid = False

	return postValid

# os.system('cmd /c "chrome.exe -remote-debugging-port=9014 --user-data-dir=\"C:/Users/aro/Documents/ChromeProfile\""')
# sleep(4)
# print("go")

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "localhost:9014")
chrome_options.add_argument('headless')
#Change chrome driver path accordingly
chrome_driver = "C:/Users/aro/Documents/chromedriver/chromedriver.exe"
browser = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)

log = get_logger()
likePosts(browser, log, 3)

# likeHashtagPosts(43, 18)

# follow(35)
# sleep(0.5)
# browser.execute_script("window.scrollBy(0,150)")

# browser.execute_script('document.getElementsByTagName('article')[1].getElementsByClassName('glyphsSpriteHeart__outline__24__grey_9 u-__7')[1].click()')


# follow(30)
	

# getFollowers(browser)
# getFollowing(browser)

# getNonfollowers()

# unfollowUsers(browser)