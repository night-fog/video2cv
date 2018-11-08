import logging

import conf
from grab_video import GrabVideo
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
    debug = False
    if conf.LOG_MAIN_LEVEL == logging.DEBUG:
        debug = True

    log = init_log()
    log.info('Program start')
    def _log(message, level=logging.INFO, quit=False):
        print(message)
        if level == logging.ERROR:
            log.error(message)
        elif level == logging.DEBUG:
            if conf.LOG_MAIN_LEVEL == logging.DEBUG:
                log.debug(message)
        else:
            log.info(message)
        if quit:
            exit(1)

    vid = GrabVideo(conf.VIDEO_DEVICE_ID, debug)
    vid.set_resolution(conf.VIDEO_WIDTH, conf.VIDEO_HEIGHT)
    status = vid.set_rgb_color(conf.VIDEO_FILTER_COLOR)
    if not status:
        _log('Filter RGB color was not set', logging.ERROR, quit=True)

    status = vid.set_color_delta(conf.VIDEO_HUE_DELTA,
                                 conf.VIDEO_SATURATION_LOW,
                                 conf.VIDEO_SATURATION_HIGH,
                                 conf.VIDEO_VALUE_LOW, conf.VIDEO_VALUE_HIGH)
    if not status:
        _log('Wrong init filter set', logging.ERROR, quit=True)

    midi_out = Data2Midi()
    while(True):
        frame_value = vid.count_pixels()
        _log(frame_value, level=logging.DEBUG)
        midi_out.send_midi_cc(frame_value)
    vid.__del__()
