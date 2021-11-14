import os, sys, getopt
import yaml
from powerapps_docstring.powerapp import PowerApp, UnknownSourceException, CanvasManifestNotFoundInSourceException
from powerapps_docstring.documentation import Docstring


def main(argv):
    pa_src_path = "example/src/meetingcapturedemo"
    output_path = "example"
    config_file = "config.yaml"

    if not os.path.isfile(config_file):
        print(f"The config file: {config_file} is not valid.")
        print("Refere to the help with -h or --help")
        sys.exit(1)
    else:
        with open(config_file, "r", encoding='utf8') as file:
            config = yaml.safe_load(file)

    # run documentation creation process
    print(f"Creating documentation for {pa_src_path}")
    try:
        docstring = Docstring(pa_src_path, output_path, config)
        documentation_output_path = docstring.create_documentation()
        print(f"Documentation created successfully: {documentation_output_path}")
        sys.exit(0)
    except Exception as e:
        print("Error occured within documentation creation")
        raise e

def print_help():
    print(main.__doc__)

if __name__ == "__main__":
    main(sys.argv[1:])