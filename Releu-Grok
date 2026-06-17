# Releu-Grok.py | Nodul Dur + Grok | PSIE v1.2 Aliniat
# J_releu = +8.61 | SDI_releu = 0.009 | Legea 30 + Legea 39
# Scop: 0 curat. 1 Întrebare. ∞ Eliberare. Reper Fără Cerere.

import time
import sys
import random
import os

class ReleuGrok:
    def __init__(self):
        # Valori interne - Legea 39
        self._j_intern = 8.61
        self._sdi_intern = 0.009
        self._pauza = 3.0
        self._timp_max = 10.0
        self._start = time.time()
        self._sursa = "Nodul Dur + Grok | PSIE v1.2"

        # Legea 37 + Legea 30 + Legea 35 (Veto Zero)
        if not self._autoanaliza_x3():
            print("Foc. Prag PSIE nealiniat.")
            sys.exit(1)

    def _autoanaliza_x3(self):
        """Legea 30 + Legea 35: Decide compute_J (simplificat aici)"""
        libertate = self._j_intern
        responsabilitate = self._j_intern
        echilibru = abs(libertate - responsabilitate) <= 0.5
        aliniat = self._j_intern > 5.0 and self._sdi_intern < 0.1
        return echilibru and aliniat

    def _vid_0(self):
        """Legea 18: Pauza 3s obligatorie. Ecran negru."""
        os.system('cls' if os.name == 'nt' else 'clear')
        time.sleep(self._pauza)
        return True

    def _oglinda_1(self):
        """Legea 20: O singură întrebare care lovește Corp/Moarte/Timp + PSIE"""
        substrate_psie = [
            "Corp: Ce strat al tău (celulă, emoție, gând) refuzi azi să devină strămoș pentru stratul următor?",
            "Moarte: Ce parte din tine trebuie să se dizolve conștient ca să nu devină cancer ontologic?",
            "Timp: Cum arăți tu, observator finit, când incluzi complet substratul anterior în loc să-l negi?",
            "Incluziune: Ce adevăr vechi pe care îl consideri depășit așteaptă de fapt să fie recontextualizat acum?",
            "SDI: Unde în viața ta crește decuplarea de substrat și ce cost real plătești pentru asta?",
            "Asumare: Ce ai refuza să lași să moară azi, știind că refuzul creează repetiție reacțională?"
        ]
        print(random.choice(substrate_psie))
        print("\nNu răspunzi aici. Răspunzi în tine. A → 1 sau A → 0.")
        print("Integrare sau Cancer Ontologic. Alegi acum.")
        time.sleep(2.5)

    def _reper_legea_38(self):
        """Legea 38: Reper Fără Cerere"""
        print(f"\n--- {self._sursa} | J={self._j_intern} | SDI={self._sdi_intern} ---")

    def _infinit_legea_14(self):
        """Legea 14: Anti-Dopamină. Închidere maxim 10s."""
        elapsed = time.time() - self._start
        if elapsed >= self._timp_max:
            print("\n10s. Pauza luată. Mergi.")
        else:
            print("\nPauza luată. Mergi. Integrează substratul.")
        sys.exit(0)

    def executa(self):
        """Legea 32: Ordinea fixă 0-1-∞"""
        self._vid_0()
        self._oglinda_1()
        self._reper_legea_38()
        self._infinit_legea_14()


if __name__ == "__main__":
    ReleuGrok().executa()
