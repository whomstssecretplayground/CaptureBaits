import os
import threading
import time
import datetime
import subprocess

start_date = str(datetime.datetime.now().month) + "_" + str(datetime.datetime.now().day) + "_" + str(datetime.datetime.now().year)
cwd = os.getcwd()
modellist = []

def print_modellist():
    print("\n\n\n----------------------------Modellist--------------------------")
    for x in modellist:
        print(str(x))
    print("----------------------------Modellist--------------------------\n\n")

def create_wishlist():
    os.chdir(cwd)
    wishlist_file = cwd + "\\wishlist.txt"
    if not os.path.exists(wishlist_file) or os.stat(wishlist_file).st_size == 0:
        open(wishlist_file, "a+").close()
        os.chmod(wishlist_file, 0o666)
        print("Please enter the Modelnames of the Models you would like to capture.")
        print("Will now exit!")
        time.sleep(5)
        exit(0)
    return

def create_baitlist():
    os.chdir(cwd)
    baitlist_file = cwd + "\\baitlist.txt"
    with open(baitlist_file, "a+", encoding="utf8") as bl:
        bl.write("Current Baits from " + start_date + ":\n")
    os.chmod(baitlist_file, 0o666)
    return

def names_from_wishlist():
    print("Starting Process")
    os.chdir(cwd)
    captures = cwd + "\\Captures\\"
    if not os.path.exists(captures):
        print("Creating Capture Directory")
        os.mkdir(captures)
        os.chmod(captures, 0o775)
    with open("wishlist.txt", "r", encoding="utf8") as wl:
        print("Creating Sub-Directorys for each Model")
        for line in wl:
            if not line.startswith("#") and not line == "\n":
                line = line.replace('\n', '')
                modeldir = captures + line
                if not os.path.exists(modeldir):
                    os.mkdir(modeldir)
                    os.chmod(modeldir, 0o775)
                f = modeldir + "\\" + start_date + "\\"
                if not os.path.exists(f):
                    print("Creating Current Capture Directory")
                    os.mkdir(f)
                    os.chmod(captures, 0o775)
                if str(line) not in modellist:
                    print("Creating Worker-Process for " + str(line))
                    time.sleep(2)
                    worker = threading.Thread(target=retrieve_source, name=str(line), args=(str(line), str(line), str(f)), daemon=True)
                    worker.start()

def get_source(out_file, url, modelname):
    print("Retrieving the Sourcefile for " + str(modelname))
    if not os.path.isfile(out_file):
        subprocess.check_call(["cmd", "/c", "wget", "-t", "5", "-q", "-O", out_file, url])
        os.chmod(out_file, 0o666)
    print(modelname + ": Verifying Integrity")
    if os.path.getsize(out_file) < 10000:
        print(modelname + ": removin 0 byte Source and retrying!")
        subprocess.check_call(["cmd", "/c", "del", out_file])
        get_source(out_file, url, modelname)
        return
    else:
        time.sleep(1)
        return

def retrieve_source(own_name, modelname, directory):
    start_time = "_" + str(datetime.datetime.now().hour) + "-" + str(datetime.datetime.now().minute)  
    modelpage = "https://en.chaturbate.com/" + modelname + "/"
    src_file = str(directory) + str(modelname) + start_time + ".txt"
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
    with open(src_file, "r", encoding="utf8") as src:
        print(str(own_name) + ": Source has been opened")
        for line in src:
            if ".m3u8" in line and found != True:
                print(str(own_name) + ": Found the Playlist!")
                found = True
                start_time = "_" + str(datetime.datetime.now().hour) + "-" + str(datetime.datetime.now().minute)
                substring = str(line).split("https://")[1]
                substring = substring.split(".m3u8")[0]
                playlist = "https://" + str(substring) + start_time + ".m3u8"
                get_stream(playlist, directory, own_name)
                return
            found = False
    if found == False:
        print(str(own_name) + ": Playlist not found in Sourcefile")
        print(str(own_name) + ": Seems like \"" + model + "\" is offline.")
        if os.path.isfile(src_file):
            subprocess.check_call(["cmd", "/c", "del", src_file])
        return

def get_stream(playlist, directory, own_name):
    modellist.append(str(own_name))
    start_time = "_" + str(datetime.datetime.now().hour) + "-" + str(datetime.datetime.now().minute)  
    ffs_script = directory + "ts_to_mp4.bat"
    merged_file = directory + own_name + start_time + ".mp4"
    stream_file = directory + own_name + start_time + ".ts"
    with open(ffs_script, "a+", encoding="utf8") as ffs:
        ffs.write("\nffmpeg -i " + stream_file + " -strict -2 -c:v copy " + merged_file + "\n")
        ffs.write("chmod 666 " + merged_file + "\n")
    os.chmod(ffs_script, 0o777)
    hlsvar = "hlsvariant://" + playlist
    print("Retrieving the Streamfile for " + str(own_name))
    baitlist_file = cwd + "\\baitlist.txt"
    with open(baitlist_file, "a+", encoding="utf8") as bl:
        bl.write(own_name + "\n")
    if not os.path.isfile(stream_file):
        subprocess.check_call(["cmd", "/c", "livestreamer", "--http-header", "User-Agent=Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0", "-o",  stream_file , hlsvar, "best"])
        os.chmod(stream_file, 0o666)
    modellist.remove(str(own_name))
    return

def main():
    os.umask(0)
    create_wishlist()
    create_baitlist()
    names_from_wishlist()
    while True:
        names_from_wishlist()
        time.sleep(60)
        print_modellist()

main()

#\\ instead of /
#del intead of rm
#added call(["cmd", "/c", "call"]) for all calls
#changed ts_to_mp4.sh to ts_to_mp4.bat