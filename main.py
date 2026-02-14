import os
import socket
import platform
import getpass
import psutil
import subprocess
import hashlib
import base64
import requests

# ---------------- CONFIG ----------------
API_TOKEN = "c581428172c6ac"

# ---------------- UTIL ----------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(r"""
 ██████╗██╗   ██╗██████╗ ███████╗███████╗████████╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝
██║      ╚████╔╝ ██████╔╝█████╗  █████╗     ██║   
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══╝     ██║   
╚██████╗   ██║   ██████╔╝███████╗██║        ██║   
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝        ╚═╝   

        CYBER TOOLKIT V6 ULTRA
--------------------------------------------------------
Commands:
 neofetch
 gpu
 ip
 fetch ip
 publicip
 osint user
 osint domain
 email osint
 headers
 dns
 whois
 hash
 base64
 ports
 clear
 exit
--------------------------------------------------------
""")

# ---------------- SYSTEM ----------------
def neofetch():
    print(f"User: {getpass.getuser()}")
    print(f"Hostname: {socket.gethostname()}")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"CPU: {platform.processor()}")
    print(f"RAM: {round(psutil.virtual_memory().total / (1024**3),2)} GB")
    print(f"Python: {platform.python_version()}\n")

def gpu_info():
    try:
        result = subprocess.run(
            ["wmic", "path", "win32_VideoController", "get", "name"],
            capture_output=True, text=True)
        print(result.stdout)
    except:
        print("GPU info not supported on this OS")

# ---------------- IPINFO LITE ----------------
def fetch_ip_info(ip="me"):
    try:
        if ip == "" or ip.lower() == "me":
            url = "https://api.ipinfo.io/lite/me"
        else:
            url = f"https://api.ipinfo.io/lite/{ip}"

        headers = {"Authorization": f"Bearer {API_TOKEN}"}

        print("\nFetching IP data...\n")

        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code != 200:
            print("API ERROR:", r.status_code)
            print(r.text)
            return

        data = r.json()

        print("============= IP INFORMATION (LITE) =============")
        for key, value in data.items():
            print(f"{key.capitalize():20} {value}")
        print("=================================================\n")

    except Exception as e:
        print("IP fetch failed:", e)

def public_ip():
    try:
        ip = requests.get("https://api.ipify.org").text
        print("Public IP:", ip)
    except:
        print("Failed to get public IP")

# ---------------- OSINT ----------------
def osint_user():
    username = input("Username: ")
    sites = [
        f"https://github.com/{username}",
        f"https://twitter.com/{username}",
        f"https://instagram.com/{username}",
        f"https://linkedin.com/in/{username}"
    ]
    for site in sites:
        try:
            r = requests.get(site)
            print(f"[{'FOUND' if r.status_code==200 else 'NOT FOUND'}] {site}")
        except:
            print(f"[ERROR] {site}")

def osint_domain():
    domain = input("Domain: ")
    os.system(f"whois {domain}")

def email_osint():
    email = input("Email: ")
    sites = [
        f"https://www.gravatar.com/{email}",
        f"https://haveibeenpwned.com/unifiedsearch/{email}"
    ]
    for site in sites:
        try:
            r = requests.get(site)
            print(f"[{'FOUND' if r.status_code==200 else 'NOT FOUND'}] {site}")
        except:
            print(f"[ERROR] {site}")

# ---------------- NETWORK TOOLS ----------------
def dns_lookup():
    domain = input("Domain: ")
    try:
        print("IP:", socket.gethostbyname(domain))
    except:
        print("DNS lookup failed")

def http_headers():
    url = input("URL (https://example.com): ")
    try:
        r = requests.get(url)
        for k,v in r.headers.items():
            print(f"{k}: {v}")
    except:
        print("Header fetch failed")

def port_scan():
    print("Scanning localhost ports 1-1024...")
    for port in range(1,1025):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)
        if s.connect_ex(("127.0.0.1", port))==0:
            print(f"Port {port} OPEN")
        s.close()

# ---------------- UTIL TOOLS ----------------
def hash_tool():
    text = input("Text: ")
    print("MD5:", hashlib.md5(text.encode()).hexdigest())
    print("SHA256:", hashlib.sha256(text.encode()).hexdigest())

def base64_tool():
    mode = input("encode/decode: ").lower()
    text = input("Text: ")
    if mode=="encode":
        print(base64.b64encode(text.encode()).decode())
    else:
        print(base64.b64decode(text.encode()).decode())

# ---------------- MAIN ----------------
def main():
    clear()
    banner()
    while True:
        cmd = input("cyber> ").lower()

        if cmd=="exit":
            break
        elif cmd=="clear":
            clear(); banner()
        elif cmd=="neofetch":
            neofetch()
        elif cmd=="gpu":
            gpu_info()
        elif cmd=="ip":
            fetch_ip_info("me")
        elif cmd=="fetch ip":
            ip = input("Enter IP: ")
            fetch_ip_info(ip)
        elif cmd=="publicip":
            public_ip()
        elif cmd=="osint user":
            osint_user()
        elif cmd=="osint domain":
            osint_domain()
        elif cmd=="email osint":
            email_osint()
        elif cmd=="dns":
            dns_lookup()
        elif cmd=="headers":
            http_headers()
        elif cmd=="hash":
            hash_tool()
        elif cmd=="base64":
            base64_tool()
        elif cmd=="ports":
            port_scan()
        else:
            print("Unknown command")

if __name__=="__main__":
    main()
