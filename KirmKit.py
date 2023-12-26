import subprocess
import os
import shutil  # Import the shutil module

# ANSI color codes
red = '\033[0;31m'
green = '\033[1;32m'  # Bright Green
cyan = '\033[1;36m'  # Bright Cyan
yellow = '\033[1;33m'  # Bright Yellow
reset = '\033[0m'  # Reset to the default color

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
    return shutil.which(command_name) is not None  # Use shutil.which to check command availability

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

# Function to center text to the left with red box background for disclaimer
def center_disclaimer(text, width=80):
    red_box = f"{red}{'#' * (width - 2)}{reset}"
    lines = text.split('\n')
    centered_lines = [f'{red_box}']
    centered_lines.extend(lines)
    centered_lines.append(red_box)
    return '\n'.join(centered_lines)

# Main script
display_banner()

# Display the disclaimer with red box background
disclaimer = (
    'Disclaimer\n\n'
    'All scripts provided are meant for educational and informational purposes only. '
    'The author does not condone or encourage any unauthorized or malicious activities. '
    'Users are expected to use these scripts responsibly and in compliance with all applicable laws and regulations.\n'
    'The author is not responsible for any misuse, damage, or consequences resulting from the use of these scripts. '
    'The scripts are provided as-is, without any warranty or guarantee of their accuracy, reliability, or suitability for any purpose.\n'
    'Use these scripts at your own risk. It is recommended to review and understand the code before running any script, '
    'and to ensure that their use aligns with ethical and legal standards.\n'
    'The author reserves the right to modify, update, or discontinue these scripts at any time. '
    'Any reliance you place on these scripts is strictly at your own discretion.\n'
    'By using these scripts, you acknowledge and agree to the terms outlined in this disclaimer.'
)

centered_disclaimer = center_disclaimer(disclaimer)

print(f'{centered_disclaimer}\n')

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

# Wait for user input before exiting
input('Press enter to exit...')
