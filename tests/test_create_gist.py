import pytest
import json


from utils.schema_validator import validate_schema


# Positive cases for creating gist
@pytest.mark.parametrize(
    "payload, truncated",
    [
        # Valid payload with all the parameters
        (
            {
                "description": "Example of a gist",
                "public": True,
                "files": {"README.md": {"content": "Hello World"}},
            },
            False,
        ),
        # Valid payload without a description
        (
            {
                "public": True,
                "files": {
                    "manual.txt": {"content": "Some other content for the text file"}
                },
            },
            False,
        ),
        # Valid payload with two files
        (
            {
                "description": "Example of a gist with two files",
                "public": False,
                "files": {
                    "test.py": {
                        "content": "import pytest\n@pytest.mark.skip\ndef test():\n    pass"
                    },
                    "config.json": {"content": '{"base_url": "testurl"}'},
                },
            },
            False,
        ),
        # Valid payload with file > 1MB
        pytest.param(
            {
                "description": "Example of a gist with truncated file",
                "public": True,
                "files": {"large_file.txt": {"content": "w" * 2 * 1024 * 1024}},
            },
            True,
            marks=pytest.mark.skip(reason="Rate limit may be exceeded"),
        ),
    ],
)
def test_create_gist_positive(client, json_schema, payload, truncated):
    try:
        # Create a gist
        response = client.create_gist(
            payload.get("public"), payload.get("files"), payload.get("description")
        )
        assert (
            response.status_code == 201
        ), f"Error while creating a gist: {response.text}"

        # Validate response via json schema
        created_gist = json.loads(response.content)
        validate_schema(created_gist, json_schema)

        # Validate sent parameters
        for file in payload.get("files"):
            assert file in created_gist.get(
                "files"
            ), f"File {file} doesn't exist in gist"
            assert "raw_url" in created_gist.get("files").get(
                file
            ), "File doesn't have a raw url"
        assert (
            created_gist.get("public") == payload["public"]
        ), "Incorect public in response"
        if "description" in payload:
            assert (
                created_gist.get("description") == payload["description"]
            ), "Description doesn't match"
        if truncated:
            assert (
                created_gist.get("truncated") == "true"
            ), "Truncated flag doesn't match"
    finally:
        # Cleanup
        if created_gist:
            client.delete_gist(created_gist.get("id"))


# Validation errors when creating a gist
@pytest.mark.parametrize(
    "payload",
    [
        # Invalid payload with object in description
        {
            "description": {"test": "description"},
            "public": True,
            "files": {"README.md": {"content": "Hello World"}},
        },
        # Invalid payload without files
        {"description": "Example of a gist", "public": True},
        # Invalid payload with empty files object
        {"description": "Example of a gist", "public": False, "files": {}},
        # Invalid payload with string instead of file
        {
            "description": "Example of a gist",
            "public": False,
            "files": "incorrect file",
        },
        # Valid payload with empty file content
        {
            "description": "Example of a gist",
            "public": False,
            "files": {"README.md": {"content": ""}},
        },
        # Invalid payload with incorrect public
        {
            "description": "Example of a gist",
            "public": "test",
            "files": {"README.md": {"content": "Hello World"}},
        },
    ],
)
def test_create_gist_validation_error(client, payload):
    response = client.create_gist(
        payload.get("public"), payload.get("files"), payload.get("description")
    )

    assert (
        response.status_code == 422
    ), f"Expected status code is incorrect, response: {response.text}"


# Access error when creating a gist
@pytest.mark.parametrize(
    "auth, expected_error", [("invalid_client", 403), ("unauthorized_client", 401)]
)
def test_create_gist_access_error(auth, expected_error, request):
    payload = {
        "description": "Example of a gist",
        "public": True,
        "files": {"README.md": {"content": "Hello World"}},
    }
    response = request.getfixturevalue(auth).create_gist(
        payload.get("public"), payload.get("files"), payload.get("description")
    )

    assert (
        response.status_code == expected_error
    ), f"Expected status code is incorrect, response: {response.text}"
