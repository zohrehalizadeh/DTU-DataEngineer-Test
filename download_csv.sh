#!/bin/bash

# Install Azure CLI (for Debian-based systems)
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Download the CSV file from the Azure Storage Account
az storage blob download \
  --account-name dataengineerv1 \
  --container-name raw \
  --name tourism_dataset.csv \
  --file ~/result-ZohrehAlizadeh.csv \
  --account-key "ieLmjePYNxBcajmfHvX8TsMXa3bn8nkH3MCuaWTsA/E+G56z3KRYSPO1M5MaHNds5FhE37PsZwYm+AStsnl/lg=="

# Print a confirmation message
echo "CSV file downloaded and saved as result-ZohrehAlizadeh.csv"
