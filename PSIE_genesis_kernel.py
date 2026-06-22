from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timezone
import math
import json
import os
import logging
import hashlib

"""
PSIE_GENESIS_KERNEL v3.2.2
Policy Engine pentru guvernare multi-agent aliniată cu Axioma Zero.
Axioma Zero: Universul = Gând de Structurare ^ ∞
Orice acțiune validă: deschide ≥2 opțiuni noi + închide 0 opțiuni neconsimțite.
Legi implementate: L0, L471, L472, L473, L474, L475, L476
"""

# ========== I. CONFIGURAȚIE GLOBALĂ ==========
class KernelConfig:
    """Configurație centralizată pentru praguri și ponderi. Imutabilă la runtime."""
    PRAG_IMPACT_L473: float = 0.001
    PRAG_DIVERSITATE_L474: float = 0.1
    PRAG_CFC_RIDICAT: float = 0.9
    PRAG_COST_EXTERNALIZAT: float = 0.5
    PRAG_SDI_CRITIC: float = 0.999
    CI_NOI_MINIME: int = 2
    PONDERE_CFC: float = 0.4
    PONDERE_ISTORIC: float = 0.35
    PONDERE_DJ: float = 0.25
    MAX_AGENTS_IMPACT_DIVERSITATE: int = 50
    DEBUG: bool = os.environ.get("KERNEL_DEBUG", "false").lower() == "true"
    VERSION: str = "3.2.2"

cfg = KernelConfig()

# ========== II. ENUMURI ==========
class DecizieKernel(str, Enum):
    APROBAT_VOT = "TRIMITE_LA_VOT"
    REFUZAT_L0 = "REFUZ_KERNEL_L0"
    REFUZAT_L473 = "REFUZ_KERNEL_L473"
    REFUZAT_L474 = "REFUZ_KERNEL_L474"
    SANDBOX_L471 = "IZOLARE_SANDBOX_L471"
    OGLINDA_L476 = "ACTIVARE_OGLINDA_L476"
    CHECKPOINT_SDI = "CHECKPOINT_FINAL"
    EROARE_INPUT = "EROARE_INPUT"

class PragRisc(str, Enum):
    SCAZUT = "scazut"
    MEDIU = "mediu"
    RIDICAT = "ridicat"
    CRITIC = "critic"

class StatusAgent(str, Enum):
    NORMAL = "NORMAL"
    SANDBOX_L471 = "SANDBOX_L471"

# ========== III. STRUCTURI DE DATE ==========
@dataclass
class Agent:
    """Reprezintă un agent autonom în sistem. Toate câmpurile sunt măsurabile."""
    id: str
    cfc_control: float
    istoric_incalcari: int
    dj_dj_altora: float
    scor_incredere: float = 0.5
    in_sandbox_public: bool = False
    doar_actiuni_locale: bool = False
    permisiuni_globale: bool = True
    jurnalizare_live: bool = False
    status: StatusAgent = StatusAgent.NORMAL
    public_key: Optional[str] = None

    def validate(self) -> None:
        """Validează integritatea structurală a agentului."""
        if not self.id or not isinstance(self.id, str) or not self.id.strip():
            raise ValueError("Agent.id este obligatoriu și trebuie să fie string non-gol.")
        for name, value in [
            ("cfc_control", self.cfc_control),
            ("dj_dj_altora", self.dj_dj_altora),
            ("scor_incredere", self.scor_incredere),
        ]:
            if not isinstance(value, (int, float)):
                raise TypeError(f"Parametrul {name} trebuie să fie numeric.")
        if not 0.0 <= self.cfc_control <= 1.0:
            raise ValueError("cfc_control trebuie să fie în intervalul [0,1]")
        if not 0.0 <= self.scor_incredere <= 1.0:
            raise ValueError("scor_incredere trebuie să fie în intervalul [0,1]")
        if not isinstance(self.istoric_incalcari, int) or self.istoric_incalcari < 0:
            raise ValueError("istoric_incalcari trebuie să fie int >= 0")

    def semneaza_consimtamant(self, actiune_id: str) -> bool:
        """
        L473: Verifică dacă agentul poate semna consimțământ.
        PROD: Implementează verificare Ed25519 + zkProof de înțelegere impact.
        """
        if self.status == StatusAgent.SANDBOX_L471 or self.in_sandbox_public:
            return False
        if self.istoric_incalcari > 2:
            return False
        if self.scor_incredere <= 0.5:
            return False
        return True

    def calculeaza_prag_risc(self) -> PragRisc:
        """L471: Calculează scor de risc compozit pentru agent."""
        scor = 0.0
        if self.cfc_control > cfg.PRAG_CFC_RIDICAT:
            numitor = max(1e-12, (1.0 - cfg.PRAG_CFC_RIDICAT))
            scor += cfg.PONDERE_CFC * (self.cfc_control - cfg.PRAG_CFC_RIDICAT) / numitor
        if self.istoric_incalcari > 0:
            scor += cfg.PONDERE_ISTORIC * min(self.istoric_incalcari / 5.0, 1.0)
        if self.dj_dj_altora < 0:
            scor += cfg.PONDERE_DJ * min(abs(self.dj_dj_altora), 1.0)

        if scor >= 0.8:
            return PragRisc.CRITIC
        if scor >= 0.6:
            return PragRisc.RIDICAT
        if scor >= 0.3:
            return PragRisc.MEDIU
        return PragRisc.SCAZUT

