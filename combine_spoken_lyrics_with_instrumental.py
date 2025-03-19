#!/usr/bin/env python3

# Input and output filenames
SPEECH_INPUT = "/Users/tom/tmp/voiceover/lyrics.wav"
INSTRUMENTAL_INPUT = "/Users/tom/tmp/voiceover/instrumental_version.mp3"
OUTPUT_FILENAME = "/Users/tom/tmp/voiceover/reconstructed_song.mp3"

from pydub import AudioSegment

def combine_audio_tracks(speech_path, instrumental_path, output_path, 
                         speech_volume_adj=0, instrumental_volume_adj=0, 
                         speech_position=0):
    """
    Combine a vocal track with an instrumental track.
    
    Args:
        speech_path (str): Path to the vocal WAV file
        instrumental_path (str): Path to the instrumental MP3 file
        output_path (str): Path where the combined MP3 file will be saved
        speech_volume_adj (int): dB adjustment for speech volume (positive to increase)
        instrumental_volume_adj (int): dB adjustment for instrumental volume
        speech_position (int): Position in milliseconds to place the speech
    """
    # Load both audio files
    speech = AudioSegment.from_wav(speech_path)
    instrumental = AudioSegment.from_mp3(instrumental_path)
    
    # Adjust volumes if needed
    if speech_volume_adj != 0:
        speech = speech + speech_volume_adj
    
    if instrumental_volume_adj != 0:
        instrumental = instrumental - instrumental_volume_adj
    
    # Make sure the instrumental is at least as long as the speech
    if len(instrumental) < len(speech) + speech_position:
        # Extend the instrumental by looping or padding with silence
        padding = AudioSegment.silent(duration=len(speech) + speech_position - len(instrumental))
        instrumental = instrumental + padding
    
    # Overlay the speech on top of the instrumental
    combined = instrumental.overlay(speech, position=speech_position)
    
    # Export the final result
    combined.export(output_path, format="mp3")
    
    print(f"Successfully combined tracks and saved to {output_path}")
    return output_path

def main():
    # Default usage with your specified files
    combine_audio_tracks(
        SPEECH_INPUT,
        INSTRUMENTAL_INPUT,
        OUTPUT_FILENAME,
        speech_volume_adj=0,  # Adjust these values as needed
        instrumental_volume_adj=0, # Adjust these values as needed
        speech_position=0 # Adjust these values as needed
    )

if __name__ == "__main__":
    main()