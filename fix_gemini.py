import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

print("Taille avant:", len(content))

# 1. Nettoyer la balise xlsx qui contient du code IA en trop
pattern = r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/xlsx/0\.18\.5/xlsx\.full\.min\.js">.*?</script>'
replacement = '<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>'
new_content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)
if new_content != content:
    print("OK: Balise xlsx nettoyee")
    content = new_content
else:
    print("INFO: Balise xlsx deja propre")

# 2. Supprimer les anciennes fonctions IA
def suppr_fn(code, nom):
    pattern = r'function\s+' + re.escape(nom) + r'\s*\([^)]*\)\s*\{'
    m = re.search(pattern, code)
    if not m:
        return code, False
    start = m.start()
    depth = 0
    i = m.end() - 1
    while i < len(code):
        if code[i] == '{': depth += 1
        elif code[i] == '}':
            depth -= 1
            if depth == 0:
                return code[:start] + code[i+1:], True
        i += 1
    return code, False

for fn in ['iaEnvoyer', 'iaEnvoyerInput', 'analyseLocale']:
    content, found = suppr_fn(content, fn)
    print(("OK supprime: " if found else "Absent: ") + fn)

# 3. Ajouter Gemini avant le dernier </script>
if "GEMINI IA SALONI" not in content:
    gemini = (
        '\n// === GEMINI IA SALONI ===\n'
        'var GK="AIzaSyAkRRS-b99r0_PcJ9zIm4z2qoYq0Kui_to";\n'
        'var GU="https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=";\n'
        'if(!S.gh)S.gh=[];\n'
        'function gCtx(){var CH=S.data.chauffeurs||[];var VE=S.data.versements||[];var DE=S.data.depenses||[];var t=td();var vj=VE.filter(function(v){return v.date===t;});var tJ=vj.reduce(function(s,v){return s+v.montant;},0);var tR=VE.reduce(function(s,v){return s+v.montant;},0);var tD=DE.reduce(function(s,v){return s+v.montant;},0);var ac=CH.filter(function(c){return c.statut==="actif";});var op=ac.filter(function(c){return vj.some(function(v){return String(v.chauffeurId)===String(c.id);});});var np=ac.filter(function(c){return!vj.some(function(v){return String(v.chauffeurId)===String(c.id);});});return "Tu es l assistant IA Saloni Manager, flotte tricycles-taxis Abidjan. Actifs:"+ac.length+". Verse:"+op.map(function(c){return c.nom;}).join(",")+". Pas verse:"+np.map(function(c){return c.nom;}).join(",")+". Jour:"+tJ+" FCFA. Total:"+tR+" FCFA. Depenses:"+tD+". Benefice:"+(tR-tD)+". Reponds en francais concis.";}\n'
        'async function iaEnvoyer(question){if(!question)return;if(!S.gh)S.gh=[];S.gh.push({r:"user",t:question});S.iaLoading=true;rScreen();try{var msgs=S.gh.slice(-8).map(function(m){return{role:m.r==="user"?"user":"model",parts:[{text:m.t}]};});var res=await fetch(GU+GK,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({system_instruction:{parts:[{text:gCtx()}]},contents:msgs})});var d=await res.json();var rep=d.candidates&&d.candidates[0]?d.candidates[0].content.parts[0].text:"Desole, erreur.";S.gh.push({r:"model",t:rep});}catch(e){S.gh.push({r:"model",t:"Erreur: "+e.message});}S.iaLoading=false;rScreen();setTimeout(function(){var b=document.getElementById("iaBox");if(b)b.scrollTop=b.scrollHeight;},100);}\n'
        'function iaEnvoyerInput(){var inp=document.getElementById("iaInput");if(!inp||!inp.value.trim())return;var q=inp.value.trim();inp.value="";iaEnvoyer(q);}\n'
    )
    last = content.rfind("</script>")
    if last >= 0:
        content = content[:last] + gemini + "\n" + content[last:]
        print("OK: Gemini ajoute")
else:
    print("INFO: Gemini deja present")

# 4. Corriger rScreenGlobal pour utiliser S.gh au lieu de S.iaHist
# Remplacer les references a S.iaHist dans le rendu IA
content = content.replace(
    'S.iaHist.length===0?',
    '(!S.gh||S.gh.length===0)?'
)
content = content.replace(
    ':S.iaHist.map(function(m){var moi=m.role==="user"',
    ':S.gh.map(function(m){var moi=m.r==="user"'
)
content = content.replace(
    'm.content.replace',
    'm.t.replace'
)
content = content.replace(
    '+(S.iaLoading?',
    '+(S.iaLoading&&S.gh&&S.gh.length>0?'
)

print("Taille apres:", len(content))

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("OK: index.html mis a jour!")
