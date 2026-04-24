import requests
import re
import os

# الألوان للتنسيق
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def scrape_proxies():
    # قائمة المصادر (يمكنك إضافة المزيد)
    sources = [
        "https://api.proxyscrape.com/v2/?request=getproxies&proxytype=all&timeout=10000&country=all&ssl=all&anonymity=all",
        "https://www.proxy-list.download/api/v1/get?type=http",
        "https://www.proxy-list.download/api/v1/get?type=https",
        "https://www.proxy-list.download/api/v1/get?type=socks4",
        "https://www.proxy-list.download/api/v1/get?type=socks5",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt"
    ]

    found_proxies = []
    print(f"[*] Starting to scrape proxies from {len(sources)} sources...")

    for url in sources:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # استخراج أي نص يطابق نمط IP:PORT
                proxies = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', response.text)
                found_proxies.extend(proxies)
                print(f"{GREEN}[+] Scraped {len(proxies)} proxies from: {url.split('/')[2]}{RESET}")
        except:
            print(f"{RED}[-] Failed to reach: {url.split('/')[2]}{RESET}")

    # إزالة التكرار
    unique_proxies = list(set(found_proxies))
    
    # حفظ النتائج
    with open("proxy.txt", "w") as f:
        for proxy in unique_proxies:
            f.write(proxy + "\n")

    print(f"\n{GREEN}[!] Done! Total unique proxies saved: {len(unique_proxies)}{RESET}")
    print(f"[*] File saved as: proxy.txt")

if __name__ == "__main__":
    scrape_proxies()
