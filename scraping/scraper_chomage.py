import os
import json
import time
import re
import csv

from bs4 import BeautifulSoup as bs
from multiprocessing import Pool
import pandas as pd
from pandas import DataFrame
from pprint import pprint
import requests

default_cols = ["ville", "lien"]

data = {
    **{col: "" for col in default_cols},
    **{f"Taux de chômage ({str(y)})": "" for y in range(2006, 2018)},
    **{f"Moyenne France ({str(y)})": "" for y in range(2006, 2018)},
}

cols = list(data.keys())


def diff(list1, list2):
    return list(set(list1).symmetric_difference(set(list2)))


# Check if chomage.csv exists
if os.path.isfile("data/chomage.csv"):
    df_chomage = pd.read_csv("data/chomage.csv", error_bad_lines=False, dtype="unicode")
    col1 = df_chomage["lien"]
    df_liens = pd.read_csv("data/liens_villes.csv")
    col2 = df_liens["lien"]
    liens = diff(col1, col2)
else:
    # Create csv chomage
    df_chomage = DataFrame(columns=cols)
    df_chomage.to_csv("data/chomage.csv", index=False)
    # Get links to scrape
    df_liens = pd.read_csv("data/liens_villes.csv")
    liens = df_liens["lien"]

# Liens
liens = [l for l in liens if l[:11] == "/management"]


def parse(lien):
    # Init dictionnary
    data = {
        **{col: "" for col in default_cols},
        **{f"Taux de chômage ({str(y)})": "" for y in range(2006, 2018)},
        **{f"Moyenne France ({str(y)})": "" for y in range(2006, 2018)},
    }

    data["lien"] = lien
    data["ville"] = df_liens[df_liens["lien"] == lien]["ville"].iloc[0]

    # Request
    req = requests.get(f"https://www.journaldunet.com{lien}/emploi")
    time.sleep(2)

    if req.status_code == 200:
        with open("data/chomage.csv", "a", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=cols, extrasaction="ignore", lineterminator="\n"
            )
            soup = bs(req.content, "html.parser")

            divs = soup.findAll("div", class_="hidden marB20")

            for div in divs:
                titre_h2 = div.find("h2")

                # Taux de chômage
                if titre_h2 != None and "Taux de chômage" in titre_h2.text:
                    # If chart exists ...
                    if div.find("script").string:
                        # javascript content
                        script = div.find("script").string
                        # Convert string to json
                        json_data = json.loads(script)

                        taux = json_data["series"][0]["data"]
                        moyennes = json_data["series"][1]["data"]
                        annees = json_data["xAxis"]["categories"]

                        for t, m, a in zip(taux, moyennes, annees):
                            try:
                                data[f"Taux de chômage ({a})"] = float(t)
                                data[f"Moyenne France ({a})"] = float(m)
                            except:
                                data[f"Taux de chômage ({a})"] = ""
                                data[f"Moyenne France ({a})"] = ""

                        writer.writerow(data)
                        print(f"[chomage] {lien}")


if __name__ == "__main__":
    with Pool(30) as p:
        p.map(parse, liens)
