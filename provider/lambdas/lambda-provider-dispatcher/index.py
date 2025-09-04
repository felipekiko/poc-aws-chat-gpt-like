import json
import boto3
import os
import uuid

def lambda_handler(event, context):
    connection_id = event['requestContext']['connectionId']
    domain = event['requestContext']['domainName']
    stage = event['requestContext']['stage']
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
