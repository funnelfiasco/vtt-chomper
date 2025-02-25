import argparse
import webvtt

from datetime import timedelta

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

    return "{:02}:{:02}:{:02}.{:03}".format(int(hours), int(minutes), int(seconds), int(milliseconds))

def main():

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

    options = argparser.parse_args()
    
    inVtt = webvtt.read(options.inputFile)
    outVtt = webvtt.WebVTT()

    for caption in inVtt.captions:
        startTime = timestamp_to_ms(caption.start)
        if startTime > (options.trimBeginning * 1000):
            startStamp = ms_to_timestamp(startTime - (options.trimBeginning*1000))
            endStamp = ms_to_timestamp(timestamp_to_ms(caption.end) - (options.trimBeginning*1000))

            outVtt.captions.append(webvtt.Caption(startStamp, endStamp, caption.text))
    
    outVtt.save(options.outputFile)

if __name__ == '__main__':
    main()  # pragma: no cover