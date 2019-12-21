import json
import os
import shutil
import xml.dom.minidom

# get file paths from configuration file
with open('config.json') as config_file:
    data = json.load(config_file)
filenames = []
vocal_sound_ids = []

audio_folder = data['CombinedOutputFolder']['path']
meeting_file = data['Data']['directories']['Meetings']['path']
participants_file = data['Data']['directories']['Participants']['path']
output_folder = data['SpeakerOutputFolder']['path']

meeting_xml = xml.dom.minidom.parse(meeting_file)
participants_xml = xml.dom.minidom.parse(participants_file)

participants = participants_xml.getElementsByTagName("participant")
meetings = meeting_xml.getElementsByTagName("meeting")


def save_file(speaker_name, target_file):
    src_dir = audio_folder + '/' + target_file
    dest_dir = output_folder + '/' + speaker_name

    if (os.path.exists(src_dir)):
        if not (os.path.exists(dest_dir)):
            os.mkdir(dest_dir)
        src_files = os.listdir(src_dir)
        print('source folder :', src_dir)
        print('destination :', dest_dir)
        for file in src_files:
            src_file = src_dir + '/' + file
            shutil.copy(src_file, dest_dir)
        print("The audio files of meeting {} is copied according to speaker {}".format(meeting_name, speaker_name))


for meeting in meetings:
    speakers = meeting.getElementsByTagName("speaker")
    meeting_name = meeting.getAttribute("observation")
    for speaker in speakers:
        speaker_name = speaker.getAttribute("global_name")
        speaker_channel = speaker.getAttribute("channel")
        target_file = meeting_name + '-' + speaker_channel
        save_file(speaker_name, target_file)
