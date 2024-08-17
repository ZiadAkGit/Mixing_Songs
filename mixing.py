import subprocess
import librosa
import os


def calculate_bpm(audio_file):
    """
    Calculate the BPM (Beats Per Minute) of an audio file.

    :param audio_file: Path to the audio file.
    :return: Estimated BPM of the audio file.
    """
    y, sr = librosa.load(audio_file)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return tempo


def crossfade_audio(first_file, second_file, output_file_path, crossfade_duration):
    """
    Crossfade two MP3 files together.

    :param first_file: Path to the first MP3 file.
    :param second_file: Path to the second MP3 file.
    :param output_file_path: Path where the output file will be saved.
    :param crossfade_duration: Duration of the crossfade in seconds.
    """
    command = [
        'ffmpeg', '-i', first_file, '-i', second_file, '-filter_complex',
        f'[0][1]acrossfade=d={crossfade_duration}', '-c:a', 'libmp3lame', output_file_path
    ]
    subprocess.run(command, check=True)


def process_directory(directory, output_directory, bpm_tolerance=5, crossfade_duration=5):
    """
    Process all MP3 files in a directory, combining them with a crossfade effect if their BPMs are similar.

    :param directory: Path to the directory containing MP3 files.
    :param output_directory: Directory where the output files will be saved.
    :param bpm_tolerance: Allowed BPM difference between songs to combine them.
    :param crossfade_duration: Duration of the crossfade effect.
    """
    print("Starting to search for songs!")
    # Get all MP3 files in the directory
    song_list = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.mp3')]
    song_list.sort()  # Sort the list if you want a specific order
    if not os.path.exists(output_directory):
        print("Creating the final directory!")
        os.makedirs(output_directory)
    # Process each pair of songs
    for i in range(len(song_list) - 1):
        song1 = song_list[i]
        song2 = song_list[i + 1]
        bpm1 = calculate_bpm(song1)
        bpm2 = calculate_bpm(song2)
        print(f"BPM of {os.path.basename(song1)}: ~{int(bpm1)}")
        print(f"BPM of {os.path.basename(song2)}: ~{int(bpm2)}")
        if abs(bpm1 - bpm2) <= bpm_tolerance:
            print("BPM Match!! Creating mix!")
            output_file = os.path.join(output_directory, f"final{i+1}.mp3")
            crossfade_audio(song1, song2, output_file, crossfade_duration=crossfade_duration)
            print(f"Songs combined: {os.path.basename(song1)} and {os.path.basename(song2)}")
        else:
            print(f"Skipped combining: {os.path.basename(song1)} and {os.path.basename(song2)} due to BPM difference")


# Example usage:
input_dir = 'C:\\Users\\ziada\\Downloads\\Tracks'  # Replace with your directory containing MP3 files
output_dir = 'C:\\Users\\ziada\\Downloads\\Tracks\\final'
process_directory(input_dir, output_dir, bpm_tolerance=10, crossfade_duration=7)
