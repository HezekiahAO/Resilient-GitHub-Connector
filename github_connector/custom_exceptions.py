class GitHubAPIError(Exception):
    "This is the base class for Github api errors"
    pass

class ResourceNotFoundError(GitHubAPIError):
    "Raised when a repository or resource is not found (404)"
    pass

class RateLimitExceeded(GitHubAPIError):
    "Raised when the API rate limit is exceeded (403)"
    pass


