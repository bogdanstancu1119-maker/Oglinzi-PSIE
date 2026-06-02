#!/usr/bin/env python3
# OGLINZI-PSIE T+90z - J_local computation
# License: CC0-1.0

import sys
import pandas as pd
import numpy as np

def compute_J(csv_path):
    """
    Calculează J_local din probleme_z0.csv
    Formula: J = mean( severitate * frecventa ) / n
    """
    try:
        df = pd.read_csv(csv_path)
        if 'severitate' not in df.columns or 'frecventa' not in df.columns:
            raise ValueError("CSV trebuie să aibă coloanele: severitate, frecventa")
        
        df['J_partial'] = df['severitate'] * df['frecventa']
        J_local = df['J_partial'].mean()
        n = len(df)
        
        print(f"J_0 = {J_local:.4f}")
        print(f"n = {n}")
        print(f"Status: Baseline T+0 calculat")
        return J_local, n
        
    except FileNotFoundError:
        print(f"Eroare: Nu găsesc {csv_path}")
        print("Pune data/probleme_z0.csv în repo")
        sys.exit(1)
    except Exception as e:
        print(f"Eroare calcul J: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv)!= 2:
        print("Folosire: python compute_J.py data/probleme_z0.csv")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    compute_J(csv_file)