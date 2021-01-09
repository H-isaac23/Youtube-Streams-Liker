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

def get_stream_link(channel_urls):
    PATH = 'C:/Program Files (x86)/geckodriver.exe'
    options = FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--mute-audio')
    driver = webdriver.Firefox(options=options, executable_path=PATH)
    video_links = {}

    for name, channel_link in channel_urls.items():
        driver.get(channel_link+'/videos')

        try:
            video_url = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="thumbnail"]'))
            )
            link = video_url.get_attribute('href')

            with open('video links.txt', 'r') as link_read:
                if link in link_read.read():
                    print(f'Video from {name} is already liked.')
                elif link not in link_read.read():
                    with open('video links.txt', 'a') as link_write:
                        video_links[name] = link
                        link_write.write(link + '\n')
                        print(f'Video stream of {name} added to queue')

        except:
            print("XPATH not found")
            driver.quit()
            return None

    driver.quit()
    return video_links

def like_video(video_urls):

    print("Logging into google...\n")

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
    except:
        print('There is a problem in the email idk lmao, driver quitting')
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
    except:
        print("Password textbox not found")
        driver.quit()

    sleep(5)

    for name, link in video_urls.items():
        driver.get(link)
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="top-level-buttons"]/ytd-toggle-button-renderer[1]/a'))
            )
            ActionChains(driver).move_to_element(button).click(button).perform()
            print(f'Video from {name} successfully liked.')
            sleep(5)
        except:
            print('Xpath not found')
            driver.quit()

    driver.quit()