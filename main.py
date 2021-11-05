import os, sys, getopt
import yaml
from powerapps_docstring.powerapp import PowerApp, UnknownSourceException
from powerapps_docstring.documentation import Docstring


def main(argv):
    """main

    Args:
        argv ([type]): [description]
    """

    # define possible arguments
    try:
        opts, args = getopt.getopt(argv,"hs:o:c:",["source=", "output=", "config="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    # if programm started without arguments, we run the GUI
    if len(opts) == 0:
        from docstring_gui import main as gui_main
        try:
            gui_main()
        except TypeError:
            # when donwstream application is terminated, it will thro a TypeError exception. 
            pass

        sys.exit(1)

    source_path = None
    output_path = None
    config_file = "config.yaml"

    # check for args provided
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
            sys.exit(1)
        elif opt in ("-s", "--source"):
            source_path = arg
        elif opt in ("-o", "--output"):
            output_path = arg
        elif opt in ("-c", "--config"):
            config_file = arg

    if source_path == None or output_path == None:
        print("Missing path to PowerApps file or documentation output folder")
        print("Refere to the help with -h or --help")
        sys.exit(1)

    # check source path
    try:
        pa_src_path = PowerApp(source_path).get_pa_src_path()
        print(pa_src_path)
    except UnknownSourceException:
        print("The source type is not valid")
        print("Refere to the help with -h or --help")
        sys.exit(1)

    # check output path
    if not os.path.isdir(output_path):
        print("The output path is not valid")
        print("Refere to the help with -h or --help")
        sys.exit(1)

    # check config file
    # set temp path to configfile if running as exe
    if hasattr(sys, '_MEIPASS'):
        temp_path = os.path.join(sys._MEIPASS)
        config_file = temp_path + "\config.yaml"

    if not os.path.isfile(config_file):
        print(f"The config file: {config_file} is not valid.")
        print("Refere to the help with -h or --help")
        sys.exit(1)
    else:
        with open(config_file, "r", encoding='utf8') as file:
            config = yaml.safe_load(file)


    docstring = Docstring(pa_src_path, output_path, config)
    docstring.create_documentation()

def print_help():
    print(main.__doc__)

if __name__ == "__main__":
    main(sys.argv[1:])