import json
from selenium.common.exceptions import NoSuchElementException, JavascriptException
from time import sleep
import random
import csv
import re
from datetime import date, datetime
from random import randint as r
import re

excludes = ["dziecko", "hotel", "hotelspa", "spa", "zabiegi", "butik", "fashionblogger", 
"mama", "nails", "studio", "kosmetyki", "krem", "fryzjer", "wellhair", "moda", "paznokcie", "salon", "sklep", 
"mum", "maluch", "420", "memes", "mem", "memy", "clinic", "klinika", "polskichlopak", "brwi", "brows", "suchar",
"brzuszku", "brzuszek", "ciąża", "official", "lash", "estetyczna", "mom", "dogsgram", "mother", "baby", "child", "przedłużanie"]

invalid_names = ["polk", "polsk", "polish", "polan", "official", "makeup", "meme"]

min_like_count = 20
max_like_count = 225

like_code = 'wpO6b '
user_name_code = 'sqdOP yWX7d     _8A5w5   ZIAjV '


def getFollowers(browser):
    variables = {}
    variables['id'] = "2120585971"
    variables['first'] = 50
    hasNext = True
    endCursor = None
    followed = []
    take = 1
    url = "https://www.instagram.com/graphql/query?query_hash=37479f2b8209594dde7facb0d904896a&variables={%22id%22:%222120585971%22,%22first%22:200}"
    
    browser.get(url)

    try:
        while hasNext is True:
            if endCursor is not None:
                nextUrl = "https://www.instagram.com/graphql/query?query_hash=37479f2b8209594dde7facb0d904896a&variables={}".format(str(json.dumps(variables)))
                print(nextUrl)
                browser.get(nextUrl)

            pre = browser.execute_script("return document.getElementsByTagName('pre')[0].textContent")
            data = json.loads(pre)['data']
            hasNext = data['user']['edge_followed_by']['page_info']['has_next_page']
            endCursor = data['user']['edge_followed_by']['page_info']['end_cursor']
            variables['after'] = endCursor

            print(take)
            take += 1

            for user in data['user']['edge_followed_by']['edges']:
                followed.append(user['node']['username'])
            sleep(1)

    except NoSuchElementException:
        print("NO PRE element")

    with open("data/meFollowed.txt", "w+") as file:
    	for follower in followed:
            file.write("%s\n" % str(follower))

    file.close()


def getFollowing(browser):
    variables = {}
    variables['id'] = "2120585971"
    variables['first'] = 50
    hasNext = True
    endCursor = None
    following = []
    take = 1
    url = "https://www.instagram.com/graphql/query?query_hash=58712303d941c6855d4e888c5f0cd22f&variables={}".format(str(json.dumps(variables)))

    browser.get(url)

    try:
        while hasNext is True:
            if endCursor is not None:
                nextUrl = "https://www.instagram.com/graphql/query?query_hash=58712303d941c6855d4e888c5f0cd22f&variables={}".format(str(json.dumps(variables)))
                print(nextUrl)
                browser.get(nextUrl)

            pre = browser.execute_script("return document.getElementsByTagName('pre')[0].textContent")
            data = json.loads(pre)['data']

            hasNext = data['user']['edge_follow']['page_info']['has_next_page']
            endCursor = data['user']['edge_follow']['page_info']['end_cursor']
            variables['after'] = endCursor

            print(take)
            take += 1

            for user in data['user']['edge_follow']['edges']:
                following.append(user['node']['username'])

            sleep(1)

    except NoSuchElementException:
        print("NO PRE element")

    with open("data/meFollowing.txt", "w+") as file:
    	for follower in following:
            file.write("%s\n" % str(follower))

    file.close()


# TODO
# mixup usernames
def getNonfollowers():
	nonFollowers = []
	followers = []
	usersImFollowing = []
	usersFollowingMe = []

	with open("data/meFollowing.txt", 'r') as following:
		usersImFollowing = following.readlines()

	with open("data/meFollowed.txt", 'r') as followed:
		usersFollowingMe = followed.readlines()

	following.close()
	followed.close()

	for user in usersImFollowing:
		if user not in usersFollowingMe:
			nonFollowers.append(user)
		else:
			followers.append(user)

	with open("data/nonFollowers.txt", "w+") as nonfollowfile:
		for item in nonFollowers:
			nonfollowfile.write("%s" % str(item))

	nonfollowfile.close()

	for user in followers:
		print(user)

