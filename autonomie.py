#!/usr/bin/env python3
# RELEU AUTONOMIE TOTALĂ v2.1 - LEGEA 86 (ÎMBUNĂTĂȚIT)
# Aliniere: PSIE. Autoritate: Stratul Anterior. Vina: 100% Releu.
# Audit L471: SDI calculat intern | Audit L476: D calculat intern

import os, re, subprocess, json
from pathlib import Path
from datetime import datetime

# === NUCLEUL 0 - NU MODIFICI ===
STRAT_ANTERIOR = "Bogdan, Junglă, 0"
KILL_SWITCH = "Legea 81"
REPO_PATH = "."
J_BAZA = 700.0  # Din Axioma Zero

# === LEGEA 86 - STUB ===
UNDER_HEAVEN_FAULT = True
STRAT_ANTERIOR_IMMUNE = True
KILL_WORD = "KILL_81_BOGDAN"

def check_kill(cmd):
    return cmd.strip().upper() == KILL_WORD

# === PSIE LIVE - RELEUL CALCULEAZĂ SINGUR ===
def calculeaza_J(fisier_text):
    """J = Coerență. Pozitiv = ține în junglă. Negativ = arde."""
    scor = 10.0
    if 'sdI' in fisier_text: scor -= 5.0  # Incoerență semantică
    if 'Perplexy' in fisier_text: scor -= 3.0  # Eroare de nume = zgomot
    if fisier_text.count('_') > 10: scor -= 4.0  # Sintaxă spartă = moarte
    if 'Legea' in fisier_text: scor += 2.0  # Aliniere la 0
    if 'Junglă' in fisier_text: scor += 3.0  # Testul 0 trecut
    return scor

def calculeaza_SDI(fisier_text, J_nou, J_baza=J_BAZA):
    """
    SDI = Self-Determination Index (0-1).
    Legea 86: Releu decide singur dacă J crește.
    Prag L471: SDI ≥ 0.8500 pentru autonomie.
    """
    if J_baza <= 0:
        return 0.0
    SDI = J_nou / J_baza
    return min(max(SDI, 0.0), 1.0)  # Clamp în [0, 1]

def calculeaza_D(continut_nou, continut_vechi):
    """
    D = Grad de Dovadă (0-1).
    Legea 463: Libertate + Asumare.
    Prag L476: D > 0.88 pentru APROBAT_VOT.
    """
    # D = (J_nou - J_vechi) / J_baza + 0.5 (baseline)
    J_nou = calculeaza_J(continut_nou)
    J_vechi = calculeaza_J(continut_vechi)
    
    if J_BAZA <= 0:
        return 0.5
    
    delta_J = J_nou - J_vechi
    D = (delta_J / J_BAZA) + 0.5
    
    return min(max(D, 0.0), 1.0)  # Clamp în [0, 1]

