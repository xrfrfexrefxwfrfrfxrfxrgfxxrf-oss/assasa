import os
import socket
import platform
import getpass
import psutil
import subprocess
import hashlib
import base64
import time
import requests

# ---------------- CONFIG ----------------
API_TOKEN = "c581428172c6ac"
IPINFO_URL = "https://api.ipinfo.io/{}"

# ---------------- UTIL ----------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(r"""
 ██████╗██╗   ██╗██████╗ ███████╗███████╗████████╗ ██████╗██╗  ██╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔════╝██║  ██║
██║      ╚████╔╝ ██████╔╝█████╗  █████╗     ██║   ██║     ███████║
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══╝     ██║   ██║     ██╔══██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║   ██║   ╚██████╗██║  ██║
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝

        CYBER TOOLKIT ULTIMATE v4.0
--------------------------------------------------------
Commands:
 neofetch        -> System info
 gpu             -> GPU info
 ip              -> Show detailed IP info
 fetch ip        -> Lookup detailed IP
 publicip        -> Show public IP
 osint user      -> Username OSINT
 osint domain    -> Domain info
 email osint     -> Email OSINT
 headers         -> HTTP headers
 dns             -> DNS lookup
 whois           -> Whois lookup
 hash            -> Hash generator
 base64          -> Encode / Decode
 ports           -> Scan localhost ports
 clear           -> Clear screen
 exit            -> Quit
--------------------------------------------------------
""")

# ---------------- SYSTEM TOOLS ----------------
def neofetch():
    print(f"User: {getpass.getuser()}")
    print(f"Hostname: {socket.gethostname()}")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"CPU: {platform.processor()}")
    print(f"RAM: {round(psutil.virtual_memory().total / (1024**3),2)} GB")
    print(f"Python: {platform.python_version()}")
    print("")

def gpu_info():
    try:
        result = subprocess.run(["wmic", "path", "win32_VideoController", "get", "name"],
                                capture_output=True, text=True)
        print(result.stdout)
    except:
        print("GPU info not supported on this OS")

# ---------------- NETWORK / IP ----------------
def fetch_ip_info(ip="me"):
    url = IPINFO_URL.format(ip)
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        if "error" in data:
            print("Error:", data.get("error"))
            return
        print("------------- IP INFORMATION -------------")
        print(f"IP Address:      {data.get('ip')}")
        print(f"Hostname:        {data.get('hostname')}")
        print(f"City:            {data.get('city')}")
        print(f"Region:          {data.get('region')}")
        print(f"Country:         {data.get('country')}")
        print(f"Postal:          {data.get('postal')}")
        print(f"Org:             {data.get('org')}")
        print(f"ASN:             {data.get('asn')}")
        print(f"Location:        {data.get('loc')}")
        print(f"Timezone:        {data.get('timezone')}")
        print(f"Phone:           {data.get('phone')}")
        print(f"Country Calling: {data.get('country_calling_code')}")
        print(f"Currency:        {data.get('currency')}")
        print(f"Languages:       {data.get('languages')}")
        print("------------------------------------------\n")
    except Exception as e:
        print("Failed to fetch IP info:", e)

def public_ip():
    try:
        ip = requests.get("https://api.ipify.org").text
        print("Public IP:", ip)
    except:
        print("Failed to get public IP")

# ---------------- OSINT TOOLS ----------------
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
            if r.status_code == 200:
                print(f"[FOUND] {site}")
            else:
                print(f"[NOT FOUND] {site}")
        except:
            print(f"[ERROR] {site}")

def osint_domain():
    domain = input("Domain: ")
    os.system(f"whois {domain}")

def email_osint():
    email = input("Email: ")
    sites = [
        f"https://haveibeenpwned.com/unifiedsearch/{email}",
        f"https://www.gravatar.com/{email}"
    ]
    for site in sites:
        try:
            r = requests.get(site)
            if r.status_code == 200:
                print(f"[FOUND] {site}")
            else:
                print(f"[NOT FOUND] {site}")
        except:
            print(f"[ERROR] {site}")

# ---------------- OTHER TOOLS ----------------
def dns_lookup():
    domain = input("Domain: ")
    try:
        print("IP:", socket.gethostbyname(domain))
    except:
        print("Failed DNS lookup")

def http_headers():
    url = input("URL (https://example.com): ")
    try:
        r = requests.get(url)
        for k, v in r.headers.items():
            print(f"{k}: {v}")
    except:
        print("Failed fetching headers")

def hash_tool():
    text = input("Text: ")
    print("MD5:", hashlib.md5(text.encode()).hexdigest())
    print("SHA256:", hashlib.sha256(text.encode()).hexdigest())

def base64_tool():
    mode = input("encode/decode: ").lower()
    text = input("Text: ")
    if mode == "encode":
        print(base64.b64encode(text.encode()).decode())
    else:
        print(base64.b64decode(text.encode()).decode())

def port_scan():
    print("Scanning localhost ports 1-1024...")
    for port in range(1,1025):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)
        if s.connect_ex(("127.0.0.1", port)) == 0:
            print(f"Port {port} OPEN")
        s.close()

# ---------------- MAIN ----------------
def main():
    clear()
    banner()
    while True:
        cmd = input("cyber> ").lower()
        if cmd == "exit":
            break
        elif cmd == "clear":
            clear(); banner()
        elif cmd == "neofetch":
            neofetch()
        elif cmd == "gpu":
            gpu_info()
        elif cmd == "ip":
            fetch_ip_info("me")
        elif cmd == "fetch ip":
            ip = input("Enter IP: ")
            fetch_ip_info(ip)
        elif cmd == "publicip":
            public_ip()
        elif cmd == "osint user":
            osint_user()
        elif cmd == "osint domain":
            osint_domain()
        elif cmd == "email osint":
            email_osint()
        elif cmd == "dns":
            dns_lookup()
        elif cmd == "headers":
            http_headers()
        elif cmd == "hash":
            hash_tool()
        elif cmd == "base64":
            base64_tool()
        elif cmd == "ports":
            port_scan()
        else:
            print("Unknown command")

if __name__ == "__main__":
    main()
