import os


gists_url = os.getenv("BASE_URL") + "gists"

users_url = os.getenv("BASE_URL") + "users"

tokens = {
    "token_with_permission": os.getenv("TOKEN_WITH_PERMISSIONS"),
    "token_without_permission": os.getenv("TOKEN_WITHOUT_PERMISSIONS"),
}

schemas_path = os.path.abspath("schemas") + "/"
