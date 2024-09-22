import os
import logging
from azure.storage.blob import BlobServiceClient, ContainerClient
from azure.core.exceptions import ResourceNotFoundError, ClientAuthenticationError, HttpResponseError

# Replace with your connection string
connection_string = "your_connection_string_here"
container_name = "your-container-name"
file_path = "path/to/your/file.txt"
blob_name = "file.txt"  # The name for the file in Blob Storage

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def upload_file_to_blob():
    try:
        # Step 1: Check if the file exists and is not empty
        if not os.path.exists(file_path):
            logger.error(f"File '{file_path}' does not exist.")
            return
        
        if os.path.getsize(file_path) == 0:
            logger.error(f"File '{file_path}' is empty.")
            return
        
        logger.info(f"File '{file_path}' found. Size: {os.path.getsize(file_path)} bytes")

        # Step 2: Connect to Azure Blob service
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        logger.info("Connected to Azure Blob service.")

        # Step 3: Check if the container exists
        container_client = blob_service_client.get_container_client(container_name)
        
        try:
            container_client.get_container_properties()
            logger.info(f"Container '{container_name}' already exists.")
        except ResourceNotFoundError:
            # Step 4: Create the container if it doesn't exist
            logger.warning(f"Container '{container_name}' not found. Creating it now...")
            container_client.create_container()
            logger.info(f"Container '{container_name}' created.")
        
        # Step 5: Upload the file to the container
        with open(file_path, "rb") as data:
            blob_client = container_client.get_blob_client(blob_name)
            blob_client.upload_blob(data, overwrite=True)
            logger.info(f"File '{blob_name}' uploaded successfully to container '{container_name}'.")

    except ClientAuthenticationError:
        logger.error("Authentication failed. Please check your connection string and credentials.")
    except HttpResponseError as e:
        logger.error(f"HTTP error occurred: {e.message}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    upload_file_to_blob()
