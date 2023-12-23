#!/usr/bin/env python -u

import subprocess
import signal
import os
import random
import string

# ANSI color codes
green = '\033[0;32m'
red = '\033[0;31m'
reset = '\033[0m'

# Configuration
MAX_CONNECTIONS = 512
VALID_CODES_FILE = "valid-codes.txt"

# Function to display the KIRMKIT banner
def display_banner():
    clear_screen()

    print(f'{green}\n'
          'K   K  III  RRRR   M   M  K   K  III  TTTTT\n'
          'K  K    I   R   R  MM MM  K  K    I     T\n'
          'KKK     I   RRRR   M M M  KKK     I     T\n'
          'K  K    I   R  R   M   M  K  K    I     T\n'
          'K   K  III  R   RR M   M  K   K  III    T    http://github.com/kirm1/KirmKit.git\n'
          '================================================================================================================================{reset}')

# Function to check if a command is available
def check_command(command_name):
    try:
        if os.name == 'nt':
            subprocess.run([command_name, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=True)
        else:
            subprocess.run([command_name, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Function to generate a random Nitro code
def generate_nitro_code():
    characters = string.ascii_letters + string.digits
    nitro_code = ''.join(random.choice(characters) for i in range(16))
    return nitro_code

# Function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to perform the Nitro code checking
def check_nitro_code(code):
    url = f'https://discord.com/api/v10/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true'

    # Perform HTTP request and capture response status
    status = subprocess.run(f'curl -s -o /dev/null -w "%{{http_code}}" -X GET "{url}"', shell=True, capture_output=True, text=True).stdout.strip()

    # Print the result with colored output
    if int(status) == 200:
        with open(VALID_CODES_FILE, 'a') as file:
            file.write(f'{code}\n')  # Append the valid code to the file
        print(f'{code}: {green}Valid!{reset}')
    else:
        print(f'{code}: {red}Invalid{reset}')

# Function to handle cleanup on Ctrl+C
def cleanup_on_interrupt(signal, frame):
    print(f'\n{red}Script interrupted.{reset} Cleaning up...')
    print(f'Valid Nitro codes saved to: {VALID_CODES_FILE}')
    exit(1)

# Function to run Nitro code generation and checking
def run_nitro_code_checks():
    counter = 0

    # Display initial message
    print(f'\nChecking Nitro codes...')

    # Set signal to catch Ctrl+C and execute cleanup function
    signal.signal(signal.SIGINT, cleanup_on_interrupt)

    # Main loop to generate and check Nitro codes
    while counter < MAX_CONNECTIONS:
        nitro_code = generate_nitro_code()

        # Check the validity of the Nitro code
        check_nitro_code(nitro_code)

        counter += 1

    # Remove the signal after completing the loop
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Display the final message
    print(f'\n{green}Script execution completed.{reset}')
    print(f'Valid Nitro codes saved to: {VALID_CODES_FILE}')

# Main script
display_banner()

# Check for required commands
if not check_command('curl'):
    print(f'[{red}Error{reset}] curl is not available. Please install it.')
    exit(1)

# Run Nitro code generation and checking
run_nitro_code_checks()
