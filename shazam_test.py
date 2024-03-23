from pydub import AudioSegment
from key import API_KEY
import base64
import requests


audio = AudioSegment.from_file("audio_samples/sample1.m4a", format="m4a")
raw_audio = audio[:3000].raw_data
base64_audio = base64.b64encode(raw_audio).decode('utf-8')

url = "https://rapidapi.p.rapidapi.com/songs/detect"

headers = {
    'content-type': "text/plain",
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': "shazam.p.rapidapi.com"
    }

response = requests.request("POST", url, data=base64_audio, headers=headers)
response_json = response.json()
track = response_json['track']

print(f"{track['title']} - {track['subtitle']}")
