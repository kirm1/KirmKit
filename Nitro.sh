#!/bin/bash

# Set your configurations here
MAX_CONNECTIONS=512

# Initialize counters
valid_count=0
invalid_count=0

# Function to generate a random Nitro code
generate_nitro_code() {
    echo $(LC_ALL=C tr -dc 'a-zA-Z0-9' < /dev/urandom | head -c 16)
}

# Function to perform the nitro code checking
check_nitro_code() {
    local code="$1"
    local url="https://discord.com/api/v9/entitlements/gift-codes/$code?with_application=false&with_subscription_plan=true"

    # Perform HTTP request and capture response status
    local status=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$url")

    # Print the Nitro code and result with colored output
    if [ "$status" -eq 200 ]; then
        echo -e "$code: \e[32mValid!\e[0m"
        ((valid_count++))
    else
        echo -e "$code: \e[31mInvalid\e[0m"
        ((invalid_count++))
    fi

    # Display updated counts at the top
    echo -ne "\rValid: $valid_count  Invalid: $invalid_count"
}

# Display initial counts
echo -e "Valid: $valid_count  Invalid: $invalid_count"

# Main script
counter=0

while [ "$counter" -lt "$MAX_CONNECTIONS" ]; do
    nitro_code=$(generate_nitro_code)

    # Check the validity of the Nitro code
    check_nitro_code "$nitro_code"

    ((counter++))
done

# Display the final counts
echo -e "\nResults:"
echo "Valid Codes: $valid_count"
echo "Invalid Codes: $invalid_count"
