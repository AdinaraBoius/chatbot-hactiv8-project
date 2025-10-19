# 🤖 Chatbot Asisten Rekomendasi Anime

Ini adalah proyek *final project* untuk program "Maju Bareng AI" dari Hacktiv8. Aplikasi ini merupakan sebuah chatbot sederhana yang dibuat menggunakan Streamlit dan ditenagai oleh Google Gemini API. Chatbot ini berperan sebagai asisten yang berpengetahuan luas untuk memberikan rekomendasi anime kepada pengguna.

## 🚀 Fitur

* **Antarmuka Chat Interaktif:** Dibuat dengan Streamlit untuk pengalaman pengguna yang mulus.
* **Kepribadian Profesional:** Chatbot diprogram untuk bersikap sebagai seorang analis anime yang ahli, menghindari stereotip, dan memberikan rekomendasi yang jelas.
* **Responsif:** Menggunakan model `gemini-2.5-flash` untuk respons yang cepat.
* **Manajemen Sesi:** Mengingat riwayat percakapan dan memiliki tombol reset.

## 🛠️ Instalasi dan Cara Menjalankan

### Prasyarat

* Pastikan Anda sudah menginstal [Miniconda](https://docs.conda.io/en/latest/miniconda.html).
* Anda memerlukan **Google AI API Key** untuk menjalankan aplikasi.

### Langkah-langkah

1.  **Buat dan Aktifkan Environment Conda**

    Buka terminal atau Anaconda Prompt, lalu jalankan perintah berikut untuk membuat lingkungan virtual baru dan mengaktifkannya:

    ```bash
    conda create -n anime-chatbot python=3.11 -y
    conda activate anime-chatbot
    ```

2.  **Instal *Dependencies***

    Setelah lingkungan aktif, instal semua *library* yang dibutuhkan dengan perintah:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Jalankan Aplikasi Streamlit**

    Jalankan aplikasi dengan perintah berikut:

    ```bash
    streamlit run streamlit_chat_app.py
    ```

    Aplikasi akan otomatis terbuka di browser Anda. Masukkan Google AI API Key Anda di sidebar untuk memulai percakapan.

## 📄 Struktur Kode

* **`streamlit_chat_app.py`**: File utama yang berisi semua logika aplikasi Streamlit, antarmuka pengguna, dan interaksi dengan Gemini API.
* **`requirements.txt`**: Daftar semua *library* Python yang diperlukan oleh proyek ini.
* **`.streamlit/secrets.toml`**: (Opsional, untuk *deployment*) File untuk menyimpan API Key secara aman saat di-*deploy* ke Streamlit Cloud.
