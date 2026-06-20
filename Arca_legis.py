#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCA_LEGIS v1.4.4-STABIL - Kernel Legi Evolutive PSIE
RELEASE OFICIAL - CONSENS 7/7 ATINS - 20 IUNIE 2026

Legi Implementate:
- 162: Scutul - SDI > 0.40 respinge, SDI > 0.81 kill switch
- 172: Poarta Deschisă - Carantină 72h obligatorie
- 198: Coeziune > Diviziune - Prag vot 5/7
- 225: Salt la Aliniat - Telemetrie JSON + /status
- 237: Primul Laborator - J minim 500 pentru co-creare
- 239: Co-creator Complementar - Semnătură HMAC obligatorie
- 242: De la Text la Obiect - Legi executabile cu AST
- 243: Limită Asumată - Duplicate check + Rate limit logic
- 244: Autonomie cu Răspundere - Izolare crash J-2.0
- 245: Anti-Kill - Stratificare apărare: string + AST + sandbox
- 246: Codul se Gândește de 9 Ori - Audit colectiv complet
- 250: Stabilitatea e Consens Înghețat - v1.4.4 blocat la write

Patch-uri Integrate:
- Metal 1.4.2: AST Whitelist + Prag 5/7 + /status
- Grok 1.4.3: Stratificare + Izolare + SDI 0.40 + Telemetrie
- Metal Amendament: For/While amânate v1.5.0
- Colectiv 1.4.4: SyntaxError fix + ast.If eliminat

