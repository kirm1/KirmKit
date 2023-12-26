import subprocess
import string
import aiohttp
import secrets
import os
import asyncio
import signal

# ANSI color codes
green = '\033[0;32m'
red = '\033[0;31m'
reset = '\033[0m'

# Configuration
VALID_CODES_FILE = "valid-codes.txt"
DELAY_BETWEEN_REQUESTS = 0.1  # Adjust the delay (in seconds) between each request

# Function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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
        subprocess.run([command_name, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Function to generate a random Nitro code using secrets module
def generate_nitro_code():
    characters = string.ascii_letters + string.digits
    nitro_code = ''.join(secrets.choice(characters) for i in range(16))
    return nitro_code

# Function to perform the Nitro code checking
async def check_nitro_code(session, code):
    url = f'https://discord.com/api/v10/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true'

    try:
        async with session.get(url) as response:
            status = response.status
            if status == 200:
                with open(VALID_CODES_FILE, 'a') as file:
                    file.write(f'{code}\n')
                print(f'{code}: {green}Valid!{reset}')
            else:
                print(f'{code}: {red}Invalid{reset}')
    except Exception as e:
        print(f'{code}: {red}Error - {e}{reset}')

# Function to handle cleanup on Ctrl+C
def cleanup_on_interrupt(sig, frame):
    print(f'\n{red}Script interrupted.{reset} Cleaning up...')
    print(f'Valid Nitro codes saved to: {VALID_CODES_FILE}')
    exit(1)

# Function to run Nitro code generation and checking
async def run_nitro_code_checks():
    # Display initial message
    print(f'\nChecking Nitro codes...')

    # Set signal to catch Ctrl+C and execute cleanup function
    signal.signal(signal.SIGINT, cleanup_on_interrupt)

    # Create an aiohttp session
    async with aiohttp.ClientSession() as session:
        try:
            while True:
                nitro_code = generate_nitro_code()

                # Check the validity of the Nitro code
                await check_nitro_code(session, nitro_code)

                # Introduce a delay between requests
                await asyncio.sleep(DELAY_BETWEEN_REQUESTS)

        except asyncio.CancelledError:
            pass

# Main script
display_banner()

# Check for required commands
if not check_command('curl'):
    print(f'[{red}Error{reset}] curl is not available. Please install it.')
    exit(1)

# Run Nitro code generation and checking
try:
    asyncio.run(run_nitro_code_checks())
except KeyboardInterrupt:
    print(f'\n{red}Script manually interrupted.{reset} Cleaning up...')
    print(f'Valid Nitro codes saved to: {VALID_CODES_FILE}')
    exit(1)

# Wait for user input before exiting
input('Press enter to exit...')
