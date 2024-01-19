# Youtube-stream-liker

A python script for automatically liking youtube videos.

## Supported Python Versions
-Python 3.7 is fully supported and tested. This library may work for earlier versions of Python3 and later versions, but I do not currently run tests on those versions.

## Third Party Libraries and Dependencies

The following libraries will be installed when you install the YSL library:
* [Selenium](https://selenium-python.readthedocs.io/)
* [Requests](https://requests.readthedocs.io/en/master/)
* [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/)

For development, you will also need the following installed:
* [Firefox](https://www.mozilla.org/en-US/firefox/new/)
* [Geckodriver](https://github.com/mozilla/geckodriver/releases)

## How is it used?

### Before making the code:
-Put the channel IDs and the channel name(or the owner's name, it's up to you) on a text file(a sample text file with the channel IDs is available above). The format of is "[Channel ID] - [Name]".(You have to do it that way, deal with it lmao)

Example:
```
UCdn5BQ06XqgXoAxIhbqw5Rg - Fubuki
UCQ0UDLQCjY0rmuxCDE38FGg - Matsuri
UCFTLzh12_nrtzqBPsTCqenA - Aki
UCD8HOxPs4Xvsm8H0ZxXGiBw - Mel
UC1CfXB_kRs3C-zaeTG3oGyg - Haato
```

### Note:
-You also need to login into Google using the regular firefox browser. Simply open firefox after installing, login to google, and just make sure you don't log out.

### 1. Installation
Install this library in a virtualenv using pip. [virtualenv](https://virtualenv.pypa.io/en/latest/) is a tool to create isolated Python environments. The basic problem it addresses is one of dependencies and versions, and indirectly permissions.

With virtualenv, it's possible to install this library without needing system install permissions, and without clashing with the installed system dependencies.
```
pip install virtualenv
virtualenv <your-env>
<your-env>\Scripts\activate
<your-env>\Scripts\pip.exe install YSL-H-isaac23
```

### 2. 
Create an instance of the class StreamLiker, and pass in the path for the text file for the channel ids of the channels you want to check for active streams.

Example:
``` python
from ysl.YSL import StreamLiker

c_id = 'C:/Users/isaac/channel_ids.txt'

# Create an instance of the StreamLiker class 
sl = StreamLiker(c_id)
```

### 3.
To start liking active streams, we first have to check if the channels that we supplied are currently streaming. To check, we can call the check_streams() method.

Example:
``` python
sl.check_streams()
```
This will store the channel ids of the currently streaming channels on a dictionary.

### 4.
Now that we have the video links, we will now like them using a selenium webdriver.
We first need to configure the selenium webdriver by passing in the path for the geckodriver.
And then pass in the firefox profile. ([This](https://www.howtogeek.com/255587/how-to-find-your-firefox-profile-folder-on-windows-mac-and-linux/#:%7E:text=The%20default%20locations%20are%3A,%2FFirefox%2FProfiles%2Fxxxxxxxx.) can help you find your profile location.)

Example:
``` python
options = ['--headless', '--mute-audio'] # the "options" variable can be passed as the second argument and is optional (No pun intended.)
firefox_profile = 'C:/Users/user/AppData/Roaming/Mozilla/Firefox/Profiles/xxxxxxxx.default-release'
sl.config_driver(path, firefox_profile, options)
```

The selenium webdriver can be configured so that the sound is muted.

Example:
``` python
firefox_profile = 'C:/Users/user/AppData/Roaming/Mozilla/Firefox/Profiles/xxxxxxxx.default-release'
sl.config_driver(path, firefox_profile, muted_sound=True)
```

In case the programmer wants to add more modifications to the selenium webdriver, you can do so by accessing the driver object at *self.driver*

After configuring the driver, we can now start liking videos.
Simply call the like_videos method.

Example:
``` python
sl.like_videos()
```

And with that, the streams of the youtubers that you want to like will now be done automatically. 
Finally, the user should end the session of the driver.
``` python
sl.driver_quit()
```

Full Code:
```python
from ysl.YSL import StreamLiker

c_id = 'C:/Users/isaac/channel_ids.txt'
sl = StreamLiker(c_id)

path = 'C:/Program Files (x86)/geckodriver.exe'
firefox_profile = 'C:/Users/user/AppData/Roaming/Mozilla/Firefox/Profiles/xxxxxxxx.default-release'
sl.check_streams()
sl.config_driver(path, firefox_profile)
sl.like_videos()
sl.driver_quit()
```

### 5. (OPTIONAL)
For math nerds(I'm not one of them but I certainly will try to become one), there are additional methods that will let you use some data from the process of liking the video for the programmer to analyze.
The data that are collected by the methods above are the number of active streams and number of streams that you liked for a single execution of the program.

The additional methods that are within the program is get_start_time(),  get_end_time(), append_data_on_file(), and append_data_on_db().
*get_start_time* and *get_end_time* will, as their name says, get the starting time and the ending time of the liking process. The recommended placement of *get_start_time* is before the *get_channels* method, and the placement for the *get_end_time* is after the *like_videos* method.

Example:
```python
from ysl.YSL import StreamLiker

c_id = 'C:/Users/isaac/channel_ids.txt'
sl = StreamLiker(c_id)

path = 'C:/Program Files (x86)/geckodriver.exe'
firefox_profile = 'C:/Users/user/AppData/Roaming/Mozilla/Firefox/Profiles/xxxxxxxx.default-release'

sl.get_start_time()
sl.check_streams()
sl.config_driver(path, firefox_profile)
sl.like_videos()
sl.get_end_time()
sl.driver_quit()
```

*append_data_on_file* takes all the data collected by the program and then stores it in a csv file. 
Put the directory in which you would want your files to be saved to as an argument.

Note: Use forward slashes.

Example:
``` python
sl.append_data_on_file("C:/Users/Stream data")
```

*append_data_on_db* takes all the data collected by the program and then stores it in your local database through mysql.
The method needs the following arguments: user, host, password, database, table_name

Example:
``` python
user = 'root'
host = 'localhost'
passwd = 'root'
database = 'YSL'
table_name = 'stream_data'
sl.append_data_on_db(user=user, host=host, passwd=passwd, database=database, table_name=table_name)
```

### Full Code

```python
from ysl.YSL import StreamLiker

user = 'root'
host = 'localhost'
db_passwd = 'baqua'
db = 'YSL'
table_name = 'stream_data'
my_dir = 'C:/Users/Stream data'
path = 'C:/Program Files (x86)/geckodriver.exe'
firefox_profile = 'C:/Users/user/AppData/Roaming/Mozilla/Firefox/Profiles/xxxxxxxx.default-release'

sl = StreamLiker('C:/Users/user/channel_ids.txt')
sl.get_start_time()
sl.check_streams()
sl.config_driver(path, firefox_profile)
sl.like_videos()
sl.get_end_time()
sl.append_data_on_file(my_dir)
sl.append_data_on_db(user, host, db_passwd, db, table_name)
sl.driver_quit()
```

## Contribution

Any ideas related to a youtube video will be entertained and implemented in the code if decided, just put the ideas on an issue. For the code, I will be doing it myself but others can suggest ideas on how to do it.
Others can also suggest ideas on how a certain part of the code can be done a lot more efficient, put those also on the issues tab.

## License

[MIT](https://choosealicense.com/licenses/mit/)
