# MOBILE COVERAGE

Request mobile coverage for a given address



## Overview

# Requirements
Python 3.5.2+

## Usage
To run the server, please execute the following from the root directory:

```
pip3 install -r requirements.txt
python3 -m swagger_server
```

and open your browser to here:

```
http://localhost:8080/api/v3/ui/
```

Your Swagger definition lives here:

```
http://localhost:8080/api/v3/swagger.json
```

To launch the integration tests, use tox:
```
sudo pip install tox
tox
```



## Installation

Install the Endpoint with docker 

```bash
  git clone https://github.com/hackolite/papernest.git
  cd ./papernest/papernot/
  docker build -t papernest .
  docker run -p 8080:8080 papernot:latest -d
```
    
## Documentation

[Api Documentation](http://0.0.0.0:8080/api/v3/ui/#/Network)
and open your browser to here:

```
http://localhost:8080/api/v3/ui/
```

Your Swagger definition lives here:

```
http://localhost:8080/api/v3/swagger.json
```

## Tox Tests

To launch the integration tests, use tox:
```
sudo pip install tox
tox
```

## Running Tests

To run tests, run the following command

```bash
    cd ./papernest/
    python3.8 -m pip install -r test-requirements.txt
    cd  ./papernot/swagger_server/test
    python3.8 test_unit.py
    python3.8 test_validation.py
```


## Usage/Examples

```python
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

```

```bash
  python3.8 test_validation.py
```
## Optimizations

pagination for easy rendering
better async

