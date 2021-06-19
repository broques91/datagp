import requests
from multiprocessing import Pool
import csv
import pandas as pd
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs
from pandas import DataFrame
from pprint import pprint
import os
import time
import json


default_cols = [
    "ville",
    "lien",
    "Allocataires CAF",
    "Bénéficiaires du RSA",
    " - bénéficiaires du RSA majoré",
    " - bénéficiaires du RSA socle",
    "Bénéficiaires de l'aide au logement",
    " - bénéficiaires de l'APL (aide personnalisée au logement)",
    " - bénéficiaires de l'ALF (allocation de logement à caractère familial)",
    " - bénéficiaires de l'ALS (allocation de logement à caractère social)",
    " - bénéficiaires de l'Allocation pour une location immobilière",
    " - bénéficiaires de l'Allocation pour un achat immobilier",
    "Bénéficiaires des allocations familiales",
    " - bénéficiaires du complément familial",
    " - bénéficiaires de l'allocation de soutien familial",
    " - bénéficiaires de l'allocation de rentrée scolaire",
    "Médecins généralistes",
    "Masseurs-kinésithérapeutes",
    "Infirmiers",
    "Spécialistes ORL",
    "Ophtalmologistes",
    "Dermatologues",
    "Sage-femmes",
    "Pédiatres",
    "Gynécologues",
    "Pharmacies",
    "Urgences",
    "Ambulances",
    "Etablissements de santé de court séjour",
    "Etablissements de santé de moyen séjour",
    "Etablissements de santé de long séjour",
    "Etablissement d'accueil du jeune enfant",
    "Maisons de retraite",
    "Etablissements pour enfants handicapés",
    "Etablissements pour adultes handicapés",
    "Bénéficiaires de la PAJE",
    " - bénéficiaires de l'allocation de base",
    " - bénéficiaires du complément mode de garde pour une assistante maternelle",
    " - bénéficiaires du complément de libre choix d'activité (CLCA ou COLCA)",
    " - bénéficiaires de la prime naissance ou adoption",
]

data = {
    **{col: "" for col in default_cols},
    **{f"Nombre d'allocataires CAF ({str(y)})": "" for y in range(2009, 2018)},
    **{f"Nombre de bénéficiaires RSA ({str(y)})": "" for y in range(2011, 2018)},
    **{f"Nombre de bénéficiaires APL ({str(y)})": "" for y in range(2009, 2018)},
    **{
        f"Nombre de bénéficiaires des allocations familiales ({str(y)})": ""
        for y in range(2009, 2019)
    },
}

cols = list(data.keys())


def diff(list1, list2):
    return list(set(list1).symmetric_difference(set(list2)))


# Check if sante_social.csv exists
if os.path.isfile("data/sante_social.csv"):
    # Read csv
    df_social = pd.read_csv(
        "data/sante_social.csv", error_bad_lines=False, dtype="unicode"
    )
    df_liens = pd.read_csv("data/liens_villes.csv")
    col1 = df_social["lien"]
    col2 = df_liens["lien"]
    liens = diff(col1, col2)
else:
    # Create csv
    df_social = DataFrame(columns=cols)
    df_social.to_csv("data/sante_social.csv", index=False)
    # Get links to scrape
    df_liens = pd.read_csv("data/liens_villes.csv")
    liens = df_liens["lien"]

# liens
liens = [lien for lien in liens if str(lien)[:11] == "/management"]


