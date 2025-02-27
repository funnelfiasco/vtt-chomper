'''
vtt-chomper: it chomps VTT files!
'''
import argparse
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

def main():
    '''This is where the magic happens.'''

    argparser = argparse.ArgumentParser(
        description='Trim the ends off of VTT files'
        )
    # Files
    argparser.add_argument(
        "-i", "--input",
        dest="inputFile",
        help="Input VTT file",
        default=0
    )
    argparser.add_argument(
        "-o", "--output",
        dest="outputFile",
        help="Output VTT file",
        default=0
    )
    # Trims
    argparser.add_argument(
        "-b", "--beginning",
        dest="trimBeginning",
        help="Seconds to trim from the beginning",
        default=0,
        type=int
    )
    argparser.add_argument(
        "-e", "--end",
        dest="trimEnd",
        help="Ending timestamp in seconds",
        default=-1,
        type=int
    )
    argparser.add_argument(
        "--whimsy",
        dest="whimsy",
        help="Chomp!",
        action='store_true'
    )
    options = argparser.parse_args()

    # Want to do a whismy?
    if options.whimsy:
        do_a_whimsy()
        sys.exit(0)

    # If both trims are zero, what exactly is it that you want me to do here?
    if options.trimBeginning == 0 and options.trimEnd == 0:
        print("No trimming requested. That was easy!")
        sys.exit(0)

    inVtt = webvtt.read(options.inputFile)
    outVtt = webvtt.WebVTT()

    # If we're chomping off the end, just use the value provided.
    # If we're not chomping off the end, use the final timestamp as the
    # comparison point for chomping.
    if options.trimEnd == -1:
        lastTimestamp = timestamp_to_ms(inVtt.captions[-1].end)
    else:
        lastTimestamp = options.trimEnd * 1000

    for caption in inVtt.captions:
        startTime = timestamp_to_ms(caption.start)
        endTime = timestamp_to_ms(caption.end)
        if startTime > (options.trimBeginning * 1000) and endTime <= lastTimestamp:
            startStamp = ms_to_timestamp(startTime - (options.trimBeginning*1000))
            endStamp = ms_to_timestamp(timestamp_to_ms(caption.end) - (options.trimBeginning*1000))

            outVtt.captions.append(webvtt.Caption(startStamp, endStamp, caption.text))

    outVtt.save(options.outputFile)

if __name__ == '__main__':
    main()  # pragma: no cover
