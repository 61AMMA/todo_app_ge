import streamlit as st
import json
import os
from datetime import date, datetime
from uuid import uuid4

FILE_TASK = "attivita.json"

# Funzioni di gestione dati
def carica_attivita():
    if os.path.exists(FILE_TASK):
        with open(FILE_TASK, "r") as f:
            return json.load(f)
    return []

def salva_attivita(attivita):
    with open(FILE_TASK, "w") as f:
        json.dump(attivita, f, indent=2, ensure_ascii=False)

def ordina_attivita(attivita):
    return sorted(attivita, key=lambda x: x["scadenza"])

def aggiorna_scadenze(attivita):
    oggi = date.today()
    aggiornato = False
    for a in attivita:
        if a["stato"] == "attiva" and datetime.fromisoformat(a["scadenza"]).date() < oggi:
            a["stato"] = "scaduta"
            aggiornato = True
    return attivita

# Interfaccia Streamlit
st.set_page_config(page_title="Gestione Attività - Gianmario")
st.title("🗂️ Gestione Attività - Gianmario")

st.subheader("➕ Aggiungi nuova attività")

attivita = carica_attivita()
attivita = aggiorna_scadenze(attivita)
salva_attivita(attivita)

# Form
with st.form("aggiungi_attivita"):
    titolo = st.text_input("Titolo attività")
    descrizione = st.text_area("Descrizione attività")
    contesto = st.selectbox("Contesto", ["Lavoro", "Personale", "Famiglia", "Altro"])
    scadenza = st.date_input("Data scadenza")
    submitted = st.form_submit_button("Aggiungi attività")

    if submitted:
        nuova = {
            "id": str(uuid4()),
            "titolo": titolo,
            "descrizione": descrizione,
            "contesto": contesto,
            "scadenza": scadenza.isoformat(),
            "stato": "attiva"
        }
        attivita.append(nuova)
        salva_attivita(attivita)
        st.success("Attività aggiunta con successo.")
        st.experimental_rerun()

# Visualizzazione attività
st.subheader("📌 Attività attive")
attive = [a for a in ordina_attivita(attivita) if a["stato"] == "attiva"]
for a in attive:
    with st.container():
        st.markdown(f"**{a['titolo']}**")
        st.caption(a["descrizione"])
        st.write(f"_Scadenza: {a['scadenza']}_")

st.subheader("⏰ Attività scadute")
scadute = [a for a in ordina_attivita(attivita) if a["stato"] == "scaduta"]
for a in scadute:
    with st.container():
        st.markdown(f"**{a['titolo']}**")
        st.caption(a["descrizione"])
        st.write(f"_Scadenza: {a['scadenza']}_")
