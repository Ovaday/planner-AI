import json
import os
from decouple import config
import boto3
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig
from django.conf import settings


def retrieve_and_cache_secrets():
    session = boto3.session.Session(
        aws_access_key_id=get_token("IAM_ACCESS_KEY"),
        aws_secret_access_key=get_token("IAM_SECRET_KEY"),
    )

    client = session.client(
        service_name='secretsmanager',
        region_name=get_token("IAM_AWS_REGION")
    )
    cache_config = SecretCacheConfig()
    cache = SecretCache(config=cache_config, client=client)

    return cache


def get_token(token_name):
    if len(token_name) < 1:
        return None

    token_value = os.getenv(token_name)
    if token_value:
        return token_value

    try:
        if "IAM_" in token_name or "DEBUG_MODE" in token_name or config('ENV') == "PROD":
            token_value = config(str(token_name))
        else:
            tokens = json.loads(settings.SECRETS.get_secret_string("dev/plannerAI"))
            token_value = tokens[str(token_name)]
        return token_value
    except Exception as e:
        print('Exception: ' + str(e))
        return None


def get_db_conn():
    return {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_token("DB_NAME"),
        'USER': get_token("DB_USER"),
        'PASSWORD': get_token("DB_PASSWORD"),
        'HOST': get_token("DB_HOST"),
        'PORT': '5432',
    }


def get_mongo_db_conn():
    return {
        'USER': get_token("MONGO_DB_USER"),
        'PASSWORD': get_token("MONGO_DB_PASSWORD"),
        'HOST': get_token("MONGO_DB_ENVIROMENT"),
    }
