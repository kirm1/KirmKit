#!/bin/bash

# ANSI color codes
cyan='\033[1;36m'
yellow='\033[1;33m'
green='\033[0;32m'
red='\033[0;31m'
reset='\033[0m'

# Function to display the KIRM banner
display_banner() {
    clear
    echo -e "${cyan}"
    cat << "EOF"
                                 K   K  III  RRRR   M   M  K   K  III  TTTTT
                                 K  K    I   R   R  MM MM  K  K    I     T
                                 KKK     I   RRRR   M M M  KKK     I     T
                                 K  K    I   R  R   M   M  K  K    I     T
                                 K   K  III  R   RR M   M  K   K  III    T    ${yellow}http://github.com/kirm1/KirmKit.git${reset}
EOF
    echo -e "${reset}"
}

# Function to check if a command is available
check_command() {
    local command_name="$1"

    if ! command -v "$command_name" &> /dev/null; then
        echo -e "[${red}Error${reset}] $command_name is not available. Please install it."
        exit 1
    fi
}

# Function to run nmap
run_nmap() {
    read -p "Enter the target IP address for nmap: " ip_address
    echo -e "\nRunning nmap with IP address: $ip_address"
    # Replace the following line with the actual nmap command
    nmap "$ip_address" --min-hostgroup 96 -sS -n -sU -T4 -A -v -PE -PP -PS80,443 -PA3389 -PU40125 -PY -g 53
}

# Function to run DDoS-Ripper
run_ddos_ripper() {
    read -p "Enter IP Address: " ip_address
    read -p "Enter Port: " port
    echo -e "\nRunning DDoS-Ripper with IP address: $ip_address"
    # Replace the following line with the actual DDoS-Ripper command
    cd DDoS-Ripper && chmod +x DRipper.py
    ./DDoS-Ripper -s "$ip_address" -p "$port" -t 443
}

# Function to run NitroGenerator
run_nitrogen() {
    cd Tools
    chmod u+x *.sh
    echo -e "\nRunning NitroGenerator" 
  ./Nitro.sh
}

# Main script
display_banner

# Display the menu
echo -e "\nChoose a tool to run:"
echo -e "${red}[${green}1${reset}${red}]${reset} ${yellow} nmap"
echo -e "${red}[${green}2${reset}${red}]${reset} ${yellow} DDoS-Ripper"
echo -e "${red}[${green}3${reset}${red}]${reset} ${yellow} NitroGenerator"

# Read user input
read -p "Enter your choice (1-3): " choice

# Check for required commands
check_command "nmap"

case $choice in
    1)
        run_nmap
        ;;
    2)
        run_ddos_ripper
        ;;
    3)
        run_nitrogen
        ;;
        
    *)
        echo -e "[${red}Error${reset}] Invalid choice. Please enter a number between 1 and 3."
        ;;
esac

echo -e "\nScript execution completed."
