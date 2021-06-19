from fake_useragent import UserAgent
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
    "Violences aux personnes",
    "Vols et dégradations",
    "Délinquance économique et financière",
    "Autres crimes et délits",
    "Violences gratuites",
    "Violences crapuleuses",
    "Violences sexuelles",
    "Menaces de violence",
    "Atteintes à la dignité",
    "Cambriolages",
    "Vols à main armée (arme à feu)",
    "Vols avec entrée par ruse",
    "Vols liés à l'automobile",
    "Vols de particuliers",
    "Vols d'entreprises",
    "Violation de domicile",
    "Destruction et dégradations de biens",
    "Escroqueries, faux et contrefaçons",
    "Trafic, revente et usage de drogues",
    "Infractions au code du Travail",
    "Infractions liées à l'immigration",
    "Différends familiaux",
    "Proxénétisme",
    "Ports ou détentions d'arme prohibée",
    "Recels",
    "Délits des courses et jeux d'argent",
    "Délits liés aux débits de boisson et de tabac",
    "Atteintes à l'environnement",
    "Délits liés à la chasse et la pêche",
    "Cruauté et délits envers les animaux",
    "Atteintes aux intérêts fondamentaux de la Nation",
]

# fonction qui va nous permettre de faire la difference entre les elements scrapes et non scrapes
def diff(list1, list2):
    return list(set(list1).symmetric_difference(set(list2)))


# Parer a l'eventualite que le script s'est arreter
if os.path.isfile("data/delinquance.csv"):
    df_delinquance = pd.read_csv(
        "data/delinquance.csv", error_bad_lines=False, dtype="unicode"
    )
    df_liens = pd.read_csv("data/liens_villes.csv")
    col1 = df_delinquance["lien"]
    col2 = df_liens["lien"]
    liens = diff(col1, col2)
else:
    df_delinquance = DataFrame(columns=cols)
    df_delinquance.to_csv("data/delinquance.csv", index=False)

    df_liens = pd.read_csv("data/liens_villes.csv")
    liens = df_liens["lien"]

liens = [lien for lien in liens if str(lien)[:11] == "/management"]


def parse(lien):
    # Pick a random user agent
    ua = UserAgent(verify_ssl=False)
    user_agent = ua.random
    headers = {"User-Agent": user_agent}

    data = {i: "" for i in cols}
    data["lien"] = lien
    data["ville"] = df_liens[df_liens["lien"] == lien]["ville"].iloc[0]

    url = f"http://www.linternaute.com/actualite/delinquance/{lien[18:]}"
    req = requests.get(url, headers=headers)

    if req.status_code == 200:
        with open("data/delinquance.csv", "a", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=cols, extrasaction="ignore", lineterminator="\n"
            )
            soup = bs(req.content, "html.parser")

            tables = soup.findAll("table", class_="odTable odTableAuto")

            if len(tables) > 0:
                for i in range(len(tables)):
                    for info in tables[i].findAll("tr")[1:]:
                        key = info.findAll("td")[0].text
                        value = info.findAll("td")[1].text
                        try:
                            data[key] = float("".join(value.split()).split("c")[0])
                        except:
                            data[key] = "nc"

            time.sleep(2)
            writer.writerow(data)
            print("[delinquance]", lien)

    elif req.status_code == 403:
        print("Forbidden")
        time.sleep(2)


if __name__ == "__main__":
    with Pool(30) as p:
        p.map(parse, liens)
