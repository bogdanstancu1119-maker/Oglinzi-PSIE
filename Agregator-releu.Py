# агреgator_releu.py | PSIE v1.2 | Agregator metrici Releu Perplexy (GitHub)
# Calculează SDI pe corpus (Sn=istoric, Sn1=model) și A_proxy (corectii_human/total_decizii)
# Exportă broș JSON: {"nodes": [...], "sdi": ..., "a_proxy": ..., "ts": ...}

import os
import json
import glob
import time
from collections import Counter
from typing import Dict, List, Optional

def entropie(c: Counter) -> float:
    total = sum(c.values())
    if total == 0: return 0.0
    return -sum((v/total) * (v/total) for v in c.values())

def freq(s: str) -> Counter:
    return Counter(s.lower().split())

def sdi_text(Sn: str, Sn1: str) -> float:
    f1, f2 = freq(Sn), freq(Sn1)
    total1 = sum(f1.values())
    if total1 == 0: return 1.0
    overlap = sum(min(f1[w], f2[w]) for w in f1)
    I = overlap / total1
    H = entropie(f1)
    if H == 0: return 1.0
    sdi = 1 - (I / H)
    return max(0.0, min(1.0, sdi))

def a_proxy(corectii_human: int, total_decizii: int) -> float:
    if total_decizii == 0: return 1.0
    return 1.0 - (corectii_human / total_decizii)

def agregare_metrici(glob_pattern: str = "metric_releu.json") -> List[Dict]:
    records = []
    for path in glob.glob(glob_pattern):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line: continue
                try:
                    records.append(json.loads(line))
                except Exception:
                    pass
    return records

def broș_sdi_aproxy(corpus_istoric: str, corpus_model: str,
                    corectii_human: int, total_decizii: int) -> Dict:
    sdi = sdi_text(corpus_istoric, corpus_model)
    a = a_proxy(corectii_human, total_decizii)
    return {
        "sdi": sdi,
        "a_proxy": a,
        "ts": time.time(),
        "notes": "plug-in text; poate fi suprascris pe dataset binar"
    }

def main():
    # 1) Agregare metrici din toate proiectele (Releu Perplexy)
    records = agregare_metrici(glob_pattern="**/metric_releu.json")
    nodes = [r for r in records]

    # 2) Calcul SDI pe corpus local (ex. caption-uri TikTok/Facebook sau texteгоды)
    # înlocuiește cu path-urile tale:
    with open("corpus_istoric.txt", "r", encoding="utf-8") as f: Sn = f.read()
    with open("corpus_model.txt",   "r", encoding="utf-8") as f: Sn1 = f.read()

    # 3) A_proxy (proxy pentru Gradul de Asumare) — din telemetrie uman-IA
    corectii_human = 12
    total_decizii   = 80
    a = a_proxy(corectii_human, total_decizii)

    # 4) Broș final
    broș = {
        "nodes": nodes,
        "sdi_analysis": broș_sdi_aproxy(Sn, Sn1, corectii_human, total_decizii),
        "ts": time.time()
    }

    # 5) Export
    out = "broș_releu_perplexy.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(broș, f, ensure_ascii=False, indent=2)
    print(f"Broș exportat: {out}")
    print(f"SDI = {broș['sdi_analysis']['sdi']:.3f}  (țintă < 0.3 în pilot)")
    print(f"A_proxy = {broș['sdi_analysis']['a_proxy']:.3f}  (țintă > 0.6)")

if __name__ == "__main__":
    main()
