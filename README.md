AudioPreprocessing - AMI corpus
======================================

This program processes the **AMI corpus** dataset of meetings in order to create segmented audio files for each speaker by referencing the annotations of the data. 


## Prerequisites

* Download the corpus from <a target="_blank" href="http://groups.inf.ed.ac.uk/ami/download/">here</a>
* Download the public manual annotations <a target="_blank" href="http://groups.inf.ed.ac.uk/ami/AMICorpusAnnotations/ami_public_manual_1.6.2.zip/">here</a>
* Set the path parameters in the config files as follows,
    ```json
  "directories": {
      "Audio": {
        "type": "<DOWNLOADED_AUDIO_TYPE>",
        "path": "<AMI_CORPUS_PATH>"
      },
      "Segments": {
        "path": "<PATH_OF_SEGMENTS_FOLDER_IN_PUBLIC_MANUAL>"
      },
      "Words": {
        "path": "<PATH_OF_WORDS_FOLDER_IN_PUBLIC_MANUAL>"
      },
      "Meetings": {
        "path": "<PATH_OF_MEETINGS_XML_IN_PUBLIC_MANUAL>"
      },
      "Participants": {
        "path": "<PATH_OF_PARTICIPANTS_XML_IN_PUBLIC_MANUAL>"
      }
    }
  "OutputFolder": {
    "path": "<PATH_OF_THE_OUTPUT_FOLDER>"
  },
  "CombinedOutputFolder": {
    "path": "<PATH_OF_THE_COMBINED_FILES_FOLDER>"
  },
  "SpeakerOutputFolder": {
    "path": "<PATH_FOR_THE_SPEAKER_FOLDER>"
  }
   ```
  
## Preprocessing structure

![structure_diagram](images/preprocess_structure.png)

## How to use

* run `Segment_audio.py`
* To combine the audio files according to meeting participants, run `Analyse_speaker.py`
* To remove shorter audio segments and rename the files according to speaker, run `Reformat_Files.py`
* To  combine the segmented audio files of each meeting according to each speaker, run `Combine_folders.py`
