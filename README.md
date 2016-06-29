# ADGMaker

Create Ableton Live Instuments from the Creative Commons Philharmonic Orchestra samples.

## Usage

Download an instrument from [http://www.philharmonia.co.uk/explore/make_music/double_bass](the Philharmonic website) and unzip it.

Then, (from a virtualenv), run:

    python adgmaker.py double_bass/

Then copy all of the .adg files to:

     ~/Music/Ableton/User\ Library/Presets/Instruments/Drum\ Rack/ 

(or wherever your Ableton is installed).

Then copy all of the mp3s to:

    ~/rjones/Music/Ableton/User Library/Samples/Imported

Then go to File -> Manage Files -> Manage User Library and use your new instruments!

## Misc Notes from Dev..

The important bit is in
Ableton:GroupDevicePreset:BranchPresets:DrumBranchPreset
ZoneSetting:ReceivingNote:80 == C2
ZoneSetting:ReceivingNote:79 == C#2

.adg files are gzipped, so remember to gzip in and out of Ableton.

Samples: http://www.philharmonia.co.uk/explore/make_music/double_bass

Useful: http://xmlgrid.net/

The Data format appears just to be hex-enoded UTF-8 with a bunch of null bytes, but I'm not sure why it even needs to be there at all.

Do we need the PresetRef item?

Useful: https://github.com/supersat/ableton-playlist-exporter/blob/master/AbletonPlaylistExporter.py

MUST COPY FILES TO /SAMPLES