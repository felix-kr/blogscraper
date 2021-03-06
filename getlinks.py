from bs4 import BeautifulSoup
import requests
import json

log = open("log.txt", "a")
IDs = json.load(open("IDs.json"))

def getlinks(id):

    links = []

    try:
        data = requests.get(IDs[id][0], timeout=1.8)
        html = data.content.decode("utf-8")
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
        print("-", file=log, end=" ", flush=True)
        return links

    soup = BeautifulSoup(html, "html.parser")

    # main filter for medium blogs
    for x in soup.find_all("div", {"class": "postArticle-readMore"}):
        x = x.find("a")["href"]
        x = x[0:x.find("?source=")]
        links.append(x)

    # filters for non medium blogs(eth, monero etc)
    filterdict = {
    "eth": ["h1"],
    "stellar": ["h1", "blog0516-summary__title entry-title"],
    "ripple": ["h2", "entry-title"],
    }

    if not links:
        for x in filterdict:
            if id == x:
                if len(filterdict[x]) != 1:
                    for y in soup.find_all(filterdict[x][0], {"class": filterdict[x][1]}):
                        links.append(y.find("a")["href"])
                else:
                    for y in soup.find_all(filterdict[x][0]):
                        links.append(y.find("a")["href"])
        if id == "xmr":
            for x in soup.find_all("h3"):
                if x.find("a"):
                    links.append("https:/getmonero.org" + x.find("a")["href"])
        elif id == "neo":
            for x in soup.find_all("a", {"class": "blog-title"}):
                links.append("https://neo.org" + x["href"])
        elif id == "verge":
            for x in soup.find_all("h2", {"class": "block-header"}):
                links.append("https://vergefora.com" + x.find("a")["href"])
        elif id == "cardano":
            for x in soup.find_all("a"):
                if ("/t/" in x["href"] and "weekly" not in x["href"]):
                    links.append("https://forum.cardano.org" + x["href"])

    print("|", file=log, end=" ", flush=True)

    return links

if __name__ == "__main__":
    for x in getlinks(""):
        print(x)
