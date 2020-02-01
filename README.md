# CaptureBaits
A Toolset for capturing Livestreams containing Adult-Content from [*Chaturbate.com*](https://chaturbate.com/ "Let the Fappening begin")

## Age Restrictions

You should be at least 18 Years or your Country's corresponding Legal Age.  
If you are under the legal Age and you have come so far, you are most likely to click on every "**I'm 18 Years or older**"-Button, so who am I to stop you.  
\*You are doing something very bad!\* \(*Makes that annoying noise, that parents usually do*\)

## Why To Use

CaptureBaits was created for an Audience, which wishes to see their favorite Model(s)'s Show,  
but do not intend to wait several Minutes/Hours until something "intresting" might happen.  
![The real Stuff](http://img.memecdn.com/Watching-Porn_o_93399.jpg "Know  your Memes")  
It is solely ment for *private* purposes and for *private* archiving of Streams.  
For more Informations please read the LICENSE

## Requirements

* Download and Install Python3 from [Python Downloadpage](https://www.python.org/downloads/)  
[add Python3 to PATH during installation and disable Path-Limit (Windows only)]
* ```python -m pip install --user -r requirements.txt```
* ```python CaptureBaits.py```

### How CaptureBaits works

* If there is no "Whishlist" or  it's empty it will create whishlist.txt and exit
* It will search the Whishlist for Modelnames and parse a (if possible) valid URL to grab the Webpage-Source
* If the Model is offline it will start from the beginning, else it will extract the Playlist
* The Playlist is handed over to streamlink, which will do the capturing
* Happy Fappening

>**Note:** *some streams are lagging, this might be either due to the Model(s)'s Bandwith or your Bandwith.  
