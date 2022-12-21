import numpy as np
import pandas as pd
import argparse

from src.tools import calcul_recommandation, calcul_conclusion

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Récupère le numéro du département.")
    parser.add_argument(
        "dep", metavar="dep", type=int, nargs="+", help="Le numéro du département"
    )

    dataset = pd.read_csv(
        "C:/Users/bapti/OneDrive/Bureau/Sorbonne/Linux/projet/data/bdd_finale.csv"
    )

    dep = parser.parse_args().dep
    if dep not in dataset.DEP.unique():
        raise ValueError("Le département spécifié n'est pas dans la base de données.")

    nb_ent = (
        dataset.groupby(by="DEP").sum().loc[:, "Sum"].loc[dep]
        - dataset.groupby(by="DEP").sum().loc[:, "Micro"].loc[dep]
    ).values[0]
    nb_jobs = (dataset.groupby(by="DEP").mean().loc[:, "SNHM14"].loc[dep]).values[0]

    print(
        f"\n{nb_ent} entreprises dans votre département pour un salaire médian de {nb_jobs:.2f}€ de l'heure.\n"
    )
    print(" L'analyse de notre robot JobFinder : ".center(100, "="))
    print("\n")
    message_emp, score_emp = calcul_recommandation(
        data=dataset.groupby(by="DEP").sum().loc[:, "Sum"]
        - dataset.groupby(by="DEP").sum().loc[:, "Micro"],
        x=(dataset.groupby(by="DEP").sum().loc[:, "Sum"].loc[dep]).values[0]
        - (dataset.groupby(by="DEP").sum().loc[:, "Micro"].loc[dep]).values[0],
        msg={
            0: "C'est une région avec (très) peu d'emplois.",
            1: "Il n'y à pas beaucoup d'emplois dans cette département.",
            2: "Le nombre d'emploi ne devrait pas être un problème dans votre département.",
            3: "Il y'a un très grand nombre d'emplois disponibles dans votre département, vous avez l'embarras du choix !",
        },
    )
    print(f"- Au niveau du nombre d'emplois : {message_emp}")
    message_rem, score_rem = calcul_recommandation(
        data=dataset.groupby(by="DEP").sum().loc[:, "SNHM14"].loc[dep],
        x=dep,
        msg={
            0: "Comptez vos deniers, ils pourraient être les derniers.",
            1: "Votre région n'est pas dans le haut du classement niveau salaire :(.",
            2: "Le salaire est satisfaisant dans votre département.",
            3: "Crésus n'a qu'a bien se tenir, vous êtes dans un département fortuné !",
        },
    )
    print(f"- Au niveau de la rémunération : {message_rem}")
    print(f"- Au global : {calcul_conclusion(score_emp + score_rem)}")
