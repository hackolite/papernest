import unittest
import requests
import json 

class TestNetworkAPI(unittest.TestCase):
    base_url = 'http://0.0.0.0:8080'  # URL de base de votre API

    def test_network_api(self):
        # Données à envoyer dans la requête POST
        data = {
            'additionalProp1': 'string',
            'additionalProp2': 'string',
            'additionalProp3': 'string'
        }

        # En-têtes de la requête
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }


        # Convert the dictionary to JSON format

        # Set the appropriate headers for JSON content
        headers = {'Content-Type': 'application/json'}

        data = json.dumps(data)
        # Effectuer la requête POST
        response = requests.post(f"{self.base_url}/api/v3/network", json=data, headers=headers)

        # Vérifier le code de statut de la réponse
        self.assertEqual(response.status_code, 200)

        # Vérifier le contenu de la réponse
        response_data = response.json()
        # Ajoutez ici vos assertions sur la réponse JSON reçue

if __name__ == '__main__':
    unittest.main()
➜  test 

