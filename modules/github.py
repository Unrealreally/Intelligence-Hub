import requests
import base64
from collections import Counter

from config import GITHUB_API, HEADERS


from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def github_request(url: str):
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=0.3, status_forcelist=[429, 500, 502, 503, 504], allowed_methods=["GET"])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    try:
        return session.get(
            url,
            headers=HEADERS,
            timeout=10
        )
    except requests.RequestException:
        return None



def request_failed():

    return {
        "success": False,
        "error": "Request failed"
    }



def github_error(message: str, response):

    return {
        "success": False,
        "error": message,
        "status_code": response.status_code
    }



def github_success(data):

    return {
        "success": True,
        "data": data
    }



# ------------------------
# User API
# ------------------------


def get_user(username: str):

    url = f"{GITHUB_API}/users/{username}"

    response = github_request(url)

    if response is None:
        return request_failed()

    if response.status_code != 200:
        return github_error(
            "GitHub API request failed",
            response
        )

    return github_success(response.json())



def get_events(username: str):

    url = (
        f"{GITHUB_API}/users/{username}"
        "/events?per_page=100"
    )

    response = github_request(url)

    if response is None:
        return request_failed()

    if response.status_code != 200:
        return github_error(
            "Failed to fetch events",
            response
        )

    return github_success(response.json())



# ------------------------
# Repository API
# ------------------------


def get_repos(username: str):

    url = (
        f"{GITHUB_API}/users/{username}/repos"
        "?per_page=100&sort=updated"
    )

    response = github_request(url)

    if response is None:
        return request_failed()

    if response.status_code != 200:
        return github_error(
            "Failed to fetch repositories",
            response
        )

    return github_success(response.json())



def get_languages(repos):

    languages = [
        repo.get("language")
        for repo in repos
        if repo.get("language")
    ]

    return Counter(languages).most_common()



def get_readme(username: str, repo_name: str):

    url = (
        f"{GITHUB_API}/repos/"
        f"{username}/{repo_name}/readme"
    )

    response = github_request(url)

    if response is None:
        return request_failed()

    if response.status_code != 200:
        return github_error(
            "Failed to fetch README",
            response
        )

    content = response.json().get("content")

    if not content:
        return {
            "success": False,
            "error": "README content not found"
        }

    try:
        readme = base64.b64decode(content).decode("utf-8")

    except Exception:

        return {
            "success": False,
            "error": "README decode failed"
        }


    return github_success(readme)



def get_repository_languages(username: str, repo_name: str):

    url = (
        f"{GITHUB_API}/repos/"
        f"{username}/{repo_name}/languages"
    )

    response = github_request(url)

    if response is None:
        return request_failed()

    if response.status_code != 200:
        return github_error(
            "Failed to fetch repository languages",
            response
        )

    return github_success(response.json())


def get_topics(username: str, repo_name: str):

    url = (
        f"{GITHUB_API}/repos/"
        f"{username}/{repo_name}/topics"
    )

    response = github_request(url)

    if response is None:
        return request_failed()

    if response.status_code != 200:
        return github_error(
            "Failed to fetch topics",
            response
        )

    data = response.json()

    return github_success({
        "names": data.get(
            "names",
            []
        )
    })


def get_contributors(username: str, repo_name: str):

    url = (
        f"{GITHUB_API}/repos/"
        f"{username}/{repo_name}/contributors"
        "?per_page=100"
    )

    response = github_request(url)

    if response is None:
        return request_failed()

    if response.status_code != 200:
        return github_error(
            "Failed to fetch contributors",
            response
        )

    return github_success(response.json())



def get_commits(username: str, repo_name: str):

    url = (
        f"{GITHUB_API}/repos/"
        f"{username}/{repo_name}"
        "/commits?per_page=100"
    )

    response = github_request(url)

    if response is None:
        return request_failed()

    if response.status_code != 200:
        return github_error(
            "Failed to fetch commits",
            response
        )

    return github_success(response.json())



def get_pull_requests(username: str, repo_name: str):

    url = (
        f"{GITHUB_API}/repos/"
        f"{username}/{repo_name}"
        "/pulls?state=all&per_page=100"
    )

    response = github_request(url)

    if response is None:
        return request_failed()

    if response.status_code != 200:
        return github_error(
            "Failed to fetch pull requests",
            response
        )

    return github_success(response.json())



def get_issues(username: str, repo_name: str):

    url = (
        f"{GITHUB_API}/repos/"
        f"{username}/{repo_name}"
        "/issues?state=all&per_page=100"
    )

    response = github_request(url)

    if response is None:
        return request_failed()

    if response.status_code != 200:
        return github_error(
            "Failed to fetch issues",
            response
        )

    return github_success(response.json())



def get_releases(username: str, repo_name: str):

    url = (
        f"{GITHUB_API}/repos/"
        f"{username}/{repo_name}"
        "/releases?per_page=100"
    )

    response = github_request(url)

    if response is None:
        return request_failed()

    if response.status_code != 200:
        return github_error(
            "Failed to fetch releases",
            response
        )

    return github_success(response.json())



def get_branches(username: str, repo_name: str):

    url = (
        f"{GITHUB_API}/repos/"
        f"{username}/{repo_name}"
        "/branches?per_page=100"
    )

    response = github_request(url)

    if response is None:
        return request_failed()

    if response.status_code != 200:
        return github_error(
            "Failed to fetch branches",
            response
        )

    return github_success(response.json())