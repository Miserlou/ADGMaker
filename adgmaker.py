# ADGMaker

import argparse

####################################################################
# Main
####################################################################

class ADGMaker(object):
    """
    Read CLI input, create ADGs.

    """

    def handle(self, argv=None):
        """
        Main function.

        Parses command, load settings and dispatches accordingly.

        """
        help_message = "Please supply a path to a folder of MP3s."
        parser = argparse.ArgumentParser(description='ADGMaker - Create Ableton Live Instruments.\n')
        parser.add_argument('samples_path', metavar='U', type=str, nargs='*', help=help_message)
        args = parser.parse_args(argv)
        vargs = vars(args)

        if not vargs['samples_path']:
            print(help_message)
            return

    def add_mp3_to_instrument(file_path):
        """
        Given a complete file path, add to the XML for this instrument.

        Samples are in the format:
            {{instrument_name}}_{{note}}_{{length}}_{{velocity}}_{{type}}.mp3
        Ex:
            double-bass_Gs3_1_piano_arco-normal.mp3

        """
        return
        
    def create_base_xml():
        """
        Create the standard cruft XML for the ADG.
        """
        return

    def write_adg(adg_name):
        """
        Create the final ADG file.
        """
        return

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
