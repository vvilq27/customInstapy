from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from random import randint as r
from selenium.common.exceptions import NoSuchElementException, JavascriptException
from util import getFollowers
from util import getFollowing
from util import getNonfollowers
from util import unfollowUsers

from datetime import date
from time import sleep

def follow(num):
	try: 
		driver.execute_script("document.getElementsByClassName(\"KL4Bh\")[{}].click()".format(num))
		sleep(r(1,100)/100.0 + r(2,4))
		
		# if user already followed go next post
		try:
			driver.execute_script("document.getElementsByClassName('oW_lN sqdOP yWX7d    y3zKF     ')[0].click()")
		except JavascriptException:
			print("already following! like and close image")
			driver.execute_script("document.getElementsByClassName('dCJp8 afkep')[0].click()")
			sleep(r(1,100)/100.0 + 1)
			driver.execute_script("document.getElementsByClassName(\"ckWGn\")[0].click()")
			return

		sleep(r(1,100)/100.0 + 1)

		# get username from post and save it in file
		# TODO add timestamp
		username = driver.execute_script("return document.getElementsByClassName('FPmhX notranslate  nJAzx')[0].href")
		with open("ifollow.txt", "a+") as users:
			users.write("%s;%s\n" % (str(date.today()), str(username)))

		users.close()

		# close user window
		driver.execute_script("document.getElementsByClassName(\"ckWGn\")[0].click()")	
		sleep(r(1,100)/100.0 + 1)

		

	except NoSuchElementException as exception:
		print(exception)
		driver.refresh()

	except JavascriptException as exception:
		# user deleted image, close empty window
		driver.execute_script("document.getElementsByClassName(\"ckWGn\")[0].click()")


chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "localhost:9014")
#Change chrome driver path accordingly
chrome_driver = "C:/Users/aro/Documents/chromedriver/chromedriver.exe"
driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
print(driver.title)


# follow(35)
# sleep(0.5)
# driver.execute_script("window.scrollBy(0,150)")

# add try catch


for i in range(25):
	follow(9+i)
	if i % 3 == 0:
		driver.execute_script("window.scrollBy(0,200)")

# getFollowers(driver)
# getFollowing(driver)

# getNonfollowers()

# unfollowUsers(driver)


