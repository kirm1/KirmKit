import subprocess
import urllib.request
import os
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Function to display the KIRMKIT banner
def display_banner():
    print(f"{Fore.GREEN}K   K  III  RRRR   M   M  K   K  III  TTTTT\nK  K    I   R   R  MM MM  K  K    I     T\nKKK     I   RRRR   M M M  KKK     I     T\nK  K    I   R  R   M   M  K  K    I     T\nK   K  III  R   RR M   M  K   K  III    T    http://github.com/kirm1/KirmKit.git\n================================================================================================================================{Style.RESET_ALL}")

# Function to download and run the nmap installer with elevated privileges
def install_nmap():
    print(f"\nDownloading and installing {Fore.RED}[{Fore.GREEN}nmap{Style.RESET_ALL}{Fore.RED}]{Style.RESET_ALL}...")

    # Download the nmap installer
    nmap_installer_url = "https://nmap.org/dist/nmap-7.94-setup.exe"
    installer_path = "nmap_setup.exe"
    urllib.request.urlretrieve(nmap_installer_url, installer_path)

    # Run the installer with elevated privileges
    result = subprocess.run(['powershell', '-Command', f'Start-Process -Wait -FilePath "{installer_path}" -Verb RunAs'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode == 0:
        print(f"{Fore.RED}[{Fore.GREEN}KirmKit{Style.RESET_ALL}{Fore.RED}]{Style.RESET_ALL} Installation Successful!")
    else:
        print(f"[{Fore.RED}ERROR{Style.RESET_ALL}] KirmKit installation failed.")
        print(result.stderr.decode())
        exit(1)

# Function to clone GitHub repositories
def clone_github_repositories():
    repos = ["https://github.com/palahsu/DDoS-Ripper.git"]

    for repo in repos:
        result = subprocess.run(['git', 'clone', repo], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            print(f'[{Fore.RED}ERROR{Style.RESET_ALL}] Failed to clone the repository.')
            print(result.stderr.decode())
            exit(1)

# Display the installation menu with color
print("\n" + Fore.GREEN + "Choose an option:" + Style.RESET_ALL)
print(f"{Fore.RED}[{Fore.GREEN}1{Style.RESET_ALL}{Fore.RED}]{Style.RESET_ALL} Install KIRMKIT")
print(f"{Fore.GREEN}[{Fore.RED}2{Style.RESET_ALL}{Fore.GREEN}]{Style.RESET_ALL} Exit")

# Prompt the user for input
choice = input("Enter your choice (1 or 2): ")

# Case statement to handle user choice
if choice == '1':
    install_nmap()
    clone_github_repositories()
elif choice == '2':
    print("\nExiting script.")
    exit(0)
else:
    print("\nInvalid choice. Please enter 1 or 2.")

input('Press enter to exit...')
