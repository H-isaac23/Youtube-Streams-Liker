from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from YSL import StreamLiker
from random import randint
import os
import time

class HoloAssist:
    def __init__(self):
        self.num_streams = None
        self.link = None

    def get_link_ids(self):

        email = os.environ.get('TEST_EMAIL')
        passwd = os.environ.get('TEST_PASS')
        sl = StreamLiker('channel ids.txt', email, passwd)
        sl.is_streaming()
        self.num_streams = sl.number_of_active_streams

        path = 'C:/Program Files (x86)/geckodriver.exe'
        options = FirefoxOptions()
        options.add_argument('--headless')
        options.add_argument('--mute-audio')
        driver = webdriver.Firefox(options=options, executable_path=path)
        links = []

        for name, channel_link in sl.currently_streaming.items():
            driver.get(channel_link + '/videos')

            try:
                video_url = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="thumbnail"]'))
                )
                link_id = video_url.get_attribute('href')[32:]

                links.append(link_id)

            except:
                print("XPATH not found")
                driver.quit()
                return None

        driver.quit()

        self.link = 'https://hololive.jetri.co/#/watch?videoId=' + ','.join(links)

    def open_holotools(self):
        print("Logging into google...\n")

        option = FirefoxOptions()
        option.add_argument('--mute-audio')
        path = 'C:/Program Files (x86)/geckodriver.exe'
        driver = webdriver.Firefox(options=option, executable_path=path)

        EMAIL = os.environ.get("TEST_EMAIL")
        PASSWORD = os.environ.get("TEST_PASS")

        driver.get(
            """https://accounts.google.com/signin/v2/identifier?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2F&ec=GAZAAQ&flowName=GlifWebSignIn&flowEntry=ServiceLogin""")
        try:
            email = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]'))
            )
            time.sleep(randint(4, 7))
            email.send_keys(EMAIL)
            email.send_keys(Keys.RETURN)
        except:
            print('There is a problem in the email idk lmao, driver quitting')
            driver.quit()

        time.sleep(5)

        try:
            password = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input"))
            )
            time.sleep(3)
            password.send_keys(PASSWORD)
            password.send_keys(Keys.RETURN)
        except:
            print("Password textbox not found")
            driver.quit()

        time.sleep(5)

        driver.get(self.link)
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div/main/div/div/div/div[3]/div[1]'))
        )
        driver.execute_script("localStorage.setItem('rulePauseOther', 0);")
        time.sleep(5)
        driver.refresh()
        time.sleep(10)

        for i in range(1, self.num_streams + 1):
            try:
                num = str(i)
                print(num, f'/html/body/div/main/div/div/div/div[3]/div[{num}]')
                elm = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f'/html/body/div/main/div/div/div/div[3]/div[{num}]'))
                )
                ActionChains(driver).move_to_element(elm).click(elm).perform()
                time.sleep(2)
            except:
                print("Yeah an error")

        time.sleep(5)
        driver.quit()

    def clear_data(self):
        self.num_streams = None
        self.link = None
