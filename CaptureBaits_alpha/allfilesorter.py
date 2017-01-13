import os

def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))

stream = os.getcwd() + "/Stream/"
deeks = sorted_ls(stream)

with open("playlist2.txt", "w") as p:
    for x in deeks:
        p.write("file \'" + stream + x + "\'\n")
