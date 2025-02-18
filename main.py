import asyncio
import websockets
import json
from gtts import gTTS
import io
import requests

# Define the URL of the server endpoint
url = "http://localhost:8880/v1/audio/speech"


async def tts_handler(websocket):
    async for message in websocket:
        try:
            # Expecting a JSON message with a "text_input" field.
            data = json.loads(message)
            text_input = data.get("text", "")
            if not text_input:
                await websocket.send(json.dumps({"error": "No text_input provided"}))
                continue

            payload = {
                "input": text_input,
                "voice": "am_liam",
                "response_format": "mp3",
                "download_format": "mp3",
                "speed": 1,
                "stream": True,
                "return_download_link": True,
            }

            response = requests.post(url, json=payload)
            if response.status_code == 200:
                # Access the response content
                # response_content = response.content
                await websocket.send(response.content)
                # audio_buffer = io.BytesIO()
                # audio_buffer.write(response_content)
                # audio_bytes = audio_buffer.getvalue()

            # Convert text_input to speech using gTTS.
            # tts = gTTS(text_input=text_input, lang="en", slow=False)
            # audio_buffer = io.BytesIO()
            # tts.write_to_fp(audio_buffer)
            # audio_bytes = audio_buffer.getvalue()

            # Send the audio bytes over the WebSocket.
            # await websocket.send(audio_bytes)
        except Exception as e:
            error_message = json.dumps({"error": str(e)})
            await websocket.send(error_message)


# def write_to_fp(fp):
#     """Do the TTS API request(s) and write bytes to a file-like object.

#     Args:
#         fp (file object): Any file-like object to write the ``mp3`` to.

#     Raises:
#         :class:`gTTSError`: When there's an error with the API request.
#         TypeError: When ``fp`` is not a file-like object that takes bytes.

#     """

#     try:
#         for idx, decoded in enumerate(self.stream()):
#             fp.write(decoded)
#             log.debug("part-%i written to %s", idx, fp)
#     except (AttributeError, TypeError) as e:
#         raise TypeError(
#             "'fp' is not a file-like object or it does not take bytes: %s" % str(e)
#         )


async def main():
    # Start the WebSocket server on localhost, port 8765.
    async with websockets.serve(tts_handler, "localhost", 8765):
        print("TTS server is running on ws://localhost:8765...")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
