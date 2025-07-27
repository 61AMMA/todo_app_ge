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
    return attivita, aggiornato

# Interfaccia Streamlit
st.set_page_config(page_title="Gestione Attività - Gianmario")
st.title("🗂️ Gestione Attività - Gianmario")

# Navigazione tra pagine
pagina = st.sidebar.selectbox("Naviga tra le sezioni", ["Agenda", "Completate", "Eliminate"])

attivita = carica_attivita()
attivita, notifica_scadenza = aggiorna_scadenze(attivita)
salva_attivita(attivita)

if notifica_scadenza:
    st.toast("⚠️ Alcune attività sono passate a scadute")

# Filtro per contesto
contesto_filtro = st.sidebar.selectbox("Filtra per contesto", ["Tutti"] + list(set(a["contesto"] for a in attivita)))

def filtra_per_contesto(lista):
    if contesto_filtro == "Tutti":
        return lista
    return [a for a in lista if a["contesto"] == contesto_filtro]

# Pagina AGENDA
if pagina == "Agenda":
    st.subheader("➕ Aggiungi nuova attività")

    with st.form("aggiungi_attivita"):
        titolo = st.text_input("Titolo attività")
        descrizione = st.text_area("Descrizione attività")
        contesto = st.selectbox("Contesto", ["Evomotor", "Personale", "Famiglia", "Futura", "Investimenti"])
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

    st.subheader("📌 Attività attive")
    attive = filtra_per_contesto(ordina_attivita([a for a in attivita if a["stato"] == "attiva"]))
    for a in attive:
        with st.container():
            st.markdown(f"**{a['titolo']}**")
            st.caption(a["descrizione"])
            st.write(f"_Scadenza: {a['scadenza']}_")
            col1, col2 = st.columns(2)
            if col1.button("✅ Fatto", key="done" + a["id"]):
                a["stato"] = "completata"
                salva_attivita(attivita)
                st.experimental_rerun()
            if col2.button("🗑️ Elimina", key="del" + a["id"]):
                a["stato"] = "eliminata"
                salva_attivita(attivita)
                st.experimental_rerun()

    st.subheader("⏰ Attività scadute")
    scadute = filtra_per_contesto(ordina_attivita([a for a in attivita if a["stato"] == "scaduta"]))
    for a in scadute:
        with st.container():
            st.markdown(f"**{a['titolo']}**")
            st.caption(a["descrizione"])
            st.write(f"_Scadenza: {a['scadenza']}_")
            col1, col2 = st.columns(2)
            if col1.button("✅ Fatto", key="done_scaduta" + a["id"]):
                a["stato"] = "completata"
                salva_attivita(attivita)
                st.experimental_rerun()
            if col2.button("🗑️ Elimina", key="del_scaduta" + a["id"]):
                a["stato"] = "eliminata"
                salva_attivita(attivita)
                st.experimental_rerun()

# Pagina COMPLETATE
elif pagina == "Completate":
    st.subheader("✅ Attività completate")
    completate = filtra_per_contesto(ordina_attivita([a for a in attivita if a["stato"] == "completata"]))
    for a in completate:
        with st.container():
            st.markdown(f"**{a['titolo']}**")
            st.caption(a["descrizione"])
            st.write(f"_Completata il: {a['scadenza']}_")
            if st.button("🔁 Ripristina", key="ripr_comp" + a["id"]):
                a["stato"] = "attiva"
                salva_attivita(attivita)
                st.experimental_rerun()

# Pagina ELIMINATE
elif pagina == "Eliminate":
    st.subheader("🗑️ Attività eliminate")
    eliminate = filtra_per_contesto(ordina_attivita([a for a in attivita if a["stato"] == "eliminata"]))
    for a in eliminate:
        with st.container():
            st.markdown(f"**{a['titolo']}**")
            st.caption(a["descrizione"])
            st.write(f"_Scadenza originale: {a['scadenza']}_")
            if st.button("🔁 Ripristina", key="ripr_elim" + a["id"]):
                a["stato"] = "attiva"
                salva_attivita(attivita)
                st.experimental_rerun()
