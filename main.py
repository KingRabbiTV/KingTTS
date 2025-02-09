import asyncio
import websockets
import json
from gtts import gTTS
import io

async def tts_handler(websocket):
    async for message in websocket:
        try:
            # Expecting a JSON message with a "text" field.
            data = json.loads(message)
            text = data.get("text", "")
            if not text:
                await websocket.send(json.dumps({"error": "No text provided"}))
                continue

            # Convert text to speech using gTTS.
            tts = gTTS(text=text, lang='en', slow=False)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_bytes = audio_buffer.getvalue()

            # Send the audio bytes over the WebSocket.
            await websocket.send(audio_bytes)
        except Exception as e:
            error_message = json.dumps({"error": str(e)})
            await websocket.send(error_message)

async def main():
    # Start the WebSocket server on localhost, port 8765.
    async with websockets.serve(tts_handler, "localhost", 8765):
        print("TTS server is running on ws://localhost:8765...")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())