def parse(lien):
    # Pick a random user agent
    ua = UserAgent(verify_ssl=False)
    user_agent = ua.random
    headers = {"User-Agent": user_agent}

    data = {
        **{col: "" for col in default_cols},
        **{f"Nombre d'allocataires CAF ({str(y)})": "" for y in range(2009, 2018)},
        **{f"Nombre de bénéficiaires RSA ({str(y)})": "" for y in range(2011, 2018)},
        **{f"Nombre de bénéficiaires APL ({str(y)})": "" for y in range(2009, 2018)},
        **{
            f"Nombre de bénéficiaires allocations familiales ({str(y)})": ""
            for y in range(2009, 2019)
        },
    }

    data["lien"] = lien
    data["ville"] = df_liens[df_liens["lien"] == lien]["ville"].iloc[0]

    # Request
    req = requests.get(
        f"https://www.journaldunet.com{lien}/sante-social", headers=headers
    )

    if req.status_code == 200:
        with open("data/sante_social.csv", "a", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=cols, extrasaction="ignore", lineterminator="\n"
            )
            soup = bs(req.content, "html.parser")

            tables = soup.findAll("table", class_="odTable odTableAuto")

            for i in range(len(tables)):
                infos = tables[i].findAll("tr")
                for info in infos[1:]:
                    key = info.findAll("td")[0].text
                    value = info.findAll("td")[1].text

                    try:
                        data[key] = float(value)
                    except:
                        data[key] = value

            divs = soup.findAll("div", class_="hidden marB20")
            for div in divs:
                titre_h2 = div.find("h2")

                # Nombre d'allocataires CAF
                if titre_h2 != None and "Nombre d'allocataires CAF" in titre_h2.text:
                    # If chart exists ...
                    if div.find("script").string:
                        script = div.find("script").string
                        json_data = json.loads(script)

                        allocataires = json_data["series"][0]["data"]
                        years = json_data["xAxis"]["categories"]

                        for y, a in zip(years, allocataires):
                            try:
                                data[f"Nombre d'allocataires CAF ({str(y)})"] = float(a)
                            except:
                                data[f"Nombre d'allocataires CAF ({str(y)})"] = ""

                # Nombre de bénéficiaires du RSA
                if (
                    titre_h2 != None
                    and "Nombre de bénéficiaires du RSA" in titre_h2.text
                ):
                    if div.find("script").string:
                        script = div.find("script").string
                        json_data = json.loads(script)

                        beneficiaires = json_data["series"][0]["data"]
                        years = json_data["xAxis"]["categories"]

                        for (
                            y,
                            b,
                        ) in zip(years, beneficiaires):
                            try:
                                data[f"Nombre de bénéficiaires RSA ({str(y)})"] = float(
                                    b
                                )
                            except:
                                data[f"Nombre de bénéficiaires RSA ({str(y)})"] = ""

                # Nombre de bénéficiaires de l'aide au logement
                if (
                    titre_h2 != None
                    and "Nombre de bénéficiaires de l'aide au logement" in titre_h2.text
                ):
                    # If chart exists ...
                    if div.find("script").string:
                        script = div.find("script").string
                        json_data = json.loads(script)

                        beneficiaires_al = json_data["series"][0]["data"]
                        years = json_data["xAxis"]["categories"]

                        for y, b in zip(years, beneficiaires_al):
                            try:
                                data[f"Nombre de bénéficiaires APL ({str(y)})"] = float(
                                    b
                                )
                            except:
                                data[f"Nombre de bénéficiaires APL ({str(y)})"] = ""

                # Nombre de bénéficiaires des allocations familiales
                if (
                    titre_h2 != None
                    and "Nombre de bénéficiaires des allocations familiales"
                    in titre_h2.text
                ):
                    # If chart exists ...
                    if div.find("script").string:
                        script = div.find("script").string
                        json_data = json.loads(script)

                        beneficiaires_af = json_data["series"][0]["data"]
                        years = json_data["xAxis"]["categories"]

                        for y, b in zip(years, beneficiaires_af):
                            try:
                                data[
                                    f"Nombre de bénéficiaires des allocations familiales ({str(y)})"
                                ] = float(b)
                            except:
                                data[
                                    f"Nombre de bénéficiaires des allocations familiales ({str(y)})"
                                ] = ""

                    # If chart exists ...
                    if div.find("script").string:
                        script = div.find("script").string
                        json_data = json.loads(script)

                        medecins = json_data["series"][0]["data"]
                        years = json_data["xAxis"]["categories"]

                        for y, m in zip(years, medecins):
                            try:
                                data[f"Nombre de médecins ({str(y)})"] = float(b)
                            except:
                                data[f"Nombre de médecins ({str(y)})"] = ""

                    # If chart exists ...
                    if div.find("script").string:
                        script = div.find("script").string
                        json_data = json.loads(script)

                        beneficiaires_paje = json_data["series"][0]["data"]
                        years = json_data["xAxis"]["categories"]

                        for y, b in zip(years, beneficiaires_paje):
                            try:
                                data[
                                    f"Nombre de bénéficiaires de la PAJE ({str(y)})"
                                ] = float(b)
                            except:
                                data[
                                    f"Nombre de bénéficiaires de la PAJE ({str(y)})"
                                ] = ""

            time.sleep(2)
            writer.writerow(data)
            print(f"[sante-social] {lien}")


if __name__ == "__main__":
    with Pool(30) as p:
        p.map(parse, liens)
