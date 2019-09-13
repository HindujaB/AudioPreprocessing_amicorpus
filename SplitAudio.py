import os

import numpy as np
from pydub import AudioSegment

split_points = [23, 69, 155, 180, 253]
vectors = []
words = []
filenames = []

audio_file = '/home/hindu/AudioPreprocessing/Kanne-Kalaimane.wav'
analysis_folder = '/home/hindu/AudioPreprocessing/SplitFiles'
samples_folder = os.path.join('/home/hindu/AudioPreprocessing/SplitFiles', 'samples')
try:
    os.makedirs(samples_folder)
except:
    pass

audio = AudioSegment.from_wav(audio_file)
start = 0
for i, t in enumerate(split_points):
    if i == len(split_points):
        break

    end = t * 1000
    print("split at [ {}:{}] ms".format(start, end))
    filename = 'SplitFiles/samples/' + str(i) + '.wav'
    audio_chunk = audio[start:end]
    audio_chunk.export(filename.format(end), format="wav")
    filenames.append(filename)

    start = end
np.savetxt(os.path.join(analysis_folder, 'filenames.txt'), filenames, fmt='%s')
