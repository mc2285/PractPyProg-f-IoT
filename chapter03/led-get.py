import requests

resp = requests.get("http://127.0.0.1:5000/led")

print(resp.status_code, resp.reason)

print(resp.text)

body = resp.json()
print(f"Ustawienie wynosi: {body['level']}")

