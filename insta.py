from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, JavascriptException
from util import getFollowers
from util import getFollowing
from util import getNonfollowers
from util import unfollowUsers
from util import likePosts

from random import randint as r
from datetime import date
from time import sleep
import os
import re

excludes = ["dziecko", "hotel", "hotelspa", "spa", "zabiegi", "butik", "fashionblogger", 
"mama", "nails", "studio", "kosmetyki", "krem", "fryzjer", "wellhair", "moda", "paznokcie", "salon", "sklep", 
"mum", "maluch", "420", "memes", "memy", "clinic", "klinika", "polskichlopak", "brwi", "brows", "suchar", "fajne"]

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

def follow(num):
	try: 
		browser.execute_script("document.getElementsByClassName('KL4Bh')[{}].click()".format(num))
		sleep(r(1,100)/100.0 + r(2,4))
		
		
		# check post hashtags
		postValid = checkPostData()

		print("Post valid: {}".format(postValid))
		username = browser.execute_script("return document.getElementsByClassName('FPmhX notranslate  nJAzx')[0].href")
		print(('current follow: ' + username))

		if postValid:
			# try to follow, if user already followed go next post
			try:
				browser.execute_script("document.getElementsByClassName('oW_lN sqdOP yWX7d    y3zKF     ')[0].click()")
				sleep(r(1,3) + 1)
				# like image
				browser.execute_script("document.getElementsByClassName('wpO6b ')[0].click()")
			except JavascriptException:
				print("already following! like and close image")
				browser.execute_script("document.getElementsByClassName('dCJp8 afkep')[0].click()")
				
				sleep(r(1,7) + 1)
				browser.execute_script("document.getElementsByClassName(\"ckWGn\")[0].click()")
				return
		else:
			# post invalid, close user window
			browser.execute_script("document.getElementsByClassName(\"ckWGn\")[0].click()")
			print("Post is invalid: ")
			sleep(r(1,100)/10.0 + 1)
			return

		sleep(r(1,100)/10.0 + 1)

		# get username from post and save it in file
		
		with open("ifollow.txt", "a+") as users:
			users.write("%s;%s\n" % (str(date.today()), str(username)))

		users.close()

		# close user window
		browser.execute_script("document.getElementsByClassName(\"ckWGn\")[0].click()")	
		sleep(r(1,2) + 1)
		try:
			browser.execute_script("document.getElementsByClassName(\"ckWGn\")[0].click()")	
			print('HAD TO DOUBLE EXIT')
		except JavascriptException:
			pass

		sleep(r(1,100)/100.0 + 1)

		

	except NoSuchElementException as exception:
		print(exception)
		browser.refresh()

	except JavascriptException as exception:
		# user deleted image, close empty window
		browser.execute_script("document.getElementsByClassName(\"ckWGn\")[0].click()")

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

# likePosts(browser, 30)

# likeHashtagPosts(43, 18)

# follow(35)
# sleep(0.5)
# browser.execute_script("window.scrollBy(0,150)")

# browser.execute_script('document.getElementsByTagName('article')[1].getElementsByClassName('glyphsSpriteHeart__outline__24__grey_9 u-__7')[1].click()')

# follow(9+9*3 + 0)

for i in range(25):
	follow(9+9*3 + i)
	print(('post num: ' + str(i)))
	if i % 3 == 0:
		browser.execute_script("window.scrollBy(0,350)")

# getFollowers(browser)
# getFollowing(browser)

# getNonfollowers()

# unfollowUsers(browser)