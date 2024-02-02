from git import getOrgFollowers, unfollowGitUsers, followGitUsers

cncfFollowers = getOrgFollowers('cncf')
kubernetesFollowers = getOrgFollowers('kubernetes')
argoprojFollowers = getOrgFollowers('argoproj')

listToFollow = list(set(cncfFollowers) | set(kubernetesFollowers) | set(argoprojFollowers))

followGitUsers(listToFollow)
print(f'following new {len(listToFollow)} users')

unfollowGitUsers(['kubernetes', 'cncf', 'argoproj'])
followGitUsers(['kubernetes', 'cncf', 'argoproj'])