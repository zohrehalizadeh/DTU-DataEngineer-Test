import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from io import StringIO

# Storage account and container details
storage_account_name = "dataengineerv1"
container_name = "raw"
blob_name = "tourism_dataset.csv"

# Construct the Blob service URL
blob_service_url = f"https://{storage_account_name}.blob.core.windows.net"

# Connect to Azure Storage using DefaultAzureCredentials
credentials = DefaultAzureCredential()
blob_service_client = BlobServiceClient(account_url=blob_service_url, credential=credentials)

# Access the specific container and blob
container_client = blob_service_client.get_container_client(container_name)
blob_client = container_client.get_blob_client(blob_name)

# Download the blob (CSV file) and read it into a Pandas DataFrame
blob_data = blob_client.download_blob().readall()
csv_data = blob_data.decode('utf-8')  # Decode bytes to a string

# Load the CSV data into a Pandas DataFrame
df = pd.read_csv(StringIO(csv_data))

# Display the DataFrame
print(df.head())  # Print the first few rows of the DataFrame

# Group by 'country' and calculate the average of 'Rate'
country_avg_rate = df.groupby('Country')['Rating'].mean().reset_index()

# Print the result
print("Average Rate by Country:")
print(country_avg_rate)

## -- SQL query to achieve the same result
## SELECT country, AVG(Rate) AS average_rate
## FROM tourism_dataset
## GROUP BY country;

# Assuming there's a 'category' column in your DataFrame
top_categories = df.groupby('Category')['Rating'].mean().reset_index()

# Sort by average rate in descending order and get the top 3
top_categories = top_categories.sort_values(by='Rating', ascending=False).head(3)

# Print the result
print("Top 3 Categories with Highest Average Rate:")
print(top_categories)

## -- SQL query to achieve the same result
## SELECT category, AVG(Rate) AS average_rate
## FROM tourism_dataset
## GROUP BY category
## ORDER BY average_rate DESC
## LIMIT 3;

# Create a new DataFrame to store results
results = pd.concat([
    country_avg_rate.assign(Type='Country Average Rate'),
    top_categories.assign(Type='Top Categories')
])

# Save the results to a CSV file
results.to_csv('Zohreh-Alizadeh.csv', index=False)

print("Results have been saved to Zohreh-Alizadeh.csv")

