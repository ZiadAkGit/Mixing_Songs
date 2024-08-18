import subprocess
import librosa
import os
import random
import ignore as ig
import requests
from bs4 import BeautifulSoup

def get_songs():
    r = requests.get("https://www.billboard.com/charts/tiktok-billboard-top-50/")
    soup = BeautifulSoup(r.text, "html.parser")
    testData = soup.select('[class*="c-title a-no-trucate a-font-primary-bold-s"]')
    counter = 1
    data = ""
    for i in testData:
        song = i.text.strip()
        data += f'{counter}. {song}\n'
        counter += 1
    return data

def temp_optimizer(tempo):
    beat_duration = 60.0 / tempo
    crossfade_duration = beat_duration * 2
    return int(crossfade_duration)

def calculate_bpm(audio_file):
    y, sr = librosa.load(audio_file)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return tempo


def crossfade_audio(first_file, second_file, output_file_path, crossfade_duration):
    command = [
        'ffmpeg', '-i', first_file, '-i', second_file, '-filter_complex',
        f'[0][1]acrossfade=d={crossfade_duration}:c1=nofade:c2=nofade', '-b:a', '320k', output_file_path
    ]
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr = subprocess.DEVNULL)


def process_directory(directory, output_directory, bpm_tolerance, genre_chosen):
    song_list = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.mp3')]
    random.shuffle(song_list)  # Shuffle the list to be random
    if not os.path.exists(output_directory):
        print("Creating the final directory!")
        os.makedirs(output_directory)
    output_file = os.path.join(output_directory, f'{genre_chosen}_final_mix.mp3')
    temp_output = song_list[0]
    bpm_temp = []
    for i in range(1, len(song_list)):
        song1 = temp_output
        song2 = song_list[i]
        bpm1 = calculate_bpm(song1)
        bpm2 = calculate_bpm(song2)
        # BPM check!
        if abs(bpm1 - bpm2) <= bpm_tolerance:
            print(f"✔️ BPM Match ✔️ - Combining {song1} and {song2} with nofade curve")
            output_temp_file = os.path.join(output_directory, f'temp_{i}.mp3')
            crossfade_duration = temp_optimizer(bpm2)
            crossfade_audio(temp_output, song2, output_temp_file, crossfade_duration)
            temp_output = output_temp_file
        else:
            bpm_temp.append(song2)
            print(f"✖️ Skipped Combining ✖️ - {song1} and {song2} don't match!")

    if not os.listdir(output_directory).__contains__(output_file):
        os.rename(temp_output, output_file)
    else:
        os.remove(output_file)
        os.rename(temp_output, output_file)

    if bpm_temp.__len__() > 0:
        temp_output = output_file
        for i in range(0, len(bpm_temp)):
            song2 = song_list[i]
            crossfade_duration = temp_optimizer(calculate_bpm(song2))
            output_temp_file = os.path.join(output_directory, f'temp_{i}.mp3')
            crossfade_audio(temp_output, song2, output_temp_file, crossfade_duration)
            temp_output = output_temp_file

    print("🗑️ - Deleting all temp files...")
    for i in os.listdir(output_directory):
        if i.__contains__('temp_'):
            os.remove(f'{output_directory}\\{i}')
    print(f"✅ - Mix Created Successfully - ✅\n📂 - Output File: {output_file}")

genre = input("Please Enter Your Genre: ")
process_directory(ig.input_dir, ig.output_dir, bpm_tolerance=9, genre_chosen=genre)

