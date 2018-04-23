import unittest
from unittest.mock import patch, Mock

from repo_version_compare import get_version_compare_url


class TestRepoCompare(unittest.TestCase):

    def test_url_with_versions_is_returned(self):

        with patch('repo_version_compare.g') as github:
            # Given
            get_repo = Mock()

            previous_version = Mock()
            previous_version.name = '0.0.1'

            latest_version = Mock()
            latest_version.name = '0.0.2'

            get_repo.get_tags.return_value = [previous_version, latest_version]
            github.get_repo.return_value = get_repo

            # When
            url = get_version_compare_url('myrepo')

            # Then
            assert url == 'https://github.com/ONSdigital/myrepo/compare/0.0.1...0.0.2'


    def test_no_versions_found_in_repo(self):

        with patch('repo_version_compare.g') as github:
            # Given
            get_repo = Mock()

            get_repo.get_tags.return_value = []

            github.get_repo.return_value = get_repo

            with self.assertRaises(SystemExit):
                get_version_compare_url('myrepo')


    def test_latest_version_only(self):

        with patch('repo_version_compare.g') as github:
            # Given
            get_repo = Mock()

            latest_version = Mock()
            latest_version.name = '0.0.1'

            get_repo.get_tags.return_value = [latest_version]
            github.get_repo.return_value = get_repo

            # When
            url = get_version_compare_url('myrepo')

            # Then
            assert url == 'https://github.com/ONSdigital/myrepo/compare/master...0.0.1'
