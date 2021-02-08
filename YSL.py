from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from collections import OrderedDict
from datetime import date
import requests
import os
import time

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
        self.streams_liked = {}
        self.video_ids = []
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
                self.currently_streaming[name] = channel_url
                self.number_of_active_streams += 1

    def get_stream_links(self):
        PATH = 'C:/Program Files (x86)/geckodriver.exe'
        options = FirefoxOptions()
        options.add_argument('--headless')
        options.add_argument('--mute-audio')
        driver = webdriver.Firefox(options=options, executable_path=PATH)
        # num_to_be_liked = 0

        for name, channel_link in self.currently_streaming.items():
            driver.get(channel_link + '/videos')

            try:
                video_url = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="thumbnail"]'))
                )
                link = video_url.get_attribute('href')

                with open('video links.txt', 'r') as link_read:
                    if link in link_read.read():
                        print(f'Video from {name} is already liked.')
                    elif link not in link_read.read():
                        self.number_of_to_be_liked_streams += 1
                        self.streams_liked[name] = link
                        self.video_ids.append(link[32:])
                        # num_to_be_liked += 1
                        with open('video links.txt', 'a') as link_write:
                            # link_write.write(link + '\n')
                            print(f'Video stream of {name} added to queue')

            except:
                print("XPATH not found")
                driver.quit()
                return None

        driver.quit()


# ysl = YSL('channel ids.txt')
# ysl.get_channels()
# print(ysl.channels)

sl = StreamLiker('channel ids.txt')
sl.get_channels()
# sl.get_start_time()
sl.is_streaming()
# print(sl.currently_streaming)
sl.get_stream_links()

