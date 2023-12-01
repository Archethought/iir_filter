import matplotlib.pyplot as plt
import scipy.io.wavfile as wav

# Load the audio file
(rate, data) = wav.read('piano2.wav')

# Plot the audio signal
plt.plot(data)
plt.show()

