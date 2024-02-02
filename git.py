from environments import GH_USERNAME, GH_TOKEN
import requests
from bs4 import BeautifulSoup

def recursiveRequestToGit(url, max_users=float('inf')):
    url = url + '?per_page=30'
    objs = []

    while len(objs) < max_users:
        response = requests.get(url, auth=(GH_USERNAME, GH_TOKEN))

        if response.status_code == 200:
            obj = response.json()
            objs.extend(obj)

            # 다음 페이지 URL 확인
            if 'next' in response.links.keys():
                url = response.links['next']['url']
            else:
                break
        else:
            print(f"Error: {response.status_code}")
            break
    print (len(objs))
    objs = [obj['login'] for obj in objs]
    
    return objs

def getMyGitFollowers():
    url = f'https://api.github.com/users/{GH_USERNAME}/followers'
    all_followers = recursiveRequestToGit(url)
    return all_followers


def getMyGitFollowing():
    url = f'https://api.github.com/users/{GH_USERNAME}/following'
    all_following = recursiveRequestToGit(url)
    return all_following

def getNotFollowingBackUsers():
    followers = getMyGitFollowers()
    following = getMyGitFollowing()
    not_following_back_users = list(set(following) - set(followers))
    return not_following_back_users

def unfollowGitUsers(not_following_back):
    for user in not_following_back:
        url = f'https://api.github.com/user/following/{user}'
        response = requests.delete(url, auth=(GH_USERNAME, GH_TOKEN))
        if response.status_code == 204:
            print(f'{user} is unfollowed')
        else:
            print(f'Error: {response.status_code}')

def followGitUsers(users):
    for user in users:
        url = f'https://api.github.com/user/following/{user}'
        response = requests.put(url, auth=(GH_USERNAME, GH_TOKEN))
        if response.status_code == 204:
            print(f'{user} is followed')
        else:
            print(f'Error: {response.status_code}')

def parseOrgFollowersPageAndGetFollowers(html):
    soup = BeautifulSoup(html, 'html.parser')
    followers = soup.find_all('span', class_='Link--secondary pl-1')
    followers = [follower.text for follower in followers]
    return followers

def getOrgFollowers(org):
    orgFollowers = []

    for page in range(1, 4):
        url = f"https://github.com/orgs/{org}/followers?page={page}"
        response = requests.get(url)
        if response.status_code == 200:
            pageFollowers = parseOrgFollowersPageAndGetFollowers(response.text)
            orgFollowers.extend(pageFollowers)
        else:
            print(f"Error: {response.status_code}")
            break
    return orgFollowers