import json
import os
import shutil

import soundfile as sf

"""
    This file identifies the audio files that are shorter than 2 seconds and remove those segments. 
    Then it renames the remaining files with the speaker name nd meeting ID.
"""

# get file paths from configuration file
with open('config.json') as config_file:
    data = json.load(config_file)
filenames = []
vocal_sound_ids = []

audio_folder = data['SpeakerOutputFolder']['path']
output_folder = data['FinalOutputFolder']['path']

speakers = os.listdir(audio_folder)


def get_duration(directory):
    f = sf.SoundFile(directory)
    audio_duration = len(f) / f.samplerate
    print('seconds = {}'.format(audio_duration))
    return audio_duration


for speaker in speakers:
    files = os.listdir(audio_folder + '/' + speaker)
    for audio_file in files:
        dir = audio_folder + '/' + speaker + '/' + audio_file
        duration = get_duration(dir)
        dest = output_folder + '/' + speaker
        if not (os.path.exists(dest)):
            os.mkdir(dest)
        print(dest)
        if duration > 2.0:
            shutil.copy(dir, dest)

speakers = os.listdir(output_folder)
for speaker in speakers:
    files = os.listdir(output_folder + '/' + speaker)
    file_ID = 0
    for audio_file in files:
        src_file = output_folder + '/' + speaker + '/' + audio_file
        file_name = speaker + '_' + audio_file.split('-')[0] + '_' + str(file_ID) + '.wav'
        dest_file = output_folder + '/' + speaker + '/' + file_name
        print('file name : ', file_name)
        os.rename(src_file, dest_file)
        file_ID += 1
