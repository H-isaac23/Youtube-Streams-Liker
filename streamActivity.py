import requests

def is_streaming(channel_url):
    response = requests.get(channel_url).text
    return '{"text":" watching"}' in response


