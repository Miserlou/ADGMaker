![ADGMaker!](http://i.imgur.com/2v7Hd3Q.png)
# ADGMaker

Automatically create and install hundreds of awesome Free (as in Freedom!) Ableton Live Instuments from the super high-quality [Philharmonia Orchestra](http://www.philharmonia.co.uk/explore/make_music/) samples.

## Installation

ADGMaker requires that you have Python, OSX, and Ableton Live installed already. Then, simply:

    $ pip install adgmaker

## Automatic Usage

The simplest way to use ADGMaker is with the '--all' and '--install' arguments, which will fetch the instrument archives from the internet, create ADGs, and install them into your Ableton installation automatically:

    $ adgmaker --all --install

Then go to File -> Manage Files -> Manage User Library and use your new instruments! You'll see them under the "Drums" tab. Tada!

## Manual Usage

Download an instrument from [the Philharmonia Orchestra website](http://www.philharmonia.co.uk/explore/make_music/double_bass) and unzip it.

Then, (from a virtualenv), run:

    python adgmaker.py double_bass/

Then copy all of the .adg files to:

     ~/Music/Ableton/User\ Library/Presets/Instruments/Drum\ Rack/ 

(or wherever your Ableton is installed).

Then copy all of the mp3s to:

    ~/Music/Ableton/User\ Library/Samples/Imported

Then go to File -> Manage Files -> Manage User Library and use your new instruments!

## Caveats

Some of the ADGs only have a few items in them, but most instruments have at least a few ADG files that have a couple of complete scales. All of the percussion instruments have been combined into a single percussion ADG.

Some of the samples have a slight delay, so you might have to manually set the sample start time to your liking. I also like to add a little bit of fade out, reverb, and put them all into the same choke group, depending on the sound I want.

## TODO

* Support other sound archives?
* Support making multi-instrument racks?
* Tests / CI!

Enjoy!
