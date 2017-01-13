import sys 
import os
import operator
import threading
import multiprocessing
import time
import datetime
import shutil
import subprocess

modellist = []
start_time = str(datetime.datetime.now().month) + "_" + str(datetime.datetime.now().day) + "_" + str(datetime.datetime.now().year)

allsorter_code = """import os

def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))

stream = os.getcwd() + "/Stream/"
deeks = sorted_ls(stream)

with open("playlist2.txt", "w") as p:
    for x in deeks:
        p.write("file \\'" + stream + x + "\\'\\n")"""

efr_code = """import os

with open("playlist.txt", "w") as e:
    with open("playlist2.txt", "r") as p:
        for line in p:
            line = line.split("file '")[1]
            line = line.split("'")[0]
            print(line)
            if os.path.getsize(line) > 10000:
                e.write("file \\'" + line + "\\'\\n")"""

wgetrc_code = """header = Accept-Language: en-us,en;q=0.5
header = Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
header = Connection: keep-alive
user_agent = Mozilla/5.0 (X11; Grabdora; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0
referer = /
robots = off"""

def create_wgetrc():
    wgetrc = "~/.wgetrc"
    if not os.path.exists(wgetrc):
        with open(wgetrc, "a+") as w:
            w.write(wgetrc_code)
        os.chmod(wgetrc, 0o666)
        print("Created a custom .wgetrc file to improve download performance.")
        exit(0)
    return

def create_wishlist():
    cwd = os.getcwd()
    os.chdir(cwd)
    wishlist_file = cwd + "/wishlist.txt"
    if not os.path.exists(wishlist_file):
        open(wishlist_file, "a+").close()
        os.chmod(wishlist_file, 0o666)
        print("Please enter the Modelnames of the Models you would like to capture.")
        print("Will now exit!")
        exit(0)
    return

def print_modellist():
    for x in modellist:
        print(str(x))

def names_from_wishlist():
    print("Starting Process")
    cwd = os.getcwd()
    os.chdir(cwd)
    captures = cwd + "/Captures/"
    if not os.path.exists(captures):
        print("Creating Capture Directory")
        os.mkdir(captures)
        os.chmod(captures, 0o775)
    with open("wishlist.txt", 'r') as wl:
        print("Creating Sub-Directorys for each Model")
        for line in wl:
            line = line.replace('\n', '')
            modeldir = captures + line
            if not os.path.exists(modeldir):
                os.mkdir(modeldir)
                os.chmod(modeldir, 0o775)
            f = modeldir + "/" + start_time + "/"
            if not os.path.exists(f):
                print("Creating Current Capture Directory")
                os.mkdir(f)
                os.chmod(captures, 0o775)
            if str(line) not in modellist:
                modellist.append(str(line))
                playlist_dir = f + "Playlist/"
                if not os.path.exists(playlist_dir):
                    os.mkdir(playlist_dir)
                stream_dir = f + "Stream/"
                if not os.path.exists(stream_dir):
                    os.mkdir(stream_dir)
                chunklist_dir = f + "Chunklists/"
                if not os.path.exists(chunklist_dir):
                    os.mkdir(chunklist_dir)
                master_playlist_file = f + "playlist.txt"
                open(master_playlist_file, "a+").close()
                os.chmod(master_playlist_file, 0o666)
                ffs_script = f + "merge.sh"
                merged_file = f + str(line) + "-" + start_time + ".mp4"
                if not os.path.isfile(ffs_script):
                    with open(ffs_script, "w+") as ffs:
                        ffs.write("ffmpeg -f concat -safe 0 -i playlist.txt -strict -2 -c:v copy " + merged_file + "\n")
                        ffs.write("chmod 666 " + merged_file)
                    os.chmod(ffs_script, 0o777)
                
                allsorter = f + "allfilesorter.py"
                if not os.path.isfile(allsorter):
                    with open(allsorter, "w") as a:
                        a.write(allsorter_code)
                efr = f + "emptyfileremover.py"
                if not os.path.isfile(efr):
                    with open(efr, "w") as e:
                        e.write(efr_code)

                print("Creating Worker-Process for " + str(line))
                time.sleep(2)
                worker = threading.Thread(target=retrieve_source, name=str(line), args=(str(line), str(line), str(f)), daemon=True)
                worker.start()

