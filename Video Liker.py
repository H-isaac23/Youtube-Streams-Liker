from like_video import like_video
from streamActivity import streamUpdate

channelId = input("Channel Id:")

if streamUpdate(channelId):
    channelId = "https://www.youtube.com/channel/" + channelId + "/live"
    print(channelId)
    like_video(channelId)