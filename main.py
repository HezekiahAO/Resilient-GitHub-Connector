from github_connecto.client import GitHubClient

if __name__ == "__main__":

    client = GitHubClient()
    repo_details = client.get_repo_details("octocat", "Hello-World")
    print("Repository Details:", repo_details)

    latest_release = client.get_latest_release("octocat", "Hello-World")
    print("Latest Release:", latest_release)