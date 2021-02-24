#!/bin/python3
#######################################################
# Many GitHub projects don't have the .gitgnore file  #
# Create a pull requests to all of them               #
# author Carlos Bilbao 2021                           #
# Contact: bilbao at vt.edu                           #
#######################################################

import requests, simplejson, os, json
from os import path

# Max size to clone a repository
MAX_REPOSITORY_SIZE = 600

# File with users name
FILE='users.json'

def commit(url,clone_url, language):

	# Retrieve repo name and owner
	repo_name = url.split('/')
	owner = repo_name[len(repo_name)-2].split(':')
	owner = owner[1]
	repo_name = repo_name[len(repo_name) - 1]
	repo_name = repo_name[:len(repo_name) - 4]

	# Make HUB_VERBOSE=true for verbose HTTP query
	pull='hub pull-request --push -b '+owner+':master -h Zildj1an:ig'
	pull = pull + ' -m "Added necessary .gitignore file" '
	pull = pull + ' -m "Request autogenerated with https://github.com/Zildj1an/ignores"'
	pull = pull + ' -m "Signed-off-by: Carlos Bilbao <bilbao@vt.edu>"'
	
	os.system('hub clone ' + url)

	# Check if there is already a .gitgnore file
	if not path.exists(repo_name + '/.gitignore'):
		
		os.chdir(repo_name)
		os.system('git checkout -b ig')

		# TODO Extend this to all the programming languages.
		if language == 'C' or language == 'C++':
			ignore_file = 'ignore_c'
		elif language == 'Java':
			ignore_file = 'ignore_java'
		else:
			ignore_file = 'ignore_py'

		os.system('cp ../git_ignores/' + ignore_file + ' ./.gitignore')
		os.system('git add .gitignore')
		os.system('git commit -S -m "Improved the project with a .gitignore file"')
	
		if os.system('hub fork') == 0:
			ret = os.system(pull)
			if ret == 0:
				print('PULLED ' + url)
				# Save the name to remove the fork in the future
				f = open('../log_repos','a')
				f.write(url + '\n')
				f.close()
			else:
				print('The pull request failed!')
		else:
			print('Forking with hub failed!')		

		os.chdir('../')

	os.system('rm -rf '+ repo_name)

# Retrieve all GitHub users until 2015
# TODO Use GitHub API for updated information by chunks
#f = open(FILE) 
#users = []
#lines = f.read().splitlines()
#f.close()
#for user in lines:
#	users.append(user)

with open(FILE) as f:
  users = json.load(f)

for _USER in users:

	USER = _USER['login']
	url = 'https://api.github.com/users/' + USER + '/repos?per_page=1000'
	r = requests.get(url)
	json = r.json()

	i = 0

	while i < len(json):

		try:
			repo = json[i]['ssh_url']
		except KeyError:
			i = i + 1
			continue;	

		if json[i]['size'] <= MAX_REPOSITORY_SIZE or True:
			if json[i]['private'] != 'true':
				language = json[i]['language']
				if language=='C' or language=='Python' or language=='Java' or language =='C++':
					commit(repo, json[i]['clone_url'],language)
		i = i + 1
	# TODO remove forks after pull requests are accepted

