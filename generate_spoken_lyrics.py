#!/usr/bin/env python3

# Input and output filenames
VOICE_ID = "CwhRBWXzGAHq8TQ4Fs17"  # Replace with actual voice ID
VOICE_NAME = "Roger" # Replace with actual voice name
OUTPUT_FILENAME = "" # replace with your full filepath (/Users/you/.../lyrics.wav)

# Use dotenv to load environment variables
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
API_KEY = os.getenv("ELEVENLABS_API_KEY")

import requests
import argparse
from pathlib import Path
from pydub import AudioSegment
import os
from dotenv import load_dotenv

# ElevenLabs API base URL
API_BASE_URL = "https://api.elevenlabs.io/v1"

def generate_speech(text, output_path, api_key, voice, stability=0.9, similarity_boost=0.75):
    """Generate speech using ElevenLabs API and convert to WAV."""
    headers = {
        "Accept": "audio/mpeg",
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost,
            "speaking_rate": 0.5
        }
    }
    
    response = requests.post(
        f"{API_BASE_URL}/text-to-speech/{voice['id']}",
        json=data,
        headers=headers
    )
    
    if response.status_code == 200:
        # Save temporary MP3 file
        temp_mp3 = output_path.with_suffix('.mp3')
        with open(temp_mp3, 'wb') as f:
            f.write(response.content)
            
        # Convert MP3 to WAV using pydub
        audio = AudioSegment.from_mp3(temp_mp3)
        audio.export(output_path, format='wav')
        
        # Remove temporary MP3 file
        temp_mp3.unlink()
        return True
    else:
        print(f"Error generating speech: {response.status_code}")
        return False

lyrics = [
    "Fitter... happier... ... ",
    "More... productive... ... ",
    "Comfortable... ... ",
    "Not drinking too much... ... "
    "Regular exercise at the gym... 3 days a week... ... ",
    "Getting on better with your associate employee contemporaries... ... ",
    "At ease... ... ",
    "Eating well... no more microwave dinners and saturated fats... ... ",
    "A patient, better driver... ... ",
    "A safer car... baby smiling in back seat... ... ",
    "Sleeping well... no bad dreams... ... ",
    "No paranoia... ... ",
    "Careful to all animals... never washing spiders down the plughole... ... ",
    "Keep in contact with old friends... enjoy a drink now and then... ... ",
    "Will frequently check credit at... moral... bank... hole in the wall... ... ",
    "Favours for favours... ... ",
    "Fond but not in love... ... ",
    "Charity standing orders... ... ",
    "On Sundays ring road supermarket... ... ",
    "No killing moths or putting boiling water on the ants... ... ",
    "Car wash... also on Sundays... ... ",
    "No longer afraid of the dark or midday shadows... ... ",
    "Nothing so ridiculously teenage and desperate... ... ",
    "Nothing so childish... ... ",
    "At a better pace... ... ",
    "Slower and more calculated",
    "No chance of escape",
    "Now self-employed... ... ",
    "Concerned but powerless... ... ",
    "An empowered and informed member of society... pragmatism not idealism... ... ",
    "Will not cry in public... ... ",
    "Less chance of illness... ... ",
    "Tires that grip in the wet... shot of baby strapped in back seat... ... ",
    "A good memory... ... ",
    "Still cries at a good film... ... ",
    "Still kisses with saliva... ... ",
    "No longer empty and frantic... ... ",
    "Like a cat... ... ",
    "Tied to a stick... ... ",
    "That's driven into... ... ",
    "Frozen winter shit... the ability to laugh at weakness... ... ",
    "Calm... ... ",
    "Fitter, healthier... and more productive... ... ",
    "A pig... ... ",
    "In a cage... ... ",
    "On antibiotics"
    ]


def create_spoken_lyrics():
    # Add pauses and formatting for better speech synthesis
    formatted_text = ""
    for lyric in lyrics:
        formatted_text += f"{lyric}. <break time='2s'/>\n"
       
    return formatted_text

def main():
    """Main function to generate the speech file."""
    # Check if API key is available
    if not API_KEY:
        print("Error: ELEVENLABS_API_KEY not found in environment variables.")
        print("Please create a .env file with your ELEVENLABS_API_KEY.")
        return
    
    output_path = Path(OUTPUT_FILENAME)
    
    # Set up voice configuration
    voice = {
        "id": VOICE_ID,
        "name": VOICE_NAME
    }
    
    # Generate the text
    speech_text = create_spoken_lyrics()
    
    print(f"Generating speech file to {output_path}...")
    success = generate_speech(
        text=speech_text,
        output_path=output_path,
        api_key=API_KEY,
        voice=voice
    )
    
    if success:
        print(f"Speech generated successfully: {output_path}")
    else:
        print("Failed to generate speech")

if __name__ == "__main__":
    main()