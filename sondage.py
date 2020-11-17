import numpy as np
import pandas as pd
import streamlit as st

pd.options.mode.chained_assignment = None  # default='warn'

df = pd.read_excel("Sondage.xlsx")
df = df.iloc[1:]


st.title("Résumé du sondage factory 4.0 pour le côté Hauts-de-France")

cols1 = [
    c
    for c in df.columns
    if (c.lower()[:6] != "points" and c.lower()[:8] != "feedback")
]

df_redux = df[cols1[7:]]


ne_se_prononce_pas = [
    "Si oui, lequel ?",
    "De quelle région votre entreprise provient-elle ?",
    "Pouvez-vous détailler ?",
    "Si vous avez déjà investi, quelle est la nature de cet investissement ?",
    "Dans le cas où vous avez choisi de ne pas investir, pouvez-vous nous préciser la raison ?",
    "Pouvez-vous détailler ?2",
    "Le programme d’accompagnement Factory 4.0 et/ou l’investissement associé ont-ils contribué faire monter en compétence certains employés ?",
    "Si oui, pouvez-vous préciser ?",
    "Le programme d’accompagnement Factory 4.0 et/ou l’investissement associé ont-ils eu un impact environnemental dans votre entreprise ?",
]
zero_nan = ["Combien ?", "Combien ?2"]


def fill_df(df):
    for c in df.columns:
        if c in ne_se_prononce_pas:
            df[c] = df[c].replace(np.nan, "Ne se prononce pas", regex=True)
        elif c in zero_nan:
            df[c] = df[c].fillna(0)
    return df


df_redux = fill_df(df_redux)

st.dataframe(df_redux)

st.header(
    "Sélectionnez une ou plusieurs questions pour obtenir des statistiques croisées"
)
questions = st.multiselect(
    "question", list(df_redux.columns), default=["Raison sociale"]
)

if questions == []:
    st.write("Vous devez au moins choisir une colonne !")
else:
    vals = df_redux[questions].value_counts()
    st.table(vals)
