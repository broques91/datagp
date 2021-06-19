import requests
from multiprocessing import Pool
import csv
import pandas as pd
from bs4 import BeautifulSoup as bs
from pandas import DataFrame
from pprint import pprint
import os
import time


# Columns
cols = [
    "ville",
    "lien",
    "Code Insee",
    "Région",
    "Département",
    "Etablissement public de coopération intercommunale (EPCI)",
    "Code postal (CP)",
    "Nom des habitants",
    "Population (2018)",
    "Population : rang national (2018)",
    "Densité de population (2018)",
    "Taux de chômage (2017)",
    "Ville fleurie",
    "Ville d'art et d'histoire",
    "Ville internet",
    "Pavillon bleu",
    "Altitude min.",
    "Altitude max.",
    "Latitude",
    "Longitude",
    "Superficie (surface)",
]


def diff(list1, list2):
    return list(set(list1).symmetric_difference(set(list2)))


# Check if infos.csv exists
if os.path.isfile("data/infos.csv"):
    df_infos = pd.read_csv("data/infos.csv")
    df_liens = pd.read_csv("data/liens_villes.csv")
    col1 = df_infos["lien"]
    col2 = df_liens["lien"]
    liens = diff(col1, col2)
else:
    # Create csv infos
    df_infos = DataFrame(columns=cols)
    df_infos.to_csv("data/infos.csv", index=False)

    # Get links
    df_liens = pd.read_csv("data/liens_villes.csv")
    liens = df_liens["lien"]

# Liens
liens = [lien for lien in liens if lien[:11] == "/management"]


def parse(lien):
    # Init dictionnary
    data = {col: "" for col in cols}
    # url
    url = f"https://www.journaldunet.com{lien}"

    req = requests.get(url)
    time.sleep(2)

    if req.status_code == 200:
        with open("data/infos.csv", "a", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cols, lineterminator="\n")
            soup = bs(req.content, "html.parser")

            data["lien"] = lien
            data["ville"] = df_liens[df_liens["lien"] == lien]["ville"].iloc[0]

            tables = soup.findAll("table", class_="odTable odTableAuto")

            for i in range(len(tables)):
                # Table rows
                tr = tables[i].findAll("tr")

                for row in tr[1:]:
                    key = row.findAll("td")[0].text
                    value = row.findAll("td")[1].text

                    if "Nom des habitants" in key:
                        data["Nom des habitants"] = value
                    elif "Taux de chômage" in key:
                        data["Taux de chômage (2017)"] = value
                    else:
                        data[key] = value

            writer.writerow(data)
            print(lien)


if __name__ == "__main__":
    with Pool(30) as p:
        p.map(parse, liens)
