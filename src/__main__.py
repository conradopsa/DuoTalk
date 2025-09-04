import argparse
import duotalker

SPEAKER_DEFAULT = "atlas" # "gaia" | "atlas" | "uranos"

def _getArgs():
    parser = argparse.ArgumentParser(description='Read a text file and optionally specify a speaker')
    parser.add_argument('filepath', help='Path to the text file to read')
    parser.add_argument('-s', '--speaker', help='Speaker name (e.g., gaia)', default=SPEAKER_DEFAULT)
    
    # Parse arguments
    args = parser.parse_args()

    return args

def main():  
    args = _getArgs()

    filepath = args.filepath
    speaker_name = args.speaker

    duotalker.start_from_file(filepath, speaker_name)


main()