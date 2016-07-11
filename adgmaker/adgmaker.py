# ADGMaker

import argparse
import fnmatch
import glob
import gzip
import pkg_resources
import platform
import requests
import shutil
import os
import zipfile
from jinja2 import Environment, FileSystemLoader

####################################################################
# Data
####################################################################

all_zip_urls = [
    "http://www.philharmonia.co.uk/assets/audio/samples/banjo/banjo.zip",
    "http://www.philharmonia.co.uk/assets/audio/samples/bass%20clarinet/bass%20clarinet.zip",
    "http://www.philharmonia.co.uk/assets/audio/samples/bassoon/bassoon.zip",
    "http://www.philharmonia.co.uk/assets/audio/samples/cello/cello.zip",
    "http://www.philharmonia.co.uk/assets/audio/samples/clarinet/clarinet.zip",
    "http://www.philharmonia.co.uk/assets/audio/samples/contrabassoon/contrabassoon.zip",
    "http://www.philharmonia.co.uk/assets/audio/samples/cor%20anglais/cor%20anglais.zip",
    "http://www.philharmonia.co.uk/assets/audio/samples/double%20bass/double%20bass.zip",
    "http://www.philharmonia.co.uk/assets/audio/samples/flute/flute.zip",
    "http://www.philharmonia.co.uk/assets/audio/samples/french%20horn/french%20horn.zip",
    "http://www.philharmonia.co.uk/assets/audio/samples/guitar/guitar.zip",
    "http://www.philharmonia.co.uk/assets/audio/samples/mandolin/mandolin.zip",
    "http://www.philharmonia.co.uk/assets/audio/samples/oboe/oboe.zip",
    "http://www.philharmonia.co.uk/assets/audio/samples/saxophone/saxophone.zip",
    "http://www.philharmonia.co.uk/assets/audio/samples/trombone/trombone.zip",
    "http://www.philharmonia.co.uk/assets/audio/samples/trumpet/trumpet.zip",
    "http://www.philharmonia.co.uk/assets/audio/samples/tuba/tuba.zip",
    "http://www.philharmonia.co.uk/assets/audio/samples/viola/viola.zip",
    "http://www.philharmonia.co.uk/assets/audio/samples/violin/violin.zip",
    "http://www.philharmonia.co.uk/assets/audio/samples/percussion/percussion.zip"
]

home_dir = os.path.expanduser("~")
samples_dir = os.path.join(home_dir, 'Music', 'Ableton', 'User Library', 'Samples', 'Imported')
adg_dir = os.path.join(home_dir, 'Music', 'Ableton', 'User Library', 'Presets', 'Instruments', 'Created')

####################################################################
# Main
####################################################################

