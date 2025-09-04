# Consumer Application

This is the frontend and API layer of the chat application, handling user interactions and WebSocket communication.

## Prerequisites

- AWS CLI configured with appropriate permissions
- The provider service must be deployed first

## Deployment

### 1. Deploy Infrastructure

Deploy the CloudFormation stack:

```bash
cd consumer/iac
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name poc-chat-gpt-consumer \
  --capabilities CAPABILITY_IAM
```

### 2. Deploy Lambda Functions

#### Consumer Dispatcher

```bash
cd lambdas/lambda-consumer-dispatcher
zip -r lambda.zip .

aws lambda update-function-code \
  --function-name lambda-consumer-dispatcher \
  --zip-file fileb://lambda.zip
```

#### Consumer Worker

```bash
cd ../lambda-consumer-worker
pip install -r requirements.txt -t .
zip -r lambda.zip .

aws lambda update-function-code \
  --function-name lambda-consumer-worker \
  --zip-file fileb://lambda.zip
```

### 3. Update Frontend Configuration

1. Get the WebSocket URL from CloudFormation outputs:
   ```bash
   aws cloudformation describe-stacks \
     --stack-name apw-app \
     --query "Stacks[0].Outputs[?OutputKey=='WebSocketURL'].OutputValue" \
     --output text
   ```

2. Update the WebSocket URL in the frontend:
   - Open `web/main.js`
   - Update the `WS_URL` constant with the URL from the previous step

## Environment Variables

### Consumer Worker
- `PROVIDER_ENDPOINT_URL`: WebSocket URL of the provider service (set in CloudFormation)
