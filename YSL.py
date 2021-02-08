import requests
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
        self.currently_streaming = {}
        self.stream_data = OrderedDict()
        self.number_of_active_streams = 0
        self.number_of_to_be_liked_streams = 0

    def get_start_time(self):
        self.start_time = time.time()
        self.time_started = time.strftime("%H:%M:%S", time.localtime())
        self.stream_data['Time Started'] = self.time_started

    def is_streaming(self):
        for name in self.channels.keys():
            channel_url = 'https://www.youtube.com/channel/' + self.channels[name]
            response = requests.get(channel_url).text
            stream_active = '{"text":" watching"}' in response
            if stream_active:
                self.currently_streaming[name] = self.channels[name]


# ysl = YSL('channel ids.txt')
# ysl.get_channels()
# print(ysl.channels)

sl = StreamLiker('channel ids.txt')
sl.get_channels()
sl.get_start_time()
sl.is_streaming()
print(sl.currently_streaming)

