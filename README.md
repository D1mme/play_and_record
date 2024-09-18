# Record and play audio from audiocard
This is a MATLAB function I personally find convenient to use when I need to playback and/or record audio from an external audiocard.
It probably makes sense to add two more functions: one for recording only and one for playback only, but I usually take the lazy way and just playback audio with all-zeros or discard the recorded data. 
 
The code is tested on Ubuntu 23.10 and Ubuntu 24.04, though I also expect it to work on Windows and maybe Mac. 
I tested it on an RME Fireface UFX III, an internal audio card and a Behringer U-Phoria UMC22. 

The code is based on the [audioPlayerRecorder](https://nl.mathworks.com/help/audio/ref/audioplayerrecorder-system-object.html). 

## Python
I also added a Python implementation which is thanks to Baturalp. The implementation is based on [sounddevice](https://pypi.org/project/sounddevice/). I made some small modifications to his code to make it better generalisable (it was originally written for the Fireface UFX III and including keyboard inputs). I didnt test it well, since I did not have an external loudspeaker available. I think it should work though! The original code at least worked :) 
