# Author: [Your Name]
# Email: [Your Email]
# Description: A script to scan directories on websites, retrieve their titles, and save results to a file.
# License: [Your License Information]

import requests
from urllib.parse import urljoin

def get_title_from_html(html):
    """Ambil judul halaman dari HTML"""
    start = html.find("<title>")
    end = html.find("</title>")
    if start != -1 and end != -1:
        return html[start + 7:end].strip()  # Menghilangkan spasi di awal dan akhir judul
    return "No Title Found"

def write_to_file(filename, text):
    """Menulis hasil temuan ke dalam file"""
    with open(filename, 'a') as file:
        file.write(text + '\n')

def scan_directory(website, dir_name, found_file):
    """Memindai direktori di website tertentu"""
    url = urljoin(website, dir_name)  # Gabungkan URL dasar dengan direktori
    try:
        response = requests.get(url, timeout=5)
        title = get_title_from_html(response.text)
        
        # Cek status code dan tampilkan hasil
        if response.status_code == 200:
            result = f"[+] Found: {url:<40} (Status: {response.status_code:>3}) - Title: {title}"

            # Cek jika title mengandung "File Manager", "Responsive Filemanager", atau "Laravel" (case-insensitive)
            if any(keyword in title for keyword in ["File Manager", "Responsive Filemanager", "Laravel"]):
                write_to_file(found_file, result)  # Menyimpan hasil yang ditemukan
                print(f"\033[32m{result}\033[0m")  # Hijau untuk hasil ditemukan dan langsung disimpan
        elif response.status_code == 403:
            result = f"[+] Forbidden: {url:<40} (Status: {response.status_code:>3}) - Title: {title}"
            print(f"\033[33m{result}\033[0m")  # Kuning untuk forbidden
        else:
            result = f"[-] Not Found: {url:<40} (Status: {response.status_code:>3})"
            print(f"\033[31m{result}\033[0m")  # Merah untuk not found
    except requests.exceptions.RequestException:
        # Tidak mencetak pesan error apa pun jika ada request exception
        pass

def main():
    # Tampilkan informasi Nama dan Email Anda saat skrip dijalankan
    print("Adit Ganteng")
    print("Email: [kangpepes@protonmail.com]\n")

    websites_file = input("list: ")
    directories_file = input("dir: ")
    found_file = "found.txt"  # File untuk menyimpan hasil

    try:
        # Membaca daftar website
        with open(websites_file, 'r') as f:
            websites = [line.strip() for line in f.readlines() if line.strip()]
        
        # Membaca daftar direktori
        with open(directories_file, 'r') as f:
            directories = [line.strip() for line in f.readlines() if line.strip()]

        # Memeriksa jika file kosong
        if not websites or not directories:
            print("Tidak ada website atau direktori yang bisa dipindai.")
            return
        
        # Memulai pemindaian
        for website in websites:
            for dir_name in directories:
                scan_directory(website, dir_name, found_file)

        print("\nSelesai!")
    
    except FileNotFoundError as e:
        print(f"File tidak ditemukan: {e}")

if __name__ == "__main__":
    main()
