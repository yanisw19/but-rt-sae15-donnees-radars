import csv


# Chargement du fichier CSV contenant les données radar

fichier_csv = "opendata-vitesses-pratiquees-voitures-radars-2023-01-01-2023-12-31-.csv"

donnees = []  # Liste qui va stocker toutes les lignes utiles du CSV

with open(fichier_csv, mode='r', encoding='utf-8') as f:
    lecteur = csv.reader(f, delimiter=';')
    entetes = next(lecteur, None)  # On saute la première ligne (en-têtes)

    for ligne in lecteur:
        # On ignore les lignes incomplètes
        if len(ligne) < 4:
            continue

        # On récupère les valeurs
        date_str = ligne[0]     # Date complète
        position = ligne[1]     # Coordonnées GPS
        mesure = ligne[2]       # Vitesse mesurée
        limite = ligne[3]       # Limite autorisée

        # On convertit les vitesses en float (dans le CSV, virgules → points)
        try:
            mesure = float(mesure.replace(',', '.'))
            limite = float(limite.replace(',', '.'))
        except:
            continue  # Si conversion impossible → on ignore

        # Extraction de l'heure dans la date
        heure = 0
        if " " in date_str and ":" in date_str:
            try:
                heure = int(date_str.split(" ")[1].split(":")[0])
            except:
                heure = 0

        # Extraction du jour (format JJ/MM/AAAA)
        jour = date_str.split(" ")[0]

        # Extraction latitude / longitude
        lat, lon = "", ""
        if " " in position:
            parts = position.split(" ")
            if len(parts) >= 2:
                lat, lon = parts[0], parts[1]

        # Calcul de l'excès (positif si dépassement)
        exces = mesure - limite

        # On stocke toutes les informations dans une liste
        donnees.append([date_str, jour, heure, lat, lon, mesure, limite, exces])



# Calcul de la moyenne des excès par plage horaire

plages = {
    "01h-04h": (1, 4),
    "05h-09h": (5, 9),
    "12h-16h": (12, 16),
    "17h-21h": (17, 21),
    "21h01-00h": (21, 23)  # Inclut aussi l’heure 00
}

moyennes_plages = {}

for nom, (debut, fin) in plages.items():
    total = 0
    n = 0
    for d in donnees:
        # Cas particulier : plage « 21h01-00h » inclut l’heure 0
        if debut <= d[2] <= fin or (nom == "21h01-00h" and d[2] == 0):
            total += d[7]
            n += 1

    # Moyenne des excès (on met un signe - car l’excès est stocké négatif)
    moyennes_plages[nom] = - round(total / n, 2) if n else 0



# Top 10 des vitesses les plus élevées

# On trie toutes les mesures par vitesse décroissante et on prend les 10 premières
stop10 = sorted(donnees, key=lambda x: x[5], reverse=True)[:10]



# Comptage du nombre d'excès par jour

compte_jours = {}
for d in donnees:
    jour = d[1]
    compte_jours[jour] = compte_jours.get(jour, 0) + 1



# Moyenne des excès pour chaque limite de vitesse

limites_data = {}
for d in donnees:
    limite = d[6]
    exces = - d[7]  # On remet l’excès en positif

    if limite not in limites_data:
        limites_data[limite] = [0, 0]  # total, compteur

    limites_data[limite][0] += exces
    limites_data[limite][1] += 1

# On calcule la moyenne par limite
moyennes_limite = {
    limite: round(tot / n, 2)
    for limite, (tot, n) in limites_data.items()
    if n > 0
}



# Création du fichier HTML avec les graphiques Chart.js

html = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Analyse des excès de vitesse</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<link rel="stylesheet" href="style.css">
</head>
<body>

<h1>Analyse des excès de vitesse</h1>

<h2>Moyenne des excès par plage horaire</h2>
<canvas id="plages"></canvas>

<h2>Top 10 des vitesses les plus élevées</h2>
<table>
<tr><th>Latitude</th><th>Longitude</th><th>Vitesse</th></tr>
"""

# Ajout du top 10 dans le tableau HTML
for t in top10:
    lat = round(float(t[3]), 1)
    lon = round(float(t[4]), 1)
    html += f"<tr><td>{lat}</td><td>{lon}</td><td>{t[5]}</td></tr>"

# Suite du HTML (graphique jours + limites)
html += """
</table>

<h2>Excès par jour</h2>
<canvas id="jours"></canvas>

<h2>Moyenne d’excès par limite</h2>
<canvas id="limites"></canvas>

<script>
// Graphique plages horaires
new Chart(document.getElementById('plages'), {
    type:'bar',
    data:{ labels:%s, datasets:[{ label:'Excès moyen (km/h)', data:%s, backgroundColor:'rgba(202,2,119,0.6)' }] }
});

// Graphique jours (limitée aux 7 premiers)
const jours_labels = %s.slice(0,7);
const jours_data   = %s.slice(0,7);
new Chart(document.getElementById('jours'), {
    type:'pie',
    data:{ labels: jours_labels, datasets:[{ data: jours_data, borderColor:'#000', borderWidth:2 }] }
});

// Graphique limites
new Chart(document.getElementById('limites'), {
    type:'line',
    data:{ labels:%s, datasets:[{ label:'Excès moyen (km/h)', data:%s }] }
});
</script>

</body>
<footer class="footer">Site produit par <strong>SOUID Ylies</strong> & <strong>GROT Yanis</strong></footer>
</html>
""" % (
    list(moyennes_plages.keys()), list(moyennes_plages.values()),
    list(compte_jours.keys()), list(compte_jours.values()),
    list(moyennes_limite.keys()), list(moyennes_limite.values())
)

# Sauvegarde du fichier HTML final
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Fichier index.html généré avec succès ! Ouvre-le dans ton navigateur.")
