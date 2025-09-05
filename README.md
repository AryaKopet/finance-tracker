# Finance Tracker Web Application

![My Skills](https://skillicons.dev/icons?i=python,flask,tailwind,sqlite&theme=dark)

## 📌 Tentang Projek
**Finance Tracker** adalah aplikasi berbasis web yang dibangun menggunakan **Flask (Python)** untuk membantu pengguna dalam mencatat, mengelola, dan memantau arus keuangan pribadi.  
Sistem ini mendukung pencatatan pemasukan maupun pengeluaran, serta menyediakan fitur **upload bukti transaksi** dan **manajemen profil dengan avatar pengguna**.

## 🎯 Fitur Utama
- ✅ Autentikasi user (Login & Logout)  
- ✅ Dashboard ringkasan pemasukan, pengeluaran, dan saldo  
- ✅ Pencatatan transaksi (pemasukan & pengeluaran)  
- ✅ Upload & lihat bukti transaksi (gambar/struk)  
- ✅ Profil user (ubah nama, email, password, dan avatar)  
- ✅ Sidebar & header responsif untuk tampilan mobile dan desktop  

## 🛠️ Teknologi yang Digunakan
- **Backend** : [Flask](https://flask.palletsprojects.com/)  
- **Frontend** : [Tailwind CSS](https://tailwindcss.com/) + [Lucide Icons](https://lucide.dev/)  
- **Database** : SQLite / PostgreSQL (via SQLAlchemy ORM)  
- **Bahasa Pemrograman** : Python 3  

## 🚀 Cara Menjalankan
1. **Clone repository**
   ```bash
   git clone https://github.com/AryaKopet/finance-tracker.git
   cd finance-tracker
2. **Buat dan aktifkan virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # MacOS/Linux
   venv\Scripts\activate      # Windows
3. **Install depedencies**
   ```bash
   pip install -r requirements.txt
4. **Inisialisasi database**
   ```bash
   python
   >>> from database import Base, engine
   >>> from models import User, Transaction
   >>> Base.metadata.create_all(bind=engine)
   >>> exit()
5. **Jalankan aplikasi**
   ```bash
   python app.py
6. **Buka di browser**
   ```bash
   http://127.0.0.1:5000

## 👨‍💻 Kontribusi
Pull request selalu diterima. Untuk perubahan besar, silakan buka issue terlebih dahulu untuk mendiskusikan perubahan yang ingin dilakukan.
