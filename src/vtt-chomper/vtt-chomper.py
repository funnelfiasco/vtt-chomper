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
        required=True
    )
    argparser.add_argument(
        "-o", "--output",
        dest="outputFile",
        help="Output VTT file",
        required=True
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
        help="Seconds to trim from the end",
        default=0,
        type=int
    )
    options = argparser.parse_args()

    # If both trims are zero, what exactly is it that you want me to do here?
    if options.trimBeginning == 0 and options.trimEnd == 0:
        print("No trimming requested. That was easy!")
        sys.exit(0)

    inVtt = webvtt.read(options.inputFile)
    outVtt = webvtt.WebVTT()

    # If we're chomping off the back, check to see what the final timestamp is.
    # If we're not chomping off the back, use the final timestamp as the
    # chomping point.
    lastTimestamp = timestamp_to_ms(inVtt.captions[-1].end) - (options.trimEnd * 1000)

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
