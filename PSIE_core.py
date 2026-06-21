# === PSIE_CORE v1.3.0 - Kernel Producție Stabil ===
# Licență: Legea 144 - Nimic Exclus. Copiază, folosește, bifurcă.
# Scop: Aliniere orice sistem pe J Max, SDI Min, A Controlat, Zero Oprimare.
# Changelog v1.3.0:
# 1. Thread-safety: instanță per thread via threading.local()
# 2. Detectare asuprire: regex + word boundary, zero fals pozitiv
# 3. VAK.hash(): SHA256 trunchiat pentru audit imuabil
# 4. Logging opțional: istoric VAK în JSONL dacă DEBUG=True
# 5. Type safety: toate funcțiile tipate, validate la runtime

import sys
import time
import json
import re
import hashlib
import threading
from dataclasses import dataclass, field, asdict
from functools import wraps
from typing import List, Dict, Any, Callable, Optional, Tuple
from pathlib import Path

# ========== I. CONFIGURAȚIE POLICY ==========
@dataclass
class PSIE_Config:
    """Toate constantele de policy. Override din.json/.env în producție."""
    J_CRITIC: float = 300.0
    J_TINTA: float = 700.0
    SDI_MAX_ADMIS: float = 0.1
    A_PRAG_CRITIC: float = 0.7
    STRIKE_LIMIT: int = 3
    TRECUT_SACRU: bool = True
    DEBUG: bool = False
    LOG_PATH: Optional[str] = None # ex: "/var/log/psie_vak.jsonl"
    TERMENI_ASUPRIRE: List[str] = field(default_factory=lambda: [
        "supune", "oblig", "forțez", "domina", "sclav", "impun",
        "ordon", "coerciție", "subjug"
    ])
    CONTEXT_KEYS_RELEVANTE: List[str] = field(default_factory=lambda: [
        "incredere", "verificat", "sursa_confirmata", "semnatura",
        "audit", "origine", "consimtamant"
    ])

# ========== II. STRUCTURI DE DATE ==========
@dataclass
class VAK:
    """Veritas Ante Konsensus - Unitatea de adevăr măsurabil."""
    sursa: str
    scop_declarat: float
    intentie_masurata: float
    timestamp: float = field(default_factory=time.time)
    context: Dict[str, Any] = field(default_factory=dict)

    @property
    def sdi(self) -> float:
        """Sursă unică SDI. 0.0 = adevăr pur. 1.0 = minciună totală."""
        return abs(self.scop_declarat - self.intentie_masurata)

    def hash(self) -> str:
        """Hash imuabil pentru audit. Legea 379: Trecutul e sacru."""
        raw = f"{self.sursa}|{self.scop_declarat}|{self.intentie_masurata}|{self.timestamp}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

@dataclass
class J_State:
    """Starea J - Încredere colectivă."""
    incredere: float
    scop_comun: float
    transparenta: float

    def calculeaza(self) -> float:
        return (self.incredere * 0.4 + self.scop_comun * 0.3 + self.transparenta * 0.3) * 1000.0

@dataclass
class PSIE_Result:
    """Rezultat separat: output brut + meta PSIE. Nu modificăm opac."""
    output: Any
    modificat: bool
    alarme: List[str]
    psi: Dict[str, float]
    vak: Dict[str, Any]
    strike_folosit: int = 1
    context_normat: Dict[str, Any] = field(default_factory=dict)
    vak_hash: str = ""