def unfollowUsers(browser, logger):
	baseUrl = "https://www.instagram.com/"
	removeUserList = []
	removedUserList = []
	unfollow_list_path = "data/remove.txt"

	unfollow_button_class_name = '_5f5mN    -fzfL     _6VtSN     yZn4P   '
	unfollow_button_class_name2 = 'BY3EC  sqdOP  L3NKy    _8A5w5    '

	SLEEP_TIME = 30

	removeIndex = 1
	removeCount = 0


	with open(unfollow_list_path, "r")  as removeUsersFile:
		removeUserList = removeUsersFile.readlines()

	removeUsersFile.close()

	for userName in removeUserList:	
		if userName is "":
			print("username is blank")
			continue

		userLink = (baseUrl + userName)
		browser.get(userLink)
		removeIndex += 1

		sleep(random.randint(2,6))

		try:
			try:
				browser.execute_script("document.getElementsByClassName('{}')[0].click()".format(unfollow_button_class_name))
			except JavascriptException as jsException:
				print("error while unfollow click, try another button script")
				try:
					browser.execute_script("document.getElementsByClassName('{}')[0].click()".format(unfollow_button_class_name2))
				except JavascriptException:
					print("Can't click, user prob already unfollowed, continue")
					continue

			browser.execute_script("document.getElementsByClassName('aOOlW -Cab_   ')[0].click()")

			# check if removing is going good
			if removeIndex % 5 == 0:
				browser.refresh()
				sleep(1)
				browser.refresh()
				sleep(1)

				element = browser.execute_script("return document.getElementsByClassName('_5f5mN    -fzfL     _6VtSN     yZn4P   ')[0]")

				if element == None:
					print("unsubscring going cool, continue")

				else:
					print("WARNING CANT UNSUBSCIRBE, ABORT!! removed: {}".format(removeCount))
					# TODO or maybe have a continueFlag that unlocks or blocks function blocks later
					return

			removeCount += 1

			# user removed, pop it from list
			removedUserList.append(userName)

			# write users remain to unfollow
			with open(unfollow_list_path, "w") as removeUsersFile:
				for user in list(set(removeUserList).difference(removedUserList)):
					removeUsersFile.write(user)

			removeUsersFile.close()

			logger.info("{}. removed user: {}".format(removeIndex, userName))
			sleep(SLEEP_TIME + abs(random.gauss(20,5)))

		except NoSuchElementException as exception:
			print('NoSuchElementException')

	logger.info("Session ended, removed: {}, could not remove {} users".format(len(removedUserList), len(removeUserList) - len(removedUserList)))


def likePosts(browser, logger, amount):
	scrollHeight = 100
	int_post_liked = 0
	scrollTime = 0.4
	

	userName = ''
	prevUserName = ''
	postValid = None

	while amount > int_post_liked:

		while userName == prevUserName:
			browser.execute_script("window.scrollBy(0, {})".format(scrollHeight))

			article = browser.execute_script("return document.getElementsByTagName('article')[4]")

			try:
				# userName = article.find_element_by_xpath('.//header/div[2]/div[1]/div/h2/a').text
				userName = article.find_element_by_xpath('.//header/div[2]/div[1]/div/a').text
			except NoSuchElementException:
				# the post is a hastag
				userName = article.find_element_by_xpath('.//header/div[2]/div[2]/div[1]/a').text

			sleep(scrollTime)

		prevUserName = userName

		try:
			postText = article.find_element_by_xpath('.//div[2]/div[1]/div/div/span/span[1]').text
		except NoSuchElementException:
			print('[Warning] Cant find postText')
			postValid = True

		if postValid == None:
			postValid = checkFollowedUserPost(postText) 

		if not postValid:
			print("[invalid post text], next post")
			continue

		flagRecentlyLikedPost = checkRecentLikeDate(userName) # last like was..
		flagPostLikeCount, likeCount = checkPostLikeCount(article, userName)

		if  flagRecentlyLikedPost and flagPostLikeCount:
			try:
				buttonLike = article.find_elements_by_class_name(like_code)[0]

				# send keys is workaround for click() function not working here for some reason
				buttonLike.send_keys("\n")
				int_post_liked +=  1

				logger.info('liking image: {}. {}'.format(int_post_liked, userName))
				
				sleep(random.randint(100,300)/100.0)
			except NoSuchElementException:
				print("Post already liked, user: {}".format(userName))
		else:
			if not flagRecentlyLikedPost:
				print("User was liked within last 3 days, next post")

			elif not flagPostLikeCount:
				print('Post has too many likes ({}) or cant get likes count'.format(likeCount))

			continue
		
		likeCounter(userName)

		sleep(3)

		browser.execute_script("window.scrollBy(0, {})".format(300))


