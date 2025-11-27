class GitHubClient:

    def __init__(self) -> None:
        pass

    # Fetches general info about a repository (stars, forks, description).
    def get_repo_details(self, owner: str, repo: str) -> dict:
        raise NotImplementedError

    # Fetches details about the latest release.
    def get_latest_release(self, owner: str, repo: str) -> dict:
        raise NotImplementedError


base_url = 'https://api.github.com'
