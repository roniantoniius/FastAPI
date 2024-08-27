import requests

# Mengambil data dari endpoint "/barang/1"
response = requests.get("http://127.0.0.1:8000/barang/0")
print("Status Code:", response.status_code)
print("Response Text:", response.text)
try:
    print("JSON Response:", response.json())
except ValueError as e:
    print("Error decoding JSON:", e)

# Mengambil data dari endpoint "/barang/?nama=Pensil"
response = requests.get("http://127.0.0.1:8000/barang/?nama=Pensil")
print("----------------------------------------------------")
print("Status Code:", response.status_code)
print("Response Text:", response.text)
try:
    print("JSON Response:", response.json())
except ValueError as e:
    print("Error decoding JSON:", e)
