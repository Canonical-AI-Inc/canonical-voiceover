#!/usr/bin/env python3

# Input and output filenames
INPUT_AUDIO = "" # replace with your full filepath to your final audio file (/Users/you/.../reconstructed_song.mp3)
OUTPUT_VIDEO = "" # replace with your full filepath to your final video file (/Users/you/.../reconstructed_song_video.mp4) 

import numpy as np
import librosa
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import LineCollection
from moviepy.editor import VideoClip, AudioFileClip
import os

def create_waveform_video(audio_path, output_path, fps=30, video_duration=None, 
                         segment_length=0.1, background_color='black', 
                         first_ten_seconds=False):
    """
    Create a video with an animated waveform visualization from an audio file.
    
    Args:
        audio_path (str): Path to input audio file
        output_path (str): Path where the output video will be saved
        fps (int): Frames per second for the output video
        video_duration (float): Duration of video in seconds (defaults to audio length)
        segment_length (float): Length of audio segment to visualize in seconds
        background_color (str): Background color of the video
        first_ten_seconds (bool): If True, only output the first 10 seconds
    """
    print(f"Loading audio file: {audio_path}")
    
    # Load audio file
    y, sr = librosa.load(audio_path, sr=None)
    
    # Get audio duration
    audio_duration = librosa.get_duration(y=y, sr=sr)
    
    # Handle first_ten_seconds option
    if first_ten_seconds:
        video_duration = min(10.0, audio_duration)
        # Limit the audio samples to the first 10 seconds
        max_samples = int(10.0 * sr)
        if len(y) > max_samples:
            y = y[:max_samples]
    elif video_duration is None:
        video_duration = audio_duration
    else:
        video_duration = min(video_duration, audio_duration)
    
    # Calculate samples per frame
    samples_per_frame = int(sr / fps)
    
    # Calculate samples per segment
    samples_per_segment = int(segment_length * sr)
    
    # Calculate total number of frames
    total_frames = int(video_duration * fps)
    
    # Number of points to display in the waveform (reduced for less detail)
    num_display_points = 1000
    
    # Custom function to convert matplotlib figure to numpy array
    def fig_to_numpy(fig):
        # Draw the figure
        fig.canvas.draw()
        
        # Get the RGBA buffer from the figure
        w, h = fig.canvas.get_width_height()
        buf = np.frombuffer(fig.canvas.tostring_argb(), dtype=np.uint8)
        buf.shape = (h, w, 4)
        
        # Convert ARGB to RGB
        buf = np.roll(buf, -1, axis=2)[:,:,:3]
        return buf
    
    # Set up the figure for plotting
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=background_color)
    ax.set_facecolor(background_color)
    ax.set_ylim(-0.8, 0.8)
    ax.set_xlim(0, 1)  # Normalized x-axis from 0 to 1
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Initialize empty line collection
    line = LineCollection([], linewidths=3, alpha=1.0)
    ax.add_collection(line)
    
    # No clock/title at the top
    
    def make_frame(t):
        # Calculate current position in audio
        current_time = t
        current_sample = int(current_time * sr)
        
        # Get audio segment around current time
        half_segment = samples_per_segment // 2
        start_sample = max(0, current_sample - half_segment)
        end_sample = min(len(y), current_sample + half_segment)
        
        # Extract audio segment
        segment = y[start_sample:end_sample]
        
        # Resample to desired display points if needed
        if len(segment) > num_display_points:
            # Resample by taking evenly spaced points
            indices = np.linspace(0, len(segment) - 1, num_display_points, dtype=int)
            segment = segment[indices]
        
        # Create x coordinates (normalized from 0 to 1)
        x = np.linspace(0, 1, len(segment))
        
        # Create segments for the line collection
        points = np.array([x, segment]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        
        # Use single blue color for waveform
        line.set_segments(segments)
        line.set_color('#00AAFF')  # Bright blue color
        
        # No clock/title update needed
        
        # Convert the matplotlib figure to an RGB frame
        return fig_to_numpy(fig)
    
    # Create MoviePy clip
    animation_clip = VideoClip(make_frame, duration=video_duration)
    
    # Add audio to the clip
    audio_clip = AudioFileClip(audio_path)
    if first_ten_seconds and audio_duration > 10.0:
        audio_clip = audio_clip.subclip(0, 10.0)
    animation_clip = animation_clip.set_audio(audio_clip)
    
    # Write the result to a file
    print(f"Creating video file: {output_path}")
    animation_clip.write_videofile(output_path, fps=fps, codec='libx264', 
                                  audio_codec='aac', audio=True)
    
    # Clean up
    plt.close(fig)
    
    try:
        audio_clip.close()
        animation_clip.close()
    except:
        # In some moviepy versions, clips might not have a close() method
        pass
    
    print(f"Video created successfully: {output_path}")
    return output_path

def main():
    create_waveform_video(
        INPUT_AUDIO,
        OUTPUT_VIDEO,
        fps=30,
        video_duration=None,  # Set to None to use full audio length
        segment_length=0.1,   # Length of audio segment to display (in seconds)
        background_color='black',
        first_ten_seconds=False  # Set to True to output only first 10 seconds
    )

if __name__ == "__main__":
    main()