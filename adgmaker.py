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
        help_message = "Please supply a command to execute."

        parser = argparse.ArgumentParser(description='ADGMaker - Create Ableton Live Instruments.\n')
        # parser.add_argument('command_env', metavar='U', type=str, nargs='*', help=help_message)

        args = parser.parse_args(argv)
        vargs = vars(args)


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
