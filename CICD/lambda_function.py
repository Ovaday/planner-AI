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
    'body': json.dumps({'error': 'Unsupported request method'}),
    "isBase64Encoded": False
}


# Intends for the AWS Lambda
def lambda_handler(event, context):
    if event['httpMethod'] == 'POST':
        http = urllib3.PoolManager()
        ssm_client = boto3.client('ssm')
        secret_name = os.environ.get('SECRETS_NAME')

        secrets_extension_endpoint = "http://localhost:2773" + \
                                     "/secretsmanager/get?secretId=" + secret_name
        response = http.request('GET', secrets_extension_endpoint, headers=headers)

        secrets = json.loads(json.loads(response.data.decode('utf-8'))["SecretString"])

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
