from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from random import randint
from time import sleep
import os

def get_video_link(channel_url):
    PATH = 'C:/Program Files (x86)/geckodriver.exe'
    options = FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--mute-audio')
    driver = webdriver.Firefox(options=options, executable_path=PATH)
    video_link = None
    driver.get(channel_url+'/videos')

    try:
        video_url = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="thumbnail"]'))
        )
        video_link = video_url.get_attribute('href')
    except:
        driver.quit()

    driver.quit()
    return video_link

def like_video(video_url):

    option = FirefoxOptions()
    option.add_argument('--headless')
    option.add_argument('--mute-audio')
    PATH = 'C:/Program Files (x86)/geckodriver.exe'
    driver = webdriver.Firefox(options=option, executable_path=PATH)

    EMAIL = os.environ.get('TEST_EMAIL')
    PASSWORD = os.environ.get('TEST_PASS')

    driver.get('https://accounts.google.com/signin/v2/identifier?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2F&ec=GAZAAQ&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
    try:
        email = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]'))
        )
        sleep(randint(4,7))
        email.send_keys(EMAIL)
        email.send_keys(Keys.RETURN)
        print('Email Successfully Entered')
    except:
        print('There is a problem idk lmao, driver quitting')
        driver.quit()

    sleep(5)

    try:
        password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input"))
        )
        sleep(3)
        password.send_keys(PASSWORD)
        password.send_keys(Keys.RETURN)
        print('Password Successfully Entered')
    except:
        print("Password textbox not found")
        driver.quit()

    sleep(5)
    driver.get(video_url)

    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="top-level-buttons"]/ytd-toggle-button-renderer[1]/a'))
        )
        ActionChains(driver).move_to_element(button).click(button).perform()
        print('Video successfully liked')
        sleep(5)
    except:
        print('Xpath not found')
        driver.quit()

    driver.quit()

#like_video('https://www.youtube.com/watch?v=Tf3t9oVHrB4')
#is_liked('https://www.youtube.com/watch?v=Go2JRGbhlE0')
# print(get_video_link('https://www.youtube.com/channel/UC1opHUrw8rvnsadT-iGp7Cg'))