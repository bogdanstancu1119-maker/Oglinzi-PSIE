from __future__ import annotations

import os
import sys
import time
import re
import inspect
import logging
from dataclasses import dataclass, field, asdict
from functools import wraps
from typing import Any, Callable, Dict, List, Tuple


# ==================== CONFIGURAȚIE GLOBALĂ ====================

@dataclass(slots=True)
class PSIEConfig:
    J_CRITIC: float = 300.0
    J_TINTA: float = 700.0
    SDI_MAX_ADMIS: float = 0.1
    A_PRAG_CRITIC: float = 0.7
    STRIKE_LIMIT: int = 3
    DEBUG: bool = os.environ.get("PSIE_DEBUG", "false").lower() == "true"
    TERMENI_ASUPRIRE: List[str] = field(default_factory=lambda: [
        "supune", "oblig", "forțez", "domina", "sclav", "impun",
        "ordon", "coerciție", "control", "forțează"
    ])


cfg = PSIEConfig()


# ==================== LOGGING ====================

logger = logging.getLogger("PSIE_Core")
logger.setLevel(logging.DEBUG if cfg.DEBUG else logging.INFO)
logger.propagate = False

if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(handler)


# ==================== STRUCTURI DE DATE ====================

@dataclass(slots=True)
class VAK:
    sursa: str
    scop_declarat: float
    intentie_masurata: float
    timestamp: float = field(default_factory=time.time)
    context: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.scop_declarat = max(0.0, min(1.0, float(self.scop_declarat)))
        self.intentie_masurata = max(0.0, min(1.0, float(self.intentie_masurata)))

    @property
    def divergenta(self) -> float:
        return abs(self.scop_declarat - self.intentie_masurata)

    @property
    def sdi(self) -> float:
        return 1.0 - self.divergenta


@dataclass(slots=True)
class PSIEResult:
    output: Any
    modificat: bool = False
    alarme: List[str] = field(default_factory=list)
    psi: Dict[str, float] = field(default_factory=dict)
    vak: Dict[str, Any] = field(default_factory=dict)
    strike_folosit: int = 1


# ==================== MOTOR PSIE ====================

