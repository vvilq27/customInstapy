import json
from selenium.common.exceptions import NoSuchElementException
from time import sleep

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

    with open("meFollowed.txt", "w+") as file:
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

    with open("meFollowing.txt", "w+") as file:
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

	with open("meFollowing.txt", 'r') as following:
		usersImFollowing = following.readlines()

	with open("meFollowed.txt", 'r') as followed:
		usersFollowingMe = followed.readlines()

	following.close()
	followed.close()

	for user in usersImFollowing:
		if user not in usersFollowingMe:
			nonFollowers.append(user)
		else:
			followers.append(user)

	with open("nonFollowers.txt", "w+") as nonfollowfile:
		for item in nonFollowers:
			nonfollowfile.write("%s" % str(item))

	nonfollowfile.close()

	for user in followers:
		print(user)

def unfollowUsers(browser):
	baseUrl = "https://www.instagram.com/"
	removeUserList = []

	with open("remove.txt", "r")  as removeUsersFile:
		removeUserList = removeUsersFile.readlines()

	removeUsersFile.close()


	for username in removeUserList:
		userLink = (baseUrl + username)
		browser.get(userLink)
		sleep(2)

		try:
			browser.execute_script("document.getElementsByClassName('_5f5mN    -fzfL     _6VtSN     yZn4P   ')[0].click()")
			sleep(1.2)
			browser.execute_script("document.getElementsByClassName('aOOlW -Cab_   ')[0].click()")
			sleep(4)
		except NoSuchElementException as exception:
			pass