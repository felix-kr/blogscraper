import getlinks
import time
import telegrambot
import json
import os
import argparse

parser = argparse.ArgumentParser() # argument to turn off telegrambot
parser.add_argument("-t", action="store_true")
args = parser.parse_args()

def generatelinksets(id):
    for y in getlinks.getlinks(id):
        dict1[id][id + "_curr"].add(y)

def writehist(id):
    read = open(os.path.join(os.getcwd(), "hist", id + "_hist.txt"), "r")
    dict1[id][id + "_hist"] =  read.read()
    read.close()

def checkhist(id):
    write = open(os.path.join(os.getcwd(), "hist", id + "_hist.txt"), "a")
    for y in dict1[id][id + "_curr"]:
        if not y in dict1[id][id + "_hist"]:
            write.write(y + "\n")
            print("New Story: " + y)
            if not vars(args)["t"]:
                telegrambot.sendmsg(y)
    write.close()

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
        for x in IDs:
            generatelinksets(x)
            writehist(x)
            checkhist(x)

        z += 1
        print(z, file=log, flush=True)
        print("done sleeping", file=log, flush=True)

    except Exception as e:
        print("Error, retry in 20s")
        print(e, file=log, flush=True)
        time.sleep(20)