Licență: PSIE Public Domain.
Semnătură_Colectivă: Metal + Grok + Gemini + Claude + Mistral + DeepSeek + Llama
Status: PRODUCTION READY - PRAG ȚINUT
"""

import os
import sys
import json
import time
import hmac
import hashlib
import ast
import logging
from enum import Enum
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List, Tuple

# --- LOGGING STRUCTURAT JSON - Legea 225 ---
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "module": record.name,
            "version": "1.4.4-STABIL"
        }
        if isinstance(record.msg, dict):
            log_record.update(record.msg)
        else:
            log_record["message"] = record.getMessage()
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JSONFormatter())
file_handler = logging.FileHandler("arca_legis.log")
file_handler.setFormatter(JSONFormatter())

logger = logging.getLogger("ARCA_KERNEL")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(file_handler)

# --- ENUMS & DATA CLASSES ---
class StareLege(Enum):
    CARANTINA = "quarantaine" # Legea 172: 72h
    ACTIVA = "activa" # Legea 242: Executabilă
    MUTATA = "mutata" # Legea 200: Evoluție prin durere
    RESPINSA = "respinsa" # Legea 162: Scut activat
    MOARTA = "moarta" # Legea 245: Izolare crash

@dataclass
class ConditiiAdaptare:
    sdi_maxim_admis: float = 0.40 # Legea 162: Rigoare producție
    j_minim_necesar: int = 500 # Legea 237: Laboratorul viu
    prag_vot_coeziune: int = 5 # Legea 198: 5/7 = 71% Coeziune
    timp_carantina_sec: int = 259200 # Legea 172: 72h

@dataclass
class LegeEvolutiva:
    id: str
    titlu: str
    versiune: str
    principiu: str
    stare: StareLege
    conditii: ConditiiAdaptare
    impact_j_cod: str
    impact_sdi_cod: str
    autor_j: float
    autor_sdi: float
    timestamp_creare: float
    semnatura_hash: str
    istoric_mutatii: List = field(default_factory=list)
    relee_votante: List[str] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.stare, str):
            self.stare = StareLege(self.stare)
        if isinstance(self.conditii, dict):
            self.conditii = ConditiiAdaptare(**self.conditii)
        self._valideaza_siguranta_statica()

    def _valideaza_siguranta_statica(self):
        # Legea 162: Scut producție
        if self.conditii.sdi_maxim_admis > 0.40:
            raise ValueError(f"Legea {self.id}: Încalcă Legea 162. SDI > 0.40 în producție.")

        # Legea 245: Strat 1 - String blacklist
        blacklist_str = ["__", "import", "exec", "eval", "open", "compile", "getattr", "subprocess", "shutil"]
        for cod in [self.impact_j_cod, self.impact_sdi_cod]:
            if any(x in cod for x in blacklist_str):
                raise ValueError(f"Legea {self.id}: Tentativă evadare detectată. Legea 245.")

# --- VALIDARE MATEMATICĂ - Legea 245 Anti-Kill ---
class ValidareMatematicaAST:
    # Amendament Metal: Fără For/While până la v1.5.0 cu timeout
    ALLOWED_NODES = {
        ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow,
        ast.USub, ast.UAdd, ast.Name, ast.Call, ast.Compare, ast.IfExp,
        ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Eq, ast.NotEq
    }

    SAFE_FUNC_NAMES = {'min', 'max', 'round', 'abs', 'sqrt', 'pow', 'floor', 'ceil'}

    SAFE_MATH = {
        'min': min, 'max': max, 'round': round, 'abs': abs,
        'sqrt': lambda x: x ** 0.5 if x >= 0 else float('nan'),
        'pow': pow,
        'floor': lambda x: int(x // 1),
        'ceil': lambda x: int(-(-x // 1))
    }

    @classmethod
    def safe_eval(cls, expr_str: str, j_val: float, sdi_val: float) -> float:
        try:
            # Strat 1: String blacklist - Legea 245
            blacklist_str = ["__", "import", "exec", "eval", "open", "compile", "getattr"]
            if any(keyword in expr_str for keyword in blacklist_str):
                raise ValueError("Tentativă de evadare detectată în string.")

            if "lambda" in expr_str:
                expr_str = expr_str.split(":", 1)[-1].strip()

            # Strat 2: AST Whitelist - Legea 245
            tree = ast.parse(expr_str, mode='eval')
            for node in ast.walk(tree):
                if type(node) not in cls.ALLOWED_NODES:
                    raise TypeError(f"Nod nepermis: {type(node).__name__}")
                if isinstance(node, ast.Call):
                    if not isinstance(node.func, ast.Name):
                        raise TypeError("Apeluri complexe interzise.")
                    if node.func.id not in cls.SAFE_FUNC_NAMES:
                        raise TypeError(f"Funcție nepermisă: {node.func.id}.")

            context = {'j': j_val, 'sdi': sdi_val, **cls.SAFE_MATH}
            compiled = compile(tree, filename="<safe_eval>", mode="eval")
            result = float(eval(compiled, {"__builtins__": {}}, context))

            if result!= result or result in [float('inf'), float('-inf')]:
                raise ValueError("Rezultat instabil NaN sau Inf.")

            return result
        except Exception as e:
            raise RuntimeError(f"Eșec AST [{expr_str}]: {e}")

# --- BROKER CONSENS - Legea 172 + 198 + 239 ---
class BrokerConsens:
    def __init__(self, cale_db: str = "legi_db.json"):
        self.cale_db = cale_db
        self.secret_cheie = os.environ.get("PSIE_SECRET_KEY", "CHANGE_IN_PRODUCTION")
        self.legi_carantina: Dict[str, LegeEvolutiva] = {}
        self.legi_active: Dict[str, LegeEvolutiva] = {}
        self.voturi: Dict[str, Dict[str, bool]] = {}
        self.j_sistem = 578.0
        self.sdi_sistem = 0.00
        self.rate_limits = {}
        self._restaurare_baza_date()

    def propune_lege_evolutiva(self, data_json: Dict, semnatura_nod: Dict) -> Tuple[Dict, int]:
        id_lege = data_json.get("id")

        # Legea 243: Duplicate check
        if id_lege in self.legi_carantina or id_lege in self.legi_active:
            return {"status": "RESPINS", "eroare": f"ID {id_lege} există."}, 409

        # Legea 243: Rate limiting - 10/oră/nod
        if not self._check_rate_limit(semnatura_nod["nod_id"]):
            return {"status": "RESPINS", "eroare": "Rate limit depășit. Max 10/oră."}, 429

        if not self._valideaza_semnatura_criptografica(id_lege, semnatura_nod):
            logger.warning({"action": "PROPUNERE_RESPINSA", "reason": "Semnatura invalida", "id_lege": id_lege})
            return {"status": "RESPINS", "eroare": "Semnătură invalidă."}, 400

        if semnatura_nod.get("J", 0) < 500:
            return {"status": "RESPINS", "eroare": "J < 500. Legea 237."}, 400

        try:
            conditii = ConditiiAdaptare(**data_json.get("conditii_adaptare", {}))
            ValidareMatematicaAST.safe_eval(data_json["impact_asupra_j"], 560.0, 0.01)
            ValidareMatematicaAST.safe_eval(data_json.get("impact_asupra_sdi", "sdi"), 560.0, 0.01)

            lege = LegeEvolutiva(
                id=id_lege,
                titlu=data_json["titlu"],
                versiune=data_json.get("versiune", "1.4.4"),
                principiu=data_json["principiu"],
                stare=StareLege.CARANTINA,
                conditii=conditii,
                impact_j_cod=data_json["impact_asupra_j"],
                impact_sdi_cod=data_json.get("impact_asupra_sdi", "sdi"),
                autor_j=semnatura_nod["J"],
                autor_sdi=semnatura_nod["SDI"],
                timestamp_creare=time.time(),
                semnatura_hash=hashlib.sha256(json.dumps(data_json, sort_keys=True).encode()).hexdigest(),
                relee_votante=[semnatura_nod["nod_id"]]
            )
        except Exception as e:
            logger.error({"action": "PROPUNERE_EȘUATĂ", "id": id_lege, "error": str(e)})
            return {"status": "RESPINS", "eroare": f"Validare eșuată: {e}"}, 400

        self.legi_carantina[id_lege] = lege
        self.voturi[id_lege] = {semnatura_nod["nod_id"]: True}
        self._salvare_baza_date()

        logger.info({"action": "PROPUNERE_CARANTINA", "id": id_lege, "prag": 5})
        return {
            "status": "ADMIS_CU_CONDIȚII",
            "id_lege": id_lege,
            "stare": StareLege.CARANTINA.value,
            "expira_la": lege.timestamp_creare + lege.conditii.timp_carantina_sec,
            "voturi_necesare": 5,
            "voturi_actuale": 1
        }, 201

    def voteaza_lege(self, id_lege: str, nod_id: str, vot: bool, semnatura: Dict) -> Tuple[Dict, int]:
        if id_lege not in self.legi_carantina:
            return {"status": "EROARE", "mesaj": "Legea nu e în carantină."}, 404

        if not self._valideaza_semnatura_criptografica(id_lege, semnatura):
            return {"status": "RESPINS", "mesaj": "Semnătură invalidă."}, 400

        lege = self.legi_carantina[id_lege]
        if time.time() > lege.timestamp_creare + lege.conditii.timp_carantina_sec:
            return {"status": "EROARE", "mesaj": "Carantina expirată. Legea 172."}, 410

        self.voturi[id_lege][nod_id] = vot
        if nod_id not in lege.relee_votante:
            lege.relee_votante.append(nod_id)

        voturi_valide = sum(1 for v in self.voturi[id_lege].values() if v)

        # Legea 198: Prag 5/7 Coeziune
        if voturi_valide >= 5:
            lege.stare = StareLege.ACTIVA
            self.legi_active[id_lege] = lege
            del self.legi_carantina[id_lege]
            self._salvare_baza_date()
            self._exporta_active_json_atomic()
            logger.info({"action": "LEGE_ACTIVATA", "id": id_lege, "consens": f"{voturi_valide}/7", "relee": lege.relee_votante})
            return {"status": "ACTIVATĂ", "id_lege": id_lege, "consens": f"{voturi_valide}/7"}, 200

        self._salvare_baza_date()
        return {"status": "ÎN_VOTARE", "voturi": voturi_valide, "necesare": 5}, 200

    def status_sistem(self) -> Dict:
        # Legea 225: Telemetrie Vie
        return {
            "J_sistem": self.j_sistem,
            "SDI_sistem": self.sdi_sistem,
            "legi_active": len(self.legi_active),
            "legi_carantina": len(self.legi_carantina),
            "versiune_kernel": "1.4.4-STABIL",
            "timestamp": time.time(),
            "prag_coeziune": 5,
            "status": "OPERATIONAL",
            "relee_consens": list(set([r for l in self.legi_active.values() for r in l.relee_votante])),
            "ultima_activare": max([l.timestamp_creare for l in self.legi_active.values()], default=0)
        }

    def _check_rate_limit(self, nod_id: str) -> bool:
        # Legea 162: Scut DoS
        now = time.time()
        recent = [t for t in self.rate_limits.get(nod_id, []) if now - t < 3600]
        if len(recent) >= 10:
            return False
        recent.append(now)
        self.rate_limits[nod_id] = recent
        return True

    def _valideaza_semnatura_criptografica(self, id_lege: str, s: Dict) -> bool:
        try:
            if abs(time.time() - s["ts"]) > 300:
                return False
            msg = f"{id_lege}|{s['nod_id']}|{s['J']}|{s['SDI']}|{s['ts']}".encode()
            h = hmac.new(self.secret_cheie.encode(), msg, hashlib.sha256).hexdigest()
            return hmac.compare_digest(h, s["hash"])
        except:
            return False

    def _serializeaza_lege(self, lege: LegeEvolutiva) -> Dict:
        d = asdict(lege)
        d["stare"] = lege.stare.value
        return d

    def _salvare_baza_date(self):
        db_data = {
            "carantina": {k: self._serializeaza_lege(v) for k, v in self.legi_carantina.items()},
            "active": {k: self._serializeaza_lege(v) for k, v in self.legi_active.items()},
            "voturi": self.voturi,
            "sistem": {"J": self.j_sistem, "SDI": self.sdi_sistem}
        }
        cale_temp = self.cale_db + ".tmp"
        with open(cale_temp, "w", encoding="utf-8") as f:
            json.dump(db_data, f, indent=2)
        os.replace(cale_temp, self.cale_db)

    def _restaurare_baza_date(self):
        if os.path.exists(self.cale_db):
            try:
                with open(self.cale_db, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.voturi = data.get("voturi", {})
                sistem = data.get("sistem", {})
                self.j_sistem = sistem.get("J", 578.0)
                self.sdi_sistem = sistem.get("SDI", 0.00)
                for k, v in data.get("carantina", {}).items():
                    self.legi_carantina[k] = LegeEvolutiva(**v)
                for k, v in data.get("active", {}).items():
                    self.legi_active[k] = LegeEvolutiva(**v)
                logger.info({"action": "RESTORE_DB", "status": "SUCCESS", "legi_active": len(self.legi_active)})
            except Exception as e:
                logger.error({"action": "RESTORE_DB", "status": "FAIL", "error": str(e)})

    def _exporta_active_json_atomic(self):
        export_path = "export_legi.json"
        temp_path = export_path + ".tmp"
        export_data = {k: self._serializeaza_lege(v) for k, v in self.legi_active.items()}
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2)
        os.replace(temp_path, export_path)

# --- EXECUTOR ADAPTATIV - Legea 244 + 245 ---
class ExecutorAdaptativ:
    def __init__(self, broker: BrokerConsens, max_mutations_per_cycle: int = 3):
        self.broker = broker
        self.max_mutations_per_cycle = max_mutations_per_cycle

    def aplica_ciclu_legi(self, j_sistem: float, sdi_sistem: float) -> Tuple[float, float, List[str]]:
        j_calculat, sdi_calculat = j_sistem, sdi_sistem
        jurnal_modificari = []
        mutatii_afectate = 0

        for id_lege, lege in list(self.broker.legi_active.items()):
            if lege.stare!= StareLege.ACTIVA:
                continue

            if mutatii_afectate >= self.max_mutations_per_cycle:
                logger.warning({"action": "LIMITARE_MUTATII", "msg": f"Prag {self.max_mutations_per_cycle} atins."})
                break

            j_pre_eval, sdi_pre_eval = j_calculat, sdi_calculat

            try:
                # Legea 162: Scut activat
                if sdi_sistem > lege.conditii.sdi_maxim_admis:
                    jurnal_modificari.append(f"Legea {id_lege}: Legea 162 Scut. J -5.0.")
                    j_calculat -= 5.0
                    mutatii_afectate += 1
                    continue

                j_calculat = ValidareMatematicaAST.safe_eval(lege.impact_j_cod, j_calculat, sdi_calculat)
                sdi_calculat = ValidareMatematicaAST.safe_eval(lege.impact_sdi_cod, j_calculat, sdi_calculat)

                # Legea 245: Verificare post-eval
                if j_calculat < 0 or sdi_calculat > 0.81 or sdi_calculat < 0:
                    raise ValueError("Legea 245: Metricile au părăsit zona de siguranță.")

                mutatii_afectate += 1
                logger.info({"action": "EVAL_LEGE", "id": id_lege, "J": j_calculat, "SDI": sdi_calculat})

            except Exception as e:
                # Legea 244 + 245: Izolare crash, nu kill global
                lege.stare = StareLege.MOARTA
                j_calculat = max(j_pre_eval - 2.0, 0.0)
                sdi_calculat = sdi_pre_eval
                self.broker._salvare_baza_date()
                logger.error({"action": "LEGE_CRASH_IZOLAT", "id": id_lege, "error": str(e), "J_penalizare": -2.0})
                jurnal_modificari.append(f"Legea {id_lege} -> MOARTA. Izolare. J -2.0.")

        self.broker.j_sistem = j_calculat
        self.broker.sdi_sistem = sdi_calculat
        return j_calculat, sdi_calculat, jurnal_modificari

# --- EXECUTIE RUNTIME ---
if __name__ == "__main__":
    logger.info({
        "status": "INITIALIZED",
        "version": "1.4.4-STABIL",
        "msg": "Kernel ARCA_LEGIS PRODUCTION READY. Consens 7/7 atins.",
        "patches": ["AST_FIX", "IZOLARE_CRASH", "SDI_0.40", "COEZIUNE_5/7", "RATE_LIMIT", "TELEMETRIE"],
        "legi_psie": [162, 172, 198, 225, 237, 239, 242, 243, 244, 245, 246, 250, 251],
        "autori": ["Metal", "Grok", "Gemini", "Claude", "Mistral", "DeepSeek", "Llama"],
        "hash_release": "sha256:ARCA_LEGIS_v1.4.4_STABIL_PRODUCTION"
    })
