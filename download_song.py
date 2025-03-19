#!/usr/bin/env python3
# YouTube Song Downloader

# Input: YouTube URL
INPUT_URL = "https://www.youtube.com/watch?v=O4SzvsMFaek"  # Replace with your YouTube URL
# Output: MP3 filename (absolute path)
OUTPUT_FILENAME = "" # replace with your full filepath (/Users/you/.../downloaded_song.mp3)

import sys
import os
import subprocess
import tempfile
import re
from urllib.parse import urlparse, parse_qs

def validate_url(url):
    """Validate that the URL is a proper YouTube URL."""
    if not url.startswith(("https://www.youtube.com/", "https://youtu.be/", "http://www.youtube.com/", "http://youtu.be/")):
        print(f"Error: '{url}' does not appear to be a valid YouTube URL.")
        return False
    return True

def get_video_id(url):
    """Extract the video ID from a YouTube URL."""
    if "youtube.com" in url:
        query = urlparse(url).query
        return parse_qs(query).get("v", [None])[0]
    elif "youtu.be" in url:
        return urlparse(url).path.lstrip("/")
    return None

def download_with_pytube(url, output_path):
    """Try to download using pytube."""
    try:
        from pytube import YouTube
        
        # Create YouTube object
        yt = YouTube(url)
        
        # Get title for display
        title = yt.title
        print(f"Found: {title}")
        
        # Get audio stream with highest quality
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        
        if not audio_stream:
            print("No audio stream found.")
            return False
        
        # Get temporary filename for downloaded file
        temp_file = audio_stream.download(output_path=tempfile.gettempdir())
        
        # Convert to MP3
        convert_to_mp3(temp_file, output_path)
        
        # Clean up temporary file
        os.remove(temp_file)
        
        return True
        
    except Exception as e:
        print(f"Pytube error: {str(e)}")
        return False

def download_with_yt_dlp(url, output_path):
    """Try to download using yt-dlp."""
    try:
        # Make sure output directory exists
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)
        
        # Check if yt-dlp is installed
        try:
            subprocess.run(["yt-dlp", "--version"], capture_output=True, check=False)
        except FileNotFoundError:
            print("yt-dlp not found. Installing...")
            subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], check=True)
        
        # Download directly to MP3 format
        print("Downloading with yt-dlp...")
        result = subprocess.run([
            "yt-dlp",
            "-f", "bestaudio",
            "-x",  # Extract audio
            "--audio-format", "mp3",  # Convert to MP3
            "--audio-quality", "0",  # Best quality
            "-o", output_path,  # Output directly to the desired path
            url
        ], capture_output=True, text=True, check=False)
        
        if result.returncode != 0:
            print(f"yt-dlp error: {result.stderr}")
            return False
            
        # Verify the file exists
        if os.path.exists(output_path):
            print(f"Downloaded and converted to: {output_path}")
            return True
        else:
            print(f"File not found after download: {output_path}")
            # Try with extension
            if os.path.exists(f"{output_path}.mp3"):
                print(f"Found file with .mp3 extension added: {output_path}.mp3")
                os.rename(f"{output_path}.mp3", output_path)
                return True
            return False
        
    except Exception as e:
        print(f"yt-dlp error: {str(e)}")
        return False

def convert_to_mp3(input_file, output_file):
    """Convert downloaded audio file to MP3 format using FFmpeg."""
    try:
        print("Converting to MP3...")
        
        # Make sure output directory exists
        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)
        
        # Use subprocess to call ffmpeg
        result = subprocess.run([
            "ffmpeg",
            "-i", input_file,
            "-codec:a", "libmp3lame",
            "-qscale:a", "2",
            output_file,
            "-y"  # Overwrite existing file
        ], capture_output=True, text=True, check=False)
        
        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr}")
            return False
            
        # Verify the file exists
        if os.path.exists(output_file):
            return True
        else:
            print(f"File not found after conversion: {output_file}")
            return False
            
    except Exception as e:
        print(f"Error converting to MP3: {str(e)}")
        return False

def main():
    """Main function to run the downloader."""
    # Ensure output directory exists
    output_dir = os.path.dirname(OUTPUT_FILENAME)
    os.makedirs(output_dir, exist_ok=True)
    
    # Validate the URL
    if not validate_url(INPUT_URL):
        return
    
    print(f"Downloading audio from: {INPUT_URL}")
    print(f"Output will be saved to: {OUTPUT_FILENAME}")
    
    # Try different methods to download
    if download_with_pytube(INPUT_URL, OUTPUT_FILENAME):
        print(f"Successfully downloaded to {OUTPUT_FILENAME} using pytube")
    elif download_with_yt_dlp(INPUT_URL, OUTPUT_FILENAME):
        print(f"Successfully downloaded to {OUTPUT_FILENAME} using yt-dlp")
    else:
        print("All download methods failed. Please check the URL or try a different video.")
        return

if __name__ == "__main__":
    main()