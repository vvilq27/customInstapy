import json
from selenium.common.exceptions import NoSuchElementException, JavascriptException
from time import sleep
import random
import csv
import re
from datetime import date

excludes = ["dziecko", "hotel", "hotelspa", "spa", "zabiegi", "butik", "fashionblogger", 
"mama", "nails", "studio", "kosmetyki", "krem", "fryzjer", "wellhair", "moda", "paznokcie", "salon", "sklep", 
"mum", "maluch", "420", "memes", "mem", "memy", "clinic", "klinika", "polskichlopak", "brwi", "brows", "suchar",
"brzuszku", "brzuszek", "ciąża"]


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

def unfollowUsers(browser):
	baseUrl = "https://www.instagram.com/"
	removeUserList = []
	removedUserList = []
	unfollow_list_path = "data/remove.txt"

	unfollow_button_class_name = '_5f5mN    -fzfL     _6VtSN     yZn4P   '
	unfollow_button_class_name2 = 'BY3EC  sqdOP  L3NKy    _8A5w5    '

	# browser.get((baseUrl + "arasssu/"))
	# currentFollowedCount = browser.execute_script("return document.getElementsByClassName('g47SY ')[2].textContent")
	# print("Current follow count: {}".format(currentFollowedCount))

	removeIndex = 1
	removeCount = 0


	with open(unfollow_list_path, "r")  as removeUsersFile:
		removeUserList = removeUsersFile.readlines()

	removeUsersFile.close()

	for userName in removeUserList:
		print(userName)
		
		lastUser = True if removeUserList.index(userName) == len(removeUserList) - 1 else False

		print(( str(removeUserList.index(userName)) + ' ' + str(len(removeUserList)) + ' ' + str(lastUser) ))

		if userName is "":
			print("username is blank")
			continue

		print("{}. removing user: {}".format(removeIndex, userName))
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

			sleep(random.randint(2,5))
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

			# if its last element then skip waiting
			if lastUser:
				sleepTime = max(5, random.gauss(20,15))
				print("Sleeping for: {}".format(sleepTime))
				sleep(sleepTime)

		except NoSuchElementException as exception:
			print('NoSuchElementException')

	print("Session ended, removed: {}, could not remove {} users".format(len(removedUserList), len(removeUserList) - len(removedUserList)))


def likePosts(browser, logger, amount):
	listUserNames = []
	scrollHeight = 150
	# TODO
	# change for loop to while until amount is liked
	# like first post
	# catch when already liked

	userName = ''
	prevUserName = ''
	postValid = None

	# TODO add csv stats
	# with open('likestats.csv', 'a+') as csv:
	for i in range(amount):

		while userName == prevUserName:
			browser.execute_script("window.scrollBy(0, {})".format(scrollHeight))

			# article = browser.execute_script("return document.getElementsByTagName('article')[4]")
			article = browser.execute_script("return document.getElementsByTagName('article')[4]")
			
			userName = article.find_element_by_xpath('.//header/div[2]/div[1]/div/h2/a').text

			sleep(0.15)

		logger.info(userName)
		prevUserName = userName

		try:
			postText = article.find_element_by_xpath('.//div[2]/div[1]/div/div/span/span[1]').text
		except NoSuchElementException:
			postValid = True

		if postValid == None:
			postValid = checkFollowedUserPost(postText)

		print(("Is post valid? " +  str(postValid)))

		if not postValid:
			print("invalid, next post")
			continue

		if userName not in listUserNames:
			try:
				print('liking image...')
				# buttonLike = article.find_elements_by_tag_name('button')[0]

				buttonLike = article.find_elements_by_class_name('wpO6b')[0]

				# send keys is workaround for click() function not working here for some reason
				buttonLike.send_keys("\n")
				
				sleep(random.randint(100,300)/100.0)
			except NoSuchElementException:
				print("Post already liked, user: {}".format(userName))
		else:
			print('User  {}  already liked in this session'.format(userName))


		listUserNames.append(userName)
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
				return postValid

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