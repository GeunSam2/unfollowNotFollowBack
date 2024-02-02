from git import getNotFollowingBackUsers, unfollowGitUsers, getOrgFollowers
from environments import UNFOLLOW_WHITE_LIST

unfollow_white_list = UNFOLLOW_WHITE_LIST.split(',')

not_following_back = getNotFollowingBackUsers()
not_following_back = list(set(not_following_back) - set(unfollow_white_list))

unfollowGitUsers(not_following_back)
print(f'Unfollowed {len(not_following_back)} users')