def get_source(out_file, url, modelname):
    print("Retrieving the Sourcefile for " + str(modelname))
    if not os.path.isfile(out_file):
        subprocess.check_call(["wget", "-t", "5", "-q", "-O", out_file, url])
        os.chmod(out_file, 0o666)
    print(modelname + ": Verifying Integrity")
    if os.path.getsize(out_file) < 10000:
        print(modelname + ": removin 0 byte Source and retrying!")
        subprocess.check_call(["rm", out_file])
        get_source(out_file, url, modelname)
        return
    else:
        time.sleep(1)
        return

def retrieve_source(own_name, modelname, directory):
    modelpage = "https://en.chaturbate.com/" + modelname + "/"
    src_file = str(directory) + str(modelname) + "_src"
    print(str(own_name) + ": Creating Thread")
    getter = threading.Thread(target=get_source, args=(str(src_file), str(modelpage), str(modelname)), daemon=False)
    getter.start()
    while getter.is_alive() == True:
        print(str(own_name) + ": Thread is still alive")
        time.sleep(1)
    print(str(own_name) + ": Saved the Sourcefile for " + str(modelname))
    print(str(own_name) + ": " + str(src_file))
    playlist_from_source(src_file, directory, modelname, own_name)

def playlist_from_source(src_file, directory, model, own_name):
    print(str(own_name) + ": Searching for Playlist")
    found = "pending"
    with open(src_file, 'r') as src:
        print(str(own_name) + ": Source has been opened")
        for line in src:
            if ".m3u8" in line and found != True:
                print(str(own_name) + ": Found the Playlist!")
                found = True
                substring = str(line).split("https://")[1]
                substring = substring.split(".m3u8")[0]
                playlist = "https://" + str(substring) + ".m3u8"
                print(str("Playlist:------------>\t" + own_name) + ": " + str(playlist))
                base_url = playlist.split("playlist.m3u8")[0]
                retrive_playlist(own_name, directory, playlist, base_url)
                return
            found = False
    if found == False:
        print(str(own_name) + ": Playlist not found in Sourcefile")
        print(str(own_name) + ": Seems like \"" + model + "\" is offline.")
        if os.path.isfile(src_file):
            subprocess.check_call(["rm", src_file])
        modellist.remove(model)
        print_modellist()
        return

def get_playlist(url, out_file, modelname):
    print("Retrieving the Playlist for " + str(modelname))
    if not os.path.isfile(out_file):
        subprocess.check_call(["wget", "-t", "5", "-q", "-O", out_file, url])
        os.chmod(out_file, 0o666)
    print(modelname + ": Verifying Integrity")
    if os.path.getsize(out_file) < 50:
        print(modelname + ": removin 0 byte Playlist and retrying!")
        subprocess.check_call(["rm", out_file])
        get_playlist(url, out_file, modelname)
        return
    else:
        time.sleep(1)
        return

def retrive_playlist(own_name, directory, playlist_url, base_url):
    time_now = str(datetime.datetime.now().hour) + "-" + str(datetime.datetime.now().minute)
    playlist_file = str(directory) + "Playlist/" + str(own_name) + "_playlist_" + time_now + ".m3u8"
    print(str(own_name) + ": Creating Thread to grab Playlist")
    player = threading.Thread(target=get_playlist, args=(str(playlist_url), str(playlist_file), str(own_name)), daemon=False)
    player.start()
    while player.is_alive() == True:
        print(str(own_name) + ": Thread is still alive")
        time.sleep(1)
    print(str(own_name) + ": Saved the Playlist for " + str(own_name))
    print(str(own_name) + ": " + str(playlist_file))
    chunklist_from_playlist(own_name, directory, playlist_file, base_url)

