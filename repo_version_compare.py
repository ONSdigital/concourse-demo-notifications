from github import Github


def get_version_compare_url(repo):
    g = Github()
    tags = g.get_repo(f'ONSdigital/{repo}').get_tags()
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
    return f'https://github.com/ONSdigital/{repo}/compare/{previous_version}...{latest_version}'


repos = ['concourse-demo-java-service',
         'concourse-demo-python-service']

for repo in repos:
    print(repo, get_version_compare_url(repo))
