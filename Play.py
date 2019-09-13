import time

import vlc

sound_file = vlc.MediaPlayer("/home/hindu/AudioPreprocessing/Kanne-Kalaimane.wav")
sound_file.play()
time.sleep(25)
print("Song played successfully!")
