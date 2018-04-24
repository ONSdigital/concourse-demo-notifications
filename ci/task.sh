#!/usr/bin/env bash
pipenv install
pipenv run python repo_version_compare.py ${SLACK_HOOK} ${REPO_NAME}