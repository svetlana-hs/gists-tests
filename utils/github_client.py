import requests
import logging
import http.client as http_client

from config import gists_url


# Enable debugging at http.client level (requests uses this under the hood)
http_client.HTTPConnection.debuglevel = 1

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

# Enable logging for requests and urllib3
logging.getLogger("requests.packages.urllib3").propagate = True


# Client for calling GitHub API
class GitHubClient:
    def __init__(self, token, custom_base_url=None):
        self.base_url = custom_base_url if custom_base_url else gists_url
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + token,
        }

    # Method POST /gists
    def create_gist(self, public, files, description=""):
        payload = {"public": public, "files": files}
        if description:
            payload["description"] = description

        response = requests.post(self.base_url, json=payload, headers=self.headers)

        return response

    # Method DELETE /gists
    def delete_gist(self, gist_id):
        response = requests.delete(self.base_url + f"/{gist_id}", headers=self.headers)

        return response

    # Method GET /gists/{gist_id}
    def get_gist(self, gist_id):
        response = requests.get(self.base_url + f"/{gist_id}", headers=self.headers)

        return response

    # Method GET /gists for authorized user
    def list_gists(self):
        response = requests.get(
            self.base_url, params={"per_page": 100}, headers=self.headers
        )

        return response

    # Method GET /users/{username}/gists for user
    def list_user_gists(self, username):
        response = requests.get(
            self.base_url + f"/{username}/gists",
            params={"per_page": 100},
            headers=self.headers,
        )

        return response
