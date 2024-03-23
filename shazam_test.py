from pydub import AudioSegment
from key import API_KEY
import base64
import requests
import os 
from IPython import embed
import pandas as pd

path_samples = "audio_samples"
songs = os.listdir(path_samples)
songs = songs[3:]

def get_song(base64_audio):
    url = "https://rapidapi.p.rapidapi.com/songs/detect"

    headers = {
        'content-type': "text/plain",
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "shazam.p.rapidapi.com"
        }

    response = requests.request("POST", url, data=base64_audio, headers=headers)
    response_json = response.json()
    
    return response_json



def trim_song(audio_segment):
    """
    If the song duration is longer than 5 seconds, it will be trimmed to 5 seconds.
    """
    duration = audio_segment.duration_seconds * 1000
    resulting_duration = 3000
    
    if duration > resulting_duration:
        trim_duration = int((duration - resulting_duration)/2)
        audio_segment = audio_segment[trim_duration:-trim_duration]
    return audio_segment

artist = []
song_title = []
    
for song in songs:

    file_foramt = song.split('.')[-1]
    path_song = os.path.join(path_samples, song)
    
    audio = AudioSegment.from_file(path_song, format=file_foramt)
    # audio = trim_song(audio)
    # print(audio.duration_seconds)
    raw_audio = audio.raw_data
    base64_audio = base64.b64encode(raw_audio).decode('utf-8')

    response = get_song(base64_audio)
    
    if 'track' not in response:
        artist.append(None)
        song_title.append(None)
        continue

    track = response['track']
    title = track['title']
    subtitle = track['subtitle']
    
    artist.append(subtitle)
    song_title.append(title)
    
    

df = pd.DataFrame({'sample_name': songs, 'artist': artist, 'song_title': song_title})
df.to_csv('test_results.csv', index=False)
