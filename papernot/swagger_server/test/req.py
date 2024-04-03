import requests
import json
# URL de l'API
url = 'http://0.0.0.0:8080/api/v3/network'

# Données à envoyer dans la requête
request_data = {
	"id1" : "157 boulevard Mac Donald 75019 Paris",
	"id4" : "5 avenue Anatole France 75007 Paris",
	"id5" : "1 Bd de Parc, 77700 Coupvray",
	"id6" : "Place d'Armes, 78000 Versailles",
	"id7" : "17 Rue René Cassin, 51430 Bezannes",
	"id8" : "78 Le Poujol, 30125 L'Estréchure"
}

# En-têtes de la requête
headers = {
    'Content-Type': 'application/json'
}

dat = json.dumps(request_data)

# Envoi de la requête POST avec les données JSON
response = requests.post(url, json=dat, headers=headers)

# Vérification du code de statut de la réponse
if response.status_code == 200:
    # Traitement de la réponse JSON
    response_data = response.json()
    print("Réponse reçue :", response_data)
elif response.status_code == 400:
    print("Requête incorrecte :", response.text)
elif response.status_code == 404:
    print("Ressource non trouvée :", response.text)
elif response.status_code == 422:
    print("Entité non traitable :", response.text)
elif response.status_code == 503:
    print("Service indisponible :", response.text)
else:
    print("Erreur inattendue :", response.text)
