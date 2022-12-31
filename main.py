# Install the necessary libraries
!pip install SpeechRecognition
!pip install openai
!pip install gTTS
!pip install pyaudio

# Import the libraries
import speech_recognition as sr
import openai
import os
from gtts import gTTS
import pyaudio
import wave

# Set the API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Define a function to generate a response from GPT-3
def generate_response(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message

# Initialize the Recognizer and set the microphone as the audio source
r = sr.Recognizer()
with sr.Microphone() as source:
    audio = r.listen(source)

# Convert the audio to text
text = r.recognize_google(audio)
print(text)

# Generate a response from GPT-3
response = generate_response(text)
print(response)

# Convert the response to audio
tts = gTTS(response)
tts.save("response.mp3")

# Play the audio
os.system("response.mp3")

# Initialize PyAudio and set the microphone as the audio source
audio = pyaudio.PyAudio()

input_device_index = None
for i in range(audio.get_device_count()):
    device_info = audio.get_device_info_by_index(i)
    if device_info["name"].lower() == "microphone":
        input_device_index = device_info["index"]
        break

if input_device_index is None:
    raise ValueError("No microphone was found")

stream = audio.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=44100,
    input=True,
    input_device_index=input_device_index,
)

# Create a Wave_write object and save the audio to a file
wavefile = wave.open("recording.wav", "wb")
wavefile.setnchannels(1)
wavefile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
wavefile.setframerate(44100)

data = stream.read(1024)
while data:
    wavefile.writeframes(data)
    data = stream.read(1024)

wavefile.close()
stream.stop_stream()
stream.close()
audio.terminate()
