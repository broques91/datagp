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
    "prix_m2",
    "Nombre de logements",
    "Nombre moyen d'habitant(s) par logement",
    "Résidences principales",
    "Résidences secondaires",
    "Logements vacants",
    "Maisons",
    "Appartements",
    "Autres types de logements",
    "Propriétaires",
    "Locataires",
    "- dont locataires HLM",
    "Locataires hébergés à titre gratuit",
    "Studios",
    "2 pièces",
    "3 pièces",
    "4 pièces",
    "5 pièces et plus",
]


def diff(list1, list2):
    return list(set(list1).symmetric_difference(set(list2)))


# Parer a l'eventualite que le script s'est arreter
if os.path.isfile("data/immobilier.csv"):
    df_immo = pd.read_csv("data/immobilier.csv", error_bad_lines=False, dtype="unicode")
    df_liens = pd.read_csv("data/liens_villes.csv")
    col1 = df_immo["lien"]
    col2 = df_liens["lien"]
    liens = diff(col1, col2)
else:
    df_immo = DataFrame(columns=cols)
    df_immo.to_csv("data/immobilier.csv", index=False)
    df_liens = pd.read_csv("data/liens_villes.csv")
    liens = df_liens["lien"]

liens = [lien for lien in liens if str(lien)[:11] == "/management"]


def parse(lien):
    data = {i: "" for i in cols}
    data["lien"] = lien
    data["ville"] = df_liens[df_liens["lien"] == lien]["ville"].iloc[0]

    req = requests.get("http://www.journaldunet.com" + lien + "/immobilier")
    time.sleep(2)

    if req.status_code == 200:
        with open("data/immobilier.csv", "a", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=cols, extrasaction="ignore", lineterminator="\n"
            )
            soup = bs(req.content, "html.parser")

            try:
                js_script = soup.findAll("script")[6].string
                json_prix = json.loads(js_script)
                try:
                    data["prix_m2"] = float(json_prix["series"][0]["data"][0])
                except:
                    data["prix_m2"] = json_prix["series"][0]["data"][0]
            except:
                data["prix_m2"] = "nc"

            tables = soup.findAll("table", class_="odTable odTableAuto")

            if len(tables) > 0:
                for i in range(len(tables)):
                    for info in tables[i].findAll("tr")[1:]:
                        cle = info.findAll("td")[0].text
                        valeur = info.findAll("td")[1].text

                        if "Locataires hébergés" in cle:
                            try:
                                data["Locataires hébergés à titre gratuit"] = float(
                                    "".join(valeur.split()).replace(",", ".")
                                )
                            except:
                                data["Locataires hébergés à titre gratuit"] = valeur
                        elif "5 pièces" in cle:
                            try:
                                data["5 pièces et plus"] = float(
                                    "".join(valeur.split()).replace(",", ".")
                                )
                            except:
                                data["5 pièces et plus"] = valeur
                        else:
                            try:
                                data[cle] = float(
                                    "".join(valeur.split()).replace(",", ".")
                                )
                            except:
                                data[cle] = valeur

            writer.writerow(data)
            print("[immo]", lien)


if __name__ == "__main__":
    with Pool(20) as p:
        p.map(parse, liens)
