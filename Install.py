import subprocess
import urllib.request
import os
import shutil
import itertools
import time
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Download a file with a simple progress bar
def download_with_progress(url: str, dest: str) -> None:
    response = urllib.request.urlopen(url)
    total = int(response.getheader('content-length', 0))
    downloaded = 0
    chunk = 8192
    with open(dest, 'wb') as out_file:
        while True:
            data = response.read(chunk)
            if not data:
                break
            out_file.write(data)
            downloaded += len(data)
            if total:
                percent = downloaded * 100 // total
                bar_len = 50
                filled = int(bar_len * percent / 100)
                bar = '=' * filled + ' ' * (bar_len - filled)
                print(f"\rDownloading: [{bar}] {percent}%", end='', flush=True)
    print()


# Function to display the KIRMKIT banner
def display_banner():
    print(f"{Fore.GREEN}K   K  III  RRRR   M   M  K   K  III  TTTTT\nK  K    I   R   R  MM MM  K  K    I     T\nKKK     I   RRRR   M M M  KKK     I     T\nK  K    I   R  R   M   M  K  K    I     T\nK   K  III  R   RR M   M  K   K  III    T    http://github.com/kirm1/KirmKit.git\n================================================================================================================================{Style.RESET_ALL}")

# Function to check if Nmap is installed
def check_nmap_installation():
    try:
        # Choose the appropriate command based on the platform
        if os.name == 'nt':  # Windows
            subprocess.run(['nmap', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        elif os.name == 'posix':  # Linux
            subprocess.run(['nmap', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

# Check if Chocolatey (choco) is installed on Windows
def check_choco_installation() -> bool:
    return shutil.which('choco') is not None

# Install Chocolatey package manager on Windows
def install_choco() -> None:
    print("\nChocolatey not found. Installing Chocolatey...")
    cmd = [
        'powershell',
        '-NoProfile',
        '-ExecutionPolicy', 'Bypass',
        '-Command', (
            "Set-ExecutionPolicy Bypass -Scope Process -Force;"
            "[System.Net.ServicePointManager]::SecurityProtocol ="
            " [System.Net.ServicePointManager]::SecurityProtocol -bor 3072;"
            " iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
        )
    ]
    subprocess.run(cmd, check=True)

# Run a command and display a simple progress bar while it executes
def run_with_progress(cmd: list[str]) -> int:
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    while process.poll() is None:
        print(f"\rInstalling: {next(spinner)}", end='', flush=True)
        time.sleep(0.1)
    print('\r', end='', flush=True)
    output = process.stdout.read() if process.stdout else ''
    if output:
        print(output)
    return process.returncode

# Function to download and run the Nmap installer with elevated privileges
def install_nmap():
    print(f"\nInstalling {Fore.RED}[{Fore.GREEN}nmap{Style.RESET_ALL}{Fore.RED}]{Style.RESET_ALL}...")

    if os.name == 'nt':
        if not check_choco_installation():
            install_choco()
        result = run_with_progress(['choco', 'install', 'nmap', '-y'])
        if result == 0:
            print(f"{Fore.RED}[{Fore.GREEN}KirmKit{Style.RESET_ALL}{Fore.RED}]{Style.RESET_ALL} Installation Successful!")
        else:
            print(f"[{Fore.RED}ERROR{Style.RESET_ALL}] KirmKit installation failed.")
            exit(1)
    else:
        result = run_with_progress(['sudo', 'apt-get', '-y', 'install', 'nmap'])
        if result == 0:
            print(f"{Fore.RED}[{Fore.GREEN}KirmKit{Style.RESET_ALL}{Fore.RED}]{Style.RESET_ALL} Installation Successful!")
        else:
            print(f"[{Fore.RED}ERROR{Style.RESET_ALL}] KirmKit installation failed.")
            exit(1)

# Function to clone GitHub repositories
def clone_github_repositories():
    repos = ["https://github.com/palahsu/DDoS-Ripper.git"]

    for repo in repos:
        repo_name = repo.split("/")[-1].split(".")[0]

        if os.path.exists(repo_name):
            replace_existing = input(f"\nFound Existing Directory '{repo_name}'. Would you like to replace it with a newer version? [Y/n]: ")
            if replace_existing.lower() != 'y':
                print(f"[{Fore.RED}ERROR{Style.RESET_ALL}] KirmKit installation has failed.")
                exit(1)
            else:
                print(f"Replacing existing '{repo_name}'...")

                # Remove existing directory in a cross-platform manner
                shutil.rmtree(repo_name, ignore_errors=True)

        print(f"\nInstalling dependencies...")

        # Run the git clone command with progress
        cmd = ['git', 'clone', repo]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, universal_newlines=True)

        # Display progress bar
        progress = 0
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if 'Receiving objects' in output:
                progress = int(output.split()[3][:-1])
                print(f"\rProgress: {'=' * progress}{'>'}{' ' * (100 - progress)}", end='', flush=True)

        if process.returncode != 0:
            print(f'\n[{Fore.RED}ERROR{Style.RESET_ALL}] Failed to install dependencies.')
            exit(1)

    print(f"\n[{Fore.GREEN}KirmKit{Style.RESET_ALL}] Installation has finished!")

# Display the installation menu with color
print("\n" + Fore.GREEN + "Choose an option:" + Style.RESET_ALL)
print(f"{Fore.RED}[{Fore.GREEN}1{Style.RESET_ALL}{Fore.RED}]{Style.RESET_ALL} Install KIRMKIT")
print(f"{Fore.GREEN}[{Fore.RED}2{Style.RESET_ALL}{Fore.GREEN}]{Style.RESET_ALL} Exit")

# Prompt the user for input
choice = input("Enter your choice (1 or 2): ")

# Case statement to handle user choice
if choice == '1':
    if check_nmap_installation():
        print(f"[{Fore.RED}nmap{Style.RESET_ALL}] Is Already Installed.")
    else:
        install_nmap()

    # Clone GitHub repositories regardless of Nmap installation status
    clone_github_repositories()

elif choice == '2':
    print("\nExiting script.")
    exit(0)
else:
    print("\nInvalid choice. Please enter 1 or 2.")

input('\nPress enter to exit...')
