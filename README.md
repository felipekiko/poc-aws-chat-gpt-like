# AWS Chat GPT-like Application

This project implements a serverless chat application using AWS services, providing a ChatGPT-like experience with streaming responses.

## Project Structure

```
.
├── consumer/               # Consumer application (frontend + API)
│   ├── iac/                # Infrastructure as Code (CloudFormation)
│   ├── lambdas/            # Lambda functions
│   └── web/                # Frontend files
└── provider/               # Provider service (LLM integration)
    ├── iac/                # Infrastructure as Code (CloudFormation)
    └── lambdas/            # Lambda functions
```

## Deployment

1. Deploy Provider
2. Deploy Consumer

## Architecture

1. **Frontend** (HTML/JS)
   - Connects to API Gateway WebSocket
   - Sends prompts and displays streaming responses

2. **API Gateway WebSocket**
   - Manages WebSocket connections
   - Routes messages to appropriate Lambda functions

3. **Lambda Functions**
   - `lambda-consumer-dispatcher`: Handles WebSocket connection management
   - `lambda-consumer-worker`: Processes prompts and streams responses
   - `lambda-provider-dispatcher`: Routes messages to the provider
   - `lambda-provider-worker`: Integrates with the LLM (Bedrock)

## Cleanup

To remove all resources:

```bash
# Delete CloudFormation stacks
aws cloudformation delete-stack --stack-name apw-app
aws cloudformation delete-stack --stack-name apw-hon
```

## To Do

- [ ] Integrate with Bedrock
