import requests
import json

token = ""
chatid = ""

methods = {"msg" : "sendMessage", "update" : "getUpdates"}

def sendmsg(newstory):
    url = "https://api.telegram.org/bot" + token + "/" + methods["msg"]
    values = {"chat_id" : chatid, "text" : newstory}
    requests.get(url, params=values)

def getupdates():
    url = "https://api.telegram.org/bot" + token + "/" + methods["update"]
    r = requests.get(url)
    data = r.content.decode("utf-8") # convert bytes to str
    answer = json.loads(data) # convert string that represents dict to dict
    return answer

if __name__ == "__main__":
    getupdates()