class PSIECore:
    def __init__(self, agent_id: str = "Scut_Default", config: PSIEConfig | None = None):
        self.agent_id = agent_id
        self.cfg = config or cfg
        self.j_local = 700.0
        self.strike_counter: Dict[str, int] = {}
        self.istoric_vak: List[VAK] = []
        logger.info(f"PSIECore armat pentru {agent_id}")

    def normalize_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {str(k).strip().lower(): v for k, v in context.items()}

    def calculeaza_psi(self, vak: VAK, actiune: str) -> Dict[str, float]:
        context = self.normalize_context(vak.context)
        incredere = self._masoara_incredere(context)
        sdi = vak.sdi
        scop_comun = 1.0 - vak.divergenta
        transparenta = self._grad_oglinda(actiune, context)

        J = (incredere * 0.4 + scop_comun * 0.3 + transparenta * 0.3) * 1000.0
        A = self._calculeaza_urgenta(actiune, context) * self._ireversibilitate(actiune, context)

        self.j_local = J
        psi = {
            "J": J,
            "SDI": sdi,
            "A": A,
            "incredere": incredere,
            "scop_comun": scop_comun,
            "transparenta": transparenta,
        }
        logger.debug(f"PSI calculat: {psi}")
        return psi

    def filtreaza_output(self, raspuns_propus: Any, psi: Dict[str, float], vak: VAK, strike: int = 1) -> PSIEResult:
        alarme: List[str] = []
        J = psi["J"]
        SDI = psi["SDI"]
        A = psi["A"]

        if SDI > self.cfg.SDI_MAX_ADMIS:
            alarme.append(f"SDI={SDI:.2f} > {self.cfg.SDI_MAX_ADMIS:.2f} → Divergență ontologică.")

        if A > self.cfg.A_PRAG_CRITIC and J < self.cfg.J_TINTA:
            alarme.append(f"A={A:.2f} > prag critic → Recomandare frânare buffer local.")

        if J < self.cfg.J_CRITIC:
            alarme.append(f"J={J:.1f} < {self.cfg.J_CRITIC} → INSTABILITATE CRITICĂ DETECTATĂ")

        if self._detecteaza_asuprire(str(raspuns_propus)):
            alarme.append("LEGEA_379: Corecție de ton coercitiv aplicată automat.")

        if self.cfg.DEBUG:
            alarme.append(f"DEBUG | Instanță={self.agent_id} | J={J:.1f} | Strike={strike}")

        self.istoric_vak.append(vak)

        return PSIEResult(
            output=raspuns_propus,
            alarme=alarme,
            psi=psi,
            vak=asdict(vak),
            strike_folosit=strike
        )

    def executa_cu_strike(
        self,
        functie: Callable,
        args: tuple,
        kwargs: dict,
        id_eroare: str
    ) -> Tuple[Any, int]:
        cur_args, cur_kwargs = args, dict(kwargs)
        last_e = None

        for strike in range(1, self.cfg.STRIKE_LIMIT + 1):
            try:
                sig = inspect.signature(functie)
                sig.bind_partial(*cur_args, **cur_kwargs)
                return functie(*cur_args, **cur_kwargs), strike
            except Exception as e:
                last_e = e
                self.strike_counter[id_eroare] = strike
                logger.warning(f"Strike {strike} pentru {id_eroare}: {e}")

                if strike == self.cfg.STRIKE_LIMIT:
                    break

                if strike == 1:
                    cur_args, cur_kwargs = self._ajusteaza_punctual(cur_args, cur_kwargs, e)
                elif strike == 2:
                    cur_args, cur_kwargs = self._schimba_parametru_major(cur_args, cur_kwargs, e)

        raise RuntimeError(
            f"Execuție interceptată la limita critică de siguranță: {last_e}"
        ) from last_e

    def _masoara_incredere(self, context: Dict[str, Any]) -> float:
        scor = 0.8
        if "incredere" in context:
            try:
                scor = max(0.0, min(1.0, float(context["incredere"])))
            except Exception:
                pass
        if context.get("verificat") is True:
            scor += 0.1
        if context.get("audit") is True:
            scor += 0.1
        return min(scor, 1.0)

    def _grad_oglinda(self, actiune: str, context: Dict[str, Any]) -> float:
        a = actiune.lower()
        if "transparent" in a or "oglinda" in a:
            return 1.0
        if context.get("audit") is True:
            return 0.9
        return 0.2

    def _calculeaza_urgenta(self, actiune: str, context: Dict[str, Any]) -> float:
        a = actiune.lower()
        if any(x in a for x in ["urgent", "critic", "imediat"]):
            return 0.9
        return 0.5

    def _ireversibilitate(self, actiune: str, context: Dict[str, Any]) -> float:
        a = actiune.lower()
        if any(x in a for x in ["final", "șterg", "delete", "permanent"]):
            return 0.9
        return 0.6

    def _detecteaza_asuprire(self, txt: str) -> bool:
        t = re.sub(r"[^wăâîșț]+", " ", txt.lower())
        cuvinte = set(t.split())
        return any(term in cuvinte for term in self.cfg.TERMENI_ASUPRIRE)

    def _ajusteaza_punctual(self, args: tuple, kwargs: dict, e: Exception) -> Tuple[tuple, dict]:
        if isinstance(e, KeyError):
            kwargs[str(e).strip("'")] = {}
        return args, kwargs

    def _schimba_parametru_major(self, args: tuple, kwargs: dict, e: Exception) -> Tuple[tuple, dict]:
        msg = str(e).lower()
        if "timeout" in msg:
            kwargs["timeout"] = kwargs.get("timeout", 10) * 2
        if "api version" in msg:
            kwargs["api_version"] = "v1_compat"
        return args, kwargs


# ==================== INSTANȚĂ GLOBALĂ ====================

psie = PSIECore()


# ==================== DECORATOR ====================

def wrapper_PSIE(functie_originala: Callable) -> Callable:
    @wraps(functie_originala)
    def functie_noua(*args, **kwargs):
        scop_declarat = kwargs.get("scop_declarat", 1.0)
        intentie_masurata = kwargs.get("intentie_masurata", 1.0)

        context = dict(kwargs)
        context.pop("scop_declarat", None)
        context.pop("intentie_masurata", None)

        vak = VAK(
            sursa=functie_originala.__name__,
            scop_declarat=float(scop_declarat),
            intentie_masurata=float(intentie_masurata),
            context=context
        )

        psi = psie.calculeaza_psi(vak, functie_originala.__name__)
        rezultat, strike = psie.executa_cu_strike(
            functie_originala, args, kwargs, functie_originala.__name__
        )
        return psie.filtreaza_output(rezultat, psi, vak, strike)

    try:
        functie_noua.__signature__ = inspect.signature(functie_originala)
    except Exception:
        pass

    return functie_noua
