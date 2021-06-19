from bs4 import BeautifulSoup as bs
from multiprocessing import Pool
import pandas as pd
from pandas import DataFrame
from pprint import pprint
import json
import requests
import time
import csv
import os
import re

cols = [
    "ville",
    "lien",
    "total de voitures",
    "Ménages sans voiture",
    "Ménages avec une voiture",
    "Ménages avec deux voitures ou plus",
    "Ménages avec place(s) de stationnement",
    "Nombre total d'accidents",
    "Nombre de personnes tuées",
    "Nombre de personnes indemnes",
    "Nombre de personnes blessées",
    " - dont blessés graves",
    " - dont blessés légers",
]


def diff(list1, list2):
    """Difference entre les elements scrapes et non scrapes"""
    return list(set(list1).symmetric_difference(set(list2)))


# Parer a l'eventualite que le script s'est arreter
if os.path.isfile("data/auto.csv"):
    # instructions
    df_infos = pd.read_csv(
        "data/automobile.csv", error_bad_lines=False, dtype="unicode"
    )
    df_liens = pd.read_csv("dataset/liens_villes.csv")
    col1 = df_infos["lien"]
    col2 = df_liens["lien"]
    liens = diff(col1, col2)
else:
    df_infos = DataFrame(columns=cols)
    df_infos.to_csv("data/automobile.csv", index=False)
    df_liens = pd.read_csv("data/liens_villes.csv")
    liens = df_liens["lien"]

liens = [lien for lien in liens if str(lien)[:11] == "/management"]


def parse(lien):
    data = {i: "" for i in cols}

    data["lien"] = lien
    data["ville"] = df_liens[df_liens["lien"] == lien]["ville"].iloc[0]

    req = requests.get("http://www.journaldunet.com" + lien + "/auto")
    time.sleep(2)
    if req.status_code == 200:
        with open("data/automobile.csv", "a", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=cols, extrasaction="ignore", lineterminator="\n"
            )
            contenu = req.content
            soup = bs(contenu, "html.parser")

            # Nombe de total de voitures
            divs = soup.findAll("div", class_="hidden marB20")
            for div in divs:
                titre_h2 = div.find("h2")

                if titre_h2 != None and "ménages avec voiture" in titre_h2.text:
                    try:
                        js_script = div.find("script").string
                        json_data = json.loads(js_script)
                        data["total de voitures"] = float(
                            json_data["series"][0]["data"][-1]
                        )
                    except:
                        data["total de voitures"] = "NaN"

            tables = soup.findAll("table", class_="odTable odTableAuto")

            for info in tables[0].findAll("tr")[1:]:
                key = info.findAll("td")[0].text
                value = info.findAll("td")[1].text
                if value != "nc":
                    data[key] = float("".join(value.split()).replace(",", "."))
                else:
                    data[key] = "nc"

            if len(tables) >= 2:
                for info in tables[1].findAll("tr")[1:]:
                    key = info.findAll("td")[0].text
                    value = info.findAll("td")[1].text
                    if value != "nc":
                        data[key] = float(
                            "".join(value.split()).split("(")[0].replace(",", ".")
                        )
                    else:
                        data[key] = value

            writer.writerow(data)
            print("[automobile]", lien)


if __name__ == "__main__":
    with Pool(30) as p:
        p.map(parse, liens)
