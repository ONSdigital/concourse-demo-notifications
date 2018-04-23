import json
import argparse
import os

import requests
from github import Github
import validators

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


def valid_slack_hook(url):
    if not validators.url(url):
        print('Slack hook URL is malformed. Please check and try again')
        exit(2)


if os.getenv('SLACK_HOOK') is None:
    print('Environment variable SLACK_HOOK not set')
    exit(3)


parser = argparse.ArgumentParser(description='Send notification via Slack of version diffs')

parser.add_argument('slack_hook', type=valid_slack_hook,
                    help='a URL for the Slack webhook')

parser.add_argument('repo_name', type=str,
                    help='git respository name')

args = parser.parse_args()

url = get_version_compare_url(args.repo_name)
requests.post(os.getenv('SLACK_HOOK'),
              data=json.dumps({"text": f'Commit diff {args.repo_name}: {url}'}))
