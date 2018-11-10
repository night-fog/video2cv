import logging

# log path and level
LOG_MAIN_PATH = 'main.log'
LOG_MAIN_LEVEL = logging.INFO

# If you have only one cam, it's commonly = 0
VIDEO_DEVICE_ID = 0
# SIze of frame to analise
VIDEO_WIDTH = 320
VIDEO_HEIGHT = 200
# color to be found in frame. tuple in format (Red, Green, Blue), [0, 255].
VIDEO_FILTER_COLOR = (250, 161, 226)
# delta of hue color (rgb color, converted to HSV)
VIDEO_HUE_DELTA = 15
# low and high border of HSV saturation filter
VIDEO_SATURATION_LOW = 0
VIDEO_SATURATION_HIGH = 255
# low and high border of HSV value filter
VIDEO_VALUE_LOW = 0
VIDEO_VALUE_HIGH = 255

# Place to send MIDI data. You can use False value for virtual port,
# if you want to use it on your local DAW.
# You also can use real midi in port, like 'Steinberg UR22mkII  Port1'.
# List of available ports can be found in log LOG_MAIN_PATH
MIDI_OUT_NAME = False
