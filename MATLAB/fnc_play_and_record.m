%Date:      November 2023
%Last edit: September 2024
%Author:    Dimme
%Descr:     This function can be used to simultaneously read and write, audio to/from a given soundcard. For example an RME Fireface.
%           the function does not do checks on the input etc, but does say if your soundcard is not found.
%
%Based on:  https://nl.mathworks.com/help/audio/ref/audioplayerrecorder-system-object.html
%
%Inputs:    device          a string describing the device. I.e. if your device is "USB CARD: RME FIREFACE", device="USB" (or any other part uniquely describing the device name). 
%           Fs              the desired sampling frequency in Hz. Note that the valid inputs depend on the device
%           audioPlayback   a LENGHT x N_Playback_channel matrix of audio. This is the audio that will be played back. It might be required to ensure the largest absolute value is 1, though I'm not entirely sure.
%           channelPlayback The channels on which the loudspeakers are connected.
%           channelReceive  The channels on which the microphones are connected.
%
%Outputs:   audioOut        A LENGTH x N_receiver_channel containing the microphone signals
%
%Notes:     - If you dont want to playback anything, just set it all zero and select an arbitrary but valid set of playback channels
%           - If you dont want to record anything, dont assing the output argument. For the receiver channels, select an arbitrary but valid set. 
%           - In my experience, not all channel assignments are allowed. For example, I once required channel 15:22 but this threw an error. Using 15:24 worked for some reason. 
%           - you can use fnc_play_and_record(). This will list the available devices.
%           - You can use fnc_play_and_record(device) or fnc_play_and_record(device, Fs). This will give you device info. 
%           - If your audioPlayback matrix does not match the channelPlayback parameter, theplayback matrix will either be truncated or zeros will be appended!
%           - In my experience, you sometimes need to restart MATLAB for the device list to update. 

function varargout = fnc_play_and_record(device, Fs, audioPlayback, channelPlayback, channelReceive)
    if nargin == 0
        flag_info_only = true;
    else
        flag_info_only = false;
    end
    if nargin == 1 
        flag_dev_info = true;
        Fs = 48000;
    elseif nargin==2
        flag_dev_info = true;
    else
        flag_dev_info = false;
    end
    if nargin == 3
        channelReceive =  [1,2];  %Recorder channels
        channelPlayback = [1,2];  %Playback channels
    end
    if nargin == 4
        channelReceive =  [1,2];  %Recorder channels
    end

    %Give user some information about audiodevices on system
    if flag_info_only 
        %Create audioPlayerRecorder object for the specified sampling frequency. I think this also accepts invalid sampling frequencies 
        playRec = audioPlayerRecorder;
        infoDev = getAudioDevices(playRec);
        disp("The following devices were recognised:")
        for i=1:length(infoDev)
            disp("     " + infoDev{i})
        end
        disp("Your device is probably the one with the longest name :)")
        disp(" ")
    end

    %Either give device specific onfo or playback and record audio
    if ~flag_info_only
        playRec = audioPlayerRecorder(Fs);
        infoDev = getAudioDevices(playRec);
        disp("The specified device is: " + device + ". testing to see if it exists...")
    
        %Select  user specified device as playback device
        for devId=1:length(infoDev)
            if isempty(strfind(infoDev{devId},device))~=1
                succes_flag = 1;
                break
            end
            succes_flag = 0;
        end
        if succes_flag==1
            disp("The selected device is: " + infoDev{devId}) 
            release(playRec)
            playRec.Device = infoDev{devId};  %update the playRec object to be the selected device
            if flag_dev_info                    %Give device specific info
                infoDevSum = info(playRec);
                disp("Some information on the selected device:")
                disp(infoDevSum);
            end
        else
            disp("The specified device was not found for the given sample frequency. Try running <fnc_play_and_record> without in- and output argumens")
        end

        %Playback audio
        if ~flag_dev_info && succes_flag == 1
            disp("Note: your audio duration is " + num2str(size(audioPlayback,1)/Fs) + " seconds");
            playRec.PlayerChannelMapping = channelPlayback;      
            playRec.RecorderChannelMapping = channelReceive;   

            %check if the specified audio has the right nuimber of channels. If not, add zeros or truncate and give warning
            if size(audioPlayback,2)>length(channelPlayback)
                disp("This device does not have sufficiently large number of playback channels for your audio. Truncating")
                audioPlayback = audioPlayback(:, 1:length(channelPlayback));
            elseif size(audioPlayback,2) < length(channelPlayback)
                disp("This device does have more playback channels than your audio input. Adding zeros")
                Nchan_audio = size(audioPlayback,2);
                Nchan = length(channelPlayback);
                audioPlayback = [audioPlayback, zeros(size(audioPlayback,1), Nchan-Nchan_audio)];
            end
            
            %Placeholder for recorded audio. 
            audioOut = zeros(size(audioPlayback,1), length(channelReceive));                

            %(4) Playback and record audio 
            buf = dsp.AsyncBuffer(size(audioPlayback,1));
            write(buf,audioPlayback);
            Indx = 0;
   
            % I read/write 512 samples. There probably are cases where it makes sense to change this (real-time processing?), though i'm not sure. 
            % Anyway, note that you can also add processing steps in this loop if they are quick enough. 
            nSample = 512;
            while buf.NumUnreadSamples >= nSample
                audioToPlay = read(buf,nSample);
                [audioRecorded,nUnderruns,nOverruns] = playRec(audioToPlay);

                audioOut(Indx+1:Indx+nSample, :) = audioRecorded;
                if nUnderruns > 0
                    fprintf('Audio player queue was underrun by %d samples.\n',nUnderruns);
                end
                if nOverruns > 0
                    fprintf('Audio recorder queue was overrun by %d samples.\n',nOverruns);
                end
                Indx = Indx+nSample;
            end
            release(buf)
            release(playRec)
        
        else
            audioOut = [];
        end
        varargout{1} = audioOut;
    end
end
