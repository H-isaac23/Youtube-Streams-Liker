from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def is_liked(video_url):
    PATH = 'C:/Program Files (x86)/geckodriver.exe'
    driver = webdriver.Firefox(executable_path=PATH)

    driver.get(video_url)

    try:
        like_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="button"]'))
        )
        print('XPATH found')
        val = like_button.get_attribute('aria-pressed')
        print(val)
    except:
        print('Attribute not found')
        driver.quit()

    driver.quit()

def get_link(channel_url):
    PATH = 'C:/Program Files (x86)/geckodriver.exe'
    driver = webdriver.Firefox(executable_path=PATH)

    driver.get(channel_url+'/videos')

    try:
        video_url = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="thumbnail"]'))
        )
        print(video_url.get_attribute('href'))
    except:
        driver.quit()

#is_liked('https://www.youtube.com/watch?v=Go2JRGbhlE0')
get_link('https://www.youtube.com/channel/UC1opHUrw8rvnsadT-iGp7Cg')