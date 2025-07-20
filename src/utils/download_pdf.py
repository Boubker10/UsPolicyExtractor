import os
import requests
from datetime import datetime

def telecharger_pdf_dossier_temp(url_pdf, dossier_temp="data/temp"):
    os.makedirs(dossier_temp, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    nom_fichier = f"document_{timestamp}.pdf"
    chemin_complet = os.path.join(dossier_temp, nom_fichier)
    
    response = requests.get(url_pdf)
    if response.status_code != 200:
        raise Exception(f"Erreur téléchargement PDF : {response.status_code}")
    
    with open(chemin_complet, "wb") as f:
        f.write(response.content)
    
    return chemin_complet
