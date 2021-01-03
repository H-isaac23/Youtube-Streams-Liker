import requests

#UCOyYb1c43VlX9rc_lT6NKQw
#UCvaTdHTWBGv3MKj3KVqJVCw
#UC1opHUrw8rvnsadT-iGp7Cg

def is_streaming(channel_id):
    channel_link = 'https://www.youtube.com/channel/' + channel_id
    response = requests.get(channel_link).text
    return '{"text":" watching"}' in response

# print(is_streaming('UC1opHUrw8rvnsadT-iGp7Cg'))
#https://www.youtube.com/channel/UC1opHUrw8rvnsadT-iGp7Cg

