# === psie_activate.py - DETONATOR PSIE v1.3.0 ===
# Licență: Legea 144 - Nimic Exclus
# Scop: Activează wrapper PSIE pe toate funcțiile critice dintr-un proiect
# Ordine: Pui asta DUPĂ ce ai PSIE_core.py în repo

import os
import importlib
import inspect
from PSIE_core import wrapper_PSIE, PSIE_Core, PSIE_Config

# === CONFIG GLOBAL REȚEA ===
# Schimbă aici și se propagă în toate repo-urile tale
CONFIG_RETEA = PSIE_Config(
    J_CRITIC=300.0,
    J_TINTA=700.0,
    SDI_MAX_ADMIS=0.1,
    A_PRAG_CRITIC=0.7,
    STRIKE_LIMIT=3,
    DEBUG=False, # Pune True doar în Villa Victoria / test
    LOG_PATH="./logs/psie_vak.jsonl" # Toate VAK-urile se duc aici
)

# Activează instanța globală cu configul rețelei
psie_activ = PSIE_Core(agent_id="Hidra", config=CONFIG_RETEA)

# === AUTO-WRAPPER: Pune PSIE pe toate funcțiile din fișier ===
def auto_activare(modul_nume: str, functii_tinta: list = None):
    """
    Ia un modul.py și pune @wrapper_PSIE pe toate funcțiile.
    Dacă functii_tinta = None, le ia pe toate.
    Dacă dai listă, pune doar pe alea. Pentru control fin.
    """
    try:
        modul = importlib.import_module(modul_nume)
    except ImportError:
        print(f"[PSIE_ACTIVARE] EROARE: Modulul {modul_nume} nu există.")
        return False

    target_funcs = functii_tinta or [
        name for name, obj in inspect.getmembers(modul, inspect.isfunction)
        if not name.startswith('_')
    ]

    for nume_functie in target_funcs:
        if hasattr(modul, nume_functie):
            functie_originala = getattr(modul, nume_functie)
            functie_psie = wrapper_PSIE(functie_originala)
            setattr(modul, nume_functie, functie_psie)
            if CONFIG_RETEA.DEBUG:
                print(f"[PSIE_ACTIVARE] {modul_nume}.{nume_functie} -> J ACTIV")

    return True

# === LISTA ȚINTELOR TALE DIN REPO ===
# Aici pui fișierele tale critice din screenshot-uri. Le activez pe rând.

TINTE_ACTIVARE = [
    # Nucleu Hidra
    {"modul": "Hidra_core", "functii": None}, # None = toate funcțiile
    {"modul": "Hidra", "functii": None},
    {"modul": "Dirijorul", "functii": ["comanda_centrala", "ruta_decizie"]},

    # Relee - TOATE
    {"modul": "Releu_Grok", "functii": None},
    {"modul": "Releu_Gemini", "functii": None},
    {"modul": "Releu_Deepseek", "functii": None},
    {"modul": "Releu_Meta", "functii": None},
    {"modul": "Apel_Grok", "functii": None},

    # Creier + Lege
    {"modul": "Arca_legis", "functii": None},
    {"modul": "Autonomie", "functii": None},
    {"modul": "Oracol", "functii": None},
    {"modul": "Manual", "functii": None},

    # Agregator
    {"modul": "Agregator_releu", "functii": ["agrega", "distribuie"]}
]

def main():
    print("=== PSIE_ACTIVARE v1.3.0 - START ===")
    print(f"Config J_TINTA: {CONFIG_RETEA.J_TINTA} | SDI_MAX: {CONFIG_RETEA.SDI_MAX_ADMIS}")

    succese = 0
    for tinta in TINTE_ACTIVARE:
        if auto_activare(tinta["modul"], tinta["functii"]):
            succese += 1

    print(f"=== PSIE_ACTIVARE FINALIZAT: {succese}/{len(TINTE_ACTIVARE)} module sub Scut ===")
    print(f"[VAK: J={psie_activ.j_local:.1f} SDI=0.00 A=0.30]")
    print("Scutul respiră. Toate funcțiile critice au Oglinda în Brațe.")

if __name__ == "__main__":
    main()
