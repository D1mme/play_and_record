import numpy as np
from fnc_play_and_record import fnc_play_and_record
import matplotlib.pyplot as plt

# List all devices which are available. This is done by calling fnc_play_and_record without any inputs
fnc_play_and_record()

# In my case, I want to use the card: "USB Audio CODEC: - (hw(1,0)). It is sufficient to specify a part of this name
# uniquely identifying the device. I chose to simply use "USB"
device = "USB"

# List information related to the device by calling with device name only. This prints a lot. For me the maximum
# number of input and output channels are usually the most interesting.
fnc_play_and_record(device)

# Let's now try to get some audio going
Fs = 48000  # Sampling frequency in Hz. The allowed values are device-dependent. Typical: 8000, 8192, 16000, 44100, 48000
channelPlayback = np.arange(1, 3)  # The playback channels. Note that they start at 1(!)
channelReceive = np.arange(1, 3)  # The receiver channels. Note that they start at 1(!)
audioPlayback = np.random.randn(10 * Fs, 2)  # The playback audio (10 seconds, gaussian noise here). Columnwise orientation!
audioPlayback = audioPlayback/np.max(np.abs(audioPlayback)) # Normalise range to -1, 1. This is usually not # necessary, but it is handy to keep the volume predictable
audioPlayback = np.float32(audioPlayback)

audioRec = fnc_play_and_record(device, Fs, audioPlayback, channelPlayback, channelReceive)

# Plot received audio signal. If audioRec == None, something went wrong during recording.
if audioRec is not None:
    plt.plot(audioRec)
    plt.xlabel('Sample Index')
    plt.ylabel('Amplitude')
    plt.title('Received audio signal at microphone(s)')
    plt.show()
