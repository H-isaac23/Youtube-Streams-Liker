from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def streamUpdate(channelId):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--profile-directory=Default')

    PATH = 'C:\Program Files (x86)\chromedriver.exe'
    driver = webdriver.Chrome(options=options, executable_path=PATH)
    streamSign = '{"text":" watching"}'

    driver.get("https://www.youtube.com/channel/{0}".format(channelId))

    html = driver.page_source
    if streamSign in html:
        return True
    else:
        return False