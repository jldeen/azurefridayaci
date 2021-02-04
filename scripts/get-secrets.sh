#!/bin/bash

# example command:
# sh scripts/get-secrets.sh

set -e

# Set the following
spName=aciazfriday
subName="ca-jessde-demo-test"

# set the subscription
az account set --subscription "$subName" && echo "Your default subscription has been set to: $subName"

# Create a service principal
    echo "Creating service principal..."
    spInfo=$(az ad sp create-for-rbac --name "$spName" \
            --role owner \
            --sdk-auth)

    # save spInfo locally
    echo $spInfo > auth.json        

    if [ $? == 0 ]; then
        
        echo '========================================================='
        echo 'GitHub secrets for configuring GitHub workflow'
        echo '========================================================='
        echo "AZURE_CREDENTIALS: $spInfo"
        echo '========================================================='
    else
        "An error occurred. Please try again."
         exit 1
    fi
