import requests


def get_access_token():
    url = 'https://oauth.fatsecret.com/connect/token'
    client_id = 'c3b5a516072c4f7a995c3190b6c7d172 '  # client ID
    client_secret = '7b21342cc42f463e85fcdfae7a2b1a0a'  # client secret
    data = {
        'grant_type': 'client_credentials',
        'scope': 'basic'
    }
    response = requests.post(url, auth=(client_id, client_secret), data=data)
    response_data = response.json()
    return response_data['access_token']


def show_food_list(query, access_token):
    url = 'https://platform.fatsecret.com/rest/server.api'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    params = {
        'method': 'foods.search',
        'search_expression': query,
        'format': 'json'
    }

    response = requests.post(url, headers=headers, params=params)
    return response.json()


def get_food_details(food_id):
    access_token = get_access_token()
    url = 'https://platform.fatsecret.com/rest/server.api'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'method': 'food.get.v4',
        'food_id': food_id,
        'format': 'json'
    }
    response = requests.post(url, headers=headers, params=params)
    return response.json()


def search_food(query):
    access_token = get_access_token()
    search_result = show_food_list(query, access_token)
    return search_result

