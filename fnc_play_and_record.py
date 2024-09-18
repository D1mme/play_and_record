import sounddevice as sd
import numpy as np


def fnc_play_and_record(device=None, Fs=48000, audio_playback=None, channel_playback=None, channel_receive=None):
    """
    Function to playback and record audio, with the ability to insert a voice command.

    Args:
        device (str, optional): Name of the audio device to use. Defaults to None.
        Fs (int, optional): Sampling frequency. Defaults to 48000.
        audio_playback (numpy.ndarray, optional): Input audio data for playback. Defaults to None.
        channel_playback (list, optional): Input channels to record from. Defaults to None.
        channel_receive (list, optional): Output channels to play back to. Defaults to None.
    Returns:
        tuple: Recorded audio data and the final index.
    """

    if device is None and audio_playback is None:
        flag_info_only = True
    else:
        flag_info_only = False

    if device is not None and audio_playback is None:
        flag_dev_info = True
    else:
        flag_dev_info = False

    # Display information about audio devices on system
    if flag_info_only:
        print("The following devices were recognized:")
        info_dev = sd.query_devices()
        for i, dev in enumerate(info_dev):
            print(f"     {i}: {dev['name']}")
        print("Your device is probably the one with the longest name :)")
        print(" ")
        return

    # Either give device-specific info or playback and record audio
    if not flag_info_only:
        info_dev = sd.query_devices()
        print(f"The specified device is: {device}. Testing to see if it exists...")

        # Select user-specified device as playback device
        success_flag = False
        for dev_id, dev in enumerate(info_dev):
            if device in dev['name']:
                success_flag = True
                break

        if success_flag:
            print(f"The selected device is: {info_dev[dev_id]['name']}")
            if flag_dev_info:
                print("Some information on the selected device:")
                print(sd.query_devices(dev_id))
        else:
            print("The specified device was not found for the given sample frequency. ")
            print("The following devices were recognized:")
            info_dev = sd.query_devices()
            for i, dev in enumerate(info_dev):
                print(f"     {i}: {dev['name']}")
            return None

        # Adjust output channels to the device's max output channels if needed
        max_output_channels = info_dev[dev_id]['max_output_channels']
        if len(channel_receive) > max_output_channels:
            print(f"The device supports a maximum of {max_output_channels} output channels. Adjusting.")
            channel_receive = list(range(1, max_output_channels + 1))

        if len(channel_playback) > info_dev[dev_id]['max_input_channels']:
            print(
                f"The device supports a maximum of {info_dev[dev_id]['max_input_channels']} input channels. Adjusting.")
            channel_playback = list(range(1, info_dev[dev_id]['max_input_channels'] + 1))

        # Playback audio received successfully
        if not flag_dev_info and success_flag:
            print(f"Note: your audio duration is {len(audio_playback) / Fs} seconds")

            if audio_playback.shape[1] < len(channel_receive):
                print("This device has more playback channels than your audio. Adding zeros.")
                audio_playback = np.hstack([audio_playback, np.zeros((audio_playback.shape[0], len(channel_receive) - audio_playback.shape[1]))])

            # Determine the maximum value between the two channel arrays
            max_in = np.max(channel_playback)
            max_out = np.max(channel_receive)
            max_channel = max(max_in, max_out)

            # Create an array of channel indices
            channel_mix = np.arange(0, max_channel)

            # Placeholder for recorded audio
            audio_out = np. zeros((audio_playback.shape[0], len(channel_mix)), dtype=np.float32)

            # Playback and record audio
            buf_size = 512
            i = 0
            try:
                with sd.Stream(device=dev_id, samplerate=Fs, channels=len(channel_mix), dtype='float32') as stream:
                    # Loop indefinitely until the program is terminated
                    while i < len(audio_playback):
                        end_index = min(i + buf_size, len(audio_playback))
                        buf = audio_playback[i:end_index].copy()

                        stream.write(buf)
                        indata = stream.read(end_index - i)[0]
                        audio_out[i:end_index] = indata

                        i += buf_size

            except Exception as e:
                print(f"An error occurred: {e}")
                return None

            return audio_out

