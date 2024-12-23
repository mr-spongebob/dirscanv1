# Author: [Mr.Spongebob]
# Email: [Kangpepes@protonmail.com]
# Description: A script to scan directories on websites, retrieve their titles, and save results to a file.

import requests
from urllib.parse import urljoin

def get_title_from_html(html):
    """Ambil judul halaman dari HTML"""
    start = html.find("<title>")
    end = html.find("</title>")
    if start != -1 and end != -1:
        return html[start + 7:end].strip()  
    return "No Title Found"

def write_to_file(filename, text):
    """Menulis hasil temuan ke dalam file"""
    with open(filename, 'a') as file:
        file.write(text + '\n')

def scan_directory(website, dir_name, found_file):
    """Memindai direktori di website tertentu"""
    url = urljoin(website, dir_name)  
    try:
        response = requests.get(url, timeout=5)
        title = get_title_from_html(response.text)
        
        
        if response.status_code == 200:
            result = f"[+] Found: {url:<40} (Status: {response.status_code:>3}) - Title: {title}"

            
            if any(keyword in title for keyword in ["File Manager", "Responsive Filemanager", "Laravel"]):
                write_to_file(found_file, result)  
                print(f"\033[32m{result}\033[0m")  
        elif response.status_code == 403:
            result = f"[+] Forbidden: {url:<40} (Status: {response.status_code:>3}) - Title: {title}"
            print(f"\033[33m{result}\033[0m")  
        else:
            result = f"[-] Not Found: {url:<40} (Status: {response.status_code:>3})"
            print(f"\033[31m{result}\033[0m")  
    except requests.exceptions.RequestException:
        
        pass

def main():
    
    print("Adit Ganteng")
    print("Email: [kangpepes@protonmail.com]\n")

    websites_file = input("list: ")
    directories_file = input("dir: ")
    found_file = "found.txt"  

    try:
        
        with open(websites_file, 'r') as f:
            websites = [line.strip() for line in f.readlines() if line.strip()]
        
        
        with open(directories_file, 'r') as f:
            directories = [line.strip() for line in f.readlines() if line.strip()]

        
        if not websites or not directories:
            print("Tidak ada website atau direktori yang bisa dipindai.")
            return
        
        
        for website in websites:
            for dir_name in directories:
                scan_directory(website, dir_name, found_file)

        print("\nSelesai!")
    
    except FileNotFoundError as e:
        print(f"File tidak ditemukan: {e}")

if __name__ == "__main__":
    main()
