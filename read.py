import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

# Configuration
duration = 3  # seconds
sample_rate = 192000  # 192 kHz
V_ref = 7.8  # reference voltage (+20dbu ~ 7.8V)
output_filename = "recorded_waveform.wav"  # Filename to save the audio


# Function to capture and plot audio data in Volts with time in microseconds
def record_and_plot_audio():
    print("Recording...")

    # capture raw audio data
    audio_data = sd.rec(
        int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="float64"
    )
    sd.wait()

    # scaling
    audio_data = audio_data.flatten()
    voltage_data = audio_data * V_ref
    time_axis_microseconds = np.linspace(
        0, duration * 1000, len(voltage_data)
    )  # Convert seconds to ms

    # normalize the audio data to the range [-1, 1] for saving to .wav
    normalized_data = np.int16(audio_data / np.max(np.abs(audio_data)) * 32767)

    # save as a .wav file
    write(output_filename, sample_rate, normalized_data)
    print(f"Audio saved as {output_filename}")

    # plot using matplotlib graph explorer tool.
    # it is really convenient, you can zoom in-out and so on
    plt.plot(time_axis_microseconds, voltage_data)
    plt.title(f"Audio Waveform in Volts ({sample_rate} Hz, {duration * 1000} ms)")
    plt.xlabel("Time [ms]")
    plt.ylabel("Voltage [V]")
    plt.grid(True)
    plt.show()


record_and_plot_audio()
