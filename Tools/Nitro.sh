#!/bin/bash

# ANSI color codes
green='\033[0;32m'
red='\033[0;31m'
reset='\033[0m'

# Configuration
MAX_CONNECTIONS=512
VALID_CODES_FILE="valid-codes.txt"

# Function to display the KIRMKIT banner
display_banner() {
    clear
    echo -e "${green}
K   K  III  RRRR   M   M  K   K  III  TTTTT
K  K    I   R   R  MM MM  K  K    I     T
KKK     I   RRRR   M M M  KKK     I     T
K  K    I   R  R   M   M  K  K    I     T
K   K  III  R   RR M   M  K   K  III    T    http://github.com/kirm1/KirmKit.git
================================================================================================================================${reset}"
}

# Function to check if a command is available
check_command() {
    local command_name="$1"

    if ! command -v "$command_name" &> /dev/null; then
        echo -e "[${red}Error${reset}] $command_name is not available. Please install it."
        exit 1
    fi
}

# Function to generate a random Nitro code
generate_nitro_code() {
    echo $(LC_ALL=C tr -dc 'a-zA-Z0-9' < /dev/urandom | head -c 16)
}

# Function to perform the Nitro code checking
check_nitro_code() {
    local code="$1"
    local url="https://discord.com/api/v10/entitlements/gift-codes/$code?with_application=false&with_subscription_plan=true"

    # Perform HTTP request and capture response status
    local status=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$url")

    # Print the Nitro code and result with colored output
    if [ "$status" -eq 200 ]; then
        echo "$code" >> "$VALID_CODES_FILE"  # Append the valid code to the file
        echo -e "$code: ${green}Valid!${reset}"
    else
        echo -e "$code: ${red}Invalid${reset}"
    fi
}

# Function to handle cleanup on Ctrl+C
cleanup_on_interrupt() {
    echo -e "\n${red}Script interrupted.${reset} Cleaning up..."
    echo "Valid Nitro codes saved to: $VALID_CODES_FILE"
    exit 1
}

# Function to run Nitro code generation and checking
run_nitro_code_checks() {
    local counter=0
    local valid_count=0

    # Display initial message
    echo -e "\nChecking Nitro codes..."

    # Set trap to catch Ctrl+C and execute cleanup function
    trap cleanup_on_interrupt INT

    # Main loop to generate and check Nitro codes
    while [ "$counter" -lt "$MAX_CONNECTIONS" ]; do
        nitro_code=$(generate_nitro_code)

        # Check the validity of the Nitro code
        check_nitro_code "$nitro_code"

        ((counter++))
    done

    # Remove the trap after completing the loop
    trap - INT

    # Display the final message
    echo -e "\n${green}Script execution completed.${reset}"
    echo "Valid Nitro codes saved to: $VALID_CODES_FILE"
}

# Main script
display_banner

# Check for required commands
check_command "curl"

# Run Nitro code generation and checking
run_nitro_code_checks
