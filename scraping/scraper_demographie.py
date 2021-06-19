import requests
from multiprocessing import Pool
import csv
import pandas as pd
from bs4 import BeautifulSoup as bs
from pandas import DataFrame
from pprint import pprint
import os
import time
import json


default_cols = [
    "ville",
    "lien",
    "Population",
    "Densité de population",
    "Nombre de ménages",
    "Habitants par ménage",
    "Nombre de familles",
    "Naissances",
    "Décès",
    "Solde naturel",
    "Hommes",
    "Femmes",
    "Moins de 15 ans",
    "15 - 29 ans",
    "30 - 44 ans",
    "45 - 59 ans",
    "60 - 74 ans",
    "75 ans et plus",
    "Familles monoparentales",
    "Couples sans enfant",
    "Couples avec enfant",
    "Familles sans enfant",
    "Familles avec un enfant",
    "Familles avec deux enfants",
    "Familles avec trois enfants",
    "Familles avec quatre enfants ou plus",
    "Personnes célibataires",
    "Personnes mariées",
    "Personnes divorcées",
    "Personnes veuves",
    "Personnes en concubinage",
    "Personnes pacsées",
    "Population étrangère",
    "Hommes étrangers",
    "Femmes étrangères",
    "Moins de 15 ans étrangers",
    "15-24 ans étrangers",
    "25-54 ans étrangers",
    "55 ans et plus étrangers",
    "Population immigrée",
    "Hommes immigrés",
    "Femmes immigrées",
    "Moins de 15 ans immigrés",
    "15-24 ans immigrés",
    "25-54 ans immigrés",
    "55 ans et plus immigrés",
]

data = {
    **{col: "" for col in default_cols},
    **{f"Nombre d'habitants ({str(y)})": "" for y in range(2006, 2019)},
    **{f"Nombre de naissances ({str(y)})": "" for y in range(1999, 2019)},
    **{f"Nombre de décès ({str(y)})": "" for y in range(1999, 2019)},
    **{f"Nombre d'étrangers ({str(y)})": "" for y in range(2006, 2018)},
    **{f"Nombre d'immigrés ({str(y)})": "" for y in range(2006, 2018)},
}

cols = list(data.keys())


def diff(list1, list2):
    return list(set(list1).symmetric_difference(set(list2)))


# Check if demographie.csv exists
if os.path.isfile("data/demographie.csv"):
    df_demo = pd.read_csv(
        "data/demographie.csv", error_bad_lines=False, dtype="unicode"
    )
    col1 = df_demo["lien"]
    df_liens = pd.read_csv("data/liens_villes.csv")
    col2 = df_liens["lien"]
    liens = diff(col1, col2)
else:
    # Create csv demographie
    df_demo = DataFrame(columns=cols)
    df_demo.to_csv("data/demographie.csv", index=False)
    # Get links to scrape
    df_liens = pd.read_csv("data/liens_villes.csv")
    liens = df_liens["lien"]

# Liens
liens = [l for l in liens if l[:11] == "/management"]


def parse(lien):
    # Init dictionnary
    data = {
        **{col: "" for col in default_cols},
        **{f"Nombre d'habitants ({str(y)})": "" for y in range(2006, 2019)},
        **{f"Nombre de naissances ({str(y)})": "" for y in range(1999, 2019)},
        **{f"Nombre de décès ({str(y)})": "" for y in range(1999, 2019)},
        **{f"Nombre d'étrangers ({str(y)})": "" for y in range(2006, 2018)},
        **{f"Nombre d'immigrés ({str(y)})": "" for y in range(2006, 2018)},
    }

    data["lien"] = lien
    data["ville"] = df_liens[df_liens["lien"] == lien]["ville"].iloc[0]

    # Request
    req = requests.get(f"https://www.journaldunet.com{lien}/demographie")
    time.sleep(2)

    if req.status_code == 200:
        with open("data/demographie.csv", "a", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=cols, extrasaction="ignore", lineterminator="\n"
            )
            soup = bs(req.content, "html.parser")

            tables = soup.findAll("table", class_="odTable odTableAuto")

            for i in range(len(tables)):
                infos = tables[i].findAll("tr")
                for info in infos[1:]:
                    # Key
                    key = info.findAll("td")[0].text
                    key = key.split("(")[0].strip()
                    # Value
                    value = info.findAll("td")[1].text
                    value = value.split("h")[0].replace(",", ".")
                    # Save to dict
                    try:
                        data[key] = float(value)
                    except:
                        data[key] = value

            divs = soup.findAll("div", class_="hidden marB20")
            for div in divs:
                titre_h2 = div.find("h2")

                # Nombre d'habitants
                if titre_h2 != None and "Nombre d'habitants" in titre_h2.text:
                    # If chart exists ...
                    if div.find("script").string:
                        # javascript content
                        script = div.find("script").string
                        # Convert string to json
                        json_data = json.loads(script)

                        habitants = json_data["series"][0]["data"]
                        years = json_data["xAxis"]["categories"]

                        for y, h in zip(years, habitants):
                            try:
                                data[f"Nombre d'habitants ({y})"] = float(h)
                            except:
                                data[f"Nombre d'habitants ({v})"] = ""

                # Naissances et décès
                if titre_h2 != None and "Naissances et décès" in titre_h2.text:
                    if div.find("script").string:
                        # javascript content
                        script = div.find("script").string
                        # Convert string to json
                        json_data = json.loads(script)

                        births = json_data["series"][0]["data"]
                        deaths = json_data["series"][1]["data"]
                        years = json_data["xAxis"]["categories"]

                        for y, b, d in zip(years, births, deaths):
                            try:
                                data[f"Nombre de naissances ({str(y)})"] = float(b)
                                data[f"Nombre de décès ({str(y)})"] = float(d)
                            except:
                                data[f"Nombre de naissances ({str(y)})"] = ""
                                data[f"Nombre de décès ({str(y)})"] = ""

                # Nombre d'étrangers
                if titre_h2 != None and "Nombre d'étrangers" in titre_h2.text:
                    if div.find("script").string:
                        # javascript content
                        script = div.find("script").string
                        # Convert string to json
                        json_data = json.loads(script)

                        strangers = json_data["series"][0]["data"]
                        years = json_data["xAxis"]["categories"]

                        for y, s in zip(years, strangers):
                            try:
                                data[f"Nombre d'étrangers ({y})"] = float(s)
                            except:
                                data[f"Nombre d'étrangers ({y})"] = ""

                # Nombre d'immigrés
                if titre_h2 != None and "Nombre d'immigrés" in titre_h2.text:
                    if div.find("script").string:
                        script = div.find("script").string
                        json_data = json.loads(script)

                        years = json_data["xAxis"]["categories"]
                        immigrants = json_data["series"][0]["data"]

                        for y, i in zip(years, immigrants):
                            try:
                                data[f"Nombre d'immigrés ({y})"] = float(i)
                            except:
                                data[f"Nombre d'immigrés ({y})"] = ""

            writer.writerow(data)
            print(f"[demographie] {lien}")


if __name__ == "__main__":
    with Pool(30) as p:
        p.map(parse, liens)
