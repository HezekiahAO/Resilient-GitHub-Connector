import os           #  To get environment variables (GITHUB_TOKEN)
import logging      #  Logging in Python provides a robust and flexible framework for tracking events that occur during the execution of the software program.
import time         # To import time module available for python's standard library.
import requests     #  To make HTTP requests from GITHUB.
from typing import Dict, Any  #  To provide type hints for dictionaries and any type.

from dotenv import load_dotenv  #  To load environment variables from a .env file.
from .custom_exceptions import GitHubAPIError, ResourceNotFoundError, RateLimitExceeded

class GitHubClient:

    base_url = 'https://api.github.com'

    def __init__(self) -> None:
        
        self.token = os.getenv('GITHUB_TOKEN')


        if not self.token:
            raise ValueError("GITHUB_TOKEN is not set. API rate limits will be very low without authentication.")


        logging.info("GitHubClient initialized with provided GITHUB_TOKEN.")



    # Fetches general info about a repository (stars, forks, description).
    def get_repo_details(self, owner: str, repo: str) -> dict:
        endpoint = f'/repos/{owner}/{repo}'
        return self.make_request('GET', endpoint=endpoint)
    

    # Fetches details about the latest release.
    def get_latest_release(self, owner: str, repo: str) -> dict:
        endpoint = f'/repos/{owner}/{repo}/releases/latest'
        return self.make_request('GET', endpoint)


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

        headers = self.get_headers()

        logging.info(f'Request: {method}{url}')

        #Retry logic for handling rate limits
        retries = 0
        backoff = 1 # Waiting time in seconds

        while retries < 3:

            try: 
                response = requests.request(method, url, headers=headers)

                # if ok -> return response json
                
                # Successful response

                if response.status_code == 200:
                    return response.json()
                
                # Resource not found

                elif response.status_code == 404:
                    logging.error(f'Resource not found: {url}')
                    raise ResourceNotFoundError(f'Resource not found: {url}')
                
                # Rate limit exceeded

                elif response.status_code in (403, 429):
                    logging.warning(f"Rate limit hit. Retry {retries + 1}/3 in {backoff}s.")

                    time.sleep(backoff)
                    backoff *= 2
                    retries += 1 
                    continue

                # Other errors

                else:
                    logging.error(f"GitHub API error {response.status_code}: {response.text}")
                    raise GitHubAPIError(
                        f"GitHub API error {response.status_code}: {response.text}"
                        )
                
            except requests.exceptions.RequestException as error:
                logging.error(f'Newtwork error: {error}')
                raise GitHubAPIError(f'Network error: {error}')
        
            # Retry Exhaustion

        raise GitHubAPIError("Exceeded maximum retries due to rate limiting.")