import requests
r = requests.get('http://localhost:5000/user/baoijsdf')
print(r.text)