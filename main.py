from grab_video_mp import GrabVideoMP
from datetime import datetime

if __name__ == '__main__':
    video_device_id = 0
    vid = GrabVideoMP(video_device_id)
    vid.set_width(320)
    vid.set_height(200)
    color1 = (150, 150, 150)
    color2 = (50, 50, 50)
    count_cycles = 100
    vid.set_color_range_filter(color1, color2)
    print(f'Start: {datetime.now()}')
    for i in range(count_cycles):
        print(str(datetime.now()) + ' ' + str(vid.count_pixels()))
    print(f'End: {datetime.now()}')
    vid.__del__()