def checkFollowedUserPost(postText):
	postValid = True
	
	listPostWords = postText.split(' ')

	for postWord in listPostWords:
		for badWord in excludes:
			if postValid and re.search(badWord, postWord):
				print("found bad word: {}".format(postWord))
				postValid = False
				break

	return postValid


def likeCounter(userLiked):
	file_path = 'data/likes.csv'

	write_lines = []
	userName = userLiked
	flagNewUser = True
	currentDate = str(date.today())

	with open(file_path, "r+") as csvFile:
		lines = csvFile.readlines()

	csvFile.close()

	for l in lines:
		record = ''

		columns = l.split(';')
		if columns[1] == userName:
			flagNewUser = False

			columns[0] = currentDate
			columns[2] = str(int(columns[2]) + 1)

			for column in columns:
				record += column.strip() + ';'

			record = record[:-1]
			record += '\n'

			write_lines.append(record)
		else:
			write_lines.append(l)

	if flagNewUser:
		record = (currentDate + ';' + userName + ';' + '1;\n')
		write_lines.append(record)

	with open(file_path, "w+") as csvFile:
		for line in write_lines:
			csvFile.write(line)

	csvFile.close()

def checkRecentLikeDate(username):
	flagLikePost = True
	file_path = 'data/likes.csv'
	userName = username
	min_day_difference = 3
	date_format = '%Y-%m-%d'
	day_difference = None

	with open(file_path, "r+") as csvFile:
		likeRecords = csvFile.readlines()

	csvFile.close()

	for record in likeRecords:
		columns = record.split(';')

		if columns[1] == userName:
			strLastLikeDate = columns[0]
			datetimeLastLikeDate = datetime.strptime(strLastLikeDate, date_format)
			today = date.today()
			day_difference = (today - datetimeLastLikeDate.date()).days

			print(('checkRecentLikeDate() | last like was: ' + str(day_difference)))	

			break

	if day_difference is not None and day_difference < min_day_difference:
		flagLikePost = False

	return flagLikePost



def checkPostLikeCount(article, userName):
	result = False
	like_count = 0

	try:
		# if len(article.find_elements_by_class_name('sqdOP')) == 1:
		# 	print('[INFO] checkPostLikeCount() | post is a video or a hashtag, next')
		# 	return False, 0

		like_count = article.find_elements_by_class_name('sqdOP')[1]
		
		# pares like txt for case when sbdy liked post
		if like_count.text == '' or like_count == 'Opublikuj':
			# like_count = article.find_elements_by_class_name('sqdOP')[1].find_element_by_xpath('.//span').text
			str_like_count = article.find_elements_by_class_name('sqdOP ')[2].text.replace(' ', '')

			cut_index = 0
			for c in str_like_count:
				if c.isdigit():
					cut_index += 1

			like_count = str_like_count[:cut_index]

			print("checkPostLikeCount() | {}".format(like_count))
		else:
			like_count = like_count.text
		result = True
	except NoSuchElementException:
		try:
			like_count = article.find_element_by_xpath('//div[2]/section[2]/div/div/button/span').text
			# like_count = article.find_elements_by_class_name('sqdOP')[9].find_elements_by_tag
			result = True
		except:
			print("[INFO] checkPostLikeCount() | cant get likes from xpath")
			result = False
	

	if result == True:
		try:
			like_count = str(like_count).replace(' ', '').split(':')[1]
			like_count = int(like_count)
			
			if like_count < min_like_count or like_count > max_like_count:
				result = False
		except:
			result = False
			print("[INFO] ({}) something wrong with xpath: '{}'".format(userName, like_count))
	else:
		print("[Error] cant get like count")

	return result, like_count


