#!/usr/bin/env python3
# Vocal Remover Script using Demucs

# Input: Song file with vocals
INPUT_AUDIO = "/Users/tom/tmp/voiceover/downloaded_song.mp3"
# Output: Song file without vocals
OUTPUT_AUDIO = "" # replace with your full filepath (/Users/you/.../instrumental_version.mp3)

import os
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path

def check_demucs_installed():
    """Check if Demucs is installed, install if not."""
    try:
        subprocess.run(["demucs", "--version"], capture_output=True, text=True, check=False)
        return True
    except FileNotFoundError:
        print("Demucs not found. Installing Demucs...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "demucs"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to install Demucs: {e}")
            return False

def create_temp_directory():
    """Create a temporary directory for processing files."""
    return tempfile.mkdtemp()

def separate_audio(input_file, output_dir, model="mdx_extra"):
    """
    Separate the vocals from the instrumental using Demucs.
    
    Parameters:
    - input_file: Path to the input audio file
    - output_dir: Directory to output separated tracks
    - model: Demucs model to use (mdx_extra, mdx_extra_q, htdemucs, etc.)
    
    Returns:
    - True if separation was successful, False otherwise
    """
    print(f"Separating audio using Demucs model '{model}'...")
    
    try:
        # Use Demucs to separate the audio into stems
        subprocess.run([
            "demucs", 
            "--two-stems=vocals", 
            "-n", model,
            "-o", output_dir,
            input_file
        ], check=True)
        
        print("Separation complete!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Separation failed: {e}")
        return False

def get_instrumental_path(output_dir, input_file, model="mdx_extra"):
    """Get the path to the instrumental file after separation."""
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    model_dir = "htdemucs" if model == "htdemucs" else "mdx_extra"
    
    # Demucs creates subfolders with model name, then song name, then stems
    instrumental_path = os.path.join(output_dir, model_dir, base_name, "no_vocals.wav")
    
    if os.path.exists(instrumental_path):
        return instrumental_path
    
    # Alternative path format for some Demucs versions
    alternative_path = os.path.join(output_dir, model_dir, base_name, "other.wav")
    if os.path.exists(alternative_path):
        return alternative_path
    
    return None

def convert_to_mp3(input_file, output_file):
    """Convert WAV to MP3 using FFmpeg."""
    print(f"Converting to MP3: {output_file}")
    
    try:
        subprocess.run([
            "ffmpeg", 
            "-i", input_file,
            "-codec:a", "libmp3lame", 
            "-qscale:a", "2", 
            output_file,
            "-y"  # Overwrite existing file
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print("Conversion complete!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed: {e}")
        return False

def cleanup(temp_dir):
    """Remove temporary directory and files."""
    try:
        shutil.rmtree(temp_dir)
        print("Temporary files cleaned up.")
    except Exception as e:
        print(f"Failed to clean up temporary files: {e}")

def main():
    """Main function to remove vocals from audio."""
    # Verify input file exists
    if not os.path.exists(INPUT_AUDIO):
        print(f"Error: Input file {INPUT_AUDIO} not found.")
        return
    
    # Check if Demucs is installed
    if not check_demucs_installed():
        return
    
    # Create temporary directory
    temp_dir = create_temp_directory()
    
    try:
        # Selected Demucs model (mdx_extra is the best quality default)
        model = "mdx_extra"
        
        # Separate vocals from instrumental
        if not separate_audio(INPUT_AUDIO, temp_dir, model):
            return
        
        # Get path to instrumental file
        instrumental_path = get_instrumental_path(temp_dir, INPUT_AUDIO, model)
        if not instrumental_path:
            print("Could not find separated instrumental file. Trying alternative path formats...")
            # Try other model names as fallback
            for alt_model in ["htdemucs", "mdx_extra_q"]:
                instrumental_path = get_instrumental_path(temp_dir, INPUT_AUDIO, alt_model)
                if instrumental_path:
                    break
            
            if not instrumental_path:
                print("Could not find separated instrumental file. Please check Demucs output.")
                return
        
        # Convert to MP3
        if not convert_to_mp3(instrumental_path, OUTPUT_AUDIO):
            return
        
        print(f"Successfully created instrumental version: {OUTPUT_AUDIO}")
        
    finally:
        # Clean up temporary files
        cleanup(temp_dir)

if __name__ == "__main__":
    main()