import os
import shutil
import subprocess
from pathlib import Path

import requests
from colorama import Fore, Style, init

init(autoreset=True)


BANNER = (
    f"{Fore.CYAN}\n"
    "K   K  III  RRRR   M   M  K   K  III  TTTTT\n"
    "K  K    I   R   R  MM MM  K  K    I     T\n"
    "KKK     I   RRRR   M M M  KKK     I     T\n"
    "K  K    I   R  R   M   M  K  K    I     T\n"
    f"K   K  III  R   RR M   M  K   K  III    T    {Fore.YELLOW}http://github.com/kirm1/KirmKit.git{Style.RESET_ALL}\n"
    f"{Fore.RED}copyright (c) 2024 KirmKit{Style.RESET_ALL}\n"
)

DISCLAIMER = (
    "Disclaimer\n\n"
    "Scripts are provided for educational purposes only.\n"
    "Use responsibly and comply with all laws."
)

DDOS_DIR = Path("DDoS-Ripper")
TOOLS_DIR = Path("Tools")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_banner():
    clear_screen()
    print(BANNER)


def command_exists(command: str) -> bool:
    return shutil.which(command) is not None

def run_in_dir(command: list[str], directory: Path) -> None:
    subprocess.run(command, cwd=directory)


def download_file(url: str, dest: Path) -> None:
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total = int(response.headers.get("content-length", 0))
    downloaded = 0
    bar_length = 50
    with open(dest, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
            downloaded += len(chunk)
            if total:
                percent = downloaded * 100 // total
                filled = int(bar_length * percent / 100)
                bar = "=" * filled + " " * (bar_length - filled)
                print(f"\rDownloading: [{bar}] {percent}%", end="", flush=True)
    print()


def install_nmap_windows() -> None:
    print(f"\n{Fore.YELLOW}nmap isn't installed. Installing now...{Style.RESET_ALL}")
    url = "https://nmap.org/dist/nmap-7.94-setup.exe"
    installer = Path("nmap_setup.exe")
    download_file(url, installer)
    print("Running installer...")
    subprocess.run([str(installer), "/S"], check=False)
    installer.unlink(missing_ok=True)


def run_nmap() -> None:
    ip = input("Enter the target IP address: ")
    args = [
        'nmap', ip, '--min-hostgroup', '96', '-sS', '-n', '-sU', '-T4', '-A', '-v',
        '-PE', '-PP', '-PS80,443', '-PA3389', '-PU40125', '-PY', '-g', '53'
    ]
    subprocess.run(args)


def run_ddos() -> None:
    ip = input("Enter the target IP address: ")
    port = input("Enter the target port: ")
    run_in_dir(['python3', 'DRipper.py', '-s', ip, '-p', port, '-t', '443'], DDOS_DIR)


def run_nitrogen() -> None:
    run_in_dir(['python3', 'Nitro.py'], TOOLS_DIR)

# Function to center text to the left with red box background for disclaimer
def center_disclaimer(text: str, width: int = 80) -> str:
    red_box = f"{Fore.RED}{'#' * (width - 2)}{Style.RESET_ALL}"
    lines = text.strip().split('\n')
    centered_lines = [red_box, *lines, red_box]
    return '\n'.join(centered_lines)

def main() -> None:
    display_banner()
    print(f"{center_disclaimer(DISCLAIMER)}\n")

    if not command_exists('nmap'):
        if os.name == 'nt':
            install_nmap_windows()
        else:
            print(f"\n{Fore.RED}[Error]{Style.RESET_ALL} nmap is not available. Please install it.")
            return

    if not command_exists('nmap'):
        print(f"\n{Fore.RED}[Error]{Style.RESET_ALL} Automatic nmap installation failed.")
        return

    if not DDOS_DIR.exists():
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} {DDOS_DIR} directory not found.")
        return

    options = {
        '1': ('nmap', run_nmap),
        '2': ('DDoS-Ripper', run_ddos),
        '3': ('NitroGenerator', run_nitrogen),
    }

    print("\nChoose a tool to run:")
    for key, (name, _) in options.items():
        print(f"{Fore.GREEN}[{key}]{Style.RESET_ALL} {name}")

    action = options.get(input("Enter your choice (1-3): "))
    if action:
        action[1]()
    else:
        print(f"\n{Fore.RED}[Error]{Style.RESET_ALL} Invalid choice.")


if __name__ == '__main__':
    main()
