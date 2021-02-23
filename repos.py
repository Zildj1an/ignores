#!/bin/python3
#######################################################
# Many GitHub projects don't have the .gitgnore file  #
# Create a pull requests to all of them               #
# author Carlos Bilbao 2021                           #
# Contact: bilbao at vt.edu                           #
#######################################################

import requests, simplejson, os
from os import path

# Max size to clone a repository
MAX_REPOSITORY_SIZE = 600

def commit(url,clone_url, language):
	# Retrieve repo name and owner
	repo_name = url.split('/')
	owner = repo_name[len(repo_name)-2].split(':')
	owner = owner[1]
	repo_name = repo_name[len(repo_name) - 1]
	repo_name = repo_name[:len(repo_name) - 4]

	pull='HUB_VERBOSE=true hub pull-request --push -b '+owner+':master -h Zildj1an:ig'
	pull = pull + ' -m "Added necessary .gitgnore file"'
	
	os.system('HUB_VERBOSE=true hub clone ' + url)

	# Check if there is already a .gitgnore file
	if not path.exists(repo_name + '/.gitignore'):
		
		os.chdir(repo_name)
		os.system('git checkout -b ig')
		# TODO Extend this to all the programming languages.
		ignore_file = 'ignore_c'
		os.system('cp ../git_ignores/ ' + ignore_file + './.gitignore')
		os.system('git add .gitignore')
		os.system('git commit -S -m "Improved the project with a .gitignore file"')
	
		if os.system('hub fork') == 0:
#			os.system('git push')
			ret = os.system(pull)
			if ret == 0:
				# Save the name to remove the fork in the future
				f = open("log_repos", "a")
				f.write(url+'\n')
				f.close()
			else:
				print('The pull request failed!')
		else:
			print('Forking with hub failed!')		

		os.chdir('../')

	os.system('rm -rf '+ repo_name)

# TODO Retrieve all GitHub users by chunks
users = ['dong-seop']

for USER in users:

	url = 'https://api.github.com/users/' + USER + '/repos?per_page=1000'
	r = requests.get(url)
	json = r.json()

	i = 0

	while i < len(json):

		repo = json[i]['ssh_url']
	
		if json[i]['size'] < MAX_REPOSITORY_SIZE:
			if json[i]['private'] != 'true':
				if json[i]['language'] == 'C':
					commit(repo, json[i]['clone_url'])
		i = i + 1

	# TODO remove forks after pull requests are accepted

