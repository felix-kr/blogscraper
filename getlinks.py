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
                links.append("https://neo.org/" +x["href"])

    print("|", file=log, end=" ", flush=True)

    return links

if __name__ == "__main__":
    for x in getlinks(""):
        print(x)
