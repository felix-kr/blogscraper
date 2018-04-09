import getlinks
import time
import telegrambot
import json
import os

IDs = json.load(open("IDs.json"))
open("log.txt", "w").close()
log = open("log.txt", "a")


dict1 = {}

for x in IDs: # setting up dict
    dict1[x] = {"url" : IDs[x]}
    dict1[x][x + "_curr"] = set()
    dict1[x][x + "_hist"] = str()

print("Starting...")
z = 0

while True:
    try:
        for x in IDs: # generating current set of links for each item in IDs
            for y in getlinks.getlinks(x):
                dict1[x][x + "_curr"].add(y)
            if not dict1[x][x + "_curr"]:
                telegrambot.sendmsg("Error with ID " + x)

        for x in IDs: # writing current content of _hist.txt files into _hist strings
            read = open(os.path.join(os.getcwd(), "hist", x + "_hist.txt"), "r")
            dict1[x][x + "_hist"] =  read.read()
            read.close()

        for x in IDs: # checking if items in _curr strings are already in _hist strings
            write = open(os.path.join(os.getcwd(), "hist", x + "_hist.txt"), "a")
            for y in dict1[x][x + "_curr"]:
                if not y in dict1[x][x + "_hist"]:
                    write.write(y + "\n")
                    print("New Story: " + y)
                    telegrambot.sendmsg(y)
            write.close()

        z += 1
        print(z, file=log, flush=True)
        time.sleep(20)
        print("done sleeping", file=log, flush=True)

    except Exception as e:
        print("Error, retry in 20s")
        print(e, file=log, flush=True)
        time.sleep(20)
