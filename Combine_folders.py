import json
import os
import re
import shutil

import numpy as np

with open('config.json') as config_file:
    data = json.load(config_file)

output_folder = data['CombinedOutputFolder']['path']
filenames = []
filepath_folder = data['OutputFolder']['path']
filepaths = filepath_folder + "/filepaths.txt"

text_file = open(filepaths, "r")
audio_files = text_file.readlines()
# print(audio_files)
# print(len(audio_files))
text_file.close()

# copy individual files into combined folders
for audio_line in audio_files:
    speaker = audio_line.split("/")[-2]
    audio_line = re.sub('\n', '', audio_line)
    speaker_directory = output_folder + "/" + speaker
    audio_file = audio_line.split("/")[-1]
    print(audio_file)
    if not (os.path.exists(speaker_directory)):
        os.mkdir(speaker_directory)
    shutil.copy(audio_line, speaker_directory + "/" + audio_file)
    filenames.append(audio_file)

# save the generated file paths to filenames.txt
np.savetxt(os.path.join(output_folder, 'filenames.txt'), filenames, fmt='%s')
