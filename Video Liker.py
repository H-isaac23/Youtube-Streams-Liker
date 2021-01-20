from like_video import like_video, get_stream_link, is_streaming
from collections import OrderedDict
from datetime import date
import os
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
video_ids = []

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

# Gets the video ids
for link in streams_liked:
    video_ids.append(link[32:])

# Time when the program ended
te = time.localtime()
time_ended = time.strftime("%H:%M:%S", te)
data['Time Ended'] = time_ended

# Total time elapsed
total_time = time.time() - start_time
data['Time elapsed'] = total_time

# Stream datas
data['No. of active streams'] = number_of_active_streams
data['No. of to-be-liked streams'] = number_of_to_be_liked_streams
data['Streams liked'] = ', '.join(video_ids)

# File naming
today = date.today()
d = today.strftime("%m/%d/%y")
hyphenated_date = '-'.join(d.split('/'))
filename = f'stream_data {hyphenated_date}.csv'

# Check if a file exists
if not os.path.exists(filename):
    with open(filename, 'a', newline='') as csv_file:
        fieldnames = ['Time elapsed', 'No. of active streams', 'No. of to-be-liked streams', 'Time Started',
                      'Time Ended',
                      'Streams liked']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

with open(filename, 'a', newline='') as csv_file:
    fieldnames = ['Time elapsed', 'No. of active streams', 'No. of to-be-liked streams', 'Time Started', 'Time Ended',
                  'Streams liked']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writerow(data)

print(f"Time finished: {time_ended}")
print("Total time elapsed: %.2f seconds." % total_time)

'''
To Do:
Make the program send the csv files on an email
Modify the program to make xlsx files instead of csv files
'''
