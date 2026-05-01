import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

print("Taille avant:", len(content))

# Trouver et remplacer tout le bloc renderIA existant
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

# Supprimer renderIA existant pour le remplacer
content, found = suppr_fn(content, 'renderIA')
print(("Supprime renderIA" if found else "renderIA absent"))

# Supprimer iaEnvoyer et iaEnvoyerInput si presents
for fn in ['iaEnvoyer', 'iaEnvoyerInput', 'gCtx']:
    content, found = suppr_fn(content, fn)
    print(("Supprime: " if found else "Absent: ") + fn)

# Supprimer variables GK et GU
content = re.sub(r'var GK="[^"]*";\n', '', content)
content = re.sub(r'var GU="[^"]*";\n', '', content)
content = re.sub(r'if\(!S\.gh\)S\.gh=\[\];\n', '', content)
content = re.sub(r'// === GEMINI IA SALONI ===\n', '', content)

# Ajouter le nouveau code complet et fonctionnel
nouveau_code = r"""
// === GEMINI IA SALONI MANAGER ===
var GK = "AIzaSyAkRRS-b99r0_PcJ9zIm4z2qoYq0Kui_to";
var GU = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=";

function gCtx() {
  var CH = S.data.chauffeurs || [];
  var VE = S.data.versements || [];
  var DE = S.data.depenses || [];
  var t = td();
  var vj = VE.filter(function(v) { return v.date === t; });
  var tJ = vj.reduce(function(s, v) { return s + v.montant; }, 0);
  var tR = VE.reduce(function(s, v) { return s + v.montant; }, 0);
  var tD = DE.reduce(function(s, v) { return s + v.montant; }, 0);
  var ac = CH.filter(function(c) { return c.statut === "actif"; });
  var op = ac.filter(function(c) { return vj.some(function(v) { return String(v.chauffeurId) === String(c.id); }); });
  var np = ac.filter(function(c) { return !vj.some(function(v) { return String(v.chauffeurId) === String(c.id); }); });
  return "Tu es l assistant IA Saloni Manager, flotte tricycles-taxis Abidjan. " +
    "Actifs:" + ac.length + ". " +
    "Ont verse aujourd hui:" + op.map(function(c) { return c.nom; }).join(",") + ". " +
    "N ont pas verse:" + np.map(function(c) { return c.nom; }).join(",") + ". " +
    "Total jour:" + tJ + " FCFA. Global:" + tR + " FCFA. Depenses:" + tD + " FCFA. Benefice:" + (tR - tD) + " FCFA. " +
    "Reponds en francais concis et pratique.";
}

async function gEnvoyer(question) {
  if (!question || !question.trim()) return;
  if (!S.gh) S.gh = [];
  S.gh.push({ r: "user", t: question.trim() });
  S.iaLoading = true;
  renderIA(document.getElementById("screen"));
  try {
    var msgs = S.gh.slice(-8).map(function(m) {
      return { role: m.r === "user" ? "user" : "model", parts: [{ text: m.t }] };
    });
    var res = await fetch(GU + GK, {
      method: "POST",
      mode: "cors",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        system_instruction: { parts: [{ text: gCtx() }] },
        contents: msgs
      })
    });
    if (!res.ok) {
      var errText = await res.text();
      throw new Error("HTTP " + res.status + ": " + errText.substring(0, 100));
    }
    var d = await res.json();
    var rep = d.candidates && d.candidates[0] ? d.candidates[0].content.parts[0].text : "Pas de reponse.";
    S.gh.push({ r: "model", t: rep });
  } catch(e) {
    S.gh.push({ r: "model", t: "Erreur: " + (e.message || String(e)) });
  }
  S.iaLoading = false;
  renderIA(document.getElementById("screen"));
  setTimeout(function() { var b = document.getElementById("gBox"); if (b) b.scrollTop = b.scrollHeight; }, 100);
}

function gEnvoyerInput() {
  var inp = document.getElementById("gInp");
  if (!inp || !inp.value.trim()) return;
  var q = inp.value.trim();
  inp.value = "";
  gEnvoyer(q);
}

function renderIA(sc) {
  if (!sc) return;
  if (!S.gh) S.gh = [];

  var suggestions = [
    "Qui n a pas verse aujourd hui ?",
    "Mon benefice ce mois ?",
    "Chauffeur le plus actif",
    "Conseils pour ameliorer mes recettes"
  ];

  var wrap = document.createElement("div");
  wrap.style.cssText = "display:flex;flex-direction:column;height:calc(100vh - 115px);background:#f8faff;";

  // Zone messages
  var box = document.createElement("div");
  box.id = "gBox";
  box.style.cssText = "flex:1;overflow-y:auto;padding:12px;";

  if (S.gh.length === 0) {
    box.innerHTML = "<div style='text-align:center;padding:30px 16px;color:#94a3b8;'>" +
      "<div style='font-size:48px;margin-bottom:12px;'>&#x1F916;</div>" +
      "<div style='font-size:15px;font-weight:700;color:#1d4ed8;margin-bottom:8px;'>Assistant Gemini IA</div>" +
      "<div style='font-size:12px;line-height:1.8;'>Posez vos questions sur votre flotte</div>" +
      "</div>";
  } else {
    S.gh.forEach(function(m) {
      var u = m.r === "user";
      var d = document.createElement("div");
      d.style.cssText = "display:flex;justify-content:" + (u ? "flex-end" : "flex-start") + ";margin-bottom:10px;";
      var p = document.createElement("div");
      p.style.cssText = "max-width:85%;padding:11px 14px;border-radius:" +
        (u ? "16px 16px 4px 16px" : "16px 16px 16px 4px") +
        ";background:" + (u ? "linear-gradient(135deg,#1d4ed8,#3b82f6)" : "#fff") +
        ";color:" + (u ? "#fff" : "#0f172a") +
        ";font-size:13px;line-height:1.6;box-shadow:0 2px 8px rgba(0,0,0,.08);" +
        "border:" + (u ? "none" : "1px solid #dbeafe") + ";white-space:pre-wrap;";
      p.textContent = m.t;
      d.appendChild(p);
      box.appendChild(d);
    });

    if (S.iaLoading) {
      var ld = document.createElement("div");
      ld.style.cssText = "display:flex;justify-content:flex-start;margin-bottom:10px;";
      ld.innerHTML = "<div style='padding:12px 16px;background:#fff;border:1px solid #dbeafe;border-radius:16px;font-size:18px;'>&#x23F3;</div>";
      box.appendChild(ld);
    }
  }
  wrap.appendChild(box);

  // Suggestions
  var sq = document.createElement("div");
  sq.style.cssText = "padding:6px 10px;background:#fff;border-top:1px solid #dbeafe;display:flex;gap:6px;overflow-x:auto;flex-shrink:0;";
  suggestions.forEach(function(s) {
    var btn = document.createElement("button");
    btn.style.cssText = "padding:5px 11px;border-radius:16px;background:#eff6ff;border:1px solid #bfdbfe;color:#1d4ed8;font-size:11px;font-weight:600;cursor:pointer;white-space:nowrap;flex-shrink:0;";
    btn.textContent = s;
    btn.onclick = function() { gEnvoyer(s); };
    sq.appendChild(btn);
  });
  wrap.appendChild(sq);

  // Input
  var row = document.createElement("div");
  row.style.cssText = "display:flex;gap:7px;padding:8px 10px;background:#fff;border-top:1px solid #dbeafe;align-items:flex-end;flex-shrink:0;";

  var ta = document.createElement("textarea");
  ta.id = "gInp";
  ta.placeholder = "Posez votre question...";
  ta.rows = 1;
  ta.style.cssText = "flex:1;border:1.5px solid #bfdbfe;border-radius:11px;padding:9px 12px;font-size:14px;resize:none;min-height:40px;max-height:80px;font-family:inherit;background:#f8faff;outline:none;";
  ta.onkeydown = function(e) {
    if (e.keyCode === 13 && !e.shiftKey) { e.preventDefault(); gEnvoyerInput(); }
  };

  var sb = document.createElement("button");
  sb.style.cssText = "height:44px;padding:0 16px;border-radius:11px;background:linear-gradient(135deg,#1d4ed8,#3b82f6);border:none;color:#fff;font-size:14px;font-weight:700;cursor:pointer;flex-shrink:0;";
  sb.textContent = "Envoyer";
  sb.onclick = function() { gEnvoyerInput(); };

  var cb = document.createElement("button");
  cb.style.cssText = "height:44px;width:44px;border-radius:11px;background:#fef2f2;border:1px solid #fecaca;color:#dc2626;font-size:13px;font-weight:700;cursor:pointer;flex-shrink:0;";
  cb.textContent = "X";
  cb.onclick = function() { S.gh = []; renderIA(sc); };

  row.appendChild(ta);
  row.appendChild(sb);
  row.appendChild(cb);
  wrap.appendChild(row);

  sc.innerHTML = "";
  sc.appendChild(wrap);

  setTimeout(function() { var b = document.getElementById("gBox"); if (b) b.scrollTop = b.scrollHeight; }, 50);
  var oldF = document.getElementById("fab"); if (oldF) oldF.remove();
}
"""

# Insérer avant le dernier </script>
last = content.rfind("</script>")
if last >= 0:
    content = content[:last] + nouveau_code + "\n" + content[last:]
    print("OK: Nouveau code Gemini insere")

print("Taille apres:", len(content))

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("OK: index.html mis a jour!")
