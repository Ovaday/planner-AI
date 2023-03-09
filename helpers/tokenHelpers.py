import os

def get_token(token_name):
    if not token_name:
        return None

    token_value = os.getenv(token_name)
    if token_value:
        return token_value

    token_value = os.getenv('LOCAL_' + token_name)
    return token_value