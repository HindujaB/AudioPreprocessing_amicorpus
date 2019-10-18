import json
import os
import xml.dom.minidom

import numpy as np
from pydub import AudioSegment

# get file paths from configuration file
with open('config.json') as config_file:
    data = json.load(config_file)
filenames = []
vocal_sound_ids = []

audio_folder = data['Data']['directories']['Audio']['path']
meeting_file = data['Data']['directories']['Meetings']['path']
segments_folder = data['Data']['directories']['Segments']['path']
words_folder = data['Data']['directories']['Words']['path']
output_folder = data['OutputFolder']['path']


# set audio type string for finding suitable audio file
def get_audio_type(audio_type_string):
    switcher = {
        "LAPEL": "Lapel",
        "HEADSET": "Headset",
    }
    return switcher.get(audio_type_string.upper(), "lapel")


audio_type = get_audio_type(data['Data']['directories']['Audio']['type'])

meeting_xml = xml.dom.minidom.parse(data['Data']['directories']['Meetings']['path'])
meetings = meeting_xml.getElementsByTagName("meeting")


# identify backchannels from words.xml
def generate_vocal_sound_list(words_file):
    vocal_sounds = words_file.getElementsByTagName("vocalsound")
    for vocal_sound in vocal_sounds:
        vocal_sound_ids.append(vocal_sound.getAttribute("nite:id"))


# create audio chunks
def generate_audio(channel, start_time, end_time, audio_index):
    start_ms = float(start_time) * 1000
    end_ms = float(end_time) * 1000
    audio_dir = audio_files_per_meeting + "/" + observation + "." + audio_type + "-" + channel + ".wav"
    if not (os.path.exists(audio_dir)):
        return
    audio = AudioSegment.from_wav(audio_dir)
    meeting_directory = output_folder + '/' + observation
    vocal_directory = meeting_directory + "/" + observation + "-" + channel
    if not (os.path.exists(meeting_directory)):
        os.mkdir(meeting_directory)
    if not (os.path.exists(vocal_directory)):
        os.mkdir(vocal_directory)
    filename = vocal_directory + "/" + observation + "-" + channel + "-" + str(audio_index) + '.wav'
    audio_chunk = audio[start_ms:end_ms]
    audio_chunk.export(filename.format(end), format="wav")
    filenames.append(filename)


# check if a chunk is a backchannel
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


# create audio chunks for each meeting and each speaker
for meeting in meetings:
    vocal_sound_ids = []
    observation = meeting.getAttribute("observation")
    audio_files_per_meeting = audio_folder + "/" + observation + "/audio"
    speakers = meeting.getElementsByTagName("speaker")
    for speaker in speakers:
        nxt_agent = speaker.getAttribute("nxt_agent")
        channel, participant = speaker.getAttribute("channel"), speaker.getAttribute("global_name")
        if not (os.path.exists(words_folder + "/" + observation + "." + nxt_agent + ".words.xml") and os.path.exists(
                segments_folder + "/" + observation + "." + nxt_agent + ".segments.xml")):
            continue
        words_file = xml.dom.minidom.parse(words_folder + "/" + observation + "." + nxt_agent + ".words.xml")
        segments_file = xml.dom.minidom.parse(segments_folder + "/" + observation + "." + nxt_agent + ".segments.xml")
        generate_vocal_sound_list(words_file)
        segments = segments_file.getElementsByTagName("nite:child")
        words = words_file.getElementsByTagName("w")
        audioIndex = 0
        for segment in segments:
            wordIDs = segment.getAttribute("href").split('id(')
            if check_vocal_sound(wordIDs) is not True:
                if len(wordIDs) == 3:
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

# save the generated file paths to filepaths.txt
np.savetxt(os.path.join(output_folder, 'filepaths.txt'), filenames, fmt='%s')
