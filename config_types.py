from typing import NamedTuple, List
import requests
import http
import logging

import validators


class GithubRepository(NamedTuple):
    username: str
    name: str

    def validate(self):
        uri = f'https://github.com/{self.username}/{self.name}'

        try:
            resp = requests.head(uri, timeout=5)
        except requests.RequestException:
            logging.exception(f'Exception occurred when validating GitHub repository "{self}"')
            return False

        if resp.status_code == http.HTTPStatus.OK:
            return True
        else:
            logging.error(f'HTTP status code {resp.status_code} encountered when validating GitHub repository "{self}"')
            return False

    def __str__(self):
        return f'{self.username}/{self.name}'


class MailingList(NamedTuple):
    name: str
    address: str
    repositories: List[GithubRepository]

    def validate(self):
        if not any(self.repositories):
            logging.error('No repositories have been specified')
            return False

        if not validators.email(self.address):
            logging.error(f'Email address "{self.address}" is not valid')
            return False

        return True

    def __str__(self):
        return self.name
