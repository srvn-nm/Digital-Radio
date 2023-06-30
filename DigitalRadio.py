import numpy as np
import scipy.signal as signal
import sounddevice as sd

SAMPLING_RATE = 48000
DURATION = 10


def read_input_file(file_path):
    """Reads the input signal from a file.

    Args:
        file_path (str): The path to the input file.

    Returns:
        list: The signal data read from the file.
    """
    with open(file_path, 'r') as file:
        signal_data = [float(line.strip()) for line in file]
    return signal_data


def apply_bandpass_filter(signal_data, cutoff_freq):
    """Applies a bandpass filter to the signal.

    A bandpass filter allows a certain range of frequencies to pass through while attenuating frequencies outside
    that range. In this function, a Butterworth lowpass filter is used to achieve the bandpass effect.

    Args:
        signal_data (list): The input signal.
        cutoff_freq (float): The cutoff frequency of the filter.

    Returns:
        numpy.ndarray: The filtered signal.
    """
    normalized_cutoff_freq = cutoff_freq / (SAMPLING_RATE / 2)
    b, a = signal.butter(4, normalized_cutoff_freq, btype='lowpass')
    filtered_signal = signal.lfilter(b, a, signal_data)
    return filtered_signal


def change_frequency(signal_data, freq_shift):
    """Shifts the frequency of the signal.

    Frequency shifting involves modifying the input signal by adding or subtracting a constant frequency value. This
    function performs frequency shifting by multiplying the signal with a complex exponential waveform.

    Args:
        signal_data (numpy.ndarray): The input signal.
        freq_shift (float): The amount of frequency shift.

    Returns:
        numpy.ndarray: The shifted signal.
    """
    time = np.arange(len(signal_data)) / SAMPLING_RATE


    start_freq = 0
    end_freq = freq_shift * 1000
    shifted_signal = signal_data * signal.chirp(time, start_freq, time[-1],  end_freq)
    return signal_data * shifted_signal

    # complex_signal = signal_data * np.exp(1j * 2 * np.pi * freq_shift * time)
    # shifted_signal = np.real(complex_signal)
    # return shifted_signal


def play_audio(audio_data):
    """Plays the audio.

    Args:
        audio_data (numpy.ndarray): The audio data to be played.
    """
    sd.play(audio_data, SAMPLING_RATE)
    sd.wait()


# Define the input file path
input_file_path = "input.txt"

# Read the input signal from the file
input_signal = read_input_file(input_file_path)

# Main program loop
while True:
    frequency = int(input("Enter the desired radio frequency (KHz): "))

    # Apply bandpass filter to the input signal
    filtered_signal = apply_bandpass_filter(input_signal, frequency)

    # Change the frequency of the filtered signal
    shifted_signal = change_frequency(filtered_signal, frequency)

    # Play the audio
    play_audio(shifted_signal)

    choice = input("Enter 'q' to quit or any other key to continue: ")
    if choice.lower() == "q":
        break
