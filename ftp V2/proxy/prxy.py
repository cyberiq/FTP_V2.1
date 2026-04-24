import requests
import threading
import queue
import os
import sys

# إعدادات الألوان للواجهة
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# البنر الفني - تم استخدام r لتجنب أخطاء الرموز
Proxy_Banner = fr"""{GREEN}
  ____                             ____ _                _             
 |  _ \ _ __ _____  ___   _        / ___| |__   ___  ___| | _____ _ __ 
 | |_) | '__/ _ \ \/ / | | |_____| |   | '_ \ / _ \/ __| |/ / _ \ '__|
 |  __/| | | (_) >  <| |_| |_____| |___| | | |  __/ (__|   <  __/ |   
 |_|   |_|  \___/_/\_\\__, |      \____|_| |_|\___|\___|_|\_\___|_|   
                       |___/                                          {RESET}"""

Cyber_Banner = r"""
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

# إعدادات الفحص
target_url = "https://www.google.com"
timeout_seconds = 5
threads_count = 30
input_file = "proxy.txt"
output_file = "live.txt"

proxy_queue = queue.Queue()
live_proxies = []

def load_proxies():
    if not os.path.exists(input_file):
        print(f"{RED}[!] Error: '{input_file}' not found!{RESET}")
        return False
    
    with open(input_file, "r") as f:
        for line in f:
            if line.strip():
                proxy_queue.put(line.strip())
    
    print(f"[*] Loaded {proxy_queue.qsize()} proxies from {input_file}")
    return True

def check_proxy():
    while not proxy_queue.empty():
        proxy = proxy_queue.get()
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        try:
            response = requests.get(target_url, proxies=proxies, timeout=timeout_seconds)
            if response.status_code == 200:
                print(f"{GREEN}[+] LIVE: {proxy}{RESET}")
                with open(output_file, "a") as f:
                    f.write(proxy + "\n")
                live_proxies.append(proxy)
            else:
                print(f"{RED}[-] DEAD: {proxy}{RESET}")
        except:
            print(f"{RED}[-] DEAD: {proxy}{RESET}")
        
        proxy_queue.task_done()

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(Proxy_Banner)
    print(f"{GREEN}{Cyber_Banner}{RESET}")
    print(f"\n{GREEN}instagram ---> @Cyber_iq{RESET}\n")
    
    if load_proxies():
        print(f"[*] Starting threads... Please wait.\n")
        
        for _ in range(threads_count):
            t = threading.Thread(target=check_proxy)
            t.daemon = True
            t.start()

        proxy_queue.join()
        
        # الميزة المطلوبة: التحقق من وجود بروكسيات تعمل
        if not live_proxies:
            print(f"\n{RED}[!] No working proxies found. Shutting down the tool...{RESET}")
            sys.exit() # إطفاء الأداة فوراً
            
        print(f"\n{GREEN}[*] Finished! Working proxies saved to: {output_file}{RESET}")
        print(f"[*] Total Live: {len(live_proxies)}")

if __name__ == "__main__":
    main()
