# Provider Service

This is the backend service that handles LLM integration and response generation for the chat application.

## Pre-requisites

- AWS CLI configured with appropriate permissions

## Deployment

### 1. Deploy Infrastructure

Deploy the CloudFormation stack:

```bash
cd provider/iac
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name poc-chat-gpt-provider \
  --capabilities CAPABILITY_IAM
```

### 2. Deploy Lambda Functions

#### Provider Dispatcher

```bash
cd lambdas/lambda-provider-dispatcher
zip -r lambda.zip .

aws lambda update-function-code \
  --function-name lambda-provider-dispatcher \
  --zip-file fileb://lambda.zip
```

#### Provider Worker

```bash
cd ../lambda-provider-worker
zip -r lambda.zip .

aws lambda update-function-code \
  --function-name lambda-provider-worker \
  --zip-file fileb://lambda.zip
```
