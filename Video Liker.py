from like_video import like_video, get_stream_link
from streamActivity import is_streaming
import time

with open('channel ids.txt', 'r') as f:
    for line in f.readlines():
        channel_id = line[:24]
        channel_link = 'https://www.youtube.com/channel/' + channel_id

        # check if streaming
        if is_streaming(channel_link):
            channel_name = line[24:-1]
            print(channel_name)
            # Get the stream link
            video_link = get_stream_link(channel_link)

            # Open files
            link_read = open('video links.txt', 'r')
            link_write = open('video links.txt', 'a')

            if video_link in link_read.read():
                print(f'Video from {channel_name} is already liked.')
            else:
                like_video(video_link)
                link_write.write(video_link + '\n')

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

print(f"Time finished: {current_time}")

