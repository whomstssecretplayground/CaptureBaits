import os
import time

cwd = os.getcwd()
print(cwd)
batches = cwd + "\\Batches"
if not os.path.exists(batches):
            os.mkdir(batches)
input = cwd + "\\list.txt"
with open(input, "r", encoding="utf-8") as l:
    for line in l:
        line = line.replace("\n", "")
        encodeddir = line.split("\\")
        length = len(encodeddir) - 1
        encodeddir = line.split("\\")[length]
        filename = encodeddir.split(".")[0]
        outfile = batches + "\\ffmpeg_" + filename + ".bat"
        encodeddir = line.split(encodeddir)[0] + "encoded\\"
        filename = encodeddir + filename + ".mp4"
        if not os.path.exists(encodeddir):
            os.mkdir(encodeddir)
        with open(outfile, "w", encoding="utf-8") as o:
            o.write("ffmpeg -i " + line + " -strict -2 -c:v nvenc_hevc -c:a libmp3lame " + filename)

#dir " DIR " /b /s /A-D /o:gn>list.txt