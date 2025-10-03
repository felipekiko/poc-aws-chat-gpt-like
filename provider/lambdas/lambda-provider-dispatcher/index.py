import json
import os
import uuid
import boto3
from botocore.config import Config
import time

def get_appconfig_flag(application, environment, configuration):
    try:
        client = boto3.client('appconfigdata')
        
        session = client.start_configuration_session(
            ApplicationIdentifier=application,
            EnvironmentIdentifier=environment,
            ConfigurationProfileIdentifier=configuration,
            RequiredMinimumPollIntervalInSeconds=15
        )
        
        response = client.get_latest_configuration(
            ConfigurationToken=session['InitialConfigurationToken']
        )
        
        if 'Configuration' in response and response['Configuration']:
            config_content = response['Configuration'].read().decode('utf-8')
            
            try:
                config = json.loads(config_content)
                service_available = config.get('isServiceAvailable', False)

                return service_available['enabled']
            except json.JSONDecodeError as e:
                return False
        else:
            return False
            
    except Exception as e:
        print(f"[ERROR] Error in get_appconfig_flag: {str(e)}")
        return False

def lambda_handler(event, context):
    service_available = get_appconfig_flag(
        os.environ['APP_CONFIG_APPLICATION'],
        os.environ['APP_CONFIG_ENVIRONMENT'],
        os.environ['APP_CONFIG_CONFIGURATION']
    )

    connection_id = event['requestContext']['connectionId']
    domain = event['requestContext']['domainName']
    stage = event['requestContext']['stage']

    if service_available == False:
        apigw_management = None
        message_system_down = 'Sistema em manutenção. Por favor, tente novamente mais tarde.'

        if not apigw_management:
            apigw_management = boto3.client('apigatewaymanagementapi', endpoint_url=f"https://{domain}/{stage}")

        apigw_management.post_to_connection(
            Data=json.dumps({'type': 'stream', 'chunk': message_system_down}),
            ConnectionId=connection_id
        )

        apigw_management.post_to_connection(
            Data=json.dumps({'type': 'end'}),
            ConnectionId=connection_id
        )

        return {
            'statusCode': 503,
            'body': json.dumps({
                'status': 'error',
                'message': message_system_down
            })
        }

    body = event.get('body')

    if body and isinstance(body, str):
        body = json.loads(body)
    elif not body:
        body = event

    prompt = body.get('prompt', '')

    sqs = boto3.client('sqs')
    queue_url = os.environ['STREAM_QUEUE_URL']
    request_id = str(uuid.uuid4())
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps({
            'connection_id': connection_id,
            'domain': domain,
            'stage': stage,
            'prompt': prompt,
            'request_id': request_id
        })
    )

    return {'statusCode': 200, 'body': json.dumps({'message': 'Recebido, processamento iniciado.'})}
