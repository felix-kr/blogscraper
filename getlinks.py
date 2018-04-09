from bs4 import BeautifulSoup
import requests
import json

log = open("log.txt", "a")
IDs = json.load(open("IDs.json"))

def getlinks(id):

    data = requests.get(IDs[id])
    html = data.content.decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")

    links = []

    # main filter for medium blogs
    for x in soup.find_all("div", {"class": "postArticle-readMore"}):
        x = x.find("a")["href"]
        x = x[0:x.find("?source=")]
        links.append(x)

    # filters for non medium blogs(eth, monero etc)
    if not links:
        if id == "xmr":
            for x in soup.find_all("h3"):
                if x.find("a"):
                    links.append("https:/getmonero.org" + x.find("a")["href"])
        elif id == "eth":
            for x in soup.find_all("h1"):
                if x.find("a"):
                    links.append(x.find("a")["href"])

    print("|", file=log, end=" ", flush=True)

    return links

if __name__ == "__main__":
    for x in getlinks(""):
        print(x)
