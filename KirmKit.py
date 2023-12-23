import subprocess
import os

# ANSI color codes
red = '\033[0;31m'
green = '\033[1;32m'  # Bright Green
cyan = '\033[1;36m'  # Bright Cyan
yellow = '\033[1;33m'  # Bright Yellow
reset = '\033[0m'  # Reset to default color

# Function to display the KIRMKIT banner
def display_banner():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
    banner_text = (
        f'{cyan}\n'
        'K   K  III  RRRR   M   M  K   K  III  TTTTT\n'
        'K  K    I   R   R  MM MM  K  K    I     T\n'
        'KKK     I   RRRR   M M M  KKK     I     T\n'
        'K  K    I   R  R   M   M  K  K    I     T\n'
        f'K   K  III  R   RR M   M  K   K  III    T    {yellow}http://github.com/kirm1/KirmKit.git{reset}\n'
        f'{red}copyright (c) 2023 KirmKit{reset}\n'
    )
    print(banner_text)

# Function to check if a command is available
def check_command(command_name):
    try:
        result = subprocess.run([command_name, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

# Function to run NitroGenerator
def run_nitrogen():
    os.chdir('Tools')  # Change to the 'Tools' directory if Nitro.py is located there
    try:
        while True:
            process = subprocess.Popen(['python', '-u', 'Nitro.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
            process.communicate()  # Ensure the process finishes and capture remaining output

            if process.returncode != 0:
                print(f"\n{red}[Error]{reset} NitroGenerator process returned non-zero exit code: {process.returncode}")

    except KeyboardInterrupt:
        print(f"\n{red}[Error]{reset} User interrupted. Exiting NitroGenerator.")
    except subprocess.CalledProcessError as e:
        print(f"\n{red}[Error]{reset} Error running NitroGenerator: {e}")
    os.chdir('..')  # Change back to the original directory

# Main script
display_banner()

# Check for required commands
if not check_command('nmap'):
    print(f"\n{red}[Error]{reset} nmap is not available. Please install it.")
    exit(1)

# Display the menu
print("\nChoose a tool to run:")
print(f"{green}[{red}1{reset}{green}]{green} nmap{reset}")
print(f"{green}[{red}2{reset}{green}]{green} DDoS-Ripper{reset}")
print(f"{green}[{red}3{reset}{green}]{green} NitroGenerator{reset}")

# Read user input
choice = input("Enter your choice (1-3): ")

# Case statement to handle user choice
if choice == '1':
    # Run nmap command
    ip = input("Enter The target IP address: ")
    subprocess.run(['nmap', ip, '--min-hostgroup', '96', '-sS', '-n', '-sU', '-T4', '-A', '-v', '-PE', '-PP', '-PS80,443', '-PA3389', '-PU40125', '-PY', '-g', '53'])
elif choice == '2':
    # Run DDoS-Ripper command
    target_ip = input("Enter The target IP address: ")
    target_port = input("Enter The target port: ")
    os.chdir('DDoS-Ripper')
    subprocess.run(['python', 'Dripper.py', '-s', target_ip, '-p', target_port, '-t', '443'])
    os.chdir('..')  # Change back to the original directory
elif choice == '3':
    # Run NitroGenerator command
    run_nitrogen()
else:
    print(f"\n{red}[Error]{reset} Invalid choice. Please enter a number between 1 and 3.")
