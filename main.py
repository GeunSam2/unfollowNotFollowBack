import requests
import os

username = os.environ.get('GH_USERNAME')
token = os.environ.get('GH_TOKEN')
white_list = os.environ.get('UNFOLLOW_WHITE_LIST')
white_list = white_list.split(',')

def recursiveRequestToGit(url):
    objs = []

    while True:
        response = requests.get(url, auth=(username, token))

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
    objs = [obj['login'] for obj in objs]
    
    return objs

def getFollowers():
    url = f'https://api.github.com/users/{username}/followers'
    all_followers = recursiveRequestToGit(url)
    return all_followers


def getFollowing():
    url = f'https://api.github.com/users/{username}/following'
    all_following = recursiveRequestToGit(url)
    return all_following


def getNotFollowingBack():
    followers = getFollowers()
    following = getFollowing()
    not_following_back = list(set(following) - set(followers))
    return not_following_back

def unfollow(not_following_back):
    for user in not_following_back:
        url = f'https://api.github.com/user/following/{user}'
        response = requests.delete(url, auth=(username, token))
        if response.status_code == 204:
            print(f'{user} is unfollowed')
        else:
            print(f'Error: {response.status_code}')

not_following_back = getNotFollowingBack()
not_following_back = list(set(not_following_back) - set(white_list))

unfollow(not_following_back)
print(f'Unfollowed {len(not_following_back)} users')