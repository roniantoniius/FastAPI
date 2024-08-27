from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel

# define our fastapi app so that we can call the method like get, post, put, and delete

app = FastAPI()

class Kategori(str, Enum):
    ALAT    = 'alat'
    MAKANAN = 'makanan'

class Barang(BaseModel):
    nama: str
    harga: float
    jumlah: int
    id: int
    kategori: Kategori

list_barang = {
    0: Barang(nama='Buku', harga=9500, jumlah=4, id=0, kategori=Kategori.ALAT),
    1: Barang(nama='Pensil', harga=2000, jumlah=10, id=1, kategori=Kategori.ALAT),
    2: Barang(nama='Roti', harga=5000, jumlah=5, id=2, kategori=Kategori.MAKANAN),
}

# Fast API itu menghasilkan data dalam format JSON secara otomatis secara serialisasi dan deserialisasi

# serialisasi adalah proses mengubah objek Python menjadi string JSON
# deserialisasi adalah proses mengubah string JSON menjadi objek Python

@app.get("/")
def index() -> dict[str, dict[int, Barang]]:
    return {"data": list_barang}