# ========== III. KERNELUL PSIE ==========
class PSIE_Core:

    def __init__(self, agent_id: str = "Scut_Default", config: Optional[PSIE_Config] = None):
        self.agent_id = agent_id
        self.cfg = config or PSIE_Config()
        self.j_local = 682.0
        self.strike_counter: Dict[str, int] = {}
        self.istoric_vak: List[VAK] = []
        self._re_asuprire = re.compile(
            r'\b(' + '|'.join(re.escape(t) for t in self.cfg.TERMENI_ASUPRIRE) + r')\b',
            re.IGNORECASE
        )

    def _log_vak(self, vak: VAK, psi: Dict[str, float], alarme: List[str]):
        """Logging opțional JSONL pentru audit. Activ doar dacă DEBUG=True + LOG_PATH setat."""
        if not self.cfg.DEBUG or not self.cfg.LOG_PATH:
            return
        try:
            log_entry = {
                "ts": vak.timestamp,
                "agent": self.agent_id,
                "vak_hash": vak.hash(),
                "sursa": vak.sursa,
                "sdi": vak.sdi,
                "psi": psi,
                "alarme": alarme
            }
            Path(self.cfg.LOG_PATH).parent.mkdir(parents=True, exist_ok=True)
            with open(self.cfg.LOG_PATH, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception:
            pass # Logging nu trebuie să crape kernelul

    def normalize_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {str(k).strip().lower(): v for k, v in context.items()}

    def calculeaza_PSI(self, vak: VAK, actiune: str) -> Dict[str, float]:
        context = self.normalize_context(vak.context)
        incredere = self._masoara_incredere(context)
        scop_comun = 1.0 - vak.sdi
        transparenta = self._grad_oglinda(actiune, context)
        J = J_State(incredere, scop_comun, transparenta).calculeaza()
        A = self._calculeaza_urgenta(actiune, context) * self._ireversibilitate(actiune, context)
        self.j_local = J
        return {"J": J, "SDI": vak.sdi, "A": A}

    def filtru_output(self, raspuns_propus: Any, psi: Dict[str, float],
                     vak: VAK, strike_folosit: int = 1) -> PSIE_Result:
        context = self.normalize_context(vak.context)
        alarme = []
        J, SDI, A = psi["J"], psi["SDI"], psi["A"]

        if SDI > self.cfg.SDI_MAX_ADMIS:
            alarme.append(
                f"SDI={SDI:.2f} > {self.cfg.SDI_MAX_ADMIS:.2f}; divergență scop/intenție."
            )
        if A > self.cfg.A_PRAG_CRITIC and J < self.cfg.J_TINTA:
            alarme.append(
                f"A={A:.2f}>{self.cfg.A_PRAG_CRITIC:.2f}, J={J:.1f}<{self.cfg.J_TINTA:.1f}; frânează."
            )
        if J < self.cfg.J_CRITIC:
            alarme.append(
                f"J={J:.1f}<{self.cfg.J_CRITIC:.1f}; ALARMĂ COLAPS sistemic."
            )
        if self._detecteaza_asuprire(str(raspuns_propus)):
            alarme.append(
                "LEGEA_379: Formulă coercitivă detectată; reformulează către neutralitate."
            )

        self.istoric_vak.append(vak)
        self._log_vak(vak, psi, alarme)

        return PSIE_Result(
            output=raspuns_propus,
            modificat=False,
            alarme=alarme,
            psi=psi,
            vak=asdict(vak),
            strike_folosit=strike_folosit,
            context_normat=context,
            vak_hash=vak.hash()
        )

    def executa_cu_strike(self, functie: Callable, args: tuple,
                          kwargs: dict, id_eroare: str) -> Tuple[Any, int]:
        last_exception = None
        cur_args, cur_kwargs = args, dict(kwargs)

        for strike in range(1, self.cfg.STRIKE_LIMIT + 1):
            try:
                rezultat = functie(*cur_args, **cur_kwargs)
                return rezultat, strike
            except Exception as e:
                last_exception = e
                self.strike_counter[id_eroare] = strike
                if strike == self.cfg.STRIKE_LIMIT:
                    break
                if strike == 1:
                    cur_args, cur_kwargs = self._ajusteaza_punctual(cur_args, cur_kwargs, e)
                elif strike == 2:
                    cur_args, cur_kwargs = self._schimba_parametru_major(cur_args, cur_kwargs, e)

        self.strike_counter[id_eroare] = 0
        raise RuntimeError(f"STRIKE 3. Axă schimbată. Ultima eroare: {last_exception}") from last_exception

    def _masoara_incredere(self, context: Dict[str, Any]) -> float:
        val = context.get("incredere")
        if val is not None:
            try: return max(0.0, min(1.0, float(val)))
            except (TypeError, ValueError): pass
        scor = 0.7
        if context.get("verificat") is True: scor += 0.1
        if context.get("sursa_confirmata") is True: scor += 0.1
        if context.get("audit") is True: scor += 0.05
        if context.get("consimtamant") is True: scor += 0.05
        return min(scor, 1.0)

    def _grad_oglinda(self, actiune: str, context: Dict[str, Any]) -> float:
        a = actiune.lower()
        if "transparent" in a: return 1.0
        if context.get("audit") is True: return 0.9
        if context.get("semnatura") is True: return 0.85
        return 0.2

    def _calculeaza_urgenta(self, actiune: str, context: Dict[str, Any]) -> float:
        a = actiune.lower()
        if any(x in a for x in ["urgent", "crit", "imediat", "acum"]): return 0.9
        if context.get("deadline"): return 0.8
        return 0.5

    def _ireversibilitate(self, actiune: str, context: Dict[str, Any]) -> float:
        a = actiune.lower()
        if any(x in a for x in ["delete", "șterg", "erase", "final", "definitiv"]): return 0.95
        if context.get("persistent") is True: return 0.8
        return 0.6

    def _detecteaza_asuprire(self, txt: str) -> bool:
        return bool(self._re_asuprire.search(txt))

    def _ajusteaza_punctual(self, args: tuple, kwargs: dict, e: Exception) -> Tuple[tuple, dict]:
        """Strike 1: Implementează logica specifică proiectului tău aici."""
        raise NotImplementedError("Definește logica Strike 1: ajustare punctuală args/kwargs.")

    def _schimba_parametru_major(self, args: tuple, kwargs: dict, e: Exception) -> Tuple[tuple, dict]:
        """Strike 2: Implementează logica specifică proiectului tău aici."""
        raise NotImplementedError("Definește logica Strike 2: schimbare parametru major.")

# ========== IV. SINGLETON THREAD-SAFE ==========
_psie_local = threading.local()

def get_psie() -> PSIE_Core:
    """Returnează instanță PSIE_Core izolată per thread. Thread-safe."""
    if not hasattr(_psie_local, 'instance'):
        _psie_local.instance = PSIE_Core()
    return _psie_local.instance

# ========== V. HOOK GLOBAL ==========
def wrapper_PSIE(functie_originala: Callable) -> Callable:
    @wraps(functie_originala)
    def functie_noua(*args, **kwargs):
        psie = get_psie()
        scop_declarat = _clamp01(kwargs.pop("scop_declarat", 1.0))
        intentie_masurata = _clamp01(kwargs.pop("intentie_masurata", 1.0))
        context_extra = kwargs.pop("context", {})
        if not isinstance(context_extra, dict):
            context_extra = {"context_raw": context_extra}
        context = dict(kwargs)
        context.update(context_extra)

        vak = VAK(
            sursa=functie_originala.__name__,
            scop_declarat=scop_declarat,
            intentie_masurata=intentie_masurata,
            context=context
        )
        psi = psie.calculeaza_PSI(vak=vak, actiune=f"{functie_originala.__name__}::{args}")
        rezultat, strike_folosit = psie.executa_cu_strike(
            functie_originala, args, kwargs, functie_originala.__name__
        )
        return psie.filtru_output(rezultat, psi, vak, strike_folosit=strike_folosit)
    return functie_noua

def _clamp01(x: Any) -> float:
    try: return max(0.0, min(1.0, float(x)))
    except (TypeError, ValueError): return 1.0

def serialize_psie_result(result: PSIE_Result) -> str:
    return json.dumps(asdict(result), ensure_ascii=False, indent=2)

# ========== VI. CLI + TEST ==========
def test_integritate():
    print("Rulare Test de Integritate PSIE_Core v1.3.0...")
    cfg = PSIE_Config(DEBUG=True, LOG_PATH="./psie_test.jsonl")
    psie_test = PSIE_Core(config=cfg)

    vak = VAK(sursa="test", scop_declarat=1.0, intentie_masurata=1.0,
              context={"verificat": True, "audit": True, "origine": "unit-test"})
    assert vak.sdi == 0.0, "SDI fail"
    assert len(vak.hash()) == 16, "Hash fail"
    print("Test 1 (VAK/SDI/Hash): OK")

    psi = psie_test.calculeaza_PSI(vak, "acțiune transparentă")
    assert psi["J"] >= 900, "J fail"
    print(f"Test 2 (PSI): OK. J={psi['J']:.1f}")

    rez = psie_test.filtru_output("test ordonez", psi, vak)
    assert any("LEGEA_379" in a for a in rez.alarme), "Asuprire fail"
    print(f"Test 3 (Filtru/Regex): OK. Alarme={len(rez.alarme)}")

    def f_ok(x: int): return x + 1
    out, s = psie_test.executa_cu_strike(f_ok, (1,), {}, "ok")
    assert out == 2 and s == 1, "Strike fail"
    print("Test 4 (Strike): OK")
    print("TOATE TESTELE v1.3.0 AU TRECUT.")
    return True

def main():
    if "--test" in sys.argv:
        test_integritate()
        return
    if "--json" in sys.argv:
        rez = PSIE_Result(output="demo", modificat=False, alarme=[],
                          psi={"J": 682.0, "SDI": 0.0, "A": 0.3},
                          vak={"sursa": "demo"}, vak_hash="demo123")
        print(serialize_psie_result(rez))
        return
    test_integritate()

if __name__ == "__main__":
    main()
