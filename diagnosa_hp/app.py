from flask import Flask, render_template, request

app = Flask(__name__)

gejala = {
    1: "Baterai cepat habis",
    2: "HP mati total",
    3: "Layar tidak menyala",
    4: "Ada garis di layar",
    5: "Layar retak",
    6: "HP panas saat digunakan",
    7: "Tidak bisa dicas",
    8: "Port charger longgar",
    9: "Suara tidak keluar",
    10: "Speaker terdengar pecah",
    11: "HP restart sendiri",
    12: "Tidak bisa masuk sistem (bootloop)"
}

kerusakan = {
    "Baterai rusak": [1, 6],
    "Port charger rusak": [7, 8],
    "Layar rusak": [3, 4, 5],
    "Speaker rusak": [9, 10],
    "Overheat": [6, 11],
    "Sistem error (bootloop)": [11, 12, 2]
}

solusi_kerusakan = {
    "Baterai rusak": [
        "Ganti baterai dengan yang baru dan original",
        "Hindari penggunaan HP saat charging",
        "Periksa apakah baterai menggelembung"
    ],
    "Port charger rusak": [
        "Bersihkan port charger dari debu",
        "Gunakan charger dengan konektor yang masih rapat",
        "Jika tetap tidak bisa dicas: ganti port charger"
    ],
    "Layar rusak": [
        "Ganti layar LCD touchscreen jika retak/tidak menyala",
        "Periksa konektor layar pada mainboard",
        "Cek voltase driver LCD jika layar gelap total"
    ],
    "Speaker rusak": [
        "Cek suara menggunakan headset untuk membandingkan",
        "Bersihkan lubang speaker dari debu",
        "Ganti speaker jika suara pecah atau hilang"
    ],
    "Overheat": [
        "Tutup aplikasi latar belakang yang berat",
        "Hindari main game saat charging",
        "Jika panas ekstrem, periksa baterai atau IC power"
    ],
    "Sistem error (bootloop)": [
        "Masuk recovery mode lalu lakukan wipe cache/factory reset",
        "Jika tidak berhasil, lakukan flashing ulang sistem",
        "Jika gagal juga, periksa IC emmc atau memori internal"
    ]
}

@app.route('/', methods=['GET', 'POST'])
def index():
    hasil = []
    pola_khusus = False

    if request.method == 'POST':
        input_gejala = set(map(int, request.form.getlist('gejala')))
        hasil = []

        for nama_kerusakan, daftar_gejala in kerusakan.items():
            cocok = input_gejala & set(daftar_gejala)
            tidak_cocok = set(daftar_gejala) - input_gejala
            persen = round((len(cocok) / len(daftar_gejala)) * 100, 2)
            if persen > 0:
                hasil.append({
                    'nama': nama_kerusakan,
                    'persen': persen,
                    'cocok': [gejala[i] for i in cocok],
                    'tidak_cocok': [gejala[i] for i in tidak_cocok],
                    'solusi': solusi_kerusakan[nama_kerusakan]
                })

        if {1, 6, 7}.issubset(input_gejala):
            pola_khusus = True

    return render_template('index.html', gejala=gejala, hasil=hasil, pola_khusus=pola_khusus)

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

