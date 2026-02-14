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

        CYBER TOOLKIT V7 FULL RECON
--------------------------------------------------------
neofetch | gpu | ip | fetch ip | publicip
osint user | osint domain | email osint
subdomains | email domain | mx
dns | headers | status | robots
whois | ports
hash | base64
clear | exit
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
        print("GPU info not supported")

# ---------------- IP INTEL ----------------
def fetch_ip_info(ip="me"):
    try:
        if ip == "" or ip.lower() == "me":
            url = "https://api.ipinfo.io/lite/me"
        else:
            url = f"https://api.ipinfo.io/lite/{ip}"

        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code != 200:
            print("API ERROR:", r.status_code)
            print(r.text)
            return

        data = r.json()

        ip_addr = data.get("ip", "N/A")
        city = data.get("city", "N/A")
        region = data.get("region", "N/A")
        country = data.get("country", "N/A")
        loc = data.get("loc", "N/A")
        org = data.get("org", "N/A")
        timezone = data.get("timezone", "N/A")
        asn = data.get("asn", "N/A")

        print("\n============= IP INTEL =============")
        print(f"IP:        {ip_addr}")
        print(f"City:      {city}")
        print(f"Region:    {region}")
        print(f"Country:   {country}")
        print(f"Location:  {loc}")
        print(f"Timezone:  {timezone}")
        print(f"Org:       {org}")
        print(f"ASN:       {asn}")

        if loc != "N/A":
            print(f"Google Maps: https://www.google.com/maps?q={loc}")

        try:
            host = socket.gethostbyaddr(ip_addr)[0]
            print(f"Reverse DNS: {host}")
        except:
            print("Reverse DNS: N/A")

        print("====================================\n")

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
    print("Checking basic footprint...")
    domain = email.split("@")[-1]
    try:
        print("Domain IP:", socket.gethostbyname(domain))
    except:
        print("Domain lookup failed")

def subdomain_lookup():
    domain = input("Domain: ")
    subs = ["www", "mail", "ftp", "dev", "api", "test"]
    for sub in subs:
        full = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(full)
            print(f"[FOUND] {full} -> {ip}")
        except:
            pass

def email_domain_check():
    email = input("Email: ")
    domain = email.split("@")[-1]
    print("Domain:", domain)
    try:
        print("IP:", socket.gethostbyname(domain))
    except:
        print("Lookup failed")

def mx_lookup():
    domain = input("Domain: ")
    os.system(f"nslookup -type=mx {domain}")

# ---------------- NETWORK ----------------
def dns_lookup():
    domain = input("Domain: ")
    try:
        print("IP:", socket.gethostbyname(domain))
    except:
        print("DNS lookup failed")

def http_headers():
    url = input("URL: ")
    try:
        r = requests.get(url)
        for k,v in r.headers.items():
            print(f"{k}: {v}")
    except:
        print("Header fetch failed")

def http_status():
    url = input("URL: ")
    try:
        r = requests.get(url)
        print("Status Code:", r.status_code)
    except:
        print("Request failed")

def robots_check():
    domain = input("Domain: ")
    try:
        r = requests.get(f"https://{domain}/robots.txt")
        print(r.text)
    except:
        print("robots.txt not found")

def port_scan():
    print("Scanning localhost ports 1-1024...")
    for port in range(1,1025):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)
        if s.connect_ex(("127.0.0.1", port))==0:
            print(f"Port {port} OPEN")
        s.close()

# ---------------- UTIL ----------------
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
        elif cmd=="subdomains":
            subdomain_lookup()
        elif cmd=="email domain":
            email_domain_check()
        elif cmd=="mx":
            mx_lookup()
        elif cmd=="dns":
            dns_lookup()
        elif cmd=="headers":
            http_headers()
        elif cmd=="status":
            http_status()
        elif cmd=="robots":
            robots_check()
        elif cmd=="ports":
            port_scan()
        elif cmd=="hash":
            hash_tool()
        elif cmd=="base64":
            base64_tool()
        else:
            print("Unknown command")

if __name__=="__main__":
    main()