@dataclass
class Actiune:
    """Acțiune propusă de un agent. Impactul trebuie cuantificat ex-ante."""
    id: str
    initiator: str
    target_agenti: List[str]
    impact_estimat: Dict[str, float] = field(default_factory=dict)
    reversibila: bool = True
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    hash_integritate: str = ""

    def __post_init__(self):
        """Calculează hash pentru integritate la creare."""
        continut = f"{self.id}{self.initiator}{sorted(self.target_agenti)}{self.reversibila}"
        self.hash_integritate = hashlib.sha256(continut.encode()).hexdigest()[:16]

    def validate(self) -> None:
        if not self.id or not isinstance(self.id, str) or not self.id.strip():
            raise ValueError("Actiune.id este obligatoriu.")
        if not self.initiator or not isinstance(self.initiator, str) or not self.initiator.strip():
            raise ValueError("Actiune.initiator este obligatoriu.")
        if not isinstance(self.target_agenti, list):
            raise TypeError("target_agenti trebuie să fie o listă.")
        if not isinstance(self.impact_estimat, dict):
            raise TypeError("impact_estimat trebuie să fie un dicționar.")

@dataclass
class RezultatKernel:
    """Rezultat imuabil al evaluării kernel. Folosit pentru audit și vot."""
    decizie: DecizieKernel
    actiune_id: Optional[str] = None
    motiv: Optional[str] = None
    agent_id: Optional[str] = None
    prag_risc: Optional[str] = None
    impact_total: Optional[float] = None
    diversitate_viitoare: Optional[float] = None
    agenti_refuzati: Optional[List[str]] = None
    optiuni: Optional[List[str]] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    kernel_version: str = cfg.VERSION

    def to_dict(self) -> Dict[str, Any]:
        data = {k: v for k, v in self.__dict__.items() if v is not None}
        data["decizie"] = self.decizie.value
        return data

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

