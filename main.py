import requests
import os
import sys
import time

API_URL = "https://api.ipwho.org/{}"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(r"""
 __        __   _     _____          _       _     
 \ \      / /__| |__ |  ___|__  _ __| | ____| |__  
  \ \ /\ / / _ \ '_ \| |_ / _ \| '__| |/ / _` '_ \ 
   \ V  V /  __/ |_) |  _| (_) | |  |   < (_| | | |
    \_/\_/ \___|_.__/|_|  \___/|_|  |_|\_\__,_| |_|
                                                    
              W E B F E T C H   v1.0
--------------------------------------------------------
Commands:
  ip         -> Show your IP info
  fetch ip   -> Lookup specific IP
  clear      -> Clear screen
  exit       -> Quit
--------------------------------------------------------
""")

def loading():
    print("Fetching data", end="")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print("\n")

def get_ip_info(ip=""):
    try:
        loading()
        url = API_URL.format(ip)
        response = requests.get(url)
        data = response.json()

        if not data.get("success", True):
            print("Error:", data.get("message"))
            return

        print("------------- IP INFORMATION -------------")
        print(f"IP Address\t{data.get('ip')}")
        print(f"City\t\t{data.get('city')}")
        print(f"Region\t\t{data.get('region')}")
        print(f"Country\t\t{data.get('country')} ({data.get('country_code')})")
        print(f"Postal Code\t{data.get('postal')}")
        print(f"Latitude / Longitude\t{data.get('latitude')} , {data.get('longitude')}")
        print(f"Time Zone\t{data.get('timezone')}")
        print(f"Calling Code\t+{data.get('calling_code')}")
        print(f"Currency\t{data.get('currency')}")
        print(f"Languages\t{data.get('languages')}")
        print(f"ASN\t\t{data.get('connection', {}).get('asn')}")
        print(f"Org\t\t{data.get('connection', {}).get('org')}")
        print("------------------------------------------\n")

    except Exception as e:
        print("Failed to fetch data:", e)

def main():
    clear()
    banner()

    while True:
        cmd = input("webfetch> ").strip().lower()

        if cmd == "exit":
            print("Goodbye 👋")
            sys.exit()

        elif cmd == "ip":
            get_ip_info("")

        elif cmd == "fetch ip":
            ip = input("Enter IP: ").strip()
            get_ip_info(ip)

        elif cmd == "clear":
            clear()
            banner()

        else:
            print("Unknown command")

if __name__ == "__main__":
    main()
