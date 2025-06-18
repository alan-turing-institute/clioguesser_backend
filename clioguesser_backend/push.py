import os
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient


def push_blob(db_account_url, container_name, blob_name, download_path):
    # Push the local SQLite database file to Azure Blob Storage
    print("Authenticating with Azure...")
    credential = DefaultAzureCredential()

    print("Creating BlobClient...", db_account_url, container_name, blob_name)
    blob_client = BlobClient(
        account_url=db_account_url,
        container_name=container_name,
        blob_name=blob_name,
        credential=credential,
    )

    local_db_path = download_path / blob_name
    print(f"Uploading {local_db_path} to Azure Blob Storage...")
    with local_db_path.open("rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    print("Upload complete.")


def main():
    # Example usage
    db_account_url = os.getenv("DB_ACCOUNT_URL")
    container_name = os.getenv("DB_CONTAINER_NAME", "databases")
    db_name = Path(os.getenv("DB_NAME"))
    blob_name = db_name.parts[-1]
    download_path = db_name.parents[0]

    push_blob(db_account_url, container_name, blob_name, download_path)


if __name__ == "__main__":
    main()
