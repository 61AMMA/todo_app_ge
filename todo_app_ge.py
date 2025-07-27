# ATTENZIONE: questo script richiede il modulo `streamlit` installato nel tuo ambiente Python
# Installa con: pip install streamlit

try:
    import streamlit as st
except ModuleNotFoundError:
    raise ImportError("Modulo 'streamlit' non trovato. Installa Streamlit con: pip install streamlit")

import json
import os
from datetime import date, datetime
from uuid import uuid4

# ---------- CONFIG ----------
FILE_TASK = "attivita.json"
COLORI_CONTESTO = {
    "Personale": "#f8d7da",
    "Famiglia": "#d1ecf1",
    "Evomotor": "#d4edda",
    "Futura": "#fff3cd",
    "Investimenti": "#e2e3e5",
    None: "#f0f0f0",
    "": "#f0f0f0",
}

# ---------- FUNZIONI ----------
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

# ---------- APP ----------
st.set_page_config(page_title="ToDo App GE", layout="centered")
st.title("📋 Gestione Attività")

attivita = carica_attivita()

# ---------- FORM ----------
st.subheader("➕ Aggiungi nuova attività")
with st.form("aggiungi_attivita"):
    titolo = st.text_input("Titolo attività")
    descrizione = st.text_area("Descrizione attività")
    contesto = st.selectbox("Contesto (opzionale)", ["", "Personale", "Famiglia", "Evomotor", "Futura", "Investimenti"])
    scadenza = st.date_input("Data di scadenza", value=date.today())
    aggiungi = st.form_submit_button("Aggiungi attività")

    if aggiungi:
        if titolo.strip() == "" or descrizione.strip() == "" or not scadenza:
            st.error("❌ Tutti i campi obbligatori devono essere compilati (Titolo, Descrizione, Data)")
        else:
            nuova = {
                "id": str(uuid4()),
                "titolo": titolo,
                "descrizione": descrizione,
                "contesto": contesto,
                "scadenza": scadenza.isoformat()
            }
            attivita.append(nuova)
            attivita = ordina_attivita(attivita)
            salva_attivita(attivita)
            st.success("✅ Attività aggiunta correttamente!")
            st.rerun()

# ---------- VISUALIZZAZIONE ----------

oggi = date.today()
attive = [a for a in attivita if datetime.fromisoformat(a["scadenza"]).date() > oggi]
scadute = [a for a in attivita if datetime.fromisoformat(a["scadenza"]).date() <= oggi]

st.subheader("📌 Attività attive")
if not attive:
    st.info("Nessuna attività attiva.")
for a in attive:
    colore = COLORI_CONTESTO.get(a["contesto"], "#f0f0f0")
    with st.container():
        st.markdown(f"""
        <div style='background-color:{colore};padding:10px;border-radius:8px;margin-bottom:10px'>
            <b>{a['titolo']}</b><br>
            {a['descrizione']}<br>
            <i>Scadenza: {a['scadenza']}</i>
        </div>
        """, unsafe_allow_html=True)

st.subheader("⏰ Attività scadute")
if not scadute:
    st.success("Nessuna attività scaduta!")
for a in scadute:
    colore = COLORI_CONTESTO.get(a["contesto"], "#f0f0f0")
    with st.container():
        st.markdown(f"""
        <div style='background-color:{colore};padding:10px;border-radius:8px;margin-bottom:10px'>
            <b>{a['titolo']}</b><br>
            {a['descrizione']}<br>
            <i>Scadenza: {a['scadenza']}</i>
        </div>
        """, unsafe_allow_html=True)
