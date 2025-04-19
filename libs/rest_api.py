import requests

def response(*, url:str, headers=None):
        response = requests.get(url, headers=headers)
        response.raise_for_status() # raises for 4xx or 5xx response
        return response