def get_chunklist(url, out_file, modelname):
    print("Retrieving Chunklist for " + str(modelname))
    if not os.path.isfile(out_file):
        subprocess.check_call(["wget", "-t", "5", "-q", "-O", out_file, url])
        os.chmod(out_file, 0o666)
    print(modelname + ": Verifying Integrity")
    if os.path.getsize(out_file) < 50:
        print(modelname + ": removin 0 byte Chunklist and retrying!")
        subprocess.check_call(["rm", out_file])
        get_chunklist(url, out_file, modelname)
        return
    else:
        time.sleep(1)
        return

def chunklist_from_playlist(own_name, directory, playlist_file, base_url):
    chunklist_dir = str(directory) + "Chunklists/"
    print(str(own_name) + ": Searching for Chunklist")
    found = "pending"
    with open(playlist_file, 'r') as pl:
        print(str(own_name) + ": Playlist has been opened")
        for line in pl:
            if ".m3u8" in line and found != True:
                line = line.replace('\n', '')
                print(str(own_name) + ": Found the Chunklist!")
                found = True
                print(str(str(own_name) + ": Chunks:------------>\t" + own_name) + ": " + str(line))
                chunklist_file = str(chunklist_dir) + str(line)
                if not os.path.isfile(chunklist_file):
                    chunklist_url = str(base_url) + str(line)
                    chunker = threading.Thread(target=get_chunklist, args=(str(chunklist_url), str(chunklist_file), str(own_name)), daemon=False)
                    chunker.start()
                    while chunker.is_alive() == True:
                        print(str(own_name) + ": Thread is still alive")
                        time.sleep(1)
                    stream_from_chunklist(own_name, chunklist_file, directory, base_url, playlist_file)
                else:
                    print(str(own_name) + ": Sleeping 15 Seconds to wait for new Chunklist")
                    time.sleep(15)
                    playlist_url = base_url + "playlist.m3u8"
                    retrive_playlist(own_name, directory, playlist_url, base_url)
                return
        found = False
    if found == False:
        print(str(own_name) + ": Chunklist not found in Playlist")
        print(str(own_name) + ": something went wrong")
        modellist.remove(own_name)
        return

def get_streamchunk(url, out_file, modelname, mf):
    print("Retrieving Streamchunk for " + str(modelname))
    if not os.path.isfile(out_file):
        subprocess.check_call(["wget", "-t", "5", "-q", "-O", out_file, url])
        os.chmod(out_file, 0o666)
    print(modelname + ": Verifying Integrity")
    if os.path.getsize(out_file)  < 100000:
        print(modelname + ": removin 0 byte Streamfile and retrying!")
        subprocess.check_call(["rm", out_file])
        get_streamchunk(url, out_file, modelname, mf)
        return
    else:
        mf.write("file \'" + str(out_file) + "\'\n")
        print(str(modelname) + ": Just downloaded a Streamchunk")
        return

def stream_from_chunklist(own_name, chunklist_file, directory, base_url, playlist_file):
    print(str(own_name) + ": Searching for Streamchunks")
    master_playlist_file = directory + "playlist.txt"
    with open(master_playlist_file, 'a') as mf:
        with open(chunklist_file, 'r') as cl:
            print(str(own_name) + ": Chunklist has been opened")
            for line in cl:
                if ".ts" in line:
                    line = line.replace('\n', '')
                    print(str(own_name) + ": Found a Streamchunk!")
                    stream_url = str(base_url) + str(line)
                    stream_file = directory + "Stream/" +  str(line)
                    streamer = threading.Thread(target=get_streamchunk, args=(str(stream_url), str(stream_file), str(own_name), mf), daemon=False)
                    streamer.start()
                    while streamer.is_alive() == True:
                           print(str(own_name) + ": Thread is still alive")
                           time.sleep(1)
    print(str(own_name) + ": Sleeping 15 Seconds to wait for new Chunklist")
    time.sleep(15)
    playlist_url = base_url + "playlist.m3u8"
    retrive_playlist(own_name, directory, playlist_url, base_url)

def main():
    os.umask(0)
    create_wgetrc()
    create_wishlist()
    names_from_wishlist()
    while True:
        names_from_wishlist()
        print("Currently following Models are being baited:")
        print_modellist()
        time.sleep(60)

main()
