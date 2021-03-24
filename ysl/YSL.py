from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from collections import OrderedDict
from random import randint
from datetime import date
import mysql.connector
import csv
import requests
import os
import time


class YSL:
    def __init__(self, channels_path):
        self.channels_path = channels_path
        self.status_codes = {1: "Checking for streams...", 2: "Logging into YouTube..."}
        self.channels = {}
        self.get_channels()

    def get_channels(self):
        with open(self.channels_path, 'r') as channels:
            for channel in channels.readlines():
                channel_id = channel[:24]
                channel_name = channel[27:-1]
                self.channels[channel_name] = channel_id


class StreamLiker(YSL):
    def __init__(self, channels_path, email, passwd):
        super(StreamLiker, self).__init__(channels_path)
        self.start_time = None
        self.time_started = None
        self.total_time_elapsed = 0
        self.time_ended = None

        self.active_streams = []
        self.currently_streaming = {}
        self.streams_liked = {}
        self.streams_liked_id = []
        self.video_ids = []
        self.stream_data = OrderedDict()
        self.number_of_active_streams = 0
        self.number_of_to_be_liked_streams = 0
        self.date = None

        self.email = email
        self.passwd = passwd

        self.driver = None
        self.options = FirefoxOptions()

        self.version = "1.5"

    def clear_data(self):
        self.start_time = None
        self.time_started = None
        self.total_time_elapsed = 0
        self.time_ended = None

        self.currently_streaming = {}
        self.streams_liked = {}
        self.streams_liked_id = []
        self.video_ids = []
        self.stream_data = OrderedDict()
        self.number_of_active_streams = 0
        self.number_of_to_be_liked_streams = 0
        self.date = None

    def get_start_time(self):
        self.start_time = time.time()
        self.time_started = time.strftime("%H:%M:%S", time.localtime())
        self.stream_data['Time Started'] = self.time_started

    def is_streaming(self):

        ##### Status Code
        print('Checking for streams...')
        print()

        for name in self.channels.keys():
            print(name, end=" - ")
            channel_url = 'https://www.youtube.com/channel/' + self.channels[name]
            response = requests.get(channel_url).text
            stream_active = '{"text":" watching"}' in response
            print("is ", end="")
            if stream_active:
                self.currently_streaming[name] = channel_url
                self.number_of_active_streams += 1
                print("currently streaming.")
            else:
                print("not streaming.")

        self.stream_data['No. of active streams'] = self.number_of_active_streams
        print()

    def like_videos(self):

        if self.number_of_active_streams == 0:
            print("There are no active streams as of the moment.")
        elif self.number_of_active_streams > 0:

            # print("Logging into google...\n")
            #
            # EMAIL = self.email
            # PASSWORD = self.passwd
            #
            # self.driver.get(
            #     """https://accounts.google.com/signin/v2/identifier?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2F&ec=GAZAAQ&flowName=GlifWebSignIn&flowEntry=ServiceLogin""")
            # try:
            #     email = WebDriverWait(self.driver, 10).until(
            #         EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]'))
            #     )
            #     time.sleep(randint(4, 7))
            #     email.send_keys(EMAIL)
            #     email.send_keys(Keys.RETURN)
            # except:
            #     self.driver_quit()
            #     assert False, "GoogleEmailError: Cannot find XPATH."
            #
            # time.sleep(5)
            #
            # try:
            #     password = WebDriverWait(self.driver, 10).until(
            #         EC.presence_of_element_located(
            #             (By.XPATH,
            #              "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input"))
            #     )
            #     time.sleep(3)
            #     password.send_keys(PASSWORD)
            #     password.send_keys(Keys.RETURN)
            # except:
            #     self.driver_quit()
            #     assert False, "GooglePasswordError: Cannot find XPATH."
            #
            # time.sleep(5)

            for name, channel_link in self.currently_streaming.items():
                is_liked = False
                like_button = None
                link = None
                self.driver.get(channel_link + '/videos')

                try:
                    video_url = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="thumbnail"]'))
                    )
                    link = video_url.get_attribute('href')
                except:
                    assert False, "LinkFetchError: Cannot find XPATH."

                self.active_streams.append(link[32:])
                self.driver.get(link)

                try:
                    like_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    '//*[@id="top-level-buttons"]/ytd-toggle-button-renderer[1]/a/yt-icon-button/button'))
                    )
                    if like_button.get_attribute("aria-pressed") == "true":
                        is_liked = True
                        print(f"Video from {name} is already liked.")

                except:
                    self.driver_quit()
                    assert False, "LikeButtonError: Cannot find XPATH."

                if not is_liked:
                    self.video_ids.append(link[32:])
                    self.number_of_to_be_liked_streams += 1
                    ActionChains(self.driver).move_to_element(like_button).click(like_button).perform()
                    print(f"Video from {name} is liked.")

            self.stream_data['No. of to-be-liked streams'] = self.number_of_to_be_liked_streams
            self.stream_data['Streams liked'] = ', '.join(self.video_ids)

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
                              'Time Ended',
                              'Streams liked']
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                csv_writer.writeheader()

        with open(my_dir + f'/{filename}', 'a', newline='') as csv_file:
            fieldnames = ['Time elapsed', 'No. of active streams', 'No. of to-be-liked streams', 'Time Started',
                          'Time Ended',
                          'Streams liked']
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
                                                                    prog_ver VARCHAR(10))""" % table_name)

        query = """INSERT INTO %s(Time_Elapsed, 
                                 Num_active_streams, 
                                 Num_liked_streams, 
                                 Time_Started, 
                                 Time_Ended, 
                                 Date,
                                 prog_ver) """ % table_name
        my_cursor.execute(query + "VALUES(%s,%s,%s,%s,%s,%s,%s)", (tel, nas, nls, ts, te, d, ver))
        db.commit()

    def start_liking_with_data(self, user, host, passwd, db, table_name, my_dir, path, options = None):
        self.get_start_time()
        self.is_streaming()
        self.config_driver(path, options)
        self.like_videos()
        self.get_end_time()
        self.append_data_on_file(my_dir)
        self.append_data_on_db(user, host, passwd, db, table_name)

    def config_driver(self, path, args=None):
        try:
            for arg in args:
                self.options.add_argument(arg)
        except:
            print("No args supplied for driver options.")

        profile = webdriver.FirefoxProfile(
            'C:/Users/ISAAC/AppData/Roaming/Mozilla/Firefox/Profiles/fwnbfuph.default-release'
        )
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        profile.update_preferences()
        desired = DesiredCapabilities.FIREFOX

        self.driver = webdriver.Firefox(
            options=self.options,
            executable_path=path,
            firefox_profile=profile,
            desired_capabilities=desired
        )

    def driver_quit(self):
        self.driver.quit()
