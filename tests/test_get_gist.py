import pytest
import json

from utils.schema_validator import validate_schema


# Positive cases for getting gist
@pytest.mark.parametrize(
    "payload",
    [
        # Valid payload with all the parameters
        {
            "description": "Example of a gist",
            "public": True,
            "files": {"README.md": {"content": "Hello World"}},
        },
        # Valid payload without a description
        {"public": True, "files": {"README.md": {"content": "Hello World"}}},
        # Valid payload with two files
        {
            "description": "Example of a gist with two files",
            "public": False,
            "files": {
                "README.md": {"content": "Hello World"},
                "config.json": {"content": '{"base_url": "testurl"}'},
            },
        },
    ],
)
def test_get_gist_positive(payload, client, json_schema):
    try:
        # Create a gist
        created_gist = client.create_gist(
            payload.get("public"), payload.get("files"), payload.get("description")
        )
        gist = created_gist.json()

        # Get a gist
        response = client.get_gist(gist.get("id"))
        assert (
            response.status_code == 200
        ), f"Error while getting a gist: {response.text}"

        # Validate response via json schema
        created_gist = json.loads(response.content)
        validate_schema(created_gist, json_schema)

        # Validate sent parameters
        for file in payload.get("files"):
            assert file in created_gist.get("files"), f"File {file} doesn't exist"
            assert "raw_url" in created_gist.get("files").get(
                file
            ), "File doesn't have a raw url"
        assert created_gist.get("public") == payload.get(
            "public"
        ), "Incorect public in response"
        if "description" in payload:
            assert created_gist.get("description") == payload.get("description")
    finally:
        # Cleanup
        if created_gist:
            client.delete_gist(created_gist.get("id"))


# Negative cases when getting gist
@pytest.mark.parametrize(
    "gist_id",
    ["e3f23640bc7f36c790eca296cafd97cf", "123567890"],
)
def test_get_gist_negative_cases(gist_id, client):
    # Get a gist
    response = client.get_gist(gist_id)

    # Validate an error
    assert (
        response.status_code == 404
    ), f"Incorrect error code, response: {response.text}"
