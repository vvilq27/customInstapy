import json
from selenium.common.exceptions import NoSuchElementException, JavascriptException
from time import sleep
import random

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

	browser.get((baseUrl + "arasssu/"))
	currentFollowedCount = browser.execute_script("return document.getElementsByClassName('g47SY ')[2].textContent")
	print("Current follow count: {}".format(currentFollowedCount))

	with open("data/remove.txt", "r")  as removeUsersFile:
		removeUserList = removeUsersFile.readlines()

	removeUsersFile.close()

	removeIndex = 1
	removeCount = 0

	for username in removeUserList:
		if username is "":
			continue
		print("{}. removing user: {}".format(removeIndex, username))
		userLink = (baseUrl + username)
		browser.get(userLink)
		removeIndex += 1
		sleep(random.randint(2,6))

		try:
			try:
				browser.execute_script("document.getElementsByClassName('_5f5mN    -fzfL     _6VtSN     yZn4P   ')[0].click()")
			except JavascriptException as jsException:
				print("error while unfollow click, try another button script")
				try:
					browser.execute_script("document.getElementsByClassName('BY3EC  sqdOP  L3NKy    _8A5w5    ')[0].click()")
				except JavascriptException:
					print("User already unfollowed, continue")
					continue

			sleep(random.randint(2,5))
			browser.execute_script("document.getElementsByClassName('aOOlW -Cab_   ')[0].click()")

			# check if removing is going good
			if removeIndex % 5 == 0:
				browser.refresh()
				sleep(3)
				browser.refresh()
				sleep(2)

				element = browser.execute_script("return document.getElementsByClassName('_5f5mN    -fzfL     _6VtSN     yZn4P   ')[0]")

				if element == None:
					print("unsubscribed, continue")
				else:
					print("WARNING CANT UNSUBSCIRBE, ABORT!! removed: {}".format(removeCount))
					return

			removeCount += 1

			sleepTime = max(5, random.gauss(30,15))
			print("Sleeping for: {}".format(sleepTime))
			sleep(sleepTime)

		except NoSuchElementException as exception:
			pass

	print("Session ended, removed: {}".format(removeCount))