from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient
from pathlib import Path
import os


def push_blob(db_account_url, container_name, blob_name, download_path):
    # Push the local SQLite database file to Azure Blob Storage
    print("Authenticating with Azure...")
    credential = DefaultAzureCredential()
    blob_client = BlobClient(
        account_url=db_account_url,
        container_name=container_name,
        blob_name=blob_name,
        credential=credential
    )
    local_db_path = download_path / blob_name
    print(f"Uploading {local_db_path} to Azure Blob Storage...")
    with local_db_path.open("rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    print("Upload complete.")

def pull_blob(
        download_path,
        account_url,
        container_name,
        blob_name,
):
    print("Authenticating with Azure...")
    credential = DefaultAzureCredential()

    blob_client = BlobClient(
        account_url=account_url,
        container_name=container_name,
        blob_name=blob_name,
        credential=credential
    )

    download_path.mkdir(parents=True, exist_ok=True)

    with (download_path / blob_name).open("wb") as f:
        print(f"Downloading blob {blob_name} to {download_path}...")
        download_stream = blob_client.download_blob()
        f.write(download_stream.readall())
        print("Download complete.")
