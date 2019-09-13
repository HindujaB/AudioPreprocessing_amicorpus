import librosa
import librosa.display
import matplotlib.pyplot as plt

data, sampling_rate = librosa.load('/home/hindu/AudioPreprocessing/Kanne-Kalaimane.wav')
plt.figure(figsize=(12, 4))
librosa.display.waveplot(data, sr=sampling_rate)

plt.savefig('plots/wavePlot.png')