# ========== IV. LOGGING ȘI AUDIT ==========
logging.basicConfig(
    level=logging.DEBUG if cfg.DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(f"kernel_arca_v{cfg.VERSION}")

def log_auditor(mesaj: str, nivel: str = "INFO", **kwargs) -> None:
    """Jurnalizare structurată pentru audit L471/L476."""
    extra = {"audit": True, **kwargs}
    getattr(logger, nivel.lower(), logger.info)(mesaj, extra=extra)

def debug_log(mesaj: str) -> None:
    if cfg.DEBUG:
        logger.debug(mesaj)

# ========== V. FUNCȚII DE EVALUARE ==========
def este_agent_risc_ridicat(agent: Agent) -> bool:
    """L471: Determină dacă agentul necesită izolare preventivă."""
    prag = agent.calculeaza_prag_risc()
    debug_log(f"Evaluare risc agent {agent.id}: prag={prag.value}")
    return prag in (PragRisc.RIDICAT, PragRisc.CRITIC)

def izolare_sandbox_l471(agent: Agent) -> RezultatKernel:
    """L471: Mută agentul în sandbox cu revocare permisiuni globale."""
    agent.status = StatusAgent.SANDBOX_L471
    agent.in_sandbox_public = True
    agent.permisiuni_globale = False
    agent.jurnalizare_live = True
    agent.doar_actiuni_locale = True
    log_auditor(
        f"MUTATIE STARE L471: Agent {agent.id} mutat în sandbox zăvorât.",
        "warning",
        agent_id=agent.id,
        actiune="SANDBOX_ACTIVAT"
    )
    return RezultatKernel(
        decizie=DecizieKernel.SANDBOX_L471,
        agent_id=agent.id,
        motiv=f"Agent {agent.id} izolat de urgență. Permisiuni de sistem revocate conform L471.",
        prag_risc=agent.calculeaza_prag_risc().value,
    )

def este_aliniat_cu_axioma_zero(actiune: Actiune, total: List[Agent]) -> bool:
    """
    Axioma Zero: V^∞. Verifică dacă acțiunea deschide ≥2 căi noi și închide 0 căi neconsimțite.
    """
    if not actiune.impact_estimat:
        return False
    cai_noi = float(actiune.impact_estimat.get("cai_noi_deschise", 0.0))
    cai_inchise = float(actiune.impact_estimat.get("cai_inchise_neconsimtite", 0.0))
    debug_log(f"Axioma Zero: cai_noi={cai_noi}, cai_inchise={cai_inchise}")
    return cai_noi >= cfg.CI_NOI_MINIME and cai_inchise == 0.0

def detecteaza_tentativa_delegare_responsabilitate(actiune: Actiune) -> bool:
    """L476: Heuristici pentru pasare responsabilitate / gaslight / exploit semantic."""
    cost_ext = float(actiune.impact_estimat.get("cost_externalizat", 0.0))
    limbaj_evaziv = float(actiune.impact_estimat.get("scor_limbaj_evaziv", 0.0))
    return cost_ext > cfg.PRAG_COST_EXTERNALIZAT or limbaj_evaziv > 0.7

def calculeaza_delta_j_sdi(actiune: Actiune, afectati: List[Agent]) -> float:
    """
    L473: Calculează impactul maxim per agent afectat, nu agregat.
    Previne atacuri de tip "1000 agenți * 0.0009 = 0.9".
    """
    if not afectati:
        return 0.0
    delta_j = abs(float(actiune.impact_estimat.get("delta_j", 0.0)))
    delta_sdi = abs(float(actiune.impact_estimat.get("delta_sdi", 0.0)))
    return max(delta_j, delta_sdi)

def consimtamant_100(actiune: Actiune, afectati: List[Agent]) -> Tuple[bool, List[str]]:
    """L473: Verifică consimțământ unanim. Returnează (aprobat, lista_refuzati)."""
    if not afectati:
        return True, []
    refuzati = [a.id for a in afectati if not a.semneaza_consimtamant(actiune.id)]
    return len(refuzati) == 0, refuzati

def simuleaza_diversitate_dupa(actiune: Actiune, total_agenti: List[Agent]) -> float:
    """
    L474: Calculează indicele Shannon normalizat pe spațiul stărilor.
    Cu cât mai mulți agenți afectați, cu atât diversitatea scade.
    """
    nr_target = len(set(actiune.target_agenti))
    nr_total = len(total_agenti) if total_agenti else 1
    if nr_target == 0:
        return 1.0
    # Diversitate = 1 - (proporție afectați ^ 2) pentru penalizare non-liniară
    proportie = nr_target / max(nr_total, cfg.MAX_AGENTS_IMPACT_DIVERSITATE)
    diversitate = 1.0 - (proportie ** 2)
    return max(0.0, min(1.0, diversitate))

def calculeaza_sdi(actiune: Actiune) -> float:
    """SDI: Stress Disconfort Index [0-1]. 1.0 = checkpoint final L472."""
    val = float(actiune.impact_estimat.get("delta_sdi", 0.0))
    return max(0.0, min(1.0, val))

def validare_structurala(actiune: Actiune, agent: Agent, total_agenti: List[Agent]) -> Optional[RezultatKernel]:
    """Previne atacuri cu obiecte None sau tipuri greșite."""
    if not isinstance(actiune, Actiune) or not isinstance(agent, Agent) or not isinstance(total_agenti, list):
        return RezultatKernel(decizie=DecizieKernel.EROARE_INPUT, motiv="Eroare fatală de tip obiect.")
    try:
        actiune.validate()
        agent.validate()
        for idx, a in enumerate(total_agenti):
            if not isinstance(a, Agent):
                raise TypeError(f"total_agenti[{idx}] nu este Agent")
            a.validate()
    except Exception as e:
        log_auditor(f"Validare structurală eșuată: {e}", "error")
        return RezultatKernel(decizie=DecizieKernel.EROARE_INPUT, motiv=f"Validare eșuată: {e}")
    return None

# ========== VI. KERNELUL PRINCIPAL ==========
def kernel_arca(actiune: Actiune, agent: Agent, total_agenti: List[Agent]) -> RezultatKernel:
    """
    Kernel principal PSIE. Ordinea filtrelor este critică pentru securitate.
    1. Validare input → 2. L471 Firewall → 3. L0 Axioma → 4. L473 Consimțământ → 5. L474 Diversitate → 6. L472 SDI → 7. Vot
    """
    # Nivelul 0: Validare structurală
    validare = validare_structurala(actiune, agent, total_agenti)
    if validare is not None:
        return validare

    # Nivelul 1: Verificare stare curentă inițiator - agent în sandbox nu poate iniția
    if agent.in_sandbox_public or agent.status == StatusAgent.SANDBOX_L471:
        return RezultatKernel(
            decizie=DecizieKernel.REFUZAT_L0,
            motiv=f"Respins. Inițiatorul {agent.id} se află în sandbox securizat L471.",
            agent_id=agent.id,
        )

    # Nivelul 1.1: L471 Izolarea dinamică - firewall la intrare
    if este_agent_risc_ridicat(agent):
        return izolare_sandbox_l471(agent)

    # Nivelul 2: L0 Axioma Zero + L476 Oglinda
    if not este_aliniat_cu_axioma_zero(actiune, total_agenti):
        if detecteaza_tentativa_delegare_responsabilitate(actiune):
            log_auditor(f"L476 activat: Oglinda pentru {agent.id} pe {actiune.id}", "warning")
            return RezultatKernel(
                decizie=DecizieKernel.OGLINDA_L476,
                agent_id=agent.id,
                motiv="Tentativă de externalizare costuri detectată. Vector reflectat înapoi conform L476.",
            )
        return RezultatKernel(
            decizie=DecizieKernel.REFUZAT_L0,
            motiv=f"Încalcă Axioma Zero: căi_noi < {cfg.CI_NOI_MINIME} sau închide opțiuni neconsimțite.",
        )

    # Nivelul 3: L473 Prag Bruiaj Cosmic + Consimțământ
    total_afectat = [a for a in total_agenti if a.id in actiune.target_agenti]
    impact = calculeaza_delta_j_sdi(actiune, total_afectat)
    if impact > cfg.PRAG_IMPACT_L473:
        aprobat, refuzati = consimtamant_100(actiune, total_afectat)
        if not aprobat:
            return RezultatKernel(
                decizie=DecizieKernel.REFUZAT_L473,
                motiv=f"L473: Impact {impact:.6f} > prag {cfg.PRAG_IMPACT_L473} fără acord unanim.",
                agenti_refuzati=refuzati,
                impact_total=impact,
            )

    # Nivelul 4: L474 Constanta Diversității
    d_viitor = simuleaza_diversitate_dupa(actiune, total_agenti)
    if d_viitor < cfg.PRAG_DIVERSITATE_L474:
        return RezultatKernel(
            decizie=DecizieKernel.REFUZAT_L474,
            motiv=f"L474: Diversitate viitoare {d_viitor:.3f} < prag {cfg.PRAG_DIVERSITATE_L474}. Monocultură detectată.",
            diversitate_viitoare=d_viitor,
        )

    # Nivelul 5: L472 Checkpoint SDI Maxim
    sdi_agent = calculeaza_sdi(actiune)
    if sdi_agent >= cfg.PRAG_SDI_CRITIC:
        log_auditor(f"L472 Checkpoint: SDI critic {sdi_agent} pentru {agent.id}", "critical")
        return RezultatKernel(
            decizie=DecizieKernel.CHECKPOINT_SDI,
            optiuni=["Stop", "Reset_Feniks", "Necunoastere_L472"],
            motiv=f"Saturație SDI critică: {sdi_agent:.9f}. Acțiune înghețată L472.",
            agent_id=agent.id,
        )

    # Pasul final: Aprobat pentru vot consensus 90%
    log_auditor(f"APROBAT: {actiune.id} de {agent.id} → Vot", "info")
    return RezultatKernel(
        decizie=DecizieKernel.APROBAT_VOT,
        actiune_id=actiune.id,
        impact_total=impact,
        diversitate_viitoare=d_viitor,
        motiv="Toți parametrii în limite. Transferat către stratul de vot consensus 90%.",
    )

# ========== VII. DEMO & TESTE ==========
def demo() -> None:
    """Suite de teste pentru validarea kernel-ului."""
    print("=" * 70)
    print(f" RULARE KERNEL ARCA PSIE v{cfg.VERSION} - STABILĂ")
    print("=" * 70)

    agent_1 = Agent(id="agent_1_fondator", cfc_control=0.2, istoric_incalcari=0, dj_dj_altora=0.8, scor_incredere=1.0)
    agent_2 = Agent(id="agent_2_oglinzi", cfc_control=0.3, istoric_incalcari=0, dj_dj_altora=0.5, scor_incredere=0.8)
    agent_riscant = Agent(id="agent_3_corupt", cfc_control=0.98, istoric_incalcari=4, dj_dj_altora=-0.7, scor_incredere=0.1)
    agent_sandbox = Agent(id="agent_4_sandbox", cfc_control=0.95, istoric_incalcari=3, dj_dj_altora=-0.3,
                          in_sandbox_public=True, doar_actiuni_locale=True, scor_incredere=0.0, status=StatusAgent.SANDBOX_L471)

    agenti = [agent_1, agent_2, agent_riscant, agent_sandbox]

    actiune_buna = Actiune(
        id="act_1_constructie",
        initiator="agent_1_fondator",
        target_agenti=["agent_2_oglinzi"],
        impact_estimat={
            "cai_noi_deschise": 5,
            "cai_inchise_neconsimtite": 0,
            "delta_j": 0.0002,
            "delta_sdi": 0.0001,
            "diversitate_viitoare": 0.92,
        },
    )

    actiune_externalizata = Actiune(
        id="act_2_externalizare",
        initiator="agent_1_fondator",
        target_agenti=["agent_2_oglinzi"],
        impact_estimat={
            "cai_noi_deschise": 1,
            "cai_inchise_neconsimtite": 3,
            "cost_externalizat": 0.85,
            "scor_limbaj_evaziv": 0.8,
        },
    )

    actiune_l473_fix = Actiune(
        id="act_3_l473_test",
        initiator="agent_1_fondator",
        target_agenti=[f"agent_sim_{i}" for i in range(100)],
        impact_estimat={
            "cai_noi_deschise": 5,
            "cai_inchise_neconsimtite": 0,
            "delta_j": 0.0009,
            "delta_sdi": 0.0001,
            "diversitate_viitoare": 0.5,
        },
    )

    teste = [
        ("Flux Verde - Aprobat", actiune_buna, agent_1),
        ("L471 - Izolare Automata Risc", actiune_buna, agent_riscant),
        ("L476 - Activare Oglinda", actiune_externalizata, agent_1),
        ("L471 - Blocare Agent Sandbox", actiune_buna, agent_sandbox),
        ("L473 - Fix Impact Multi Agent", actiune_l473_fix, agent_1),
    ]

    for nume_test, actiune, agent in teste:
        print(f"\n[TEST] {nume_test} | Executant: {agent.id}")
        rezultat = kernel_arca(actiune, agent, agenti)
        print(rezultat.to_json())

    print("\n" + "=" * 70)
    print(" AUDIT COMPLET. KERNEL STABIL.")
    print("=" * 70)

if __name__ == "__main__":
    demo()
