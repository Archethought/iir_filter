import numpy as np
import scipy.signal as signal
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt

# Load the audio file "piano2.wav"
fs, audio_data = wavfile.read("taunt.wav")

# ANSI 1/3 octave center frequencies in Hz
center_frequencies = [
    20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 
    200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 
    2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000
]

# Bandwidths for each band
# bandwidths = [f * 0.1 for f in center_frequencies]
bandwidths = [cf * (10 ** (1 / 20) - 1) for cf in center_frequencies]

# A-weighting filter coefficients (from ANSI S1.4-1983 standard)
A_weighting = [
    3.5041384e-2, -2.4928984e-2, 7.7573297e-3,
    -6.2351528e-4, -3.4972643e-5, -8.3279871e-4,
    1.2752674e-3, 2.7317999e-4, 1.9789250e-4
]

# List to store the filtered and A-weighted decibel readings for each band
weighted_decibel_readings = []

# Iterate through each band, apply the IIR filter, apply A-weighting, and calculate the decibel reading
for i in range(len(center_frequencies)):
    f0 = center_frequencies[i]
    Q = f0 / bandwidths[i]
    b, a = signal.iirpeak(f0, Q, fs=fs)
    
    filtered_audio = signal.lfilter(b, a, audio_data)
    
    # Apply A-weighting
    weighted_audio = signal.lfilter(A_weighting, 1, filtered_audio)
    
    # Calculate the decibel reading
    db_reading = 10 * np.log10(np.mean(weighted_audio**2))
    weighted_decibel_readings.append(db_reading)

# Plot the 1/3 octave A-weighted decibel readings
plt.semilogx(figsize=(12, 6))
plt.bar(center_frequencies, weighted_decibel_readings, width=0.8*np.diff(center_frequencies + [center_frequencies[-1]*1.3]), align='edge')
plt.xlabel('Center Frequency (Hz)')
plt.ylabel('A-weighted Decibel Reading (dB)')
plt.title('1/3 Octave A-weighted Decibel Readings (ANSI Frequencies)')
plt.grid(True)
plt.xticks(rotation=45)
plt.show()
