import boto3
import os, json
import urllib3

headers = {"X-Aws-Parameters-Secrets-Token": os.environ.get('AWS_SESSION_TOKEN')}
success_response = {
    'statusCode': 200,
    'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    },
    'body': json.dumps({
        'success': True
    }),
    "isBase64Encoded": False
}

error_response = {
    'statusCode': 405,
    'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    },
    'body': json.dumps({'error': 'Incorrect request'}),
    "isBase64Encoded": False
}


def lambda_handler(event, context):
    if event['httpMethod'] == 'POST':
        ssm_client = boto3.client('ssm')
        body = json.loads(event['body'])
        if body and not body['repository']['fork'] and body['repository']['url'] == os.environ.get('REPO_URL'):
            secrets = {}
            if body['ref'] == os.environ.get('DEV_REF'):
                secrets = get_aws_secrets('DEV_SECRETS_NAME')
            elif body['ref'] == os.environ.get('PROD_REF'):
                secrets = get_aws_secrets('PROD_SECRETS_NAME')
            else:
                return success_response

            response = ssm_client.send_command(
                Targets=[{"Key": "InstanceIds", "Values": [secrets['EC2_INSTANCE_ID']]}],
                DocumentName='AWS-RunShellScript',
                DocumentVersion='1',
                TimeoutSeconds=600,
                Comment='string',
                Parameters={"workingDirectory": [secrets['EC2_ENV_DIR']], "executionTimeout": ["3600"],
                            "commands": [secrets['EC2_DEPLOY_COMMAND']]},
            )
            return success_response

        else:
            return error_response
    else:
        return error_response


def get_aws_secrets(env_secrets_name):
    http = urllib3.PoolManager()
    secret_name = os.environ.get(env_secrets_name)

    secrets_extension_endpoint = "http://localhost:2773" + "/secretsmanager/get?secretId=" + secret_name
    response = http.request('GET', secrets_extension_endpoint, headers=headers)

    return json.loads(json.loads(response.data.decode('utf-8'))["SecretString"])