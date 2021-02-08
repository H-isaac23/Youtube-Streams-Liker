import os
from datetime import date
import time
from collections import OrderedDict

class YSL:
    def __init__(self, channels_path):
        self.channels_path = channels_path
        self.status_codes = {1: "Checking for streams...", 2: "Logging into YouTube..."}
        self.channels = {}

    def get_channels(self):
        with open(self.channels_path, 'r') as channels:
            for channel in channels.readlines():
                channel_id = channel[:24]
                channel_name = channel[27:-1]
                self.channels[channel_name] = channel_id

class StreamLiker(YSL):
    def __init__(self, channels_path):
        super(StreamLiker, self).__init__(channels_path)
        self.start_time = None
        self.time_started = None
        self.stream_data = OrderedDict()

    def get_start_time(self):
        self.start_time = time.time()
        self.time_started = time.strftime("%H:%M:%S", time.localtime())
        self.stream_data['Time Started'] = self.time_started


# ysl = YSL('channel ids.txt')
# ysl.get_channels()
# print(ysl.channels)

sl = StreamLiker('channel ids.txt')
sl.get_channels()
print(sl.channels)