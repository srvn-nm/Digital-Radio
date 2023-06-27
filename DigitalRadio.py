import numpy as np
import scipy.signal as signal
import sounddevice as sd

SAMPLING_RATE = 480000
DURATION = 10


# reading inputs from the file
def read_input_file(file_path):
    with open(file_path, 'r') as file:
        signal_data = [float(line.strip()) for line in file]
    return signal_data


# filtering the signal with the given frequency
def apply_bandpass_filter(signal_data, cutoff_freq):
    normalized_cutoff_freq = cutoff_freq / (SAMPLING_RATE / 2)
    b, a = signal.butter(4, normalized_cutoff_freq, btype='lowpass')
    filtered_signal = signal.lfilter(b, a, signal_data)
    return filtered_signal
