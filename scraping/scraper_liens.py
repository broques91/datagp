import requests
from bs4 import BeautifulSoup as bs
import csv
import pandas as pd
from pandas import DataFrame

cols = ["ville", "lien"]

df = DataFrame(columns=cols)
df.to_csv("data/liens_villes.csv", index=False)

# Data
data = {}
data["ville"] = ""
data["lien"] = ""

with open("data/liens_villes.csv", "a", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")

    url = "https://www.journaldunet.com/management/ville/guadeloupe/departement-971/villes"

    req = requests.get(url)
    soup = bs(req.content, "html.parser")
    table_villes = soup.find("div", class_="odListBox marB20")
    liens = table_villes.findAll("a")

    for lien in liens:
        if "/ville-" in lien["href"]:
            data["ville"] = lien.text
            data["lien"] = lien["href"]

            writer.writerow(data)
