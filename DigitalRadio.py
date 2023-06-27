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
def app

