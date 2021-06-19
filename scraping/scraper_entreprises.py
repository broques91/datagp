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
    "Nombre d'entreprises",
    "- dont commerces et services aux particuliers",
    "Entreprises créées",
    "Commerces",
    "Services aux particuliers",
    "Services publics",
    "Epiceries",
    "Boulangeries",
    "Boucheries, charcuteries",
    "Librairies, papeteries, journaux",
    "Drogueries et quincalleries",
    "Banques",
    "Bureaux de Poste",
    "Garages, réparation automobile",
    "Electriciens",
    "Grandes surfaces",
    "Commerces spécialisés alimentaires",
    "Commerces spécialisés non alimentaires",
    "Services généraux",
    "Services automobiles",
    "Services du bâtiment",
    "Autres services",
]

data = {
    **{i: "" for i in cols},
    **{f"{str(annee)} (nbre de creations)": "" for annee in range(2005, 2020)},
    **{f"{str(annee)} (nbre d'entreprises)": "" for annee in range(2005, 2020)},
}

cols = list(data.keys())


def diff(list1, list2):
    return list(set(list1).symmetric_difference(set(list2)))


# Parer a l'eventualite d'un bug pendant le scraping
if os.path.isfile("data/entreprises.csv"):
    df_entreprises = pd.read_csv(
        "data/entreprises.csv", error_bad_lines=False, dtype="unicode"
    )
    df_liens = pd.read_csv("data/liens_villes.csv")
    cols1 = df_entreprises["lien"]
    cols2 = df_liens["lien"]
    liens = diff(cols1, cols2)
else:
    df_entreprises = DataFrame(columns=cols)
    df_entreprises.to_csv("data/entreprises.csv", index=False)
    df_liens = pd.read_csv("data/liens_villes.csv")
    liens = df_liens["lien"]

liens = [lien for lien in liens if str(lien)[:11] == "/management"]


def parse(lien):
    data = {
        **{i: "" for i in cols},
        **{f"{str(annee)} (nbre de creations)": "" for annee in range(2005, 2020)},
        **{f"{str(annee)} (nbre d'entreprises)": "" for annee in range(2005, 2020)},
    }

    data["lien"] = lien
    data["ville"] = df_liens[df_liens["lien"] == lien]["ville"].iloc[0]

    req = requests.get(f"http://www.journaldunet.com{lien}/entreprises")
    time.sleep(2)

    if req.status_code == 200:
        with open("data/entreprises.csv", "a", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=cols, extrasaction="ignore", lineterminator="\n"
            )
            soup = bs(req.content, "html.parser")

            tables = soup.findAll("table", class_="odTable odTableAuto")

            if len(tables) > 0:
                for i in range(len(tables)):
                    for info in tables[i].findAll("tr")[1:]:
                        cle = info.findAll("td")[0].text
                        valeur = info.findAll("td")[1].text
                        try:
                            data[cle] = float("".join(valeur.split()))
                        except:
                            data[cle] = "nc"

            # Evolution du nombre et de creations d'entreprises
            divs = soup.findAll("div", class_="marB20")
            for div in divs:
                titre_h2 = div.find("h2")

                if titre_h2 != None and "Nombre d'entreprises" in titre_h2.text:
                    js_script = div.find("script").string
                    json_data_en = json.loads(js_script)
                    annees = json_data_en["xAxis"]["categories"]
                    entreprises = json_data_en["series"][0]["data"]

                    for annee, entreprise in zip(annees, entreprises):
                        data[f"{str(annee)} (nbre d'entreprises)"] = float(entreprise)

                if titre_h2 != None and "Créations d'entreprises" in titre_h2.text:
                    js_script = div.find("script").string
                    json_data_en = json.loads(js_script)
                    annees = json_data_en["xAxis"]["categories"]
                    creations = json_data_en["series"][0]["data"]

                    for annee, creation in zip(annees, creations):
                        data[f"{str(annee)} (nbre de creations)"] = float(creation)

            writer.writerow(data)
            print("[entreprises]", lien)


if __name__ == "__main__":
    with Pool(30) as p:
        p.map(parse, liens)
