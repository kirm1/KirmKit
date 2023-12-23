#!/bin/bash

# ANSI color codes
green='\033[0;32m'
red='\033[0;31m'
reset='\033[0m'

# Function to display the KIRM banner
display_banner() {
    clear
    echo -e "${green}"
    cat << "EOF"
                                 K   K  III  RRRR   M   M  K   K  III  TTTTT
                                 K  K    I   R   R  MM MM  K  K    I     T
                                 KKK     I   RRRR   M M M  KKK     I     T
                                 K  K    I   R  R   M   M  K  K    I     T
                                 K   K  III  R   RR M   M  K   K  III    T    http://github.com/kirm1/KirmKit.git
================================================================================================================================
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
    DDoS-Ripper -s "$ip_address" -p "$port" -t 443
}

# Function to run Th3Inspector
run_th3inspector() {
    echo -e "${green}Running Th3Inspector...${reset}"
    # Replace the following line with the actual Th3Inspector command
    Th3Inspector
}

# Function to run Nitro Generator
run_nitro_generator() {
    echo -e "${green}Running Nitro Generator...${reset}"
    # Replace the following line with the actual Nitro Generator command
    /Tools/./Nitro.sh
}

# Main script
display_banner

# Display the menu
echo -e "\nChoose a tool to run:"
echo -e "[${green}1${reset}] nmap"
echo -e "[${green}2${reset}] DDoS-Ripper"
echo -e "[${green}3${reset}] Th3Inspector"
echo -e "[${green}4${reset}] Nitro Generator"

# Read user input
read -p "Enter your choice (1-4): " choice

# Check for required commands
check_command "nmap"

case $choice in
    1)
        run_nmap
        ;;
    2)
        check_command "DDoS-Ripper"
        run_ddos_ripper
        ;;
    3)
        run_th3inspector
        ;;
    4)
        run_nitro_generator
        ;;
    *)
        echo -e "[${red}Error${reset}] Invalid choice. Please enter a number between 1 and 4."
        ;;
esac

echo -e "\nScript execution completed."
