import os
from decouple import config

def get_token(token_name):
    if len(token_name) < 1:
        return None

    token_value = os.getenv(token_name)
    if token_value:
        return token_value

    token_value = config('LOCAL_' + str(token_name))
    return token_value