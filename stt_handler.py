import assemblyai as aai
import os
import time
from threading import Timer

# Configure your API key
assemblyai_api_key = os.getenv("ASSEMBLYAI_API_KEY")
aai.settings.api_key = assemblyai_api_key
print(assemblyai_api_key)

# Add these global variables
current_speech = ""
last_speech_time = time.time()
speech_timer = None

def on_open(session_opened: aai.RealtimeSessionOpened):
    print("Session ID:", session_opened.session_id)

def on_data(transcript: aai.RealtimeTranscript):
    global current_speech, last_speech_time, speech_timer

    if isinstance(transcript, aai.RealtimeFinalTranscript):
        current_speech = transcript.text + " "
        last_speech_time = time.time()

        if speech_timer:
            speech_timer.cancel()

        speech_timer = Timer(2.0, process_speech)
        speech_timer.start()

        print(transcript.text, end="\r\n")
    else:
        # For partial transcripts, just print without adding to current_speech
        print(transcript.text, end="\r")

def process_speech():
    global current_speech
    if current_speech.strip():
        print(f"\nProcessed speech: {current_speech.strip()}")
        # Exit the program after processing the speech
        print("Exiting program...")
        os._exit(0)
    current_speech = ""

def on_error(error: aai.RealtimeError):
    print("An error occurred:", error)

def on_close():
    print("Closing Session")
    if speech_timer:
        speech_timer.cancel()

# Create a real-time transcriber
transcriber = aai.RealtimeTranscriber(
    sample_rate=16_000,
    on_data=on_data,
    on_error=on_error,
    on_open=on_open,
    on_close=on_close,
)

# Connect to the AssemblyAI API
transcriber.connect()

# Start streaming audio from the microphone
microphone_stream = aai.extras.MicrophoneStream(sample_rate=16_000)
transcriber.stream(microphone_stream)

# The program will now exit automatically after processing speech
