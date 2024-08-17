import subprocess
import librosa
import os
import random
import ignore as ig


def calculate_bpm(audio_file):
    y, sr = librosa.load(audio_file)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return tempo


def crossfade_audio(first_file, second_file, output_file_path, crossfade_duration):
    command = [
        'ffmpeg', '-i', first_file, '-i', second_file, '-filter_complex',
        f'[0][1]acrossfade=d={crossfade_duration}', '-c:a', 'libmp3lame','-b:a', '320k', output_file_path
    ]
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr = subprocess.DEVNULL)


def process_directory(directory, output_directory, bpm_tolerance, crossfade_duration,genre_chosen):
    print("Starting to search for songs!")
    song_list = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.mp3')]
    random.shuffle(song_list)  # Shuffle the list to be random
    if not os.path.exists(output_directory):
        print("Creating the final directory!")
        os.makedirs(output_directory)
    output_file = os.path.join(output_directory, f'{genre_chosen}_final_mix.mp3')
    temp_output = song_list[0]
    for i in range(1, len(song_list)):
        song1 = temp_output
        song2 = song_list[i]
        bpm1 = calculate_bpm(song1)
        bpm2 = calculate_bpm(song2)
        print(f"BPM of {song1} is: ~{bpm1}")
        print(f"BPM of {song2} is: ~{bpm2}")
        if abs(bpm1 - bpm2) <= bpm_tolerance:
            print("BPM Match - combining songs")
            output_temp_file = os.path.join(output_directory, f'temp_{i}.mp3')
            crossfade_audio(temp_output, song2, output_temp_file, crossfade_duration)
            temp_output = output_temp_file
        else:
            print(f"Skipped combining: {song1} and {song2} due to BPM difference")
    os.rename(temp_output, output_file)
    for i in os.listdir(output_directory):
        if i.__contains__('temp_'):
            os.remove(f'{output_directory}\\{i}')
    print(f"Mix created successfully: {output_file}\nAll temp files were deleted!")


process_directory(ig.input_dir, ig.output_dir, bpm_tolerance=25, crossfade_duration=6, genre_chosen=ig.genre)
