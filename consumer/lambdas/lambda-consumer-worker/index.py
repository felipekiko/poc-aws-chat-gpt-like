import json
import boto3
import os
import websocket
import time
import threading

class WebSocketClient:
    def __init__(self, ws_url, apigw_management, connection_id, prompt):
        self.ws_url = ws_url
        self.apigw_management = apigw_management
        self.connection_id = connection_id
        self.prompt = prompt
        self.ws = None
        self.keep_running = True

    def on_message(self, ws, message):
        try:
            try:
                message_data = json.loads(message)
                
                if isinstance(message_data, dict) and message_data.get('type') == 'end':
                    return
                    
                if isinstance(message_data, dict):
                    if 'chunk' in message_data:
                        response = {
                            'type': 'stream',
                            'chunk': str(message_data['chunk'])
                        }
                    else:
                        response = {
                            'type': 'stream',
                            'chunk': str(message_data)
                        }
                else:
                    response = {
                        'type': 'stream',
                        'chunk': str(message_data)
                    }
            except (json.JSONDecodeError, TypeError):
                response = {
                    'type': 'stream',
                    'chunk': str(message)
                }
            
            self.apigw_management.post_to_connection(
                ConnectionId=self.connection_id,
                Data=json.dumps(response)
            )
        except Exception as e:
            print(f"Error forwarding message: {e}")
            self.keep_running = False

    def on_error(self, ws, error):
        print(f"WebSocket error: {error}")
        self.keep_running = False

    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket connection closed")
        self.keep_running = False

    def on_open(self, ws):
        print("WebSocket connection opened")

        ws.send(json.dumps({
            'action': 'sendPrompt',
            'prompt': self.prompt
        }))

    def run(self):
        self.ws = websocket.WebSocketApp(
            self.ws_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )
        
        def run_ws():
            self.ws.run_forever()
            
        ws_thread = threading.Thread(target=run_ws)
        ws_thread.daemon = True
        ws_thread.start()
        
        ws_thread.join()

def lambda_handler(event, context):
    try:
        ws_url = os.environ.get('PROVIDER_ENDPOINT_URL')
            
        for record in event.get('Records', []):
            try:
                msg = json.loads(record['body'])
                connection_id = msg.get('connection_id')
                domain = msg.get('domain')
                stage = msg.get('stage')
                prompt = msg.get('prompt')
                
                if not all([connection_id, domain, stage, prompt]):
                    print("Missing required fields in message")
                    continue
                
                apigw_management = boto3.client(
                    'apigatewaymanagementapi',
                    endpoint_url=f"https://{domain}/{stage}"
                )
                
                ws_client = WebSocketClient(ws_url, apigw_management, connection_id, prompt)
                ws_client.run()
                
            except Exception as e:
                print(f"Error processing record: {e}")
                try:
                    apigw_management.post_to_connection(
                        ConnectionId=connection_id,
                        Data=json.dumps({
                            'type': 'error',
                            'message': f'Error processing request: {str(e)}'
                        })
                    )
                except:
                    pass
                
    except Exception as e:
        print(f"Error in lambda_handler: {e}")
        raise
