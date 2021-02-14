# Youtube-stream-liker

This is a project using python which looks through a file with channel IDs and checks whether a stream from that channel is active or not. If there is a stream, the script will like the video with the email and password provided by the user.

## Note(Project Status)
The project is now currently on the phase of creating a GUI, although I may not have enough time to do it in the coming weeks because of school and other side projects that I want to do. As of now, the program is already complete based on what I had originally planned, though I might pick this up again in the future if I want to learn about GUIs.

## Libraries Used

-Selenium, requests, os, random, time, collections, mysql-connector-python

## How is it used?

### Before making the code:
Copy the YSL.py file into your repository.

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
# Legend: ******* - put table name here

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
    my_cursor.execute("""CREATE TABLE IF NOT EXISTS *******(NID INT PRIMARY KEY AUTO_INCREMENT, 
                                                            Time_Elapsed DECIMAL(6, 2), 
                                                            Num_active_streams SMALLINT UNSIGNED, 
                                                            Num_liked_streams SMALLINT UNSIGNED, 
                                                            Time_Started VARCHAR(10), 
                                                            Time_Ended VARCHAR(10), 
                                                            Streams_Liked SMALLINT UNSIGNED, 
                                                            Date VARCHAR(15))""")

    my_cursor.execute("""INSERT INTO *******(Time_Elapsed, 
                                             Num_active_streams, 
                                             Num_liked_streams, 
                                             Time_Started, 
                                             Time_Ended, 
                                             Date) 
                                             VALUES(%s,%s,%s,%s,%s,%s)""",
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

### start_liking_with_data(self, user, host, passwd, db)
This method combines all of the mentioned methods above into a single function in order to shorten the needed lines of code to perform all of them.
```python
def start_liking_with_data(self, user, host, passwd, db):
    self.get_start_time()
    self.is_streaming()
    self.get_stream_links()
    self.like_videos()
    self.get_end_time()
    self.append_data_on_file()
    self.append_data_on_db(user, host, passwd, db)
```
The user then needs to pass the needed arguments if the user wants to append the data onto their own database.
Example:
```python
from YSL import StreamLiker

email = 'yt@test.com'
yt_passwd = 'fubukibestfriend'
user = 'root'
host = 'localhost'
db_passwd = 'baqua'
db = 'YSL'

sl = StreamLiker('channel ids.txt', email, yt_passwd)
sl.start_liking_with_data(user, host, db_passwd, db)
```

## Contribution

Any ideas related to a youtube video will be entertained and implemented in the code if decided, just put the ideas on an issue. For the code, I will be doing it myself but others can suggest ideas on how to do it.
Others can also suggest ideas on how a certain part of the code can be done a lot more efficient, put those also on the issues tab.

## License


[MIT](https://choosealicense.com/licenses/mit/)
