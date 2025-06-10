#!/bin/bash

# Written by the one and only JOEL SEAMAN

installJQ () {
    # Check if jq is already installed
    if ! command -v jq &> /dev/null; then
        echo "jq is not found. Installing jq..."

        # Check if Xcode Command Line Tools are installed
        if ! command -v xcode-select &> /dev/null; then
            echo "Xcode Command Line Tools are not found. Installing..."
            xcode-select --install
            echo "Xcode Command Line Tools installed successfully."
        fi

        # Download jq binary
        curl -LO https://github.com/stedolan/jq/releases/download/jq-1.6/jq-osx-amd64

        # Make jq binary executable
        chmod +x jq-osx-amd64

        # Move jq binary to /usr/local/bin
        sudo mv jq-osx-amd64 /usr/local/bin/jq

        echo "jq has been installed successfully."
    fi
}

# Jamf URL saved in Policy parameters
jssAddress="$4"

# Jamf API account username and password
jssAPIUsernameEncrypted="$5"
jssAPIUsernameSalt="e3b9fb035cfe651c"
jssAPIUsernamePassphrase="d7944542a203a54bee81c1cb"

jssAPIPasswordEncrypted="$6"
jssAPIPasswordSalt="da3c68d5e7d2ed84"
jssAPIPasswordPassphrase="7df2052d0b211db16b0b41b0"

# Decryption Function
DecryptString() {
    # Usage: ~$ DecryptString "Encrypted String" "Salt" "Passphrase"
    echo "${1}" | /usr/bin/openssl enc -aes256 -md md5 -d -a -A -S "${2}" -k "${3}"
}

# Variables to call the decrypt function and store the plain text Username and password
jssAPIUsername=$(DecryptString $jssAPIUsernameEncrypted $jssAPIUsernameSalt $jssAPIUsernamePassphrase)
jssAPIPassword=$(DecryptString $jssAPIPasswordEncrypted $jssAPIPasswordSalt $jssAPIPasswordPassphrase)

# Variable declarations
bearerToken=""
ComputerID=""
clientManagementID=""
LAPSPass=""

# API call to return the Secure Bearer Token to use in later API calls
getBearerToken() {
	response=$(curl -s -u "$jssAPIUsername":"$jssAPIPassword" "$jssAddress"/api/v1/auth/token -X POST)
	bearerToken=$(echo "$response" | plutil -extract token raw -)
	tokenExpiration=$(echo "$response" | plutil -extract expires raw - | awk -F . '{print $1}')
	tokenExpirationEpoch=$(date -j -f "%Y-%m-%dT%T" "$tokenExpiration" +"%s")
}


# Run AppleScript to get Target Computer
ComputerName=$(osascript -e 'set userInput to text returned of (display dialog "Enter Target Computer Name (MCS0XXXX - Case sensitive):" default answer "")')

echo "Target Computer: $ComputerName"

getComputerID () {
    jamfID=$(curl -X GET "$jssAddress/api/v1/computers-inventory?section=GENERAL&page=0&page-size=500&sort=id%3Aasc&filter=general.name%3D%3D%22$ComputerName%22" -H "accept: application/json" -H "Authorization: Bearer $bearerToken")
    ComputerID=$(echo "$jamfID" | jq -r '.results[0].id')

    if [ "$ComputerID" = "null" ]; then
        echo "ComputerID is not available."
    else
        echo echo "ComputerID: Retrieved"
    fi
}

getManagementID() {
    # API Call to return the Client Management ID needed to retrieve the LAPS Password via API
    managementid=$(curl -X GET "$jssAddress/api/v1/computers-inventory/$ComputerID?section=GENERAL" -H "accept: application/json" -H "Authorization: Bearer $bearerToken")
    # jq (JSON Query) to parse the JSON output from the API
    clientManagementID=$(echo "$managementid" | jq -r '.general.managementId')

    #Check if JSON has been parsed correctly
    if [ "$clientManagementID" = "null" ]; then
        echo "Management ID is not available."
    else
        echo "Management ID: Retrieved"
    fi
}

getAdminPassword() {
    # API to output the current Admin Password - Takes Client Management ID as an input
    jamfLAPS=$(curl -X GET "$jssAddress/api/v2/local-admin-password/$clientManagementID/account/adminlaps/password" -H "accept: application/json" -H "Authorization: Bearer $bearerToken")
    LAPSPass=$(echo "$jamfLAPS"| jq -r '.password')

    #Check if JSON has been parsed correctly
    if [ "$LAPSPass" = "null" ]; then
        echo "LAPS Password is not available."
    else
        echo "LAPS Password: Retrieved"
    fi
}

# Calling all the functions
installJQ
getBearerToken
getComputerID
getManagementID
getAdminPassword

# Function to copy text to clipboard using pbcopy 
copy_to_clipboard() {
  echo "$1" | pbcopy
}


# Create an AppleScript command to display the GUI dialog
osascript <<EOD
  set theText to "$LAPSPass"

  display dialog "Username: adminlaps \n\nPassword: \n$LAPSPass" buttons {"Copy", "Quit"} default button 1 with title "Admin LAPS" with icon note
  set theButton to button returned of the result

  if theButton is "Copy" then
    do shell script "echo " & quoted form of theText & " | pbcopy"
    display dialog "Username: adminlaps \n\nPassword: \n$LAPSPass" buttons {"Copy", "Quit"} default button 1 with title "Admin LAPS" with icon note
    else
    end
EOD
exit 0