import os
import pytest
import json

import config
from utils.github_client import GitHubClient
from utils.schema_validator import load_schema


@pytest.fixture(scope="session")
def token():
    return config.tokens.get("token_with_permission")


@pytest.fixture(scope="session")
def token_without_permission():
    return config.tokens.get("token_without_permission")


@pytest.fixture(scope="session")
def client(token):
    return GitHubClient(token)


@pytest.fixture(scope="session")
def users_client(token):
    return GitHubClient(token, config.users_url)


@pytest.fixture(scope="session")
def invalid_client(token_without_permission):
    return GitHubClient(token_without_permission)


@pytest.fixture(scope="session")
def unauthorized_client():
    return GitHubClient("")


@pytest.fixture(scope="session")
def json_schema():
    path = os.path.join(config.schemas_path, "gist.json")
    return load_schema(path)


@pytest.fixture
def simple_gist(client):
    description = "Example of a gist"
    public = True
    files = {"README.md": {"content": "Hello World!"}}
    response = client.create_gist(public, files, description)
    gist = json.loads(response.content)
    yield gist
    client.delete_gist(gist["id"])
