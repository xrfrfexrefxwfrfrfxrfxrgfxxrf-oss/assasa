import subprocess
import os
import sys
import time

API_TOKEN = "c581428172c6ac"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(r"""
 __        __   _     _____          _       _     
 \ \      / /__| |__ |  ___|__  _ __| | ____| |__  
  \ \ /\ / / _ \ '_ \| |_ / _ \| '__| |/ / _` '_ \ 
   \ V  V /  __/ |_) |  _| (_) | |  |   < (_| | | |
    \_/\_/ \___|_.__/|_|  \___/|_|  |_|\_\__,_| |_|

              W E B F E T C H   v3.0
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
        time.sleep(0.4)
        print(".", end="", flush=True)
    print("\n")

def fetch_ip(ip=""):
    try:
        loading()

        if ip == "":
            url = "https://api.ipinfo.io/lite/me"
        else:
            url = f"https://api.ipinfo.io/lite/{ip}"

        result = subprocess.run(
            ["curl", "-s", "-H", f"Authorization: Bearer {API_TOKEN}", url],
            capture_output=True,
            text=True
        )

        print("------------- IP INFORMATION -------------")
        print(result.stdout)
        print("------------------------------------------\n")

    except Exception as e:
        print("Error:", e)

def main():
    clear()
    banner()

    while True:
        cmd = input("webfetch> ").strip().lower()

        if cmd == "exit":
            break

        elif cmd == "ip":
            fetch_ip("")

        elif cmd == "fetch ip":
            ip = input("Enter IP: ").strip()
            fetch_ip(ip)

        elif cmd == "clear":
            clear()
            banner()

        else:
            print("Unknown command")

    input("\nPress ENTER to close...")

if __name__ == "__main__":
    main()
