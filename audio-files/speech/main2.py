import os

def play_mp3(file_path):
    os.system(f'afplay "{file_path}"')

play_mp3('../audio-files/hayden_prompt-1.mp3')

