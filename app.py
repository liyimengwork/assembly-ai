import assemblyai as aai
import os

# Configure your API key
assemblyai_api_key = os.getenv("ASSEMBLYAI_API_KEY")
aai.settings.api_key = assemblyai_api_key
print(assemblyai_api_key)

def on_open(session_opened: aai.RealtimeSessionOpened):
    print("Session ID:", session_opened.session_id)

def on_data(transcript: aai.RealtimeTranscript):
    if not transcript.text:
        return
    if isinstance(transcript, aai.RealtimeFinalTranscript):
        print(transcript.text, end="\r\n")
    else:
        print(transcript.text, end="\r")

def on_error(error: aai.RealtimeError):
    print("An error occurred:", error)

def on_close():
    print("Closing Session")

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

# The program will continue to transcribe until interrupted (e.g., Ctrl+C)
try:
    input("Press Enter to stop transcribing...")
except KeyboardInterrupt:
    pass

# Close the connection
transcriber.close()