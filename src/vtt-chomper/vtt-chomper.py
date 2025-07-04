'''
vtt-chomper: it chomps VTT files!
'''
import argparse
from datetime import datetime as dt
import sys

import webvtt

def timestamp_to_ms(timestamp):
    """Converts a VTT timestamp string (hh:mm:ss.mmm) to milliseconds."""
    hours, minutes, secondsWithMs = timestamp.split(":")
    seconds, milliseconds = secondsWithMs.split(".")

    return (int(hours) * 3600 + int(minutes) * 60 + int(seconds)) * 1000 + int(milliseconds)

def ms_to_timestamp(msTime):
    """Converts milliseconds to a VTT timestamp string (hh:mm:ss.mmm)"""
    hours, minSecMs = divmod(msTime, 3600000)
    minutes, secMs = divmod(minSecMs, 60000)
    seconds, milliseconds = divmod(secMs, 1000)

    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

def time_to_secs(timestamp):
    '''Convert HH:MM:SS timestamps to seconds'''

    if timestamp.isdigit():
        return int(timestamp)

    hours = minutes = seconds = "00"
    if ":" in timestamp:
        minutes, seconds = timestamp.rsplit(':', maxsplit=1)
        if ":" in minutes:
            hours, minutes = minutes.split(':')
    else:
        print(f"Timestamp {timestamp} not in seconds or HH:MM:SS")
        sys.exit(1)

    try:
        timeSecs = dt.strptime(f"{hours}:{minutes}:{seconds}", "%H:%M:%S") - dt(1900,1,1)
    except ValueError:
        print(f"This does not look like a real timestamp: {timestamp}")
        sys.exit(1)
    return int(timeSecs.total_seconds())


def do_a_whimsy():
    """Prints an ASCII art alligator. It's not that deep."""

    print('     _    _')
    print('____/ \\__/ \\____oo__')
    print('    \\O/  \\O/        \\')
    print('                    )')
    print('-----VVVVVVVVVVVVVVV')
    print('')
    print('         VTT')
    print('')
    print('-----^^^^^^^^^^^^^^\\')
    print('____________________)')

def get_options():
    """Get the options
        Returns: options <class 'argparse.Namespace'>
    """

    argparser = argparse.ArgumentParser(
        description='Trim the ends off of VTT files'
        )
    # Files
    argparser.add_argument(
        "-i", "--input",
        dest="inputFile",
        help="Input VTT file"
    )
    argparser.add_argument(
        "-o", "--output",
        dest="outputFile",
        help="Output VTT file"
    )
    # Trims
    argparser.add_argument(
        "-b", "--beginning",
        dest="trimBeginning",
        help="Seconds or HH:MM:SS to trim from the beginning",
        default=0,
        type=str
    )
    argparser.add_argument(
        "-e", "--end",
        dest="trimEnd",
        help="Ending timestamp in seconds or HH:MM:SS",
        type=str
    )
    argparser.add_argument(
        "--whimsy",
        dest="whimsy",
        help="Chomp!",
        action='store_true'
    )

    return argparser.parse_args()

def chomp_it(inVtt,firstTimestamp, lastTimestamp):
    """Does the chomping
        Input: inVtt <class 'webvtt.webvtt.WebVTT'>
        Output: outVtt <class 'webvtt.webvtt.WebVTT'>
    """
    outVtt = webvtt.WebVTT()

    for caption in inVtt.captions:
        startTime = timestamp_to_ms(caption.start)
        endTime = timestamp_to_ms(caption.end)
        if startTime > firstTimestamp and endTime <= lastTimestamp:
            startStamp = ms_to_timestamp(startTime - firstTimestamp)
            endStamp = ms_to_timestamp(timestamp_to_ms(caption.end) - firstTimestamp)

            outVtt.captions.append(webvtt.Caption(startStamp, endStamp, caption.text))

    return outVtt

def validate_times(trimBeginning, trimEnd, lastTimestamp):
    '''Make sure the times that the user specified are reasonable.'''

    # If both trims are zero, what exactly is it that you want me to do here?
    if (trimEnd and trimBeginning == trimEnd) or (not trimBeginning and not trimEnd):
        print("No trimming requested. That was easy!")
        sys.exit(1)
    elif lastTimestamp <= trimBeginning * 1000:
        print("The end time can't be less than the start time. What are you doing?")
        sys.exit(1)


def main():
    '''This is where the magic happens.'''

    options = get_options()

    # Want to do a whimsy?
    if options.whimsy:
        do_a_whimsy()
        sys.exit(0)

    try:
        inVtt = webvtt.read(options.inputFile)
    except TypeError:
        print("You need to specify an input file, silly!")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Chompy could not find {options.inputFile}")
        sys.exit(1)
    except PermissionError:
        print(f"Permission denied for {options.inputFile}")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Unicdode error for {options.inputFile}. Is this a vtt file?")
        sys.exit(1)

    trimBeginning = time_to_secs(options.trimBeginning)
    # If we're chomping off the end, just use the value provided.
    # If we're not chomping off the end, use the final timestamp as the
    # comparison point for chomping.
    if options.trimEnd:
        trimEnd = time_to_secs(options.trimEnd)
        lastTimestamp = trimEnd * 1000
    else:
        lastTimestamp = timestamp_to_ms(inVtt.captions[-1].end)
        # We still need to define trimEnd to make validate_times happy
        trimEnd = options.trimEnd

    validate_times(trimBeginning, trimEnd, lastTimestamp)

    # Do the chomping!
    outVtt = chomp_it(inVtt, trimBeginning * 1000, lastTimestamp)

    try:
        outVtt.save(options.outputFile)
    except webvtt.errors.MissingFilenameError:
        print("No output file specified!")
        sys.exit(1)
    except PermissionError:
        print(f"Permission denied to {options.outputFile}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Directory not found for {options.outputFile}")
        sys.exit(1)

if __name__ == '__main__':
    main()  # pragma: no cover
