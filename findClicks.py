import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy as np


samplerate, data = wav.read(r'./degraded.wav')
data = data / 32768
position = []
for i in range(len(data)):
    if abs(data[i]) > 0.9 or abs(data[i]) == 0.5:
        position.append(i)
plt.plot(data)
position = np.array(position)
np.save('detectionfile.npy', position)