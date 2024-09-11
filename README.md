# Record and play audio from audiocard
This is a MATLAB function I personally find convenient to use when I need to playback and/or record audio from an external audiocard.
It probably makes sense to add two more functions: one for recording only and one for playback only, but I usually take the lazy way and just playback audio with all-zeros or discard the recorded data. 
 
The code is used on Ubuntu 23.10 and Ubuntu 24.04. I tested it on an RME Fireface UFXIII and an internal audio card. 

The code is based on the [audioPlayerRecorder](https://nl.mathworks.com/help/audio/ref/audioplayerrecorder-system-object.html). 
