#!/bin/bash

# Set your configurations here
WEBHOOK_URLS=("https://discord.com/api/webhooks/1187719161711964161/KH-lFRrBonikKkBF1BZlpV2uUx5f5ppQXIlmHju7YgYUmezz5OtRfWSJ0jYoj_4vF-Lf" "https://discord.com/api/webhooks/1187844583493730394/VTlOUN0y-sBXNyYEO9jyfcJWJRNayXW73cjfrSazAzAUCcksMDg10xSdwlGUX6oGNZR8")
MAX_CONNECTIONS=512
TIMEOUT=10
FILE_NAME="nitro_codes.txt"

# Function to generate a random Nitro code
generate_nitro_code() {
    echo $(LC_ALL=C tr -dc 'a-zA-Z0-9' < /dev/urandom | head -c 16)
}

# Function to create JSON payload for the embed
create_embed_payload() {
    local code="$1"
    local status="$2"
    local webhook_url="$3"

    local color
    local status_text
    local gift_url

    case "$status" in
        "valid")
            color="65280"  # Green
            status_text="Valid"
            gift_url="https://discord.gift/$code"
            ;;
        "invalid")
            color="16711680"  # Red
            status_text="Invalid"
            ;;
    esac

    # Use jq for creating a JSON payload
    jq -n \
        --arg status_text "$status_text" \
        --arg code "$code" \
        --arg gift_url "$gift_url" \
        --argjson color $color \
        '{"content": "", "embeds": [{"title": "Nitro Code Check", "description": $status_text, "color": $color, "fields": [{"name": "Nitro Code", "value": $code}, {"name": "Gift URL", "value": $gift_url}]}]}' | \
    curl -H "Content-Type: application/json" -X POST -d @- "$webhook_url"
}

# Function to perform the nitro code checking
check_nitro_code() {
    local code="$1"
    local webhook_url="$2"
    local url="https://discord.com/api/v9/entitlements/gift-codes/$code?with_application=false&with_subscription_plan=true"

    # Perform HTTP request and capture response status
    local status=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$url")

    # Debugging: Print the Nitro code and HTTP status to console
    echo "Code: $code | Status: $status"

    # Check if the status is 200 (Valid Nitro code)
    if [ "$status" -eq 200 ]; then
        create_embed_payload "$code" "valid" "$webhook_url"
    else
        create_embed_payload "$code" "invalid" "$webhook_url"
    fi
}

# Main script
counter=0

while [ "$counter" -lt "$MAX_CONNECTIONS" ]; do
    nitro_code=$(generate_nitro_code)

    # Debugging: Print the Nitro code to console
    echo "Generated Nitro Code: $nitro_code"

    # Distribute requests among webhooks
    if [ "$((counter % 2))" -eq 0 ]; then
        check_nitro_code "$nitro_code" "${WEBHOOK_URLS[0]}" &
    else
        check_nitro_code "$nitro_code" "${WEBHOOK_URLS[1]}" &
    fi

    ((counter++))
done

# Wait for all background jobs to finish
wait
