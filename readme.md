# 🎵 Song Mixer Python Script 🎵

This Python script allows you to mix songs together by crossfading between them, automatically fetching songs from the TikTok Billboard Top 50, and calculating the BPM (beats per minute) of your audio files. 

## ✨ Features

- **🎧 Fetch Top Songs:** Automatically fetch the top songs from the TikTok Billboard Top 50.
- **💥 BPM Calculation:** Calculate the BPM of any audio file using the `librosa` library.
- **🎚️ Crossfade Songs:** Seamlessly mix two audio files with a crossfade effect using `ffmpeg`.

## 🚀 Getting Started

### Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- librosa library
- ffmpeg
- requests library
- beautifulsoup4 library

You can install the required Python libraries using pip install:

- pip install librosa
- pip install requests
- pip install beautifulsoup4

### Installation

Clone this repository to your local machine:

- git clone https://github.com/ziadakgit/Mixing_Songs.git
- cd Mixing_Songs

## 🛠️ Usage

### 1. Fetch the Top Songs

To get the top songs from the TikTok Billboard Top 50, run the `get_songs()` function:

from mixing import get_songs

top_songs = get_songs()
print(top_songs)

This will print the top 50 songs in a formatted list.

### 2. Calculate BPM of an Audio File

To calculate the BPM of an audio file, use the `calculate_bpm()` function:

from mixing import calculate_bpm

bpm = calculate_bpm("path/to/your/audiofile.mp3")
print(f"The BPM of the audio file is: {bpm}")

Replace `"path/to/your/audiofile.mp3"` with the path to your audio file.

### 3. Crossfade Two Audio Files

To crossfade two audio files together, use the `crossfade_audio()` function:

from mixing import crossfade_audio

crossfade_audio("path/to/first_audio.mp3", "path/to/second_audio.mp3", "output_file.mp3", 10)

This command will crossfade the two audio files with a 10-second overlap and save the output as `output_file.mp3`.

### 4. Run the Script from the Command Line

You can also run the script from the command line:

- python mixing.py

Ensure you modify the script to your specific needs, such as setting the paths to your audio files and choosing the crossfade duration.


## 🤝 Contributing

Feel free to fork this repository, submit pull requests, and suggest new features!

## 📧 Contact

If you have any questions, feel free to contact me via [GitHub](https://github.com/ziadakgit).