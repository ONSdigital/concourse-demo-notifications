import json
import argparse
import re

import requests
import sys
from github import Github
import validators

g = Github()
semantic_version_regex = re.compile('\d+\.\d+\.\d+')


def get_version_compare_url(respository_name):
    repo = g.get_repo(f'ONSdigital/{respository_name}')
    tags = repo.get_tags()

    tag_names = [tag.name for tag in tags if semantic_version_regex.match(tag.name)]
    tag_names.sort(key=lambda version: list(map(int, version.split('.'))), reverse=True)

    if len(tag_names) == 0:
        print(f'No current or previous versions found in {respository_name}.')
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
        raise argparse.ArgumentTypeError('Slack hook URL is malformed. Please check and try again.')
    return url


def parse_args(args):
    parser = argparse.ArgumentParser(description='Send notification via Slack of version diffs')
    parser.add_argument('slack_hook', type=valid_slack_hook,
                        help='a URL for the Slack webhook')
    parser.add_argument('repo_name', type=str,
                        help='git respository name')
    return parser.parse_args(args)


if __name__ == '__main__':

    args = parse_args(sys.argv[1:])

    url = get_version_compare_url(args.repo_name)
    requests.post(args.slack_hook,
                  data=json.dumps({"text": f'Release notes for {args.repo_name}: {url}'}))