import subprocess
import librosa
import os
import random
import requests
from bs4 import BeautifulSoup

import ignore


def get_songs():
    """Fetch song titles from the TikTok Billboard Top 50 page."""
    try:
        r = requests.get("https://www.billboard.com/charts/tiktok-billboard-top-50/")
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        testData = soup.select('[class*="c-title a-no-trucate a-font-primary-bold-s"]')
        data = "\n".join([f"{i+1}. {song.text.strip()}" for i, song in enumerate(testData)])
        return data
    except Exception as e:
        print(f"Error fetching songs: {e}")
        return ""


def temp_optimizer(tempo):
    """Calculate crossfade duration based on tempo."""
    try:
        beat_duration = 60.0 / float(tempo)  # Convert tempo to float
        crossfade_duration = beat_duration * 2
        return crossfade_duration
    except ZeroDivisionError:
        print("Error: Tempo cannot be zero.")
        return 0.3  # Default fallback value


def calculate_bpm(audio_file):
    """Calculate the BPM (tempo) of an audio file."""
    try:
        y, sr = librosa.load(audio_file, sr=None)  # Use native sampling rate
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        return tempo
    except Exception as e:
        print(f"Error calculating BPM for {audio_file}: {e}")
        return None


def crossfade_audio(first_file, second_file, output_file_path, crossfade_duration):
    """Perform crossfade between two audio files and save the output."""
    crossfade_d = crossfade_duration*1000
    print("The duration is: ", crossfade_d)
    command1 = [
        'ffmpeg', '-i', first_file, '-i', second_file, '-filter_complex',
        f'[0][1]acrossfade=d={crossfade_d}ms:c1=nofade:c2=nofade', '-b:a', '320k', output_file_path
    ]
    try:
        subprocess.run(command1, check=True)
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error during crossfade: {e}")


def validate_file(file_path):
    """Check if a file exists and is not empty."""
    return os.path.isfile(file_path) and os.path.getsize(file_path) > 0


def cleanup_temp_files(output_directory):
    """Delete all but the last two temporary files in the output directory."""
    temp_files = sorted(
        [os.path.join(output_directory, f) for f in os.listdir(output_directory) if f.startswith('temp_')],
        key=os.path.getmtime
    )
    if len(temp_files) > 2:
        for temp_file in temp_files[:-2]:
            try:
                os.remove(temp_file)
                print(f"Deleted old temp file: {temp_file}")
            except Exception as e:
                print(f"Error deleting temp file {temp_file}: {e}")


def process_directory(directory, output_directory, bpm_tolerance, genre_chosen, bpm_check):
    """Process a directory of songs and generate a mixed output."""
    song_list = [
        os.path.join(directory, f)
        for f in os.listdir(directory) if f.lower().endswith('.mp3')
    ]
    print(f"Number of songs in directory: {len(song_list)}")

    if len(song_list) < 2:
        print("Not enough songs to process.")
        return

    random.shuffle(song_list)

    if not os.path.exists(output_directory):
        print("Creating the output directory!")
        os.makedirs(output_directory)

    output_file = os.path.join(output_directory, f'{genre_chosen}_final_mix.mp3')
    temp_output = song_list[0]

    for i in range(1, len(song_list)):
        song1 = temp_output
        song2 = song_list[i]

        # Validate input files
        if not (validate_file(song1) and validate_file(song2)):
            print(f"Skipping invalid or empty file: {song1} or {song2}")
            continue

        bpm1 = calculate_bpm(song1)
        bpm2 = calculate_bpm(song2)

        if bpm1 is None or bpm2 is None:
            print(f"Skipping song pair due to BPM calculation failure: {song1}, {song2}")
            continue

        # BPM check
        if bpm_check and abs(bpm1 - bpm2) > bpm_tolerance:
            print(f"✖️ Skipped Combining ✖️ - {song1} and {song2} don't match BPM!")
            continue

        if bpm_check and abs(bpm1 - bpm2) <= bpm_tolerance:
            print(f"✔️ Combining {song1} and {song2} With BPM Check!")
            crossfade_duration = temp_optimizer(bpm2)
            output_temp_file = os.path.join(output_directory, f'temp_{i}.mp3')
            crossfade_audio(temp_output, song2, output_temp_file, crossfade_duration)
            temp_output = output_temp_file
        elif not bpm_check:
            print(f"✔️ Combining {song1} and {song2} Without BPM Check!")
            output_temp_file = os.path.join(output_directory, f'temp_{i}.mp3')
            crossfade_audio(temp_output, song2, output_temp_file, 0)
            temp_output = output_temp_file

        # Cleanup old temp files
        cleanup_temp_files(output_directory)

    print(f"Mixing completed. Final output saved at: {output_file}")


# Example usage (replace 'input_dir' and 'output_dir' with actual directories)
process_directory(
    directory=ignore.input_dir,
    output_directory=ignore.output_dir,
    bpm_tolerance=9,
    genre_chosen="club",
    bpm_check=False,
)
