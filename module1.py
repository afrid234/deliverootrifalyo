import requests

url = "https://auth-sandbox.developers.deliveroo.com/oauth2/token"

headers = {
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded",
    "authorization": "Basic dHFianVoNWoyYXNkNTFuYnYzNDQ4cWFiNjprZDJkZjlkaGo4cGUzZHYzY2tyMHVkdHQwYmo4NGtoZW9vNnRrdWsxdXVnMzlmbDY4OWM="
}

response = requests.post(url, headers=headers)

print(response.text)
