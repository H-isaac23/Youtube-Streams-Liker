import requests

#UCOyYb1c43VlX9rc_lT6NKQw
#UCvaTdHTWBGv3MKj3KVqJVCw

def is_streaming(channel_id):
    channel_link = 'https://www.youtube.com/channel/' + channel_id
    response = requests.get(channel_link)

    #soup = BeautifulSoup(response, 'lxml')

    return '{"text":" watching"}' in response.text

print(is_streaming('UCvaTdHTWBGv3MKj3KVqJVCw'))

