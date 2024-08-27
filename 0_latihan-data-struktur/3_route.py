from enum import Enum
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

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

barang = {
    0: Barang(nama='Buku', harga=9500, jumlah=4, id=0, kategori=Kategori.ALAT),
    1: Barang(nama='Pensil', harga=2000, jumlah=10, id=1, kategori=Kategori.ALAT),
    2: Barang(nama='Roti', harga=5000, jumlah=5, id=2, kategori=Kategori.MAKANAN),
}

@app.get("/")
def index() -> dict[str, dict[int, dict]]:
    return {"data": {key: item.dict() for key, item in barang.items()}}

@app.get("/barang/{barang_id}")
def kueri_barang_id(barang_id: int) -> dict[str, dict]:
    if barang_id not in barang:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    return {"data": barang[barang_id].dict()}  # Memperbaiki struktur data yang dikembalikan

@app.get("/barang/")
def kuery_barang_parameter(
    nama: str | None = None,
    harga: float | None = None,
    jumlah: int | None = None,
    kategori: Kategori | None = None,
) -> dict[str, dict | list[dict]]:
    
    def periksa_barang(item: Barang):
        return all(
            (
                nama is None or item.nama == nama,
                harga is None or item.harga == harga,
                jumlah is None or item.jumlah == jumlah,
                kategori is None or item.kategori == kategori,
            )
        )
    
    periksa = [item.dict() for item in barang.values() if periksa_barang(item)]

    return {"kueri": {"nama": nama, "harga": harga, "jumlah": jumlah, "kategori": kategori}, "hasil": periksa}

@app.post("/")
def tambah_barang(item: Barang) -> dict[str, Barang]:

    if item.id in barang:
        HTTPException(status_code=400, detail=f"Barang dengan {item.id=} sudah ada")
    
    barang[item.id] = item
    return {"added": item}

# update
@app.put("/update/{barang_id}")
def update(
    barang_id: int,
    nama: str | None = None,
    harga: float | None = None,
    jumlah: int | None = None,
) -> dict[str, Barang]:
    
    if barang_id not in barang:
        HTTPException(status_code=404, detail="Barang dengan {barang_id} tidak ditemukan")
    
    if all(info is None for info in (nama, harga, jumlah)):
        raise HTTPException(
            status_code=400, detail="Tidak ada parameter yang diubah"
        )
    
    item = barang[barang_id]
    if nama is not None:
        item.nama = nama
    if harga is not None:
        item.harga = harga
    if jumlah is not None:
        item.jumlah = jumlah
    
    return {"updated": item}


# delete
@app.delete("/delete/{barang_id}")
def hapus_barang(barang_id: int) -> dict[str, Barang]:

    if barang_id not in barang:
        raise HTTPException(status_code=404, detail="Baran dengan {barang_id} tidak ditemukan")
    
    item = barang.pop(barang_id)
    return {"dihapus": item}