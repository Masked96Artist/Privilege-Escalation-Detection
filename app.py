import subprocess
import socket
import csv
import platform
import psutil
import pyautogui
import webbrowser
import time
import os
import re
import logging
import pyshark
import win32com.client
import argparse
from datetime import datetime, timedelta

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


print("""
 ________ ___________  ________            ____     _______  
 \______   \\_   _____/ /  _____/          /_   |    \   _  \\
  |     ___/ |    __)_ /   \\  ___          |   |    /  /_\\  \\
  |    |     |        \\\\    \\_\\  \\         |   |    \\  \\_/   \\
  |____|    /_______  / \\______  /         |___| /\\  \\_____  /
                    \\/         \\/                \\/        \\/
""")

def get_system_stats():
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent

    stats_str = (
        f"CPU Usage: {cpu_percent}%\n"
        f"Memory Usage: {memory_percent}%\n"
        f"Disk Usage: {disk_percent}%"
    )

    return stats_str

def append_to_csv(filename, data):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

def combine():
    cpu_percent = get_system_stats()
    
    filename = "system_stats.csv"
    data = [cpu_percent]
    append_to_csv(filename, data)
    
    print("System statistics appended to", filename)
        
def get_local_ip():
    try:
        hostname = socket.gethostname()

        ip_address = socket.gethostbyname(hostname)
        
        return ip_address
    except socket.error as e:
        print("Error:", e)

