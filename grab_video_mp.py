from math import ceil
from multiprocessing import Process, Queue, cpu_count

import cv2


class GrabVideoMP:
    _cap = None
    _filter = None
    _frame_size = None

    def __init__(self, camera_id=0):
        self._cap = cv2.VideoCapture(camera_id)

    def __del__(self):
        self._cap.release()
        cv2.destroyAllWindows()

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

    def set_color_range_filter(self, color1: tuple, color2: tuple):
        if not isinstance(color1, tuple) or len(color1) != 3 or not isinstance(
                color2, tuple) or len(color2) != 3:
            return False

        if not self._are_tuple_items_colors(
                    color1) or not self._are_tuple_items_colors(color2):
            return False

        self._filter = dict()
        self._filter['min_red'], self._filter['max_red'] = self._int_min_max(color1[0], color2[0])
        self._filter['min_green'], self._filter['max_green'] = self._int_min_max(color1[1], color2[1])
        self._filter['min_blue'], self._filter['max_blue'] = self._int_min_max(color1[2], color2[2])
        return True

    def _are_colors_in_range(self, bgr: tuple):
        if bgr[0] >= self._filter['min_blue'] and \
                bgr[0] <= self._filter['max_blue'] and \
                bgr[1] >= self._filter['min_green'] and \
                bgr[1] <= self._filter['max_green'] and \
                bgr[2] >= self._filter['min_red'] and \
                bgr[2] <= self._filter['max_red']:
            return 1
        else:
            return 0

    def _mp_pixels_in_frame(self, frame, proc_count):
        def worker(frame, out_q):

            pixels = 0
            for i in range(len(frame)):
                for j in range(len(frame[i])):
                    pixels += self._are_colors_in_range(frame[i][j])
            out_q.put(pixels)

        out_q = Queue()
        chunksize = int(ceil(len(frame) / float(proc_count)))
        procs = []

        for i in range(proc_count):
            p = Process(
                target=worker,
                args=(frame[chunksize * i:chunksize * (i + 1)], out_q))
            procs.append(p)
            p.start()

        pixel_count = 0
        for i in range(proc_count):
            pixel_count += out_q.get()

        for p in procs:
            p.join()

        return pixel_count

    def count_pixels(self):
        '''
        Pixel count in frame from video input, that are in range of filter
        colors (including borders)
        If filter is not set, count returns 1 without reading a frame.
        :return:
        % of pixels, what pass the filter in current frame
        '''
        if self._filter is None:
            return 1.0
        ret, frame = self._cap.read()
        pixel_count = self._mp_pixels_in_frame(frame, cpu_count())
        return  pixel_count / (self._frame_size / 100.0)

    '''
    # if problems with closed cam occur
    def open_cap(self):
        if not self._cap.isOpened():
            self._cap.open()
    '''