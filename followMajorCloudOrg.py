from git import getOrgFollowers, unfollowGitUsers, followGitUsers, getMyGitFollowing

unfollowGitUsers(['kubernetes', 'cncf', 'argoproj'])
followGitUsers(['kubernetes', 'cncf', 'argoproj'])

cncfFollowers = getOrgFollowers('cncf')
kubernetesFollowers = getOrgFollowers('kubernetes')
argoprojFollowers = getOrgFollowers('argoproj')
alreadyFollowing = getMyGitFollowing()

listToFollow = list(set(cncfFollowers) | set(kubernetesFollowers) | set(argoprojFollowers))
listToFollow = list(set(listToFollow) - set(alreadyFollowing))

followGitUsers(listToFollow)
print(f'following new {len(listToFollow)} users')