import json

import os
import requests
from github import Github

g = Github()

def get_version_compare_url(respository_name):
    repo = g.get_repo(f'ONSdigital/{respository_name}')
    tags = repo.get_tags()

    tag_names = [tag.name for tag in tags]
    tag_names.sort(key=lambda version: list(map(int, version.split('.'))), reverse=True)

    if len(tag_names) == 0:
        print(f'No current or previous versions found in {repo}.')
        exit(1)
    elif len(tag_names) == 1:
        latest_version = tag_names[0]
        previous_version = 'master'
    else:
        latest_version = tag_names[0]
        previous_version = tag_names[1]
    return f'https://github.com/ONSdigital/{respository_name}/compare/{previous_version}...{latest_version}'


repos = ['concourse-demo-java-service',
         'concourse-demo-python-service']

if os.getenv('SLACK_HOOK') == None:
    print('Environment variable SLACK_HOOK not set')
    exit(2)

for repo in repos:
    url = get_version_compare_url(repo)
    requests.post(os.getenv('SLACK_HOOK'),
                  data=json.dumps({"text": f'Commit diff {repo}: {url}'}))
