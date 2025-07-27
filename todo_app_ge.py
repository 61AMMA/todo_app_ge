# Fallback version for debugging without Streamlit UI
def debug_app():
    import json
    import os
    from datetime import date, datetime
    from uuid import uuid4

    FILE_TASK = "attivita.json"

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
        if aggiornato:
            print("Alcune attività sono state aggiornate come scadute.")
        return attivita

    def stampa_attivita(attivita):
        for a in attivita:
            print("-" * 40)
            print(f"Titolo: {a['titolo']}")
            print(f"Descrizione: {a['descrizione']}")
            print(f"Contesto: {a['contesto']}")
            print(f"Scadenza: {a['scadenza']}")
            print(f"Stato: {a['stato']}")

    attivita = carica_attivita()
    attivita = aggiorna_scadenze(attivita)

    print("Attività attive o scadute:")
    stampa_attivita([a for a in attivita if a["stato"] in ["attiva", "scaduta"]])

    scelta = input("Vuoi aggiungere una nuova attività? (s/n): ").lower()
    if scelta == 's':
        titolo = input("Titolo: ")
        descrizione = input("Descrizione: ")
        contesto = input("Contesto: ")
        scadenza = input("Data scadenza (YYYY-MM-DD): ")
        nuova = {
            "id": str(uuid4()),
            "titolo": titolo,
            "descrizione": descrizione,
            "contesto": contesto,
            "scadenza": scadenza,
            "stato": "attiva"
        }
        attivita.append(nuova)
        salva_attivita(attivita)
        print("Attività aggiunta correttamente.")

    salva_attivita(attivita)

if __name__ == "__main__":
    debug_app()