def follow(browser, logger, amount):
	SLEEP_TIME = 30
	SCROLL_HEIGHT = 370
	follow_counter = 0
	post = 0

	post_code = 'eLAPa'
	username_code = 'sqdOP '

	buttons = None
	userName = None

	while follow_counter < amount:
		# scroll page
		if post % 3 == 0:
			scroll(browser, SCROLL_HEIGHT)

		post += 1

		try: 
			article = browser.execute_script("return document.getElementsByClassName('{}')[{}].click()".format(post_code, (post % 3) + 35))

			try:
				userName = browser.execute_script("return document.getElementsByClassName('{}')[1].href".format(username_code))
			except JavascriptException:
				print("chuja a nie username")
				
			userNameValid = validUsername(userName)

			sleep(r(1,100)/100.0 + r(1,2))
			
			# check post likeHashtagPosts
			postValid = checkPostData(browser, False)
			
			if postValid and userNameValid:
				# try to follow, if user already followed go next post
				try:
					browser.execute_script("document.getElementsByClassName('oW_lN sqdOP yWX7d    y3zKF     ')[0].click()")
					sleep(r(1,3) + 1)
					# like image
					browser.execute_script("document.getElementsByClassName('wpO6b ')[0].click()")
				except JavascriptException:
					print("already following! like and close image")
					browser.execute_script("document.getElementsByClassName('wpO6b ')[0].click()")
					
					sleep(r(1,7) + 1)
					exitPost(browser)
					
					continue

				logger.info("{}. followed user: {}".format(follow_counter, userName))
				follow_counter += 1
				sleep(r(30,50))

				# get username from post and save it in file
				with open("ifollow.txt", "a+") as users:
					users.write("%s;%s\n" % (str(date.today()), str(userName)))

				users.close()

				# close user window
				sleep(r(1,2) + 1)
				
				exitPost(browser)
				# sleep(r(1,2) + 1)
				sleep(1)


			else:
				# post invalid, close user window
				print("post invalid for user: {}, username valid? {}".format(userName, userNameValid))
					
				exitPost(browser)

				sleep(r(1,100)/10.0 + 1)

				continue

		except NoSuchElementException as exception:
			print("[ERROR] NoSuchElementException: \r\n{}".format(exception))
			browser.refresh()

		except JavascriptException as exception:
			# user deleted image, close empty window
			print("[ERROR] JS exception: \r\n{}".format(exception) )
			sleep(1.5)
			exitPost(browser)

		sleep(3)


def checkPostData(browser, flagPrint = True):
	postValid = True
	strPostDescription = None

	try:
		strPostDescription  = browser.find_element_by_xpath('.//div[2]/div[1]/ul/div/li/div/div/div[2]/span').text
	except NoSuchElementException:
		try:
			strPostDescription  = browser.find_element_by_xpath('.//div[2]/div[1]/ul/ul[1]/div/li/div/div[1]/div[2]/span').text
		except Exception:
			print("[Error] checkPostData | Cannot find post description")
			postValid = False

	if postValid is not False:
		if flagPrint:
			print(strPostDescription)
		listPostWords = strPostDescription.split(' ')

		for postWord in listPostWords:
			for badWord in excludes:
				if re.search(badWord, postWord):
					print("checkPostData | found bad word: {}".format(postWord))
					postValid = False
					return False

	return postValid


def likeHashtagPosts(browser, log, like_amount, startOffset):
	SCROLL_HEIGHT = 400
	like_code = 'wpO6b '
	username_code = 'sqdOP '
	post_counter = 0
	like_counter = 1

	try: 
		while like_counter < like_amount:
			if post_counter % 3 == 0:
				scroll(browser, SCROLL_HEIGHT)
				print('>>>>>>>>>>>\t\tscrolll timeeeeeee: {}'.format(post_counter))
				post_counter = 0

			browser.execute_script("document.getElementsByClassName(\"KL4Bh\")[{}].click()".format(post_counter + startOffset+1 ))
			sleep(r(1,100)/100.0 + r(2,4))
			post_counter += 1
			
			# check post hashtags
			postValid = checkPostData(browser)

			if not postValid:
				sleep(r(1,100)/10.0 + 1)

				continue

			browser.execute_script("document.getElementsByClassName('{}')[0].click()".format(like_code))
			sleep(r(1,7) + 1)

			# get username from post and save it in file
			# TODO add timestamp
			username = browser.execute_script("return document.getElementsByClassName('{}')[1].href".format(username_code))
			print("{}. Post valid: {} for user: {}".format(like_counter, postValid, username))
			
			with open("likedImage.txt", "a+") as users:
				users.write("%s;%s\n" % (str(date.today()), str(username)))

			users.close()

			print('>>>>>>>>> \t\t counter check: {}'.format(post_counter))
			like_counter += 1


			# close user window
			exitPost(browser)
			sleep(r(4,10))


	except NoSuchElementException as exception:
		print(exception)
		browser.refresh()

	except JavascriptException as exception:
		# click blind spot to exit
		exitPost(browser)
		print('exit post')
		print(exception)


def exitPost(browser):
	browser.execute_script('document.elementFromPoint(10, 10).click()')

def scroll(browser, height = 350):
	browser.execute_script("window.scrollBy(0,%s)" % height)

def validUsername(username):

	for badWord in invalid_names:
			if re.search(badWord, username):
				return False

	return True