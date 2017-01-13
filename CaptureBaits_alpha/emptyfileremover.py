import os

with open("playlist.txt", "w") as e:
    with open("playlist2.txt", "r") as p:
        for line in p:
            line = line.split("file '")[1]
            line = line.split("'")[0]
            print(line)
            if os.path.getsize(line) > 10000:
                e.write("file \'" + line + "\'\n")
