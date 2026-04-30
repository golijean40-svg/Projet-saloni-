import re

with open(“index.html”, “r”, encoding=“utf-8”) as f:
content = f.read()

module = “””
// == ASSISTANT IA GEMINI ==
var GEMINI_KEY = “AIzaSyAkRRS-b99r0_PcJ9zIm4z2qoYq0Kui_to”;
var GEMINI_URL = “https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=”;

function getContextFlotte() {
var CH = S.data.chauffeurs || [];
var VE = S.data.versements || [];
var DE = S.data.depenses || [];
var t = td();
var vj = VE.filter(function(v){ return v.date===t; });
var totalJ = vj.reduce(function(s,v){ return s+v.montant; }, 0);
var totalR = VE.reduce(function(s,v){ return s+v.montant; }, 0);
var totalD = DE.reduce(function(s,v){ return s+v.montant; }, 0);
var actifs = CH.filter(function(c){ return c.statut===“actif”; });
var ontPaye = actifs.filter(function(c){ return vj.some(function(v){ return String(v.chauffeurId)===String(c.id); }); });
var nontPaye = actifs.filter(function(c){ return !vj.some(function(v){ return String(v.chauffeurId)===String(c.id); }); });
return “Tu es l assistant de gestion de flotte Saloni Manager pour un gerant de tricycles-taxis a Abidjan. “
+ “Chauffeurs actifs: “ + actifs.length + “. “
+ “Ont verse aujourd hui: “ + ontPaye.map(function(c){ return c.nom; }).join(”, “) + “. “
+ “N ont pas verse: “ + nontPaye.map(function(c){ return c.nom; }).join(”, “) + “. “
+ “Total verse aujourd hui: “ + totalJ + “ FCFA. “
+ “Total global: “ + totalR + “ FCFA. “
+ “Depenses: “ + totalD + “ FCFA. “
+ “Benefice net: “ + (totalR - totalD) + “ FCFA. “
+ “Reponds toujours en francais, de maniere concise.”;
}

async function envoyerMessageIA() {
var inp = document.getElementById(“iaInput”);
if (!inp || !inp.value.trim()) return;
var msg = inp.value.trim();
inp.value = “”;
if (!S.iaHist) S.iaHist = [];
S.iaHist.push({ role: “user”, text: msg });
S.iaLoading = true;
renderIAMessages();
try {
var messages = S.iaHist.slice(-10).map(function(m) {
return { role: m.role === “user” ? “user” : “model”, parts: [{ text: m.text }] };
});
var res = await fetch(GEMINI_URL + GEMINI_KEY, {
method: “POST”,
headers: { “Content-Type”: “application/json” },
body: JSON.stringify({
system_instruction: { parts: [{ text: getContextFlotte() }] },
contents: messages
})
});
var data = await res.json();
var rep = data.candidates && data.candidates[0] ? data.candidates[0].content.parts[0].text : “Desole, erreur.”;
S.iaHist.push({ role: “model”, text: rep });
} catch(e) {
S.iaHist.push({ role: “model”, text: “Erreur de connexion.” });
}
S.iaLoading = false;
renderIAMessages();
}

