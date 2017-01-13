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

### Requirements \*nix

* Install ffmpeg from your Packet Manager
* Install Python3 from your Packet Manager
* Install livestreamer from your Packet Manager
* Download or Clone this Repo

### Requirements Windows

* Download and Install Python3 from [Python Downloadpage](https://www.python.org/downloads/release/python-360/)  
add Python3 to PATH during installation and disable Path-Limit
* Download ffmpeg from [ffmpeg Downloadpage](https://ffmpeg.zeranoe.com/builds/) as static linked Version  
Unpack the downloaded Archive and move Content to SysWoW64 and System32
* Download livestreamer from [livestreamer Downloadpage](http://docs.livestreamer.io/install.html#windows-binaries)  
Install and copy livestreamer.exe from Installation-Folder to SysWoW64 and System32
* Download wget from [Wget Downloadpage](https://eternallybored.org/misc/wget/)  
Unpack the downloaded Archive and move Content to SysWoW64 and System32
* Download or Clone this Repo

## How to use

### \*nix
Open Directory in Terminal
Execute the Shell Scripts:
* run_capturebaits.sh -> Recommended
* run_capturebaits_logging.sh -> if you want logging 
* run_capturebaits_verbose.sh -> if you want logged debug output to help me with fixing Issues

>*Exit via Ctrl + C*

### Windows
Either open Directory in CMD and execute python Capturebaits.py or
Execute the Shell Scripts:
* run_capturebaits.bat -> Recommended
* run_capturebaits_logging.bat -> if you want logging 
* run_capturebaits_verbose.bat -> if you want logged debug output to help me with fixing Issues

>*Exit via Ctrl + C*

### How CaptureBaits work

* If there is no "Whishlist" or  it's empty it will create whishlist.txt and exit
* It will search the Whishlist for Modelnames and parse a (if possible) valid URL to grab the Webpage-Source
* If the Model is offline it will start from the beginning, else it will extract the Playlist
* The Playlist is handed over to livestreamer, which will do the capturing
* Execute the *ts_to_mp4.sh/ts_to_mp4.bat* to simply copy the data from *.ts* to *.mp4*  
It seems that videoplayers can't handle *.ts* that good compared to *.mp4* 

>**Note:** *some streams are lagging, this might be either due to the Model(s)'s Bandwith or your Bandwith.  
This can mostly be reduced/fix by reencoding the .ts using a __real__ encoder.  
My recommendation would be __libx265__ or __nvenc_hvec__  
I've decided to use copy, so that even lower-end devices are able to handle those files properly*  

### ffmpeg-batch-creator.py
Small and handy script to create some batch/shell script files for batch encoding using nvenc-hvec(x265)  
**_Only use if you have a GTX 960 or better_**  
Just dump all the *.ts* files into one **folder** and run

##### \*nix
> find **path/to/folder** -maxdepth 1 -type f | tee list.txt

Let ffmpeg-batch-creator.py run through list.txt  
This will create a bunch of *.sh* files to encode the videos 

#### Windows
> dir **path\\to\\folder** /b /s /A-D /o:gn > list.txt  

Let ffmpeg-batch-creator.py run through list.txt  
This will create a bunch of *.bat* files to encode the videos

**Alternatively you can just change the encoding option from "-c:v copy" to "-c:v \*yourpreferedencoder\*",**  
**in the function get_stream()**
```python
with open(ffs_script, "a+", encoding="utf8") as ffs:
        ffs.write("\nffmpeg -i " + stream_file + " -strict -2 -c:v copy " + merged_file + "\n")
        ffs.write("chmod 666 " + merged_file + "\n")
```