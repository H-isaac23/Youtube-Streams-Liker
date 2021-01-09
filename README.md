# Youtube-stream-liker

This is a project using python which looks through a file with channel IDs and checks whether a stream from that channel is active or not. If there is a stream, the script will like the video with the email and password in the environment variables.

## How is it used?

There is a file named "channel ids.txt" and in that file, the first 24 characters are the channel IDs of the youtubers which regularly stream.
To add a channel to the text file, simply add the channel ID of the youtuber you want to track at the very bottom.
To start liking streams, simply run the python file and it will check the channels of each channel IDs in the text file, and then like the video stream if they are currently streaming.

## Libraries Used

-Selenium, requests, os, random, time

## Contribution

Any ideas related to a youtube video will be entertained and implemented in the code if decided. For the code, I will be doing it myself but others can suggest ideas as to how to do it.

## License


[MIT](https://choosealicense.com/licenses/mit/)
