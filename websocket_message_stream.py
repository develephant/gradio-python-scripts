import asyncio
import json
import websockets

''' Connect the websocket '''
# async def establish_connection():
#     ws_client = ws.connect(f"ws://{config.comfy_server}/ws?clientId={client_id}") 
#     return ws_client

# Async generator that yields only messages with status == "ok"
async def wsm_stream(uri):
    try:
        async with websockets.connect(uri) as ws:
            print(f"Connected to {uri}")
            async for raw_message in ws:
                try:
                    message = json.loads(raw_message)

                    msg_type = message.get('type')

                    yield_message = False

                    if 'executing' in msg_type:
                        yield_message = True
                    elif 'executed' in msg_type:
                        pass
                    elif 'execution_success' in msg_type:
                        yield_message = True
                    elif 'progress_state' in msg_type:
                        pass
                    elif 'progress' in msg_type:
                        yield_message = True
                    elif 'status' in msg_type:
                        pass


                except json.JSONDecodeError:

                    print(f"Skipping non-JSON message: {raw_message}")
                    continue

                # Conditional yield
                if yield_message == True:
                    yield message
                else:
                    print(f"Ignored message with status: {message.get('type')}") 



    except websockets.ConnectionClosed:
        print("WebSocket connection closed.")
    except Exception as e:
        print(f"Error: {e}")

# Consumer
# async def main():
#     uri = "wss://echo.websocket.events"  # Public test WebSocket
#     async for msg in wsm_stream(uri):
#         print(f"✅ Received OK message: {msg}")

if __name__ == "__main__":
    pass
    # asyncio.run(main())
