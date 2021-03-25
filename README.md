# Youtube-stream-liker

YouTube Stream Liker (YSL) is a package developed for automated liking of Active YouTube streams by the channels provided by the user.

## Note(Project Status)
The project is now done with the main goal it aimed to reach.
It is now currently on the phase of creating a GUI, as I have been planning to turn this as a desktop application, although I may not have enough time to do it in the coming weeks because of school and other side projects that I want to do. As of now, the program is already complete based on what I had originally planned, though I might pick this up again in the future if I want to learn about GUIs.

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
Create an instance of the class StreamLiker, and pass in the text file for the channel ids of the channels you want checked, the email, and then the password of your youtube account.
And the configure the driver by passing the path for the driver and the options.(Driver options is optional)

Example:
``` python
from ysl.YSL import StreamLiker

email = 'email@test.com'
passwd = 'qwerty'
c_id = 'channels id.txt'

# Create an instance of the StreamLiker class 
sl = StreamLiker(c_id, email, passwd)

# Configure the driver.
sl.config_driver('C:/Program Files (x86)/geckodriver.exe')

# Example(with options): sl.config_driver('C:/Program Files (x86)/geckodriver.exe', ['--headless'])
```

### 3.
To start liking active streams, we first have to check if the channels that we supplied are currently streaming. To check, we can call the is_streaming() method.
Example:
``` python
sl.is_streaming()
```
This will store the channel ids of the currently streaming channels on a dictionary.

### 4.
Now that we have the video links, we will now like them using a selenium webdriver.
We first need to configure the selenium webdriver by passing in the path for the geckodriver.

Example:
``` python
# options = ['headless', '--mute-audio'], the "options" variable can be passed as the second argument.
sl.config_driver(path)
```

After configuring the driver, we can now start liking videos.
Simply call the like_videos method.

Example:
``` python
sl.like_videos()
```

And with that, the streams of the youtubers that you want to like can now be done automatically. 
Finally, the user should end the session of the driver.
``` python
sl.driver_quit()
```

Full Code:
```python
from ysl.YSL import StreamLiker

email = 'email@test.com'
passwd = 'qwerty'
c_id = 'channels id.txt'
sl = StreamLiker(c_id, email, passwd)

path = 'C:/Program Files (x86)/geckodriver.exe'
sl.is_streaming()
sl.config_driver(path)
sl.like_videos()
sl.driver_quit()
```
*Note*: In case the user wants to put the process into a for loop for multiple

### 5. (OPTIONAL)
For math nerds(I'm not one of them but I certainly will try to become one), there are additional methods that will let you use some data from the process of liking the video for the programmer to analyze.
The data that are collected by the methods above are the number of active streams and number of streams that you liked for a single execution of the program.

The additional methods that are within the program is get_start_time(),  get_end_time(), append_data_on_file(), and append_data_on_db().
*get_start_time* and *get_end_time* will, as their name says, get the starting time and the ending time of the liking process. The recommended placement of *get_start_time* is before the *get_channels* method, and the placement for the *get_end_time* is after the *like_videos* method.

Example:
```python
from ysl.YSL import StreamLiker

email = 'email@test.com'
passwd = 'qwerty'
c_id = 'channels id.txt'
sl = StreamLiker(c_id, email, passwd)

sl.get_start_time()
sl.is_streaming()
sl.config_driver('C:/Program Files (x86)/geckodriver.exe')
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

email = 'yt@test.com'
yt_passwd = 'fubukibestfriend'
user = 'root'
host = 'localhost'
db_passwd = 'baqua'
db = 'YSL'
table_name = 'stream_data'
my_dir = 'C:/Users/Stream data'

sl = StreamLiker('channel ids.txt', email, yt_passwd)
sl.get_start_time()
sl.is_streaming()
sl.config_driver('C:/Program Files (x86)/geckodriver.exe')
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
