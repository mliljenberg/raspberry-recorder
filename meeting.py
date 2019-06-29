"""
meeting listening app
"""


import time
import logging
import subprocess
from voice_engine.source import Source
from voice_engine.channel_picker import ChannelPicker
from voice_engine.kws import KWS
from voice_engine.ns import NS
from voice_engine.doa_respeaker_4mic_array import DOA
from avs.alexa import Alexa
from pixels import pixels

# TODO: Fix this function so it records for one minute then listen if anything is said,
#   if something is said it should then start recording again?
def main():
    logging.basicConfig(level=logging.DEBUG)

    src = Source(rate=16000, channels=4) 
    ch1 = ChannelPicker(channels=4, pick=1)
    ns = NS(rate=16000, channels=1)
    kws = KWS(model='snowboy')
    doa = DOA(rate=16000)

    def on_detected(keyword):
        direction = doa.get_direction()
        logging.info('detected {} at direction {}'.format(keyword, direction))
        pixels.wakeup(direction)
        record = "arecord -Dac108 -f S32_LE -r 16000 -c 4 -d 10 hello.wav"
        p = subprocess.Popen(record, shell=True)

    kws.on_detected = on_detected

    src.link(ch1)
    ch1.link(ns)
    ns.link(kws)

    src.link(doa)

    src.recursive_start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    src.recursive_stop()


if __name__ == '__main__':
    main()
