from like_video import like_video, get_stream_link
from streamActivity import is_streaming
from collections import OrderedDict
import time
import csv

start_time = time.time()

# data for csv
data = OrderedDict()

# Time Started
ts = time.localtime()
time_started = time.strftime("%H:%M:%S", ts)
data['Time Started'] = time_started

# Stream data
number_of_active_streams = 0
number_of_to_be_liked_streams = 0
streams_liked = []

with open('channel ids.txt', 'r') as f:
    video_links = {}
    currently_streaming = {}

    print("Checking for streams...\n")

    for line in f.readlines():
        channel_id = line[:24]
        channel_link = 'https://www.youtube.com/channel/' + channel_id

        # check if streaming
        if is_streaming(channel_link):
            number_of_active_streams += 1
            channel_name = line[27:-1]
            currently_streaming[channel_name] = channel_link

    # Get the stream links and stream data
    video_links, number_of_to_be_liked_streams = get_stream_link(currently_streaming)

    for v in video_links.values():
        streams_liked.append(v)

    print()

    if video_links is None:
        print("XPath Exception: There seems to be a problem with your internet connection.")
        print("Troubleshoot your internet and restart the program.")
    elif video_links == {}:
        print("All streams on the channels you provided are already liked.")
    else:
        like_video(video_links)

te = time.localtime()
time_ended = time.strftime("%H:%M:%S", te)
data['Time Ended'] = time_ended

total_time = time.time() - start_time
data['Time elapsed'] = total_time
# with open('times.txt', 'a') as times:
#     times.write(str(total_time) + ' seconds\n')

data['No. of active streams'] = number_of_active_streams
data['No. of to-be-liked streams'] = number_of_to_be_liked_streams
data['Streams liked'] = ', '.join(streams_liked)

with open('stream_data.csv', 'a', newline='') as csv_file:
    fieldnames = ['Time elapsed', 'No. of active streams', 'No. of to-be-liked streams', 'Time Started', 'Time Ended',
                  'Streams liked']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writerow(data)

print(f"Time finished: {time_ended}")
print("Total time elapsed: %.2f seconds." % total_time)
