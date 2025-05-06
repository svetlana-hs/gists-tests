# End-to-end tests for Gists API
Testing methods of creating and getting gists via the GitHub REST API for gists.
https://docs.github.com/en/rest/gists/gists

## Install env and packages
```sh
python3 -m venv .env
.env/bin/pip3 install -r requirements.txt`
```

## Run tests
```sh
.env/bin/python -m pytest --color=yes -vv --tb=short
```
Environment from pytest.ini is used by default, for running with another environment, use the flag
```sh
pytest -c pytest.stage.ini
```
where pytest.stage.ini - file with environment configuration.

## Project description
There are tests for two methods:
1. test_create_gist.py with test cases for `POST /gists`, https://docs.github.com/en/rest/gists/gists#create-a-gist
2. test_get_gist.py with test cases for `GET /gists/{gist_id}`, https://docs.github.com/en/rest/gists/gists#get-a-gist

JSON-Schema is used for validating responses.
