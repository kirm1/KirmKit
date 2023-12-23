#!/bin/bash

# ANSI color codes
green='\033[0;32m'
red='\033[0;31m'
reset='\033[0m'

# Function to display the KIRMKIT banner
clear
echo -e "${green}
K   K  III  RRRR   M   M  K   K  III  TTTTT
K  K    I   R   R  MM MM  K  K    I     T
KKK     I   RRRR   M M M  KKK     I     T
K  K    I   R  R   M   M  K  K    I     T
K   K  III  R   RR M   M  K   K  III    T    http://github.com/kirm1/KirmKit.git
================================================================================================================================${reset}"

# Function to install KIRMKITS TOOLS
install_kirm_and_dependencies() {
    local main_package="nmap"
    local dependencies=("python3")

    echo -e "\nInstalling ${red}[${green}KirmKit${reset}${red}]${reset} Tools..."

    sudo apt-get install -y "$main_package" "${dependencies[@]}" > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        echo -e "${red}[${green}KirmKit${reset}${red}]${reset} Installation Successful!${reset}"
    else
        echo -e "[${red}ERROR${reset}] KIRMKIT Tools installation failed."
        exit 1
    fi
}

# Function to clone GitHub repositories
clone_github_repositories() {
    local repos=("https://github.com/palahsu/DDoS-Ripper.git")

    for repo in "${repos[@]}"; do
        git clone "$repo" > /dev/null 2>&1

        if [ $? -ne 0 ]; then
            echo -e "[${red}ERROR${reset}] Failed to clone the repository."
            exit 1
        fi
    done
}

# Display the installation menu with color
echo -e "\n${green}Choose an option:${reset}"
echo -e "${red}[${green}1${reset}${red}]${reset} Install KIRMKIT"
echo -e "${green}[${red}2${reset}${green}]${reset} Exit"

# Prompt the user for input
read -e -p "Enter your choice (1 or 2): " choice

# Case statement to handle user choice
case $choice in
    1)
        install_kirm_and_dependencies
        clone_github_repositories
        ;;
    2)
        echo -e "\nExiting script."
        exit 0
        ;;
    *)
        echo -e "\nInvalid choice. Please enter 1 or 2."
        ;;
esac
