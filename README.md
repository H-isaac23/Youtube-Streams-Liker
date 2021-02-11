# Youtube-stream-liker

This is a project using python which looks through a file with channel IDs and checks whether a stream from that channel is active or not. If there is a stream, the script will like the video with the email and password in the environment variables.

## How is it used?
### 1. (Using the YSL.py File)
Create an instance of the class StreamLiker, and pass in the text file for the channel ids of the channels you want checked, the email, and then the password of your youtube account.
Example:
``` python
from YSL import StreamLiker

email = 'email@test.com'
passwd = 'qwerty'
c_id = 'channels id.txt'
sl = StreamLiker(c_id, email, passwd)
```

### 2.
To start liking active streams, we first have to check if the channels that we supplied are currently streaming. To check, we can call the is_streaming() method.
Example:
``` python
sl.is_streaming()
```
This will store the channel ids of the currently streaming channels on a dictionary.

### 3.
In order to like the stream, we first need to get the video links of the streams. This is when we call get_stream_links() method.
Example:
``` python
sl.get_stream_links()
```

This will also store the links in a dictionary.

### 4.
Now that we have the video links, we will now like them using a selenium webdriver. Simply call the method like_videos() to get started.
Example:
``` python
sl.like_videos()
```

And with that, the streams of the youtubers that you want to like can now be done automatically. 
The user can then tinker with the code, like putting the above block of code into a for loop so that the script will regularly check the provided channels whether they are streaming or not.

### 5. (OPTIONAL)
For math nerds(I'm not one of them but I certainly will try to become one), there are additional methods that will let you use some data from the process of liking the video for the programmer to analyze.
The data that are collected by the methods above are the number of active streams and number of streams that you liked for a single execution of the program.

The additional methods that are within the program is get_start_time(),  get_end_time(), append_data_on_file(), and append_data_on_db().
*get_start_time* and *get_end_time* will, as their name says, get the starting time and the ending time of the liking process. The recommended placement of *get_start_time* is before the *get_channels* method, and the placement for the *get_end_time* is after the *like_videos* method.

Example:
```python
from YSL import StreamLiker

email = 'email@test.com'
passwd = 'qwerty'
c_id = 'channels id.txt'
sl = StreamLiker(c_id, email, passwd)

sl.get_start_time()
sl.is_streaming()
sl.get_stream_links()
sl.like_videos()
sl.get_end_time()
```

*append_data_on_file* takes all the data collected by the program and then stores it in a csv file. (Note: A folder named "Stream data" must be created first in order for this method to work.)
Example:
``` python
sl.append_data_on_file()
```

*append_data_on_db* takes all the data collected by the program and then stores it in your local database through mysql.
The method needs the following arguments: user, host, password, database
As of the moment, the user of this program might have to configure the code inside the *append_data_on_db* method in order to select the table on which the user will append the data to.
```python
def append_data_on_db(self, user, host, passwd, database):
    tel = self.stream_data["Time elapsed"]
    nas = self.stream_data["No. of active streams"]
    nls = self.stream_data["No. of to-be-liked streams"]
    ts = self.stream_data["Time Started"]
    te = self.stream_data["Time Ended"]
    d = self.date

    db = mysql.connector.connect(
        user=user,
        host=host,
        passwd=passwd,
        database=database
    )

    my_cursor = db.cursor()
    my_cursor.execute("INSERT INTO [PUT TABLE NAME HERE](Time_Elapsed, Num_active_streams, Num_liked_streams, Time_Started, Time_Ended, Date) VALUES(%s,%s,%s,%s,%s,%s)",
                      (tel, nas, nls, ts, te, d))
    db.commit()
```

The user can then use the method normally.
Example:
```python
user = 'root'
host = 'localhost'
passwd = 'root'
database = 'YSL'
sl.append_data_on_db(user=user, host=host, passwd=passwd, database=database)
```

## Libraries Used

-Selenium, requests, os, random, time, collections

## Contribution

Any ideas related to a youtube video will be entertained and implemented in the code if decided. For the code, I will be doing it myself but others can suggest ideas on how to do it.

## License


[MIT](https://choosealicense.com/licenses/mit/)
