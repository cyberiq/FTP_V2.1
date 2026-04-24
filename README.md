# FTP_V2.1
ftp brutforce

🛠️ FTP Penetration Testing Suite: Technical Overview 🚀
This system is a sophisticated multi-threaded security tool designed to audit FTP server credentials while maintaining anonymity through a dynamic proxy-rotation layer. It consists of two main modules working in a "Chain of Command" sequence.

📂 1. The Architecture (The Map) 🗺️
The tool follows a strict directory structure to manage its logic and data:

ftp_2.1.py: The "Brain" (Main Engine).

user.txt & pass.txt: The "Payloads" (Credential lists).

proxy/: The "Safe Zone" (Contains the proxy scraper/checker and results).

🛡️ 2. Module One: The Proxy Sentinel (prxy.py) 🛰️
Before the attack begins, the system ensures you are protected.

Validation: It reads raw proxies from proxy.txt.

Threaded Checking: It uses 30 concurrent threads to ping a target (like Google) to see if the proxy is "Live."

Filtering: Only successful proxies are saved to live.txt.

The Kill-Switch: 🛑 Crucial Feature: If prxy.py finishes and finds zero working proxies, the entire tool shuts down immediately. This prevents the script from accidentally exposing your real IP address during the FTP test.

🔑 3. Module Two: The FTP Engine (ftp_2.1.py) ⚡
Once the proxies are ready, the main engine takes over:

A. Automated Launch 🤖
The script automatically triggers the proxy module first. You don't have to run them separately; the "Chain of Command" is fully automated.

B. Proxy Tunneling (SOCKS5/HTTP) 🌪️
Standard Python FTP libraries don't support proxies. This tool uses PySocks to monkey-patch the global socket. This means every single packet sent to the target FTP server is forced through a proxy tunnel.

C. Smart Rotation 🔄
The tool doesn't just use one proxy. It uses a Round-Robin algorithm:

Attempt 1 (User A: Pass 1) -> Proxy 1

Attempt 2 (User A: Pass 2) -> Proxy 2

Attempt 3 (User A: Pass 3) -> Proxy 3
This makes it extremely difficult for Firewalls or Intrusion Detection Systems (IDS) to ban you, because the requests come from different IPs every second.

D. Multi-Threaded Brute-Forcing 🏎️
The tool processes users and passwords in batches of 10.

It logs in, tests the credentials, and exits.

If a match is found (SUCCESS!), it immediately stops all threads, prints the result in a bold green banner, and saves the "hit" to results.txt.

📊 4. The Workflow Summary 📈
Initialization: Clears screen and displays the Cyber_iq ASCII Art. 🎨

Proxy Scan: Runs prxy.py to filter out dead connections. 🔍

Safety Check: Verifies if live.txt has data. If empty -> EXIT. ⚠️

Targeting: Asks the user for the Target IP. 🎯

Execution: Loops through user.txt and pass.txt.

Success: Saves valid credentials to results.txt. ✅

⚠️ Technical Requirements
To run this setup, the environment must have:

Python 3.x

pip install requests PySocks

Correct permissions to read/write files in the local directory.
