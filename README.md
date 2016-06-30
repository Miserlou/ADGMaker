# ADGMaker

Automatically create and install hundreds of awesome Free (as in Freedom!) Ableton Live Instuments from the super high-quality [Philharmonic Orchestra](http://www.philharmonia.co.uk/explore/make_music/) samples.

## Installation

ADGMaker requires that you have Python, OSX, and Ableton Live installed already. Then, simply:

    $ pip install adgmaker

## Automatic Usage

The simplest way to use ADGMaker is with the '--all' and '--install' arguments, which will fetch the instrument archives from the internet, create ADGs, and install them into your Ableton installation automatically:

    $ adgmaker --all --install

Then go to File -> Manage Files -> Manage User Library and use your new instruments! You'll see them under the "Drums" tab. Tada!

## Manual Usage

Download an instrument from [the Philharmonic Orchestra website](http://www.philharmonia.co.uk/explore/make_music/double_bass) and unzip it.

Then, (from a virtualenv), run:

    python adgmaker.py double_bass/

Then copy all of the .adg files to:

     ~/Music/Ableton/User\ Library/Presets/Instruments/Drum\ Rack/ 

(or wherever your Ableton is installed).

Then copy all of the mp3s to:

    ~/Music/Ableton/User\ Library/Samples/Imported

Then go to File -> Manage Files -> Manage User Library and use your new instruments!

## Caveats

Some of the samples have a slight delay, so you might have to manually set the sample start time to your liking. I also like to add a little bit of fade out, reverb, and put them all into the same choke group, depending on the sound I want.

## TODO

* Support other sound archives?
* Support making multi-instrument racks?
* Tests / CI!

Enjoy!
