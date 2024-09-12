%Author:        Dimme de Groot
%Date:          November 2023
%Last update:   September 2024
%Descr:         This script shows how to use the fnc_play_and_record function
%               Note that you might need to change certain settings (e.g. device) based on your system. But first try to run it :)

clear all
close all

%%%%%%%%%%%%%%%%%
% Choose device %
%%%%%%%%%%%%%%%%%

% Step 1: give user some info
fnc_play_and_record()                 %Give user some info

% Step 2: User specifies desired device from the list. 
device = "HDA";                     %Audio device. Run fnc_play_and_record without arguments to get a list of devices. See below.
Fs = 48000;                         %Sampling frequency in Hz
fnc_play_and_record(device, Fs);    %Test if device exists

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% User selects playback and recording channels %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
playback_chan = 1:2;    %Playback channels; note: the maximum number and valid ranges are device dependent 
record_chan = 1:2;      %Recorder channels; note: the maximum number and valid ranges are device dependent

%%%%%%%%%%%%%%%%%%%%%%%%%
% Define playback audio %
%%%%%%%%%%%%%%%%%%%%%%%%%
train = load("train"); %this loads the audio y and corresponding sample rate Fs. I just used a single channel audiofile. The code will add all-zero channels automatically. 
audioPlay = resample(train.y, Fs, train.Fs);  %resample to desired frequency

%%%%%%%%%%%%%%%%%%%
% Play and record %
%%%%%%%%%%%%%%%%%%%
audioRec = fnc_play_and_record(device, Fs, audioPlay, playback_chan, record_chan);

