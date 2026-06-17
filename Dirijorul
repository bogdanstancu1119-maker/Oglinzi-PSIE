# orchestrator_releu.py | PSIE v1.2 | Orchestrator global pentru Agregator-releu.py (GitHub)
# Rulează agregatorul pe toate repo-urile, cucerește broș central, calculează SDI & A_proxy
# Exportă broș_global.json cu metrici agregate și semnale de veto (SDI > 0.1)

import os
import json
import glob
import subprocess
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

def find_repos(root_dir: str = ".") -> List[str]:
    # asumăm că fiecare repo are un fișier Agregator-releu.py
    repos = []
    for path in glob.glob(os.path.join(root_dir, "**/Agregator-releu.py"), recursive=True):
        repo_root = os.path.dirname(path)
        repos.append(repo_root)
    return repos

def run_aggregator(repo_path: str) -> bool:
    script = os.path.join(repo_path, "Agregator-releu.py")
    if not os.path.exists(script): return False
    try:
        # rulează agregatorul în repo
        subprocess.run(["python", script], cwd=repo_path, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False

def agregare_metrici_globale(glob_pattern: str = "**/metric_releu.json") -> List[Dict]:
    records = []
    for path in glob.glob(glob_pattern, recursive=True):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line: continue
                try:
                    records.append(json.loads(line))
                except Exception:
                    pass
    return records

def main():
    # 1) Caută repo-uri
    repos = find_repos(root_dir=".")
    print(f"Repo-uri găsite: {len(repos)}")

    # 2) Rulează agregatorul pe fiecare repo
    success_count = 0
    for r in repos:
        if run_aggregator(r): success_count += 1
    print(f"Agregatori rulați: {success_count}/{len(repos)}")

    # 3) Cucerește broș central (metrici din toate repo-urile)
    records = agregare_metrici_globale(glob_pattern="**/metric_releu.json")
    nodes = records

    # 4) Calcul SDI pe corpus local (înlocuiește cu path-urile tale)
    Sn_path = "corpus_istoric.txt"
    Sn1_path = "corpus_model.txt"
    if os.path.exists(Sn_path) and os.path.exists(Sn1_path):
        with open(Sn_path, "r", encoding="utf-8") as f: Sn = f.read()
        with open(Sn1_path, "r", encoding="utf-8") as f: Sn1 = f.read()
        sdi = sdi_text(Sn, Sn1)
    else:
        sdi = 0.002  # placeholder

    # 5) A_proxy (proxy pentru Gradul de Asumare) — din telemetrie uman-IA
    corectii_human = 12
    total_decizii   = 80
    a = a_proxy(corectii_human, total_decizii)

    # 6) Broș global final
    broș_global = {
        "nodes": nodes,
        "sdi_analysis": {
            "sdi": sdi,
            "a_proxy": a,
            "ts": time.time(),
            "notes": "plug-in text; poate fi suprascris pe dataset binar"
        },
        "repos_executed": len(repos),
        "success_count": success_count,
        "ts": time.time()
    }

    # 7) Export și semnal veto
    out = "broș_global_releu_perplexy.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(broș_global, f, ensure_ascii=False, indent=2)
    print(f"Broș global exportat: {out}")
    print(f"SDI = {broș_global['sdi_analysis']['sdi']:.3f}  (țintă < 0.3 în pilot)")
    print(f"A_proxy = {broș_global['sdi_analysis']['a_proxy']:.3f}  (țintă > 0.6)")

    # 8) Veto PSIE: dacă SDI > 0.1, semnalăm
    if broș_global['sdi_analysis']['sdi'] > 0.1:
        print("[VETO] SDI > 0.1 — decuplare detectată. Intervineți.")

if __name__ == "__main__":
    main()
