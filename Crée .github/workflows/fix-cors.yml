import re, os

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Remplacer l'appel fetch Gemini par une version corrigee
old_fetch = (
    'var res=await fetch(GU+GK,{method:"POST",'
    'headers:{"Content-Type":"application/json"},'
    'body:JSON.stringify({'
)
new_fetch = (
    'var res=await fetch(GU+GK,{method:"POST",'
    'mode:"cors",'
    'headers:{"Content-Type":"application/json"},'
    'body:JSON.stringify({'
)

if old_fetch in content:
    content = content.replace(old_fetch, new_fetch, 1)
    print("OK: mode cors ajoute")
else:
    print("Pattern non trouve - recherche alternative")
    # Chercher le fetch Gemini
    idx = content.find('fetch(GU+GK')
    if idx >= 0:
        print("Fetch trouve a position:", idx)
        print("Contexte:", content[idx:idx+150])

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("OK: index.html mis a jour!")
