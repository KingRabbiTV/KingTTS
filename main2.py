from RealtimeTTS import TextToAudioStream, SystemEngine, AzureEngine, ElevenlabsEngine

def my_audio_chunk_handler(chunk):
    # Here, 'chunk' is a byte string representing a PCM audio chunk.
    # You can process it (e.g., stream it over a network, save to a file, etc.)
    print("Received audio chunk of", len(chunk), "bytes")

engine = SystemEngine() # replace with your TTS engine
stream = TextToAudioStream(engine, on_audio_chunk=my_audio_chunk_handler)
stream.feed("Hello world! How are you today?")
# stream.play_async()