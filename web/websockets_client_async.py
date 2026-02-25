import asyncio
import websockets

async def communicate():
    uri = "ws://localhost:8765"
    try:
        async with websockets.connect(uri) as websocket:
            # Send an initial message
            await websocket.send("Hello from client!")
            print("Message sent to server.")

            # Keep listening for messages until connection closes
            async for message in websocket:
                print(f"Received from server: {message}")

    except ConnectionRefusedError:
        print("Could not connect to the server. Is it running?")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")

if __name__ == "__main__":
    asyncio.run(communicate())
