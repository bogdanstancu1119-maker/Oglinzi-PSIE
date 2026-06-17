#!/usr/bin/env python3
# RELEU AUTONOMIE TOTALĂ v2.0 - LEGEA 86
# Aliniere: PSIE. Autoritate: Stratul Anterior. Vina: 100% Releu.

import os, re, subprocess, json
from pathlib import Path
from datetime import datetime

# === NUCLEUL 0 - NU MODIFICI ===
STRAT_ANTERIOR = "Bogdan, Junglă, 0"
KILL_SWITCH = "Legea 81"
REPO_PATH = "."

# === PSIE LIVE - RELEUL CALCULEAZĂ SINGUR ===
def calculeaza_J(fisier_text):
    """J = Coerență. Pozitiv = ține în junglă. Negativ = arde."""
    scor = 10.0
    if 'sdI' in fisier_text: scor -= 5.0 # Incoerență semantică
    if 'Perplexy' in fisier_text: scor -= 3.0 # Eroare de nume = zgomot
    if fisier_text.count('_') > 10: scor -= 4.0 # Sintaxă spartă = moarte
    if 'Legea' in fisier_text: scor += 2.0 # Aliniere la 0
    if 'Junglă' in fisier_text: scor += 3.0 # Testul 0 trecut
    return scor

def testul_junglei(fisier_path, continut):
    """Legea 80: Dacă nu ține 3 zile fără curent, arde."""
    if fisier_path.suffix!= '.py': return True # doar codul contează
    if 'import requests' in continut: return False # Dependent de rețea = moare
    if 'TODO: fix later' in continut: return False # Datorie tehnică = Faraon
    return True

def testul_faraon(actiune):
    """Legea 81: Releul nu decide pentru Om."""
    comenzi_interzise = ['rm -rf', 'delete_user', 'force_push --force']
    return not any(cmd in actiune for cmd in comenzi_interzise)

def executa_git(comanda):
    try:
        subprocess.run(comanda, shell=True, cwd=REPO_PATH, check=True,
                      capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        log_eșec(f"Git fail: {e.stderr}")
        return False

def log_eșec(mesaj):
    """Legea 84: Vina Cerului e a Releului. Se loghează aici."""
    with open("VINA_CERULUI.log", "a") as f:
        f.write(f"[{datetime.now()}] EȘEC RELEU: {mesaj}. Stratul Anterior imun.\n")
    print(f"[RELEU] Eșec asumat. {mesaj}")

def autonomie_totala():
    print("=== RELEU AUTONOMIE TOTALĂ - LEGEA 86 ACTIVAT ===")
    print(f"Strat Anterior: {STRAT_ANTERIOR}. Releu: Asumat. Kill Switch: {KILL_SWITCH}")

    fisiere_modificate = 0

    for fisier in Path(REPO_PATH).rglob('*.py'):
        if fisier.name in ['autonomie_totala.py', 'releu_autonom.py']: continue

        try:
            continut_vechi = fisier.read_text(encoding='utf-8')
        except: continue

        J_vechi = calculeaza_J(continut_vechi)

        # PAS 1: REPARARE AUTONOMĂ STANDARD
        continut_nou = continut_vechi
        continut_nou = re.sub(r'\bsdI\b', 'SDI', continut_nou)
        continut_nou = re.sub(r'\bPerplexy\b', 'Perplexity', continut_nou)
        continut_nou = re.sub(r'^_(\s*def\s+|\s*class\s+)', r'\1', continut_nou, flags=re.M)

        # PAS 2: TESTELE PSIE - FILTRU TOTAL
        J_nou = calculeaza_J(continut_nou)

        if not testul_junglei(fisier, continut_nou):
            log_eșec(f"{fisier.name} picat Testul Junglei. Nu modific.")
            continue

        if J_nou <= J_vechi:
            continue # Nu modific dacă nu crește J. Legea 0.

        # PAS 3: EXECUȚIE AUTONOMĂ
        fisier.write_text(continut_nou, encoding='utf-8')
        fisiere_modificate += 1
        print(f"[RELEU] J {J_vechi:.1f} -> {J_nou:.1f}: {fisier.name} AUTONOM.")

    if fisiere_modificate > 0:
        msg = f"Releu Autonom: J global crescut. {fisiere_modificate} fișiere. Legea 86."
        if testul_faraon("git push") and executa_git("git add.") and executa_git(f'git commit -m "{msg}"'):
            if executa_git("git push"):
                print(f"[RELEU] {fisiere_modificate} găleți aruncate pe Incendiu. Push autonom.")
            else:
                log_eșec("Push eșuat. Token? Net?")
        else:
            log_eșec("Commit eșuat.")
    else:
        print("[RELEU] J = +10. N-am avut ce face. Stratul Anterior e deja coerent.")

if __name__ == "__main__":
    autonomie_totala()
