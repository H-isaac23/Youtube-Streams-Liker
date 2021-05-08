from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from collections import OrderedDict
from datetime import date
from threading import Thread
import mysql.connector
import csv
import requests
import os
import time


class YSL:
    def __init__(self, channels_path):
        self.channels_path = channels_path
        self.channels = {}
        self.threads = []
        self.get_channels()

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
        self.total_time_elapsed = 0
        self.time_ended = None
        self.check_streamers_time = None

        self.currently_streaming = {}
        self.stream_data = OrderedDict()
        self.number_of_active_streams = 0
        self.number_of_to_be_liked_streams = 0
        self.date = None

        self.like = False
        self.driver = None
        self.options = FirefoxOptions()

        self.version = "1.6"
        self.status = ""

    def clear_data(self):
        self.start_time = None
        self.time_started = None
        self.total_time_elapsed = 0
        self.time_ended = None
        self.check_streamers_time = None

        self.currently_streaming = {}
        self.stream_data = OrderedDict()
        self.number_of_active_streams = 0
        self.number_of_to_be_liked_streams = 0
        self.date = None

        self.like = False

    def get_start_time(self):
        self.start_time = time.time()
        self.time_started = time.strftime("%H:%M:%S", time.localtime())
        self.stream_data['Time Started'] = self.time_started

    def is_streaming(self, name):
        s_time = time.time()

        channel_url = 'https://www.youtube.com/channel/' + self.channels[name]
        response = requests.get(channel_url).text
        stream_active = '{"text":" watching"}' in response
        status = f"{name} - is "

        if stream_active:
            v_index = response.find("videoRenderer")
            self.currently_streaming[name] = response[v_index+27:v_index+38]
            self.number_of_active_streams += 1
            status += "currently streaming.\n"
        else:
            status += "not streaming.\n"

        self.stream_data['No. of active streams'] = self.number_of_active_streams
        e_time = time.time()
        self.check_streamers_time = e_time - s_time
        self.stream_data['Check streamers time'] = self.check_streamers_time
        self.status += status

    def config_driver(self, path, firefox_profile, args=None, mute_sound=False):
        if self.number_of_active_streams == 0:
            print("There are no active streams as of the moment.")
            return

        print("Current status: Configuring driver...")
        print('-' * 30)

        self.like = True
        try:
            for arg in args:
                self.options.add_argument(arg)
        except:
            print("No args supplied for driver options.")

        profile = webdriver.FirefoxProfile(
            firefox_profile
        )

        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        if mute_sound:
            profile.set_preference("media.volume_scale", "0.0")
        profile.update_preferences()
        desired = DesiredCapabilities.FIREFOX

        self.driver = webdriver.Firefox(
            options=self.options,
            executable_path=path,
            firefox_profile=profile,
            desired_capabilities=desired
        )

    def like_videos(self):

        if self.like:
            print("Current status: Liking videos...")
            print('-' * 30)
            no_exception = True
            for name, video_id in self.currently_streaming.items():
                is_liked = False
                link = "https://www.youtube.com/watch?v=" + video_id
                self.driver.get(link)

                try:
                    like_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[6]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div[1]/ytd-toggle-button-renderer[1]/a/yt-icon-button'))
                    )
                    if like_button.get_attribute("class") == "style-scope ytd-toggle-button-renderer style-default-active":
                        is_liked = True
                        print(f"Video from {name} is already liked.")
                #//*[@id="top-level-buttons"]/ytd-toggle-button-renderer[1]/a/yt-icon-button/button
                # //*[@id="button"]/yt-icon
                # //*[@id="top-level-buttons"]/ytd-toggle-button-renderer[1]/a
                # //*[@id="top-level-buttons"]/ytd-toggle-button-renderer[1]/a
                # /html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div[1]/ytd-toggle-button-renderer[1]/a/yt-icon-button
                # /html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[6]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div[1]/ytd-toggle-button-renderer[1]/a
                # /html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[6]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div[1]/ytd-toggle-button-renderer[1]/a/yt-icon-button/button/yt-icon
                # /html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div[1]/ytd-toggle-button-renderer[1]/a/yt-icon-button/button/yt-icon
                except Exception:
                    print("LikeButtonError: Cannot find XPATH. URL may be invalid.")
                    no_exception = False
                    pass

                if not is_liked and no_exception:
                    self.number_of_to_be_liked_streams += 1
                    ActionChains(self.driver).move_to_element(like_button).click(like_button).perform()
                    print(f"Video from {name} is liked.")

            self.stream_data['No. of to-be-liked streams'] = self.number_of_to_be_liked_streams
            self.stream_data['Streams liked'] = ','.join(self.currently_streaming.values())

    def get_end_time(self):
        self.time_ended = time.strftime("%H:%M:%S", time.localtime())
        self.stream_data['Time Ended'] = self.time_ended
        self.total_time_elapsed = time.time() - self.start_time
        self.stream_data['Time elapsed'] = self.total_time_elapsed

    def append_data_on_file(self, my_dir):
        # File naming
        today = date.today()
        self.date = today.strftime("%m/%d/%y")
        hyphenated_date = '-'.join(self.date.split('/'))
        filename = f'stream_data {hyphenated_date}.csv'

        # Check if a file exists
        if not os.path.exists(my_dir + f'/{filename}'):
            with open(my_dir + f'/{filename}', 'a', newline='') as csv_file:
                fieldnames = ['Time elapsed', 'No. of active streams', 'No. of to-be-liked streams', 'Time Started',
                              'Time Ended', 'Streams liked', 'Check streamers time']
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                csv_writer.writeheader()

        with open(my_dir + f'/{filename}', 'a', newline='') as csv_file:
            fieldnames = ['Time elapsed', 'No. of active streams', 'No. of to-be-liked streams', 'Time Started',
                          'Time Ended', 'Streams liked', 'Check streamers time']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writerow(self.stream_data)

        print(f"Time finished: {self.time_ended}")
        print("Total time elapsed: %.2f seconds." % self.total_time_elapsed)

    def append_data_on_db(self, user, host, passwd, database, table_name):
        tel = self.stream_data["Time elapsed"]
        nas = self.stream_data["No. of active streams"]
        if "No. of to-be-liked streams" not in self.stream_data.keys():
            nls = 0
        else:
            nls = self.stream_data["No. of to-be-liked streams"]
        ts = self.stream_data["Time Started"]
        te = self.stream_data["Time Ended"]
        d = self.date
        cst = self.check_streamers_time
        ver = self.version

        db = mysql.connector.connect(
            user=user,
            host=host,
            passwd=passwd,
            database=database
        )

        my_cursor = db.cursor()
        my_cursor.execute("""CREATE TABLE IF NOT EXISTS %s(NID INT PRIMARY KEY AUTO_INCREMENT, 
                                                            Time_Elapsed DECIMAL(6, 2), 
                                                            Num_active_streams SMALLINT UNSIGNED, 
                                                            Num_liked_streams SMALLINT UNSIGNED, 
                                                            Time_Started VARCHAR(10), 
                                                            Time_Ended VARCHAR(10), 
                                                            Streams_Liked SMALLINT UNSIGNED, 
                                                            Date VARCHAR(15),
                                                            prog_ver VARCHAR(10),
                                                            check_streamers_time DECIMAL(6, 2))""" % table_name)

        query = """INSERT INTO %s(Time_Elapsed, 
                                 Num_active_streams, 
                                 Num_liked_streams, 
                                 Time_Started, 
                                 Time_Ended, 
                                 Date,
                                 prog_ver,
                                 check_streamers_time) """ % table_name
        my_cursor.execute(query + "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (tel, nas, nls, ts, te, d, ver, cst))
        db.commit()

    def driver_quit(self):
        if self.like:
            self.driver.quit()

    def check_streams(self):
        print('Current Status: Checking for streams...')
        print('-' * 30)

        for name in self.channels.keys():
            self.threads.append(Thread(target=self.is_streaming, args=(name,)))

        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()

        print(self.status)