class ADGMaker(object):
    """
    Read CLI input, create ADGs.

    """

    jenv = Environment(loader=FileSystemLoader(os.path.dirname(os.path.realpath(__file__))),
                         trim_blocks=True)

    # Ex: {'cello_05_forte_arco-normal': [ xml, xml, .. ]
    adgs = {}
    vargs = None
    default_note = 104

    def handle(self, argv=None):
        """
        Main function.

        Parses command, load settings and dispatches accordingly.

        """
        help_message = "Please supply a path to a folder of MP3s or --all. See --help for more options."
        parser = argparse.ArgumentParser(description='ADGMaker - Create and install Ableton Live Instruments.\n')
        parser.add_argument('samples_path', metavar='U', type=str, nargs='*', help=help_message)
        parser.add_argument('-d', '--debug', action='store_true', help='Debug (no delete XML)', default=False)
        parser.add_argument('-i', '--install', action='store_true', help='Install into Ableton directory', default=False)
        parser.add_argument('-a', '--all', action='store_true', help='Fetch all available instruments from philharmonia website', default=False)
        parser.add_argument('-v', '--version', action='store_true', default=False,
            help='Display the current version of ADGMaker')

        args = parser.parse_args(argv)
        self.vargs = vars(args)

        if self.vargs['version']:
            version = pkg_resources.require("adgmaker")[0].version
            print(version)
            return

        # Samples are an important requirement.
        if not self.vargs['samples_path'] and not self.vargs['all']:
            print(help_message)
            return

        # Make sure we have the necessary dirs to install into.
        if self.vargs['install']:
            if not os.path.exists(samples_dir):
                os.makedirs(samples_dir)

            if not os.path.exists(adg_dir):
                os.makedirs(adg_dir)

        if self.vargs['samples_path']:
            self.create_adg_from_samples_path(self.vargs['samples_path'][0])

        if self.vargs['all']:
            for zip_url in all_zip_urls:

                # Download the zip
                zip_file_name = zip_url.rsplit('/',1)[1]
                print("\nDownloading " + zip_file_name + "..\n")

                with open(zip_file_name, 'wb') as handle:
                    response = requests.get(zip_url, stream=True)
                    for block in response.iter_content(1024):
                        handle.write(block)

                # Unzip to a directory
                dir_name = zip_file_name.split('.zip')[0]
                zip_ref = zipfile.ZipFile(zip_file_name, 'r')
                zip_ref.extractall(dir_name)
                zip_ref.close()

                # Delete zip
                os.remove(zip_file_name) 

                # Create ADG from samples
                self.create_adg_from_samples_path(dir_name)

                self.adgs = {}

        print("Done! Remember to update your User Library in Live to see these new instruments!")

    def create_adg_from_samples_path(self, samples_path):
        """
        Create an ADG from the samples path.

        """

        # Normalize the input
        if samples_path[-1] != os.sep:
            samples_path = samples_path + os.sep
        
        # Percussion is a folder of folders
        given_name = None
        if 'percussion' in samples_path:
            mp3_list = []
            for root, dirnames, filenames in os.walk(samples_path):
                for filename in fnmatch.filter(filenames, '*.mp3'):
                    mp3_list.append(os.path.join(root, filename))
            given_name = 'percussion'

        else:
            samples_path = samples_path + '*.mp3'
            mp3_list = glob.glob(samples_path)

        for mp3 in mp3_list:
            file_path = os.path.abspath(mp3)
            self.add_mp3_to_instrument(file_path, given_name)

        for adg_name in self.adgs.keys():
            final_xml = self.create_base_xml(adg_name)
            adg_file = self.create_adg(adg_name, final_xml)

            if self.vargs['install']:
                print("Installing " + adg_file + "..")
                dest_path = os.path.join(adg_dir, adg_file)
                shutil.move(adg_file, dest_path)

        return adg_file

    def add_mp3_to_instrument(self, file_path, given_name=None):
        """
        Given a complete file path, add to the XML for this instrument.

        Samples are in the format:
            {{instrument_name}}_{{note}}_{{length}}_{{velocity}}_{{hit_type}}.mp3
        Ex:
            double-bass_Gs3_1_piano_arco-normal.mp3

        """
        instrument_xml = self.create_instrument_xml(file_path)
        file_name_no_mp3 = file_path.split('.mp3')[0].split(os.sep)[-1]
        instrument_name, note, length, velocity, hit_type = file_name_no_mp3.split('_')

        if given_name:
            adg_name = given_name
        else:
            adg_name = instrument_name + '_' + length + "_" + velocity + '_' + hit_type

        if self.adgs.has_key(adg_name):
            adg_contents = self.adgs[adg_name]
        else:
            adg_contents = []

        adg_contents.append(instrument_xml)
        self.adgs[adg_name] = adg_contents

        # Install the MP3?
        if self.vargs['install']:
            dest_path = os.path.join(samples_dir, file_name_no_mp3 + '.mp3')
            shutil.move(file_path, dest_path)

        return
        
    def create_base_xml(self, adg_name):
        """
        Create the standard cruft XML for the ADG.
        """

        items = self.adgs[adg_name]
        xml = self.jenv.get_template('base_xml.tpl').render(
                items=items,
            )

        return xml

    def create_instrument_xml(self, file_path):
        """
        name: cello_C2_05_forte_arco-normal
        mp3_name: cello_C2_05_forte_arco-normal.mp3
        note_value: 80
        ableton_path: userfolder:/Users/rjones/Downloads/cello/#cello_C2_05_forte_arco-normal.mp3
        """

        file_name_no_mp3 = file_path.split('.mp3')[0].split(os.sep)[-1]
        instrument_name, note, length, velocity, hit_type = file_name_no_mp3.split('_')

        name = file_name_no_mp3
        mp3_name = name + '.mp3'
        note_value = self.string_to_midi_note(note)
        ableton_path = "userfolder:" + file_path.rsplit(os.sep, 1)[0] + os.sep + '#' + mp3_name

        data = file_path.encode('utf-16').encode('hex').upper()

        xml = self.jenv.get_template('instrument_xml.tpl').render(
                name=name,
                mp3_name=mp3_name,
                note_value=note_value,
                ableton_path=ableton_path,
                data=data
            )

        return xml

    def create_adg(self, adg_name, xml):
        """
        Create the final ADG file.
        """

        xml_name = adg_name + '.xml'
        adg_file = adg_name + '.adg'

        f = open(xml_name,'w')
        f.write(xml) 
        f.close()

        with open(xml_name) as f_in, gzip.open(adg_file, 'wb') as f_out:
            f_out.writelines(f_in)

        if not self.vargs.get('d', False):
            os.remove(xml_name) 

        print("Created " + adg_file + "!")

        return adg_file

    ##
    # Utility
    ##

    def string_to_midi_note(self, midstr):
        """ 
            In Ableton, C3 = 60 supposedly,

            but,

            ZoneSetting:ReceivingNote:80 == C2
            ZoneSetting:ReceivingNote:79 == C#2


        """

        # I am a bad person.
        notes_ref = {

            'C0': 104,           
            'Cs0': 103,
            'D0': 102,
            'Ds0': 101,
            'E0': 100,
            'F0': 99,
            'Fs0': 98,
            'G0': 97,
            'Gs0': 96,
            'A0': 95,
            'As0': 94,
            'B0': 93,

            'C1': 92,           
            'Cs1': 91,
            'D1': 90,
            'Ds1': 89,
            'E1': 88,
            'F1': 87,
            'Fs1': 86,
            'G1': 85,
            'Gs1': 84,
            'A1': 83,
            'As1': 82,
            'B1': 81,
            
            'C2': 80,           
            'Cs2': 79,
            'D2': 78,
            'Ds2': 77,
            'E2': 76,
            'F2': 75,
            'Fs2': 74,
            'G2': 73,
            'Gs2': 72,
            'A2': 71,
            'As2': 70,
            'B2': 69,

            'C3': 68,           
            'Cs3': 67,
            'D3': 66,
            'Ds3': 65,
            'E3': 64,
            'F3': 63,
            'Fs3': 62,
            'G3': 61,
            'Gs3': 60,
            'A3': 59,
            'As3': 58,
            'B3': 57,

            'C4': 56,           
            'Cs4': 55,
            'D4': 54,
            'Ds4': 53,
            'E4': 52,
            'F4': 51,
            'Fs4': 50,
            'G4': 49,
            'Gs4': 48,
            'A4': 47,
            'As4': 46,
            'B4': 45,

            'C5': 44,           
            'Cs5': 43,
            'D5': 42,
            'Ds5': 41,
            'E5': 40,
            'F5': 39,
            'Fs5': 38,
            'G5': 37,
            'Gs5': 36,
            'A5': 35,
            'As5': 34,
            'B5': 33,

            'C6': 32,           
            'Cs6': 31,
            'D6': 30,
            'Ds6': 29,
            'E6': 28,
            'F6': 27,
            'Fs6': 26,
            'G6': 25,
            'Gs6': 24,
            'A6': 23,
            'As6': 22,
            'B6': 21,

            'C7': 20,           
            'Cs7': 19,
            'D7': 18,
            'Ds7': 17,
            'E7': 16,
            'F7': 15,
            'Fs7': 14,
            'G7': 13,
            'Gs7': 12,
            'A7': 11,
            'As7': 10,
            'B7': 9,

            'C8': 8,           
            'Cs8': 7,
            'D8': 6,
            'Ds8': 5,
            'E8': 4,
            'F8': 3,
            'Fs8': 2,
            'G8': 1,
            'Gs8': 0,
            'A8': -1,
            'As8': -2,
            'B8': -3,

        }

        note = notes_ref.get(midstr, None)
        if note:
            return note
        else:
            note = self.default_note
            self.default_note = self.default_note - 1

            if self.default_note == 0:
                self.default_note = 104

            return note

def handle(): # pragma: no cover
    """
    Main program execution handler.
    """

    if platform.system() != "Darwin":
        print("ADGMaker currently only works for OSX. Sorry.")
        return

    try:
        adg_maker = ADGMaker()
        adg_maker.handle()
    except (KeyboardInterrupt, SystemExit): # pragma: no cover
        return
    except Exception as e:
        print(e)

if __name__ == '__main__': # pragma: no cover
    handle()
