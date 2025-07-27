try:
    import streamlit as st
except ImportError:
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

# ---------- UI ----------
st.set_page_config(page_title="ToDo App GE", layout="wide")
st.title("🗓️ Gestione Attività - Gianmario")

pagina = st.sidebar.selectbox("Seleziona pagina", ["Agenda", "Completate", "Eliminate"])
attivita = carica_attivita()
oggi = date.today()

# Aggiorna stato scadute
def aggiorna_scadenze():
    aggiornato = False
    for a in attivita:
        if a["stato"] == "attiva" and datetime.fromisoformat(a["scadenza"]).date() < oggi:
            a["stato"] = "scaduta"
            aggiornato = True
    if aggiornato:
        st.warning("⚠️ Alcune attività sono appena passate a scadute.")

aggiorna_scadenze()

if pagina == "Agenda":
    with st.form("nuova_attivita"):
        st.subheader("➕ Aggiungi nuova attività")
        titolo = st.text_input("Titolo attività")
        descrizione = st.text_area("Descrizione attività")
        contesto = st.selectbox("Contesto", ["", "Personale", "Famiglia", "Evomotor", "Futura", "Investimenti"])
        scadenza = st.date_input("Data scadenza", min_value=oggi)
        aggiungi = st.form_submit_button("Aggiungi attività")

        if aggiungi:
            if titolo and descrizione and scadenza:
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
            else:
                st.error("Compila tutti i campi obbligatori.")

    contesto_filtrato = st.selectbox("Filtra per contesto", ["Tutti"] + list(COLORI_CONTESTO.keys()))

    def mostra_task(lista, titolo):
        st.subheader(titolo)
        for a in lista:
            if contesto_filtrato != "Tutti" and a["contesto"] != contesto_filtrato:
                continue
            bg = COLORI_CONTESTO.get(a["contesto"], "#ffffff")
            with st.container():
                st.markdown(f"""
                <div style='background-color:{bg}; padding:10px; border-radius:10px;'>
                    <strong>{a['titolo']}</strong><br>
                    <em>{a['descrizione']}</em><br>
                    <small>Scadenza: {a['scadenza']} - Contesto: {a['contesto']}</small><br>
                </div>
                """, unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Fatto", key="done" + a["id"]):
                        a["stato"] = "completata"
                        salva_attivita(attivita)
                        st.experimental_rerun()
                with col2:
                    if st.button("🗑️ Elimina", key="del" + a["id"]):
                        a["stato"] = "eliminata"
                        salva_attivita(attivita)
                        st.experimental_rerun()

    attive = [a for a in ordina_attivita(attivita) if a["stato"] == "attiva"]
    scadute = [a for a in ordina_attivita(attivita) if a["stato"] == "scaduta"]

    mostra_task(attive, "🟢 Attività Attive")
    mostra_task(scadute, "🔴 Attività Scadute")

elif pagina == "Completate":
    st.subheader("✅ Attività Completate")
    completate = [a for a in ordina_attivita(attivita) if a["stato"] == "completata"]
    for a in completate:
        bg = COLORI_CONTESTO.get(a["contesto"], "#ffffff")
        with st.container():
            st.markdown(f"""
            <div style='background-color:{bg}; padding:10px; border-radius:10px;'>
                <strong>{a['titolo']}</strong> - <em>{a['descrizione']}</em><br>
                <small>Scadenza: {a['scadenza']} - Contesto: {a['contesto']}</small>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔁 Ripristina", key="res-com" + a["id"]):
                a["stato"] = "attiva"
                salva_attivita(attivita)
                st.experimental_rerun()

elif pagina == "Eliminate":
    st.subheader("🗑️ Attività Eliminate")
    eliminate = [a for a in ordina_attivita(attivita) if a["stato"] == "eliminata"]
    for a in eliminate:
        bg = COLORI_CONTESTO.get(a["contesto"], "#ffffff")
        with st.container():
            st.markdown(f"""
            <div style='background-color:{bg}; padding:10px; border-radius:10px;'>
                <strong>{a['titolo']}</strong> - <em>{a['descrizione']}</em><br>
                <small>Scadenza: {a['scadenza']} - Contesto: {a['contesto']}</small>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔁 Ripristina", key="res-eli" + a["id"]):
                a["stato"] = "attiva"
                salva_attivita(attivita)
                st.experimental_rerun()
