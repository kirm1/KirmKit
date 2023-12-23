#!/bin/bash

# ANSI color codes
green='\033[0;32m'
red='\033[0;31m'
reset='\033[0m'

# Function to display the KIRMKIT banner
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

# Function to install KIRMKITS TOOLS
install_kirm_and_dependencies() {
    local main_package="nmap"
    local dependencies=("perl" "python3")

    # Display the list of dependencies and their installation status
    echo -e "\nInstalling [${green}$main_package${reset}] and its dependencies: ${dependencies[@]}"

    # Install KIRM and its dependencies
    sudo apt-get install -y "$main_package" "${dependencies[@]}" > /dev/null 2>&1

    # Check if the installation was successful
    if [ $? -eq 0 ]; then
        echo -e "\n[${green}$main_package${reset}] installation successful."
    else
        echo -e "\n[${red}$main_package${reset}] installation failed."
        exit 1
    fi
}

# Function to clone GitHub repositories
clone_github_repositories() {
    local repos=("https://github.com/palahsu/DDoS-Ripper.git" "https://github.com/Moham3dRiahi/Th3inspector.git")

    # Clone each repository
    for repo in "${repos[@]}"; do
        repo_name=$(basename "$repo" .git)
        echo -e "\nCloning GitHub repository: ${green}$repo_name${reset}"
        git clone "$repo" > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo -e "[${green}$repo_name${reset}] Clone successful."

            # Check if the cloned repository is Th3Inspector
            if [ "$repo_name" = "Th3inspector" ]; then
                # Navigate into the Th3Inspector directory
                cd "$repo_name" || exit 1

                # Run setup script (replace with the actual setup command)
                echo -e "\nRunning Th3Inspector setup script..."
                ./install.sh

                # Navigate back to the script's original directory
                cd - || exit 1
            fi
        else
            echo -e "[${red}$repo_name${reset}] Clone failed."
            exit 1
        fi
    done
}

# Display the installation menu with color
echo -e "\n${green}Choose an option:${reset}"
echo -e "[${green}1${reset}] Install KIRMKIT"
echo -e "[${red}2${reset}] Exit"

# Move cursor to the next line and prompt the user
echo -en "Enter your choice (1 or 2): "
read -e choice

case $choice in
    1)
        # Install KIRM and its dependencies
        install_kirm_and_dependencies

        # Clone GitHub repositories
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