def run_nmap(options, target, output_file):
    options ='-A -O -sC'
    target = get_local_ip()
    command = ["nmap"] + options.split() + [target]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        parsed_output = []
        lines = result.stdout.splitlines()
        for line in lines:
            if "/tcp" in line:  
                parts = line.split()
                port = parts[0].split("/")[0]
                state = parts[1]
                service = parts[2]
                parsed_output.append([port, state, service])

        with open(output_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Port', 'State', 'Service'])
            csv_writer.writerows(parsed_output)
        
        print("Nmap output written to", output_file)
        
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        
def get_operating_system():
    os_name = platform.system()
    os_version = platform.version()
    architecture = platform.architecture()

    return os_name,os_version,architecture

def save_to_file(file_paths, output_file):
    with open(output_file, 'w') as f:
        for file_path in file_paths:
            f.write(file_path + '\n')

def memory():
    memory_percent = psutil.virtual_memory().percent
    return memory_percent

def find_vulnerable_files(directories):
    vulnerable_files = []

    for directory in directories:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_permissions = os.stat(file_path).st_mode & 0o777
                    if file_permissions != 0o666:  
                        vulnerable_files.append(file_path)
                except Exception as e:
                    print(f"Error accessing file: {file_path} - {e}")

    count = len(vulnerable_files)
    return vulnerable_files,count

def check_eternal_blue_vulnerability(b):
    if b <= "11":
        webbrowser.open("https://ncua.gov/newsroom/ncua-report/2017/protect-your-systems-against-eternalblue-vulnerability")
        pyautogui.hotkey('ctrl', 't')  
        time.sleep(7)
        pyautogui.hotkey('ctrl', 'w')
        print("System is vulnerable to EternalBlue")
        CVE1 = "CVE-2017-0144"
    else:
        print("You have updated your system:)")
        CVE1 = None
    
    return CVE1

def scan_and_save_vulnerable_files(directories_to_scan):
    vulnerable_files = find_vulnerable_files(directories_to_scan)
    if vulnerable_files:
        with open('vulnerable_files.txt', 'w') as f:
            f.truncate(0)
        save_to_file(vulnerable_files, 'vulnerable_files.txt')
        print("Vulnerable files found. Saved to vulnerable_files.txt")
        webbrowser.open("https://devineer.medium.com/linux-permissions-unraveled-how-to-avoid-chmod-777-and-keep-the-chaos-at-bay-8874e069a121")
    else:
        print("No vulnerable files found.")
    
def run_sudo_l():
    try:
        result = subprocess.run(['sudo', 'find','/', '-perm', '-u=s'], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None

def find_setuid_files(root_dir='/'):
    setuid_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if os.stat(file_path).st_mode & 0o4000:
                    setuid_files.append(file_path)
            except Exception as e:
                print(f"Error accessing file: {file_path} - {e}")
    return setuid_files

def is2faenabled():
    try:
        sshconfig = subprocess.checkoutput(["cat", "/etc/ssh/sshdconfig"]).decode("utf-8")
        if "ChallengeResponseAuthentication yes" in sshconfig:
            return True
        else:
            return False
    except FileNotFoundError:
        print("The SSH configuration file was not found.")
        return False
    except subprocess.CalledProcessError:
        print("Error running the 'cat' command on /etc/ssh/sshdconfig.")
        return False
    
def enable_2fa():
    try:
        subprocess.run(["sudo", "sed", "-i", "s/^#?ChallengeResponseAuthentication no/ChallengeResponseAuthentication yes/", "/etc/ssh/sshd_config"], check=True)
        print("2FA has been enabled in the SSH configuration file.")
        
        subprocess.run(["sudo", "systemctl", "restart", "sshd"], check=True)
        print("SSH service has been restarted to apply the changes.")
    except subprocess.CalledProcessError:
        print("Error modifying SSH configuration file or restarting SSH service.")
        
def tfa_check():
    if not is2faenabled():
        print("do you want to enable Two factor Authentication?if Yes type 1: ")
        fa_yes=int(input())
        if(fa_yes==1):
            enable_2fa()
        else:
            pass
    else:
        print("2FA is already enabled.")
        
def regx():
    RED = "\033[31m"
    RESET = "\033[0m"


    malicious_patterns = [
        'authentication failure',
        'failed password',
        'malware',
        'suspicious activity',
        ]
    malicious_regex = re.compile('|'.join(malicious_patterns), re.IGNORECASE)
    return malicious_regex,RED,RESET

def analyze_logs(file_path):
    malicious_regex,RED,RESET = regx()
    timestamp_pattern = re.compile(r'^\w{3} \d{1,2} \d{2}:\d{2}:\d{2}')
    two_weeks_ago = datetime.now() - timedelta(weeks=2)
    with open(file_path, 'r') as f:
        for line in f:
            match = timestamp_pattern.search(line)
            if match:
                try:
                    log_time = datetime.strptime(match.group(), "%b %d %H:%M:%S")    
                    log_time = log_time.replace(year=datetime.now().year)
                except ValueError:
                    continue  
                
                if log_time >= two_weeks_ago:
                    if malicious_regex.search(line):
                        print(f"{RED}{line.strip()}{RESET}")
                    else:
                        print(line.strip())

def find_log_files():
    log_paths = [
        "/var/log/",
        "/var/log/syslog",
        "/var/log/messages",
        "/var/log/auth.log",
        "/var/log/apache2/access.log",
        "/var/log/apache2/error.log",
        "/var/log/nginx/access.log",
        "/var/log/nginx/error.log",
        "/var/log/mysql/error.log",
        "/var/log/postgresql/postgresql.log",
        "/var/log/audit/audit.log",
        "/var/log/samba/log.smbd",
        "/var/log/squid/access.log",
        "/var/log/squid/cache.log",
        "/var/log/ufw.log",
        "/var/log/auth.log",
        "/var/log/secure",
        "/var/log/boot.log",
        "/var/log/dmesg",
        "/var/log/kern.log",
        "/var/log/apt/history.log",
        "/var/log/yum.log",
        "/var/log/lastlog"
    ]

    found_logs = []
    for path in log_paths:
        if os.path.exists(path):
            found_logs.append(path)

    return found_logs

def run_quick_scan(scan_duration_minutes=1):
    time.sleep(2)
    maximize_settings_window()
    pyautogui.write('Virus & threat protection')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.hotkey('win','up')
    time.sleep(1)
    pyautogui.moveTo(529,879)
    pyautogui.doubleClick()
    time.sleep(2)

    scan_duration = scan_duration_minutes * 60
    time.sleep(scan_duration)

    screenshot = pyautogui.screenshot()
    screenshot.save('scan_result.png')
    print('Screenshot taken and saved as scan_result.png')
    
def capture_network_traffic():
    try:
        
        subprocess.run(
            ['tshark', '-c', str(packet_count), '-w', capture_file_path],
            check=True
        )
        print(f"Network traffic captured and saved to {capture_file_path}")
    except subprocess.CalledProcessError as e:
        print("Error capturing network traffic:", e)


def analyze_capture_file():
    
    capture = pyshark.FileCapture(capture_file_path)

    
    for packet in capture:
        
        if hasattr(packet, 'ip'):
            if int(packet.ip.hdr_len) != 20: 
                print(f"Malformed packet: {packet.ip} - IP header length: {packet.ip.hdr_len}")
                
def check_for_updates():
    try:
        update_session = win32com.client.Dispatch("Microsoft.Update.Session")
        update_searcher = update_session.CreateUpdateSearcher()
        search_result = update_searcher.Search("IsInstalled=0")
        if search_result.Updates.Count > 0:
            print("Available updates:")
            for update in search_result.Updates:
                print(update.Title)
            return True
        else:
            print("No updates available.")
            return False
    except Exception as e:
        print("Error:", e)
        return False

def install_updates():
    try:
        update_installer = win32com.client.Dispatch("Microsoft.Update.Installer")
        installation_result = update_installer.Install()
        if installation_result.ResultCode == 2:
            print("Updates installed successfully.")
        else:
            print("Failed to install updates.")
    except Exception as e:
        print("Error:", e)

def windows_update():
    print("Checking for available updates...")
    if check_for_updates():
        install = input("Do you want to install updates? (yes/no): ").lower()
        if install == 'yes':
            print("Installing updates...")
            install_updates()
        else:
            print("Updates not installed.")
    else:
        print("No updates available.")
        
def detect_abnormal_activity(bash_history_file, csv_output_file):
    """Detects abnormal activity in Bash shell history and saves the findings to a CSV file."""
    abnormal_patterns = [
        r"sudo .*",  
        r"rm .*",    
        r"chmod .*",  
        r"chown .*",  
        r"wget .*",   
        r"Cronpab .*",
        r"/etc/passwd .*", 
    ]
    
    abnormal_regex = re.compile('|'.join(abnormal_patterns), re.IGNORECASE)
    with open(bash_history_file, 'r') as history_file:
        with open(csv_output_file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Command", "Abnormal Behavior"])
            
            for line in history_file:
                line = line.strip()
                if abnormal_regex.search(line):
                    writer.writerow([line, "Potential abnormal behavior detected"])

    print(f"Abnormal activity has been saved to {csv_output_file}")

def ab_activity():
    """Main function to parse command-line arguments and detect abnormal activity."""
    parser = argparse.ArgumentParser(description="Detect abnormal activity in Bash shell history")
    parser.add_argument("output_file", type=str, help="Path to save the abnormal activity CSV file")
    
    args = parser.parse_args()
    home_directory = os.path.expanduser("~")
    peg_folder_path = os.path.join(home_directory, "peg 1.0")
    bash_history_file = os.path.join(peg_folder_path, "bash_history.txt")
    detect_abnormal_activity(bash_history_file, args.output_file)
    
def check_kernel_version():
    
    kernel_version = subprocess.check_output(['uname', '-r']).decode().strip()
    print("Kernel version:", kernel_version)

def check_package_version(package_name):
    try:
        
        package_info = subprocess.check_output(['dpkg', '-s', package_name]).decode()
        version_line = [line for line in package_info.split('\n') if line.startswith('Version:')]
        if version_line:
            version = version_line[0].split(': ')[1].strip()
            print(f"{package_name} version:", version)
        else:
            print(f"Unable to find version information for {package_name}")
    except subprocess.CalledProcessError:
        print(f"Error: Unable to check version for {package_name}")

def kernel_info():
    print("Checking system components versions...\n")
    
   
    print("Checking kernel version...")
    check_kernel_version()
    print()

    
    packages_to_check = ['bash', 'openssl', 'libc6', 'libssl-dev']  

   
    for package in packages_to_check:
        print(f"Checking {package} version...")
        check_package_version(package)
        print()
        
def save_bash_history():
    home_directory = os.path.expanduser("~")
    bash_history_path = os.path.join(home_directory, ".zsh_history")
    output_file_path = os.path.join(home_directory, "peg 1.0", "bash_history.txt")
    
    try:
        with open(bash_history_path, "r", encoding="ISO-8859-1") as history_file:
            bash_history = history_file.readlines()
        peg_folder_path = os.path.join(home_directory, "peg 1.0")
        os.makedirs(peg_folder_path, exist_ok=True)
        with open(output_file_path, "w", encoding="UTF-8") as output_file:
            output_file.writelines(bash_history)
        
        print(f"Bash shell history has been saved to {output_file_path}")
    
    except Exception as e:
        print(f"An error occurred while accessing Bash history: {e}")

def maximize_settings_window():
    pyautogui.press('win')
    time.sleep(3)
    pyautogui.write('Windows Security')
    time.sleep(2)
    pyautogui.press('enter')
    time.sleep(3)

    window = pyautogui.getWindowsWithTitle('Settings')[0]
    window.maximize()
        
def get_openssl_version():
    try:
        openssl_version_output = subprocess.check_output(['openssl', 'version']).decode().strip()
        openssl_version = openssl_version_output.split()[1]
        return openssl_version
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None

def check_heartbleed_vulnerability():
    vulnerable_versions = ["1.0.1", "1.0.1a", "1.0.1b", "1.0.1c", "1.0.1d", "1.0.1e", "1.0.1f", "1.0.1g"]
    
    openssl_version = get_openssl_version()
    
    if openssl_version in vulnerable_versions:
        print("System is vulnerable to Heartbleed")
        webbrowser.open("https://www.openssl.org/news/secadv/20140407.txt")
        cve = "CVE-2014-0160"
    else:
        print("Your OpenSSL version is not vulnerable:)")
        cve = None

    return cve
    
a,b,c = get_operating_system()
if(a == "Windows"):
    check_eternal_blue_vulnerability(b)
    time.sleep(3)
    print("do you want to know about the exploit?(y/n)")
    try:
        yes_or_no =input().lower()
        if(yes_or_no == "y"):
           webbrowser.open("https://www.cvedetails.com/cve/CVE-2017-0143/")   
        else:
            print(";)")
    except(TypeError):
        print("type y or n")
    
    print("Plzzz..... be patient while PEG 1.0 scans the files in your system :)")    
    directories_to_scan = ['C:\\Windows', 'C:\\Program Files', 'C:\\Users']
    time.sleep(4)
    scan_and_save_vulnerable_files(directories_to_scan)
    time.sleep(4)
    ask=input("do you wanna run quickScan?(y/n)").lower()
    if(ask == 'y'):
        run_quick_scan(scan_duration_minutes=2)
    else:
        print("seems like somebody is secured:)")
    time.sleep(10)
    windows_update()

if(a == "Linux"):
    setuid_files = find_setuid_files()
    
    if setuid_files:
        print("Files with setuid bit set:")
        for file_path in setuid_files:
            print(file_path)
        save_to_file(setuid_files, 'success.txt')
        print("Successful results saved to success.txt")
    else:
        print("No files with setuid bit set found.")
    time.sleep(5)    
    if(b == "5.6.0" or "5.6.1"):
        webbrowser.open("https://www.rapid7.com/blog/post/2024/04/01/etr-backdoored-xz-utils-cve-2024-3094/")
        CVE2="CVE-2024-3094"
        
    if(b <= "4.8.3"):
        print("system is vulnerable to Dirty Cow")
        webbrowser.open("https://www.redhat.com/en/blog/understanding-and-mitigating-dirty-cow-vulnerability")
        CVE3="CVE-2016-5195"
    
    check_heartbleed_vulnerability()    
    sudo_l_output = run_sudo_l()
    if sudo_l_output:
        print("Output of sudo -l command:")
        print(sudo_l_output)
    else:
        print("Error executing command with sudo.")
        
    tfa_check()
    time.sleep(4)
    file_path = find_log_files()
    analyze_logs(file_path)
    time.sleep(4)
    capture_file_path = 'network_capture.pcap'
    packet_count = 2000
    capture_network_traffic()
    analyze_capture_file()
    time.sleep(3)
    save_bash_history()
    ab_activity()
    time.sleep(3)
    kernel_info()
    time.sleep(3)
        
mem = memory()
if(mem <= 75):
    print("Quit application's to decrease the memory usage")

    
cpu=get_system_stats()
print(cpu)
