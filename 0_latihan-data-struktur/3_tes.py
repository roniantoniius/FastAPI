import requests

print("Tambah Barang: ")
print(
    requests.post(
        "http://127.0.0.1:8000/",
        json={
            "nama": "Kertas",
            "harga": 1000,
            "jumlah": 20,
            "id": 3,
            "kategori": "alat",
        }).json()
)

print(requests.get("http://127.0.0.1:8000/").json())
print()

print("Update barang:")
print(requests.put("http://127.0.0.1:8000/update/0?count=9001").json())
print(requests.get("http://127.0.0.1:8000/").json())
print()

print("Hapus Barang:")
print(requests.delete("http://127.0.0.1:8000/delete/0").json())
print(requests.get("http://127.0.0.1:8000/").json())