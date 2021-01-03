from like_video import like_video, get_video_link
from streamActivity import is_streaming

channelId = input("Channel Id:")
channel_link = 'https://www.youtube.com/channel/' + channelId

if is_streaming(channelId):
    video_link = get_video_link(channel_link)
    like_video(video_link)