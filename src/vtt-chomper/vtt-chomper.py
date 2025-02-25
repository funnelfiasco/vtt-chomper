import webvtt

from datetime import timedelta

INPUT_FILE="input.vtt"
OUTPUT_FILE="output.vtt"
START_SECONDS=492

def timestamp_to_ms(timestamp):
    """Converts a VTT timestamp string (hh:mm:ss.mmm) to milliseconds."""
    hours, minutes, secondsWithMs = timestamp.split(":")
    seconds, milliseconds = secondsWithMs.split(".")
    
    return (int(hours) * 3600 + int(minutes) * 60 + int(seconds)) * 1000 + int(milliseconds)

def ms_to_timestamp(msTime):
    """Converts milliseconds to a VTT timestamp string (hh:mm:ss.mmm)"""
    #return str(timedelta(seconds=msTime/1000))[:-3]
    hours, minSecMs = divmod(msTime, 3600000)
    minutes, secMs = divmod(minSecMs, 60000)
    seconds, milliseconds = divmod(secMs, 1000)

    return "{:02}:{:02}:{:02}.{:03}".format(int(hours), int(minutes), int(seconds), int(milliseconds))

def main():

    inVtt = webvtt.read(INPUT_FILE)
    outVtt = webvtt.WebVTT()

    for caption in inVtt.captions:
        startTime = timestamp_to_ms(caption.start)
        if startTime > (START_SECONDS * 1000):
            startStamp = ms_to_timestamp(startTime - (START_SECONDS*1000))
            endStamp = ms_to_timestamp(timestamp_to_ms(caption.end) - (START_SECONDS*1000))

            outVtt.captions.append(webvtt.Caption(startStamp, endStamp, caption.text))
    
    outVtt.save(OUTPUT_FILE)

if __name__ == '__main__':
    main()  # pragma: no cover