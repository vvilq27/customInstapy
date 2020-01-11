from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, JavascriptException
from util import getFollowers
from util import getFollowing
from util import getNonfollowers
from util import unfollowUsers


from random import randint as r
from datetime import date
from time import sleep
import os

excludes = ["dziecko", "hotel", "hotelspa", "spa", "zabiegi", "butik", "fashionblogger", 
"mama", "nails", "studio", "kosmetyki", "krem", "fryzjer", "wellhair", "moda", "paznokcie", "salon", "sklep", 
"mum", "maluch", "420", "memes", "mem", "memy", "clinic", "klinika"]

def follow(num):
	try: 
		browser.execute_script("document.getElementsByClassName(\"KL4Bh\")[{}].click()".format(num))
		sleep(r(1,100)/100.0 + r(2,4))
		
		
		# check post hashtags
		postValid = checkPostData()

		print("Post valid: {}".format(postValid))

		if postValid:
			# try to follow, if user already followed go next post
			try:
				browser.execute_script("document.getElementsByClassName('oW_lN sqdOP yWX7d    y3zKF     ')[0].click()")
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
		# TODO add timestamp
		username = browser.execute_script("return document.getElementsByClassName('FPmhX notranslate  nJAzx')[0].href")
		with open("ifollow.txt", "a+") as users:
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

# TODO
# return invalidity reason/hashtag
def checkPostData():
	postValid = True
	strPost = browser.execute_script("return document.querySelector(\"body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > div.EtaWk > ul > div > li > div > div > div.C4VMK > span\").innerText")

	listPostWords = strPost.split('#')

	for tag in listPostWords:
		print("checking tag: {}".format(tag))

		if tag in excludes:
			postValid = False

		if postValid == False:
			return
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
print(browser.title)


# follow(35)
# sleep(0.5)
# browser.execute_script("window.scrollBy(0,150)")

# add try catch

browser.get('https://www.instagram.com/explore/tags/warsawoldtown/')

sleep(4)

for i in range(2):
	follow(16+i)
	if i % 3 == 0:
		browser.execute_script("window.scrollBy(0,200)")

# getFollowers(browser)
# getFollowing(browser)

# getNonfollowers()

# unfollowUsers(browser)