function renderIAMessages() {
var box = document.getElementById(“iaBox”);
if (!box) return;
box.innerHTML = “”;
if (!S.iaHist || S.iaHist.length === 0) {
box.innerHTML = “<div style=\“text-align:center;padding:40px 20px;color:#94a3b8;\”><div style=\“font-size:48px;margin-bottom:12px;\”>\u{1F916}</div><div style=\“font-size:14px;font-weight:700;color:#1d4ed8;\”>Assistant Saloni IA</div><div style=\“font-size:12px;margin-top:8px;\”>Posez vos questions sur votre flotte</div></div>”;
return;
}
S.iaHist.forEach(function(m) {
var moi = m.role === “user”;
var bbl = document.createElement(“div”);
bbl.style.cssText = “display:flex;justify-content:” + (moi ? “flex-end” : “flex-start”) + “;margin-bottom:10px;”;
var inner = document.createElement(“div”);
inner.style.cssText = “max-width:82%;background:” + (moi ? “linear-gradient(135deg,#1d4ed8,#3b82f6)” : “#fff”) + “;color:” + (moi ? “#fff” : “#0f172a”) + “;border-radius:” + (moi ? “16px 16px 4px 16px” : “16px 16px 16px 4px”) + “;padding:11px 14px;font-size:13px;line-height:1.6;box-shadow:0 2px 8px rgba(0,0,0,.08);border:” + (moi ? “none” : “1px solid #dbeafe”) + “;”;
inner.textContent = m.text;
bbl.appendChild(inner);
box.appendChild(bbl);
});
if (S.iaLoading) {
var load = document.createElement(“div”);
load.style.cssText = “display:flex;justify-content:flex-start;margin-bottom:10px;”;
load.innerHTML = “<div style=\“background:#fff;border:1px solid #dbeafe;border-radius:16px 16px 16px 4px;padding:12px 16px;display:flex;gap:5px;align-items:center;\”><div style=\“width:8px;height:8px;border-radius:50%;background:#1d4ed8;animation:pulse .8s infinite;\”></div><div style=\“width:8px;height:8px;border-radius:50%;background:#1d4ed8;animation:pulse .8s infinite .2s;\”></div><div style=\“width:8px;height:8px;border-radius:50%;background:#1d4ed8;animation:pulse .8s infinite .4s;\”></div></div>”;
box.appendChild(load);
}
box.scrollTop = box.scrollHeight;
}

function renderIA(sc) {
var wrap = document.createElement(“div”);
wrap.style.cssText = “display:flex;flex-direction:column;height:calc(100vh - 115px);”;
var iaBox = document.createElement(“div”);
iaBox.id = “iaBox”;
iaBox.style.cssText = “flex:1;overflow-y:auto;padding:14px;background:#f8faff;”;
wrap.appendChild(iaBox);
var suggestions = document.createElement(“div”);
suggestions.style.cssText = “padding:8px 12px;background:#fff;border-top:1px solid #dbeafe;display:flex;gap:6px;overflow-x:auto;”;
[“Qui n a pas verse ?”, “Mon benefice ?”, “Conseils recettes”, “Resume du jour”].forEach(function(s) {
var btn = document.createElement(“button”);
btn.style.cssText = “padding:6px 12px;border-radius:20px;background:#eff6ff;border:1px solid #bfdbfe;color:#1d4ed8;font-size:11px;font-weight:700;cursor:pointer;white-space:nowrap;flex-shrink:0;”;
btn.textContent = s;
btn.onclick = function() { var inp = document.getElementById(“iaInput”); if (inp) { inp.value = s; envoyerMessageIA(); } };
suggestions.appendChild(btn);
});
wrap.appendChild(suggestions);
var inputDiv = document.createElement(“div”);
inputDiv.style.cssText = “padding:10px 12px;background:#fff;border-top:1px solid #dbeafe;display:flex;gap:8px;align-items:flex-end;”;
var ta = document.createElement(“textarea”);
ta.id = “iaInput”;
ta.placeholder = “Posez votre question…”;
ta.rows = 1;
ta.style.cssText = “flex:1;min-height:42px;max-height:90px;resize:none;border-radius:12px;padding:10px 12px;font-size:14px;border:1.5px solid #bfdbfe;background:#f8faff;font-family:inherit;”;
ta.onkeydown = function(e) { if (e.keyCode === 13 && !e.shiftKey) { e.preventDefault(); envoyerMessageIA(); } };
var sendBtn = document.createElement(“button”);
sendBtn.textContent = “\u2191”;
sendBtn.style.cssText = “width:44px;height:44px;border-radius:12px;background:linear-gradient(135deg,#1d4ed8,#3b82f6);border:none;color:#fff;font-size:20px;cursor:pointer;flex-shrink:0;”;
sendBtn.onclick = function() { envoyerMessageIA(); };
var clearBtn = document.createElement(“button”);
clearBtn.textContent = “\u{1F5D1}”;
clearBtn.style.cssText = “width:44px;height:44px;border-radius:12px;background:#fef2f2;border:1px solid #fecaca;font-size:16px;cursor:pointer;flex-shrink:0;”;
clearBtn.onclick = function() { S.iaHist = []; renderIAMessages(); };
inputDiv.appendChild(ta);
inputDiv.appendChild(sendBtn);
inputDiv.appendChild(clearBtn);
wrap.appendChild(inputDiv);
sc.innerHTML = “”;
sc.appendChild(wrap);
renderIAMessages();
}
“””

if “GEMINI_KEY” not in content:
content = content.replace(”</script>”, module + “\n</script>”, 1)
print(“OK: Module Gemini IA ajoute”)
else:
print(“INFO: Module deja present”)

old_screen = ‘if(S.tab===“carte”){renderCarte(sc);’
new_screen = ’if(S.tab===“ia”){renderIA(sc);var oldF=document.getElementById(“fab”);if(oldF)oldF.remove();return;}\n ’ + old_screen
if ‘renderIA(sc)’ not in content:
content = content.replace(old_screen, new_screen, 1)
print(“OK: Rendu IA ajoute”)

with open(“index.html”, “w”, encoding=“utf-8”) as f:
f.write(content)

print(“OK: index.html mis a jour avec Gemini IA!”)
