import os
from dotenv import load_dotenv


load_dotenv()


GITHUB_API = "https://api.github.com"

GRAPHQL_API = "https://api.github.com/graphql"


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "User-Agent": "Intelligence-Hub"
}