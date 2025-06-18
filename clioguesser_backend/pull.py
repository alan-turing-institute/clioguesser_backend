import os
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient


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
        credential=credential,
    )

    download_path.mkdir(parents=True, exist_ok=True)

    with (download_path / blob_name).open("wb") as f:
        print(f"Downloading blob {blob_name} to {download_path}...")
        download_stream = blob_client.download_blob()
        f.write(download_stream.readall())
        print("Download complete.")


def main():
    # Example usage
    db_account_url = os.getenv("DB_ACCOUNT_URL")
    container_name = os.getenv("DB_CONTAINER_NAME", "databases")
    db_name = Path(os.getenv("DB_NAME"))
    blob_name = db_name.stem
    download_path = db_name.parents[0]

    pull_blob(download_path, db_account_url, container_name, blob_name)


if __name__ == "__main__":
    main()
