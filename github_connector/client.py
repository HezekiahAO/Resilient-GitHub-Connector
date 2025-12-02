import os           #  To get environment variables (GITHUB_TOKEN)
import logging      #  Logging in Python provides a robust and flexible framework for tracking events that occur during the execution of the software program.
import time         # To import time module available for python's standard library.
import requests     #  To make HTTP requests from GITHUB.
from typing import Dict, Any  #  To provide type hints for dictionaries and any type.



class GitHubClient:

    base_url = 'https://api.github.com'

    def __init__(self) -> None:
        
        self.token = os.getenv('GITHUB_TOKEN')


        if not self.token:
            raise ValueError("GITHUB_TOKEN is not set. API rate limits will be very low without authentication.")


        logging.info("GitHubClient initialized with provided GITHUB_TOKEN.")



    # Fetches general info about a repository (stars, forks, description).
    def get_repo_details(self, owner: str, repo: str) -> dict:
        raise NotImplementedError

    # Fetches details about the latest release.
    def get_latest_release(self, owner: str, repo: str) -> dict:
        raise NotImplementedError


    def get_headers(self) -> Dict[str, str]:
        headers = {
            'Accept': 'application/vnd.github.+json',
        }

        if self.token:
            headers['Authorization'] = f'token {self.token}'

        return headers


# The Core of my API, the Make request, it handles building the URL, sending the request, detecting errors, retrying on rate limits, converting responses to JSON and raising custom exceptions.

    def make_request(self, method: str, endpoint: str) -> Dict[str, Any]:
        
        "Makes an HTTP request to the GitHub API."

        url = f'{self.base_url,}{endpoint}'

        header = self.get_headers()

        logging.info(f'Request: {method}{url}')

        #Retry logic for handling rate limits
        retries = 3
        backoff = 1 # seconds