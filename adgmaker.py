# ADGMaker

import argparse
import glob
import gzip
import os
from jinja2 import Environment, FileSystemLoader

####################################################################
# Main
####################################################################

class ADGMaker(object):
    """
    Read CLI input, create ADGs.

    """
    jenv = Environment(loader=FileSystemLoader(os.getcwd()),
                         trim_blocks=True)

    # Ex: {'cello_05_forte_arco-normal': [ xml, xml, .. ]
    adgs = {}
    vargs = None

    def handle(self, argv=None):
        """
        Main function.

        Parses command, load settings and dispatches accordingly.

        """
        help_message = "Please supply a path to a folder of MP3s."
        parser = argparse.ArgumentParser(description='ADGMaker - Create Ableton Live Instruments.\n')
        parser.add_argument('samples_path', metavar='U', type=str, nargs='*', help=help_message)
        parser.add_argument('-d', action='store_true', help='Debug (no delete XML)', default=False)

        args = parser.parse_args(argv)
        self.vargs = vars(args)

        # Samples are an important requirement.
        if not self.vargs['samples_path']:
            print(help_message)
            return

        # Normalize the input
        samples_path = self.vargs['samples_path'][0]
        if samples_path[-1] != os.sep:
            samples_path = samples_path + os.sep
        samples_path = samples_path + '*.mp3'

        mp3_list = glob.glob(samples_path)
        for mp3 in mp3_list:
            file_path = os.path.abspath(mp3)
            self.add_mp3_to_instrument(file_path)

        for adg_name in self.adgs.keys():
            final_xml = self.create_base_xml(adg_name)
            self.create_adg(adg_name, final_xml)

        print("Done!")

    def add_mp3_to_instrument(self, file_path):
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
        adg_name = instrument_name + '_' + length + "_" + velocity + '_' + hit_type

        if self.adgs.has_key(adg_name):
            adg_contents = self.adgs[adg_name]
        else:
            adg_contents = []

        adg_contents.append(instrument_xml)
        self.adgs[adg_name] = adg_contents

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

        return

    ##
    # Utility
    ##

    def string_to_midi_note(self, midstr):
        """ 
            Stolen from: http://stackoverflow.com/questions/13926280/musical-note-string-c-4-f-3-etc-to-midi-note-value-in-python 
        """
        notes = [["C"],["Cs"],["D"],["Ds"],["E"],["F"],["Fs"],["G"],["Gs"],["A"],["As"],["B"]]
        answer = 0
        i = 0
        letter = midstr[:-1]
        for note in notes:
            if letter.upper() == note[0]:
                answer = i
                break
            i += 1
        answer += (int(midstr[-1]))*12
        return answer

def handle(): # pragma: no cover
    """
    Main program execution handler.
    """

    try:
        adg_maker = ADGMaker()
        adg_maker.handle()
    except (KeyboardInterrupt, SystemExit): # pragma: no cover
        return
    except Exception as e:
        print(e)

if __name__ == '__main__': # pragma: no cover
    handle()
