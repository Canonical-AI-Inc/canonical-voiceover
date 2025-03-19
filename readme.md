# Audio Track Creator

A tool to create custom tracks by combining AI-generated voice with instrumental music. This project lets you download songs from YouTube, remove vocals, generate spoken lyrics, and combine them with the instrumental track to create a new audio experience with visualization.

## Setup

1. Install required packages:
   ```
   pip install -r requirements.txt
   ```

2. For voice generation, create a `.env` file in the project directory with your ElevenLabs API key:
   ```
   ELEVENLABS_API_KEY=your_api_key_here
   ```

## Usage

Run the scripts in this order:

1. **Download a song**:
   Edit `download_song.py` to set your YouTube URL and output filename:
   ```
   python download_song.py
   ```

2. **Create instrumental version**:
   Edit `remove_vocals.py` to set your input and output filenames:
   ```
   python remove_vocals.py
   ```

3. **Generate spoken lyrics**:
   Edit `generate_spoken_lyrics.py` to set your ElevenLabs voice ID and output filename:
   ```
   python generate_spoken_lyrics.py
   ```

4. **Combine vocals with instrumental**:
   Edit `combine_spoken_lyrics_with_instrumental.py` to set your input and output filenames:
   ```
   python combine_spoken_lyrics_with_instrumental.py
   ```

5. **Create visualization** (optional):
   Edit `song_to_waveform.py` to set your input audio and output video filenames:
   ```
   python song_to_waveform.py
   ```

## Files

- `download_song.py`: Downloads audio from YouTube
- `remove_vocals.py`: Creates instrumental version by removing vocals
- `generate_spoken_lyrics.py`: Creates AI-spoken lyrics using ElevenLabs
- `combine_spoken_lyrics_with_instrumental.py`: Mixes spoken lyrics with instrumental
- `song_to_waveform.py`: Creates waveform visualization video

## License

This project is licensed under the Apache License 2.0 - see LICENSE file for details.