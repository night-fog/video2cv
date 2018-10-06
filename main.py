from datetime import datetime
import logging

from grab_video_mp import GrabVideoMP

import conf


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
    vid = GrabVideoMP(conf.VIDEO_DEVICE_ID)
    vid.set_resolution(conf.VIDEO_WIDTH, conf.VIDEO_HEIGHT)
    vid.set_color_range_filter(conf.VIDEO_FILTER_COLOR1, conf.VIDEO_FILTER_COLOR1)
    count_cycles = 100
    print(f'Start: {datetime.now()}')
    for i in range(count_cycles):
        print(str(datetime.now()) + ' ' + str(vid.count_pixels()))
    print(f'End: {datetime.now()}')
    vid.__del__()
