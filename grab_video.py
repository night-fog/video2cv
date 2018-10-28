from math import ceil
from datetime import datetime

import cv2
import numpy as np

from var_validators import is_int


class GrabVideo:
    _cap = None
    _filter_min = None
    _filter_max = None
    _frame_size = None
    _rgb_color = [0, 0, 0]
    _hue_delta = 0
    _fps_data = {
        'start' : None,
        'frames': 0
    }
    _saturation = {
        'low': 0,
        'high': 256
    }
    _value = {
        'low': 0,
        'high': 256
    }

    def __init__(self, camera_id=0, debug=False):
        self._cap = cv2.VideoCapture(camera_id)
        self._debug = debug

    def __del__(self):
        self._cap.release()
        cv2.destroyAllWindows()

    def _count_fps(self):
        if not self._fps_data.get('start'):
            self._fps_data['start'] = datetime.now()
        self._fps_data['frames'] += 1
        time = (datetime.now() - self._fps_data['start'])
        time_delta = time.seconds + (time.microseconds / 1000000.0)
        print(f'fps={(self._fps_data.get("frames") / time_delta)}')


    def _int_min_max(self, val1, val2):
        if val1 >= val2:
            return val2, val1
        else:
            return val1, val2

    def set_resolution(self, width, height):
        self._cap.set(3, width)
        self._cap.set(4, height)
        self._frame_size = width * height

    def _are_tuple_items_colors(self, tuple_obj: list, int_min=0,
                                   int_max=256, tuple_len=3):
        if not isinstance(tuple_obj, tuple) or len(tuple_obj) != tuple_len:
            return False
        for item in tuple_obj:
            if item > int_max or item < int_min:
                return False
        return True

    def set_rgb_color(self, rgb_color: tuple):
        if not isinstance(rgb_color, tuple) or len(
            rgb_color) != 3 or not self._are_tuple_items_colors(rgb_color):
            return False
        self._rgb_color = [rgb_color[2], rgb_color[1], rgb_color[0]]
        return True

    @staticmethod
    def limit_colors(val, min=0, max=255):
        if val < 0:
            return 0
        elif val > 255:
            return 255
        else:
            return val

    def _color2hsv_delta(self):
        hsv = cv2.cvtColor(np.uint8([[self._rgb_color]]), cv2.COLOR_BGR2HSV)[0][0]
        self._filter_min = np.array([self.limit_colors((hsv[0] - self._hue_delta)),
                                     self.limit_colors((self._saturation.get('low'))),
                                     self.limit_colors((self._value.get('low')))])
        self._filter_max = np.array([self.limit_colors((hsv[0] + self._hue_delta)),
                                     self.limit_colors((self._saturation.get('high'))),
                                     self.limit_colors((self._value.get('high')))])

    def set_color_delta(self, hue_delta: int = -1, saturation_low: int = -1,
                            saturation_high: int = -1, value_low: int = -1,
                            value_high: int = -1):
        if hue_delta != -1:
            self._hue_delta = hue_delta
        if saturation_low != -1 and (saturation_low < self._saturation['high']):
            self._saturation['low'] = saturation_low
        if saturation_high != -1 and (saturation_high > self._saturation['low']):
            self._saturation['high'] = saturation_high
        if value_low != -1 and (value_low < self._value['high']):
            self._value['low'] = value_low
        if value_high != -1 and (value_high > self._value['low']):
            self._value['high'] = value_high
        self._color2hsv_delta()
        return True

    def _count_pixels(self):
        '''
        Pixel count in frame from video input, that are in range of filter
        colors (including borders)
        If filter is not set, count returns 1 without reading a frame.
        :return:
        % of pixels, what pass the filter in current frame
        '''
        if self._filter_min is None or self._filter_max is None:
            return 1.0
        ret, frame = self._cap.read()
        if ret is False:
            return 0.0
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask_hsv = cv2.inRange(frame_hsv, self._filter_min, self._filter_max)
        pixel_count = cv2.countNonZero(mask_hsv)
        if self._debug:
            #self._count_fps()
            frame_hsv = cv2.bitwise_and(frame, frame, mask=mask_hsv)
            cv2.imshow('frame', frame)
            cv2.imshow('mask', frame_hsv)
        data = pixel_count / self._frame_size
        return data

    def count_pixels(self):
        count = self._count_pixels()
        k = cv2.waitKey(0) & 0xFF
        if k == 27:
            self.__del__()
        return count
