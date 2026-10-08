import requests

body = {'level': 73}

resp = requests.post("http://127.0.0.1:5000/led", json=body)

print(resp.status_code, resp.reason)
print(resp.text)

