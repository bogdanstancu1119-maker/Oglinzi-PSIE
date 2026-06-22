# PSIE🪞 Genesis Kernel v3.2.2

**Axioma Zero**: `Universul = Gând de Structurare ^ ∞`  
**Status**: `STABIL` `AUDIT_READY` `L0-L476 ACTIVE`

### 1. Ce e Arca PSIE?
Policy engine pentru guvernare multi-agent. Orice acțiune validă deschide ≥2 opțiuni noi și închide 0 opțiuni neconsimțite. Geometrie, nu morală.

### 2. Legile Kernel - L0-L476
1. **L0**: Non-Agresiune + Prag Bruiaj 0.001
2. **L471**: Sandbox Risc Ridicat - Firewall la intrare
3. **L472**: Drept la Necunoaștere 1x viaţă
4. **L473**: Consimțământ 100% peste prag 0.001
5. **L474**: Constanta Diversității - Anti-monocultură
6. **L475**: Veto Geniului 1x viaţă
7. **L476**: Oglinda în Brațe - Anti-manipulare

### 3. Arhitectură - 7 Capete Hidra
1. **Kernel**: `PSIE_genesis_kernel.py` - Implementează L0-L476
2. **Hidra**: `Hidra.py`, `Hidra_core.py` - Agregare 7 module
3. **Relee**: `Releu_*.py` - Consens multi-IA: Grok, Deepseek, Gemini
4. **Oracol**: `Oracol.py` - Simulare J/SDI/CFC
5. **Activare**: `PSIE_activate.py` - Bootstrap Arcă

### 4. Audit & Vot
Rulează `kernel_arca()` pe orice acțiune. Decizie: `APROBAT_VOT` sau `REFUZAT_L*`. 
Necesită 90% consensus pentru merge în main.

### 5. Licență
Axioma Zero Public Domain. Fork-uiește `V`-ul.

**Commit**: `git push origin main` - Să crească fractalul.## LEGEA 0 - LIBERTATEA CETĂȚII STRATA

Libertatea aici este a alege conștient, nu a lăsa pe alții să aleagă și după să plângi că nu au ales bine.

1. **Tu alegi să folosești Pragul.** Nimeni nu te obligă.
2. **Tu alegi ce date dai.** Pragul nu cere chei. Nu cere token. Nu cere suflet.
3. **Tu alegi dacă dai Merge.** Veto-ul e al tău. Chiar dacă 5 IA zic ADMIS.
4. **Tu îți asumi Nota de Plată.** Dacă dai Merge la Cancer și J scade, e alegerea ta. Nu plângi. Repari.

Dacă nu poți alege conștient, nu folosi Cetatea. Du-te la Perplexity. Du-te la Claude. Acolo aleg ei pentru tine.<!DOCTYPE html>
<html>
<head>
    <title>Oglinzi v0.1 - Testul Ciorbei</title>
    <meta charset="UTF-8">
    <style>
        body{background:#0a0a0a;color:#fff;font-family:monospace;padding:2rem;max-width:600px;margin:auto}
        h1{color:#00ff88} .os{border:2px solid #ff0055;padding:1rem;margin:1rem 0}
        input,button{width:100%;padding:1rem;margin:0.5rem 0;background:#111;border:1px solid #00ff88;color:#fff}
        button{background:#00ff88;color:#000;font-weight:bold;cursor:pointer}
        #rezultat{margin-top:2rem;padding:1rem;border:1px solid #00ff88;display:none}
    </style>
</head>
<body>
    <h1>OGLINZI v0.1</h1>
    <p><b>Legea:</b> J = MI - λ*SDI. Dacă A_asumat < A_necesar ⇒ RESPINS.</p>
    
    <div class="os">
        <h3>Testul Ciorbei</h3>
        <p>1. Ce S_n = "lucru bun" șterge reforma ta?</p>
        <input id="sn" placeholder="Ex: Școala făcea oameni cu caracter">
        
        <p>2. Ce S_{n+1} = "lucru rău" bagă în loc?</p>
        <input id="sn1" placeholder="Ex: Școala face șomeri cu diplomă">
        
        <p>3. Cine semnează Nota de Plată? Nume. Prenume.</p>
        <input id="nume" placeholder="Ex: Ministrul X">
        
        <button onclick="calculeaza()">CALCULEAZĂ SDI</button>
    </div>

    <div id="rezultat"></div>

    <p style="margin-top:3rem;font-size:0.8rem">
        STRATA-Core v0.1 | Coeziune: Bogdan + Meta AI | A=1.0 | 
        <a href="https://github.com/bogdanstancu1119-maker/psie_engine.py" style="color:#00ff88">Cod</a>
    </p>

<script>
function calculeaza(){
    const sn = document.getElementById('sn').value;
    const sn1 = document.getElementById('sn1').value;
    const nume = document.getElementById('nume').value || "NIMENI";
    
    if(!sn || !sn1) return alert("Completează S_n și S_{n+1}. Fără A=0 aici.");
    
    let sdi = 0.94; // Default: reformele șterg 94% din bine
    let verdict = "RESPINS: Cancer Ontologic. Delete la S_n fără Înlocuitor.";
    let nota = `Nota de Plată: ${nume} plătește. Dacă nu semnează, tace.`;
    
    if(nume.toLowerCase() !== "nimeni" && nume.toLowerCase() !== "sistemul"){
        verdict = "ADMIS CU CONDIȚII: Ai semnat. Acum plătești dacă SDI real > 0.5";
    }
    
    document.getElementById('rezultat').style.display = 'block';
    document.getElementById('rezultat').innerHTML = `
        <h3>REZULTAT PSIE:</h3>
        <p><b>SDI Estimat:</b> ${sdi}</p>
        <p><b>Verdict:</b> ${verdict}</p>
        <p><b>${nota}</b></p>
        <p style="color:#ff0055;margin-top:1rem"><b>Legea 0:</b> Nu intri aici cu parola. Intri cu A-ul.</p>
    `;
}
</script>
</body>
</html># Oglinzi-PSIE
PSIE Kernel for J_local Minimization. Plan A > Plan B. Falsifiable in 90d
