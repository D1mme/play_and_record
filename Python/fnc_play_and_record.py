import sounddevice as sd
import numpy as np


def fnc_play_and_record(device=None, Fs=48000, audio_playback=None, channel_playback=None, channel_receive=None):
    """
    Function to playback and record audio, with the ability to insert a voice command.

    Args:
        device (str, optional): Name of the audio device to use. Defaults to None.
        Fs (int, optional): Sampling frequency. Defaults to 48000.
        audio_playback (numpy.ndarray, optional): Input audio data for playback. Defaults to None.
        channel_receive (list, optional): Input channels to record from. Defaults to None.
        channel_playback (list, optional): Output channels to play back to. Defaults to None.
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

    if audio_playback is not None:
        assert audio_playback.shape[1] == len(channel_playback), ("Row dimension of the playback signal should match "
                                                                  "the number of playback channels")

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
                print(" ")
        else:
            print("The specified device was not found for the given sample frequency. ")
            print("The following devices were recognized:")
            info_dev = sd.query_devices()
            for i, dev in enumerate(info_dev):
                print(f"     {i}: {dev['name']}")
            print(" ")
            return None

        # Adjust output channels to the device's max output channels if needed
        if not flag_dev_info and success_flag:
            terminate_flag = False
            max_output_channels = info_dev[dev_id]['max_output_channels']
            if max(channel_playback) > max_output_channels:
                print(f"The device supports up to {max_output_channels} playback channels. A larger one was specified. Terminating.")
                terminate_flag = True

            if max(channel_receive) > info_dev[dev_id]['max_input_channels']:
                print(
                    f"The device supports up to of {info_dev[dev_id]['max_input_channels']} receiver channels. A larger one was specified. Terminating.")
                terminate_flag = True

            if not terminate_flag:
                # Determine the maximum value between the two channel arrays
                max_in = np.max(channel_receive)
                max_out = np.max(channel_playback)
                max_channel = max(max_in, max_out)   # Note that max_channel is also the number of channels

                # Create an array of channel indices based on the max
                channel_mix = np.arange(0, max_channel)

                # Placeholder for recorded audio
                audio_out = np.zeros((audio_playback.shape[0], len(channel_receive)), dtype=np.float32)

                # Playback and record audio
                print(f"Note: your audio duration is {len(audio_playback) / Fs} seconds")
                buf_size = 512
                buf_default = np.zeros((buf_size, len(channel_mix)), dtype='float32')  # The default playback audio is all zeros.
                i = 0
                try:
                    # Note that sd.Stream does not take channels, but instead takes a number of channels (!!!!)
                    # Hence, in the code above, we need to make the number of channels and the playback audio match the
                    # target channels as specified by the user
                    with sd.Stream(device=dev_id, samplerate=Fs, channels=max_channel, dtype='float32') as stream:
                        # Loop indefinitely until the program is terminated
                        while i + buf_size < len(audio_playback):
                            end_index = i + buf_size

                            # Set the buffer: all-zeros apart from the channels containing the playback signals.
                            buf = buf_default
                            buf[:, channel_playback-1] = audio_playback[i:end_index, :]  # The offset by 1 is due to counting from zero

                            stream.write(buf)
                            indata = stream.read(end_index - i)[0]
                            audio_out[i:end_index] = indata[:, channel_receive-1]  # The offset by 1 is due to counting from zero

                            i += buf_size

                except Exception as e:
                    print(f"An error occurred: {e}")
                    return None

                return audio_out
            else:
                return None

