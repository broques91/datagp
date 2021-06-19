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
    "Actifs en emploi",
    "Aides familiaux",
    "Autres personnes sans activité de 15-64 ans",
    "CDD",
    "CDI et fonction publique",
    "Chômeurs",
    "Emplois aidés",
    "Employeurs",
    "Femmes à temps partiel",
    "Hommes à temps partiel",
    "Inactifs",
    "Indépendants",
    "Intérimaires",
    "Les 15 à 24 ans à temps partiel",
    "Les 25 à 54 ans à temps partiel",
    "Les 55 à 64 ans à temps partiel",
    "Non-salariés",
    "Part des actifs 15-24 ans (%)",
    "Part des actifs 25-54 ans (%)",
    "Part des actifs 55-64 ans (%)",
    "Part des actifs femmes (%)",
    "Part des actifs hommes (%)",
    "Retraités et pré-retraités de 15-64 ans",
    "Salariés",
    "Salariés à temps partiel",
    "Stages et apprentissages",
    "Stagiaires et étudiants de 15-64 ans",
    "Taux d'activité femmes (%)",
    "Taux d'activité hommes (%)",
    "Taux d'emploi 15-24 ans (%)",
    "Taux d'emploi 25-54 ans (%)",
    "Taux d'emploi 55-64 ans (%)",
    "Taux d'emploi femmes (%)",
    "Taux d'emploi hommes (%)",
    "Taux de chômage 15-24 ans (%)",
    "Taux de chômage 25-54 ans (%)",
    "Taux de chômage 55-64 ans (%)",
    "Taux de chômage femmes (%)",
    "Taux de chômage hommes (%)",
]


def diff(list1, list2):
    return list(set(list1).symmetric_difference(set(list2)))


# Parer a l'eventualite que le script s'est arreter
if os.path.isfile("data/emploi.csv"):
    df_emploi = pd.read_csv("data/emploi.csv", error_bad_lines=False, dtype="unicode")
    df_liens = pd.read_csv("data/liens_villes.csv")
    col1 = df_emploi["lien"]
    col2 = df_liens["lien"]
    liens = diff(col1, col2)
else:
    df_emploi = DataFrame(columns=cols)
    df_emploi.to_csv("data/emploi.csv", index=False)
    df_liens = pd.read_csv("data/liens_villes.csv")
    liens = df_liens["lien"]

liens = [lien for lien in liens if str(lien)[:11] == "/management"]


def parse(lien):
    data = {i: "" for i in cols}
    data["lien"] = lien
    data["ville"] = df_liens[df_liens["lien"] == lien]["ville"].iloc[0]

    req = requests.get(f"http://www.journaldunet.com{lien}/emploi")
    time.sleep(2)

    if req.status_code == 200:
        with open("data/emploi.csv", "a", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=cols, extrasaction="ignore", lineterminator="\n"
            )
            soup = bs(req.content, "html.parser")

            tables = soup.findAll("table", class_="odTable odTableAuto")

            if len(tables) > 0:
                # collecte du tableau 1, 4, 5, 6, 7
                for i in [0, 3, 4, 5, 6]:
                    for table in tables[i].findAll("tr")[1:]:
                        cle = table.findAll("td")[0].text
                        valeur = table.findAll("td")[1].text
                        try:
                            data[cle] = float("".join(valeur.split()))
                        except:
                            data[cle] = "nc"

                # Collecte du tableau 2
                for table in tables[1].findAll("tr")[1:]:
                    cle = table.findAll("td")[0].text
                    valeurh = table.findAll("td")[1].text
                    valeurf = table.findAll("td")[3].text
                    try:
                        data[cle + " hommes (%)"] = float(
                            valeurh.split()[0].replace(",", ".")
                        )
                        data[cle + " femmes (%)"] = float(
                            valeurf.split()[0].replace(",", ".")
                        )
                    except:
                        data[cle + " hommes (%)"] = "nc"
                        data[cle + " femmes (%)"] = "nc"

                # Collecte du tableau 3
                for table in tables[2].findAll("tr")[1:]:
                    cle = table.findAll("td")[0].text
                    valeur15_24 = table.findAll("td")[1].text
                    valeur25_54 = table.findAll("td")[2].text
                    valeur55_64 = table.findAll("td")[3].text
                    try:
                        data[cle + " 15-24 ans (%)"] = float(
                            valeur15_24.split("%")[0].replace(",", ".")
                        )
                        data[cle + " 25-54 ans (%)"] = float(
                            valeur25_54.split("%")[0].replace(",", ".")
                        )
                        data[cle + " 55-64 ans (%)"] = float(
                            valeur55_64.split("%")[0].replace(",", ".")
                        )
                    except:
                        data[cle + " 15-24 ans (%)"] = "nc"
                        data[cle + " 25-54 ans (%)"] = "nc"
                        data[cle + " 55-64 ans (%)"] = "nc"

            writer.writerow(data)
            print("[emploi]", lien)


if __name__ == "__main__":
    with Pool(30) as p:
        p.map(parse, liens)
