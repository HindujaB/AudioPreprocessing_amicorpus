import os
import xml.dom.minidom

import numpy as np
from pydub import AudioSegment

# TODO: create functions to navigate through directory
# TODO: Organize functions in files

meeting_xml = xml.dom.minidom.parse("manual/meetings.xml")
segmentsA_xml = xml.dom.minidom.parse("manual/ES2002a.A.segments.xml")
wordsA_xml = xml.dom.minidom.parse("manual/ES2002a.A.words.xml")

meeting_name = "ES2002a"
speaker_NXTAgent = 'A'
filenames = []
vocal_sound_ids = []

meetings = meeting_xml.getElementsByTagName("meeting")


def generate_vocal_sound_list():
    vocal_sounds = wordsA_xml.getElementsByTagName("vocalsound")
    for vocal_sound in vocal_sounds:
        vocal_sound_ids.append(vocal_sound.getAttribute("nite:id"))


generate_vocal_sound_list()


def get_channel_participants(speakers):
    for speaker in speakers:
        if speaker.getAttribute("nxt_agent") == speaker_NXTAgent:
            return speaker.getAttribute("channel"), speaker.getAttribute("global_name")


for meeting in meetings:
    observation = meeting.getAttribute("observation")
    if observation == meeting_name:
        speakers = meeting.getElementsByTagName("speaker")
        channel, participant = get_channel_participants(speakers)

audio_file = meeting_name + ".Lapel-" + channel + ".wav"

segments = segmentsA_xml.getElementsByTagName("nite:child")
words = wordsA_xml.getElementsByTagName("w")


def generate_audio(channel, start_time, end_time, audio_index):
    start_ms = float(start_time) * 1000
    end_ms = float(end_time) * 1000
    audio = AudioSegment.from_wav(audio_file)
    filename = 'SplitFiles/samples/' + meeting_name + "-" + channel + "-" + str(audio_index) + '.wav'
    audio_chunk = audio[start_ms:end_ms]
    audio_chunk.export(filename.format(end), format="wav")
    filenames.append(filename)


def check_vocal_sound(word_id_list):
    start_id = word_id_list[1].replace('..', '').replace(')', '')
    if len(word_id_list) == 3:
        end_id = word_id_list[2].replace(')', '')
        if start_id in vocal_sound_ids or end_id in vocal_sound_ids:
            return True
    elif start_id in vocal_sound_ids:
        return True
    else:
        return False


audioIndex = 0
for segment in segments:
    wordIDs = segment.getAttribute("href").split('id(')
    if check_vocal_sound(wordIDs) is not True:
        start = wordIDs[1].replace('..', '').replace(')', '')
        end = wordIDs[2].replace(')', '')
        audioIndex += 1
    else:
        continue
    for word in words:
        wordID = word.getAttribute("nite:id")
        if wordID == start:
            start_time = word.getAttribute("starttime")
        elif wordID == end:
            end_time = word.getAttribute("endtime")
            break

    generate_audio(channel, start_time, end_time, audioIndex)

np.savetxt(os.path.join('/home/hindu/AudioPreprocessing/SplitFiles', 'filenames.txt'), filenames, fmt='%s')


