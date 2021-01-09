from like_video import like_video, get_stream_link
from streamActivity import is_streaming
import time

start_time = time.time()

with open('channel ids.txt', 'r') as f:
    video_links = {}
    currently_streaming = {}

    print("Checking for streams...")

    for line in f.readlines():
        channel_id = line[:24]
        channel_link = 'https://www.youtube.com/channel/' + channel_id

        # check if streaming
        if is_streaming(channel_link):
            channel_name = line[27:-1]
            currently_streaming[channel_name] = channel_link

    # Get the stream links
    video_links = get_stream_link(currently_streaming)

    print()

    if video_links is None:
        print("XPath Exception: There seems to be a problem with your internet connection.")
        print("Troubleshoot your internet and restart the program.")
    elif video_links == {}:
        print("All streams on the channels you provided are already liked.")
    else:
        like_video(video_links)

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

total_time = time.time() - start_time
with open('times.txt', 'a') as times:
    times.write(str(total_time) + ' seconds\n')

print(f"Time finished: {current_time}")
print("Total time elapsed: %.2f seconds." % total_time)
