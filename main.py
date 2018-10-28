from datetime import datetime
import logging

#from grab_video_mp import GrabVideoMP
from grab_video import GrabVideo

import conf
from data2midi import Data2Midi


def init_log():
    log = logging.getLogger()
    handler = logging.FileHandler(conf.LOG_MAIN_PATH, 'a', encoding='UTF-8')
    handler.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    log.addHandler(handler)
    log.setLevel(conf.LOG_MAIN_LEVEL)
    return log

if __name__ == '__main__':
    log = init_log()
    vid = GrabVideo(conf.VIDEO_DEVICE_ID)
    vid.set_resolution(conf.VIDEO_WIDTH, conf.VIDEO_HEIGHT)
    assert vid.set_rgb_color(conf.VIDEO_FILTER_COLOR), 'Filter RGB color was not set'
    assert vid.set_color_delta(conf.VIDEO_HUE_DELTA, conf.VIDEO_SATURATION_LOW, conf.VIDEO_SATURATION_HIGH, conf.VIDEO_VALUE_LOW, conf.VIDEO_VALUE_HIGH), 'Wrong init filter set'
    midi_out = Data2Midi()
    default_velocity = 127
    while(True):
        midi_out.send_midi_cc(Data2Midi.float_to_127(vid.count_pixels()))
        #midi_out.send_midi_note(Data2Midi.float_to_127(vid.count_pixels()), default_velocity)
    #midi_out.stop_all()
    vid.__del__()
