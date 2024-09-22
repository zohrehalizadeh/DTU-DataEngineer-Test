import os
from azure.identity import ClientSecretCredential
from azure.monitor.query import LogsQueryClient
from azure.monitor.query import LogsQueryStatus

# Set up Azure credentials
client_id = os.getenv("AZURE_CLIENT_ID")  # Add your client ID here
tenant_id = os.getenv("AZURE_TENANT_ID")  # Add your tenant ID here
client_secret = os.getenv("AZURE_CLIENT_SECRET")  # Add your client secret here

# Authenticate using ClientSecretCredential (service principal)
credential = ClientSecretCredential(client_id=client_id, tenant_id=tenant_id, client_secret=client_secret)

# Initialize the LogsQueryClient
logs_client = LogsQueryClient(credential)

# Define the query (KQL) to fetch logs from a specific resource
query = """
AzureActivity
| where ResourceProvider == "Microsoft.Compute"
| where ResourceId contains "your-resource-id"
| order by TimeGenerated desc
"""

# Time range for the query (last 1 day in this example)
time_range = "P1D"

# The workspace ID where the logs are stored (typically Log Analytics workspace ID)
workspace_id = "your-log-analytics-workspace-id"

def download_logs():
    try:
        # Step 3: Run the query to fetch logs
        response = logs_client.query_workspace(
            workspace_id=workspace_id,
            query=query,
            timespan=time_range
        )

        # Check the status of the query
        if response.status == LogsQueryStatus.PARTIAL:
            print("Query partially successful. Some logs might be missing.")
            print(response.partial_error)
        elif response.status == LogsQueryStatus.FAILURE:
            print(f"Query failed: {response.error}")
            return
        
        # Step 4: Process and save logs locally
        logs = response.tables[0].rows
        if not logs:
            print("No logs found.")
            return

        with open("azure_logs.txt", "w") as log_file:
            for log in logs:
                log_file.write(f"{log}\n")
        
        print("Logs downloaded successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_logs()
