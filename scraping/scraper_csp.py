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

cols = [
    "ville",
    "lien",
    "Agriculteurs exploitants",
    "Artisans, commerçants, chefs d'entreprise",
    "Cadres et professions intellectuelles supérieures",
    "Professions intermédiaires",
    "Employés",
    "Ouvriers",
    "Aucun diplôme",
    "Brevet des collèges",
    "CAP / BEP ",
    "Baccalauréat / brevet professionnel",
    "De Bac +2 à Bac +4",
    "Bac +5 et plus",
    "Aucun diplôme (%) hommes",
    "Aucun diplôme (%) femmes",
    "Brevet des collèges (%) hommes",
    "Brevet des collèges (%) femmes",
    "CAP / BEP  (%) hommes",
    "CAP / BEP  (%) femmes",
    "Baccalauréat / brevet professionnel (%) hommes",
    "Baccalauréat / brevet professionnel (%) femmes",
    "De Bac +2 à Bac +4 (%) hommes",
    "De Bac +2 à Bac +4 (%) femmes",
    "Bac +5 et plus (%) hommes",
    "Bac +5 et plus (%) femmes",
]


def diff(list1, list2):
    return list(set(list1).symmetric_difference(set(list2)))


if os.path.isfile("data/csp.csv"):
    df_csp = pd.read_csv("data/csp.csv", error_bad_lines=False, dtype="unicode")
    df_liens = pd.read_csv("data/liens_villes.csv")
    col1 = df_csp["lien"]
    col2 = df_liens["lien"]
    liens = diff(col1, col2)
else:
    df_csp = DataFrame(columns=cols)
    df_csp.to_csv("data/csp.csv", index=False)
    df_liens = pd.read_csv("data/liens_villes.csv")
    liens = df_liens["lien"]

liens = [lien for lien in liens if str(lien)[:11] == "/management"]


def parse(lien):
    data = {i: "" for i in cols}
    data["ville"] = df_liens[df_liens["lien"] == lien]["ville"].iloc[0]
    data["lien"] = lien

    req = requests.get(f"http://www.journaldunet.com{lien}/csp-diplomes")

    if req.status_code == 200:
        with open("data/csp.csv", "a", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=cols, extrasaction="ignore", lineterminator="\n"
            )
            soup = bs(req.content, "html.parser")

            tables = soup.findAll("table", class_="odTable odTableAuto")
            for i in range(len(tables) - 1):
                for table in tables[i].findAll("tr")[1:]:
                    cle = table.findAll("td")[0].text
                    valeur = table.findAll("td")[1].text

                    try:
                        data[cle] = float("".join(valeur.split()))
                    except:
                        data[cle] = ""

            for table in tables[-1].findAll("tr")[1:]:
                cle = table.findAll("td")[0].text
                valeurh = table.findAll("td")[1].text
                valeurf = table.findAll("td")[3].text

                try:
                    data[cle + " (%) hommes"] = float(
                        valeurh.split("%")[0].replace(",", ".")
                    )
                    data[cle + " (%) femmes"] = float(
                        valeurf.split("%")[0].replace(",", ".")
                    )
                except:
                    data[cle + " (%) hommes"] = ""
                    data[cle + " (%) femmes"] = ""

            time.sleep(1)
            writer.writerow(data)
            print("[csp]", lien)


if __name__ == "__main__":
    with Pool(30) as p:
        p.map(parse, liens)
