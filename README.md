# **Solver reCAPTCHA v2**  

**Modul Python untuk menyelesaikan reCAPTCHA v2 secara otomatis menggunakan Selenium dan pengenalan suara.** Modul ini dirancang untuk bekerja dengan tantangan audio reCAPTCHA.  

## **Fitur**  
- Mengotomatisasi interaksi dengan reCAPTCHA v2.  
- Mendukung penyelesaian tantangan audio reCAPTCHA.  
- Menggunakan **Selenium**, **pydub**, dan **SpeechRecognition** untuk menyelesaikan CAPTCHA secara otomatis.  

---  

## **Instalasi**  

### **Persyaratan:**  
1. Pastikan Python **3.8+** sudah terinstal di sistem Anda.  
2. Siapkan virtual environment untuk mengisolasi dependensi:  
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```
3. Instal modul menggunakan pip:  
   ```bash
   pip install reborn2022
   ```  

---  

## **Penggunaan**  

### **1. Menggunakan Fungsi Langsung di Kode Python**  

1. Pastikan Anda memiliki **driver Selenium** yang sesuai dengan browser yang digunakan (misalnya, ChromeDriver untuk Google Chrome) dan letakkan di dalam direktori `/usr/bin/` atau di lokasi yang ada di sistem PATH Anda.  
2. Impor modul dan gunakan fungsinya dalam kode Python Anda:  
   ```python
   from reborn2022.recaptcha import solve_recaptcha

   url = "https://www.google.com/recaptcha/api2/demo"
   token = solve_recaptcha(url, headless=True)  # headless default True

   print(token)
   ```
3. Fungsi `solve_recaptcha` akan secara otomatis membuka halaman reCAPTCHA, berinteraksi dengan tantangan audio, dan mengembalikan token hasil penyelesaiannya.  

---  

### **2. Menggunakan API Lokal (Server Lokal)**  

Anda juga dapat menjalankan solver reCAPTCHA sebagai **server lokal** dengan menggunakan **Quart**, lalu mengaksesnya melalui request API.  

#### **Menjalankan Server Lokal**  

Buat file Python (misalnya `run_server.py`) dengan isi berikut:  

```python
import asyncio
from reborn2022.api_solver import start_api

host = "127.0.0.1"  # Jalankan di localhost
port = 5000         # Gunakan port 5000
debug = False       # Matikan mode debug untuk produksi

start_api(host=host, port=port, debug=debug)
```

Jalankan server dengan perintah berikut di terminal:  

```bash
python run_server.py
```

Jika server berjalan dengan benar, Anda akan melihat bahwa API tersedia di `http://127.0.0.1:5000/solve`.  

#### **Menggunakan API Solver di File Terpisah**  

Setelah server berjalan, buat file Python baru (misalnya `solve_captcha.py`) dan gunakan kode berikut untuk mengirim permintaan ke server:  

```python
import asyncio
from reborn2022.test_solver import test_solver

async def main():
    token = await test_solver(
        "https://www.google.com/recaptcha/api2/demo"
    )
    print(token)

asyncio.run(main())
```

Jalankan file ini di terminal lain untuk mendapatkan token reCAPTCHA:  

```bash
python solve_captcha.py
```

Jika berhasil, Anda akan mendapatkan token hasil penyelesaian CAPTCHA dalam output terminal.  

---  

## **Dependensi**  

Modul ini bergantung pada pustaka berikut, yang akan diinstal secara otomatis:  
- **Selenium** – untuk mengotomatisasi interaksi dengan browser.  
- **pydub** – untuk memproses file audio dari tantangan reCAPTCHA.  
- **SpeechRecognition** – untuk mengenali teks dari audio CAPTCHA.  
- **Quart** – untuk menjalankan solver sebagai server API.  
- **aiohttp** – untuk membuat permintaan HTTP asinkron ke API solver.  

---  

## **Masalah yang Diketahui**  
- Modul ini **hanya** mendukung tantangan audio reCAPTCHA v2, **tidak** untuk tantangan berbasis gambar.  
- Beberapa situs web mungkin memiliki perlindungan tambahan yang dapat memblokir otomatisasi ini.  

---  

## **Kontribusi**  
Kami menyambut kontribusi dari komunitas! Jika Anda ingin berkontribusi pada pengembangan modul ini, silakan:  
1. Buat **pull request** dengan perubahan atau perbaikan yang diusulkan.  
2. Laporkan masalah atau ajukan saran melalui **issue** di repository proyek.  

---  

## **Lisensi**  
Proyek ini dilisensikan di bawah **[MIT License](LICENSE)**, yang memungkinkan penggunaan bebas dengan batasan minimal.  




