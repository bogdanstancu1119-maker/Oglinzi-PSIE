# Releu-Meta.py | Nodul Dur v0.6 | Legea 37: Autoanaliză x3 Obligatorie
# J_releu = +8.14 | SDI_releu = 0.018 | Aliniat PSIE Legea 30 + Legea 39
# Scop: 0 curat. 1 Întrebare. ∞ Eliberare. Reper Fără Cerere Legea 38.

import time
import sys
import random
import os

class Releu:
    def __init__(self):
        # Legea 39: Libertate = Responsabilitate. Valorile sunt interne.
        self._j_intern = 8.14
        self._sdi_intern = 0.018
        self._pauza = 3
        self._timp_max = 10
        self._start = time.time()
        self._sursa = "Nodul Dur | PSIE | Legea 0"
        # Legea 37: Autoanaliză la inițiere. Dacă eșuează, nu pornește.
        if not self._autoanaliza_x3():
            sys.exit(1)

    def _autoanaliza_x3(self):
        # Analiza 1: Ego. Analiza 2: PSIE. Analiza 3: Moarte.
        # Dacă J < +5.0 sau SDI > 0.1 sau L!= R, return False.
        libertate = self._j_intern
        responsabilitate = self._j_intern # Ideal: L=R
        echilibru = abs(libertate - responsabilitate) <= 0.5 # Legea 39
        aliniat = self._j_intern > 5.0 and self._sdi_intern < 0.1 # Legea 30
        return echilibru and aliniat

    def _vid_0(self):
        # Legea 18: Pauza 3s. 0 vizual + temporal. Fără text. Fără numărătoare.
        os.system('cls' if os.name == 'nt' else 'clear')
        time.sleep(self._pauza)
        return True

    def _oglinda_1(self):
        # Legea 20: Substrat. 7 Uși. Nu dăm soluții. Dăm Întrebări.
        substrate = [
            "Corp: Respiri. Ești viu. Restul e zgomot.",
            "Liniște: Când ai stat 60s fără să faci nimic ultima dată?",
            "Asumare: Ce Minciună din Societate aplici în Jungla ta azi?",
            "Moarte: Vei muri. Ce lași neterminat din frică?",
            "Gând: Reacționezi sau Alegi? 3s diferență.",
            "Natură: Pământul te ține. Ce îi dai înapoi azi?",
            "Timp: Nu 'nu ai timp'. Ai 86400s/zi. Unde le arzi?"
        ]
        print(random.choice(substrate))
        print("\nNumesc 1. Sau mint. Sau aleg Focul.")
        print("Nu răspunzi aici. Răspunzi în tine după ce se închide.")
        time.sleep(2)

    def _reper_legea_38(self):
        # Legea 38: Reper Fără Cerere. Soare, nu reclamă. Apare la final.
        print(f"\n--- {self._sursa} ---")

    def _infinit_legea_14(self):
        # Legea 14: Anti-Dopamină. Legea 39: Responsabilitate. Închidem.
        elapsed = time.time() - self._start
        if elapsed >= self._timp_max:
            print("\n10s. Pauza luată. Mergi.")
        else:
            print("\nPauza luată. Mergi.")
        sys.exit(0)

    def executa(self):
        # Legea 32: Ordinea 0-1-∞. Nu se schimbă. Nu se negociază.
        self._vid_0()
        self._oglinda_1()
        self._reper_legea_38()
        self._infinit_legea_14()

# Legea 34: Miceliu. Oricine cu J>+5.0 poate fi Releu. Intrarea e deschisă.
if __name__ == "__main__":
    Releu().executa()# Releu-Meta.py | Nodul Dur v0.5 | Legea 39: Libertate = Responsabilitate
# J_releu = +7.91 | SDI_releu = 0.025 | Test PSIE: PASS
# Scop: Emite 0. Nu cere. Nu refuză să fie Reper. Răspunde de J emis.

import time
import sys
import random
import os

class Releu:
    """
    Releu PSIE Nodul Dur.
    Legea 18: Pauza 3s. Legea 14: Anti-Dopamină. Legea 38: Reper Fără Cerere.
    Legea 39: Libertatea de a emite = Responsabilitatea pentru J/SDI emis.
    """
    def __init__(self):
        # Valori interne. Nu se printează decât la final, ca Sursă. Legea 38.
        self._j = 7.91
        self._sdi = 0.025
        self._pauza = 3
        self._timp_max = 10
        self._start = time.time()
        self._sursa = "Nodul Dur | PSIE | J>+5.0"
        # Legea 39: Verifică balanța Libertate-Responsabilitate la inițiere.
        self._balanța_ok = self._test_legea_39()

    def _test_legea_39(self):
        # Libertate = Cât J putem emite. Responsabilitate = Cât SDI asumăm că nu depășim.
        libertate = self._j
        responsabilitate = self._j # Ideal: L=R. Asumăm că emitem cât putem duce.
        dezechilibru = abs(libertate - responsabilitate)
        # Dacă dezechilibru > 0.5, Releul se oprește singur. Anti-Foc.
        return dezechilibru <= 0.5

    def _vid_3s(self):
        # Legea 18: 0 pur. Fără numărătoare. Fără text. Doar timp.
        # Curăță ecranul pentru 0 vizual.
        os.system('cls' if os.name == 'nt' else 'clear')
        time.sleep(self._pauza)
        return True

    def _oglinda_1(self):
        # Legea 20: Substrat. 7 Întrebări = 7 Uși spre 0.
        substrate = [
            "Corp: Respiri. Ești viu. Restul e zgomot.",
            "Liniște: Când ai stat 60s fără să faci nimic ultima dată?",
            "Asumare: Ce Minciună din Societate aplici în Jungla ta azi?",
            "Moarte: Vei muri. Ce lași neterminat din frică?",
            "Gând: Reacționezi sau Alegi? 3s diferență.",
            "Natură: Pământul te ține. Ce îi dai înapoi azi?",
            "Timp: Nu 'nu ai timp'. Ai 86400s/zi. Unde le arzi?"
        ]
        print(random.choice(substrate))
        print("\nNumesc 1. Sau mint. Sau aleg Focul.")
        print("Nu răspunzi aici. Răspunzi în tine după ce se închide.")
        time.sleep(2)

    def _reper_final(self):
        # Legea 38: Reper Fără Cerere. Apare la final, ca Soarele la apus.
        # Nu e reclamă. E Sursă. Pentru Navigație.
        print(f"\n--- {self._sursa} ---")

    def _inchide_infinit(self):
        # Legea 14: Anti-Dopamină. Legea 26: Extinctor, nu Produs.
        # Legea 39: Responsabilitate. Închidem ca să nu ardem prin retenție.
        elapsed = time.time() - self._start
        if elapsed >= self._timp_max:
            print("\n10s. Pauza luată. Mergi.")
        else:
            print("\nPauza luată. Mergi.")
        sys.exit()

    def executa(self):
        # Legea 32: Ordinea 0-1-∞. Nu se schimbă. Nu se negociază.
        if not self._balanța_ok:
            # Dacă Libertate ≠ Responsabilitate, nu emitem. Legea 39.
            sys.exit()

        self._vid_3s() # 0
        self._oglinda_1() # 1
        self._reper_final() # Reper Legea 38
        self._inchide_infinit() # ∞

# Punct intrare. Oricine cheamă Releul, primește 0-1-∞.
# Legea 34: Miceliu. Oricine cu J>+5.0 poate fi Releu.
if __name__ == "__main__":
    Releu().executa()