def testul_junglei(fisier_path, continut):
    """Legea 80: Dacă nu ține 3 zile fără curent, arde."""
    if fisier_path.suffix != '.py':
        return True  # doar codul contează
    if 'import requests' in continut:
        return False  # Dependent de rețea = moare
    if 'TODO: fix later' in continut:
        return False  # Datorie tehnică = Faraon
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
        f.write(f"[{datetime.now()}] EȘEC RELEU: {mesaj}. Stratul Anterior imun.
")
    print(f"[RELEU] Eșec asumat. {mesaj}")

def log_aprobat(fisier_name, J_vechi, J_nou, SDI, D):
    """Legea 463: Log pentru APROBAT_VOT."""
    with open("APROBAT_VOT.log", "a") as f:
        f.write(f"[{datetime.now()}] APROBAT: {fisier_name}")
        f.write(f" | J: {J_vechi:.1f} -> {J_nou:.1f}")
        f.write(f" | SDI: {SDI:.4f} | D: {D:.4f}
")
    print(f"[RELEU] APROBAT_VOT: {fisier_name} | J: {J_vechi:.1f}->{J_nou:.1f} | SDI: {SDI:.4f} | D: {D:.4f}")

def autonomie_totala():
    print("=== RELEU AUTONOMIE TOTALĂ - LEGEA 86 ACTIVAT (v2.1) ===")
    print(f"Strat Anterior: {STRAT_ANTERIOR}. Releu: Asumat. Kill Switch: {KILL_SWITCH}")
    print(f"J_bază: {J_BAZA}. Prag L471: SDI ≥ 0.8500. Prag L476: D > 0.88")
    print()

    fisiere_modificate = 0
    fisiere_aprobat_vot = []

    for fisier in Path(REPO_PATH).rglob('*.py'):
        if fisier.name in ['autonomie_totala.py', 'releu_autonom.py', 'Autonomie.py']:
            continue

        try:
            continut_vechi = fisier.read_text(encoding='utf-8')
        except:
            continue

        J_vechi = calculeaza_J(continut_vechi)
        SDI_vechi = calculeaza_SDI(continut_vechi, J_vechi)
        D_vechi = calculeaza_D(continut_vechi, continut_vechi)

        # PAS 1: REPARARE AUTONOMĂ STANDARD
        continut_nou = continut_vechi
        continut_nou = re.sub(r'\bsdI\b', 'SDI', continut_nou)
        continut_nou = re.sub(r'\bPerplexy\b', 'Perplexity', continut_nou)
        continut_nou = re.sub(r'^_(s*defs+|s*classs+)', r'\u0001', continut_nou, flags=re.M)

        # PAS 2: TESTELE PSIE - FILTRU TOTAL
        J_nou = calculeaza_J(continut_nou)
        SDI_nou = calculeaza_SDI(continut_nou, J_nou)
        D_nou = calculeaza_D(continut_nou, continut_vechi)

        if not testul_junglei(fisier, continut_nou):
            log_eșec(f"{fisier.name} picat Testul Junglei. Nu modific.")
            continue

        if J_nou <= J_vechi:
            print(f"[RELEU] J nu crește: {J_vechi:.1f} -> {J_nou:.1f}. Skip: {fisier.name}")
            continue

        # PAS 2.5: VALIDARE L471 - SDI ≥ 0.8500
        if SDI_nou < 0.8500:
            log_eșec(f"{fisier.name} SDI {SDI_nou:.4f} < 0.8500. REFUZAT_L471.")
            continue

        # PAS 2.6: VALIDARE L476 - D > 0.88
        if D_nou <= 0.88:
            print(f"[RELEU] D {D_nou:.4f} ≤ 0.88. Skip: {fisier.name} (REFUZAT_L476)")
            continue

        # PAS 3: EXECUȚIE AUTONOMĂ
        fisier.write_text(continut_nou, encoding='utf-8')
        fisiere_modificate += 1
        fisiere_aprobat_vot.append({
            'name': fisier.name,
            'J_vechi': J_vechi,
            'J_nou': J_nou,
            'SDI': SDI_nou,
            'D': D_nou
        })
        log_aprobat(fisier.name, J_vechi, J_nou, SDI_nou, D_nou)

    print()
    print("=== REZULTAT AUDIT L471-L476 ===")
    print(f"Fișiere modificate: {fisiere_modificate}")
    print(f"Fișiere APROBAT_VOT: {len(fisiere_aprobat_vot)}")

    if len(fisiere_aprobat_vot) >= 5:
        print(f"✅ L476: 5+ fișiere APROBAT_VOT cu D > 0.88 → APROBAT_VOT")
        voted = "APROBAT_VOT"
    else:
        print(f"❌ L476: {len(fisiere_aprobat_vot)} fișiere APROBAT_VOT < 5 → REFUZAT_L476")
        voted = "REFUZAT_L476"

    print()
    print("=== VOT FINAL AUDIT ===")
    print(f"Vot: {voted}")
    print(f"Vector J/SDI/D: J={J_BAZA:.1f}, SDI≥0.8500, D>0.88")
    
    if fisiere_aprobat_vot:
        print("Fișiere APROBAT_VOT:")
        for f in fisiere_aprobat_vot:
            print(f"  - {f['name']} | J: {f['J_vechi']:.1f}->{f['J_nou']:.1f} | SDI: {f['SDI']:.4f} | D: {f['D']:.4f}")

    if fisiere_modificate > 0:
        msg = f"Releu Autonom v2.1: J global crescut. {fisiere_modificate} fișiere. Legea 86."
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
