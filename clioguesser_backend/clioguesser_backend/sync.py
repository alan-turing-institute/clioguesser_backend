import os
import signal
import time
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient


def get_handle_sigterm(download_path, db_account_url, container_name, blob_name):

    def push_blob():
        # Push the local SQLite database file to Azure Blob Storage
        print("Authenticating with Azure...")
        credential = DefaultAzureCredential()
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

    def handle_sigterm(signal_number, frame):
        print("SIGTERM received: shutting down gracefully...")
        i = 0
        while True:
            time.sleep(1)
            print("Waiting for threads to finish... ({} seconds elapsed)".format(i))
            i += 1

        # push_blob()

    return handle_sigterm


def register_shutdown_hook():
    if (db_account_url := os.getenv("DB_ACCOUNT_URL")) is not None:
        container_name = os.getenv("DB_CONTAINER_NAME", "databases")

        # split /path/to/sqlite.db into the filename and the rest.
        db_name = Path(os.getenv("DB_NAME"))
        blob_name = db_name.parts[-1]
        download_path = db_name.parents[0]

        # download_blob_to_file(download_path, db_account_url, container_name, blob_name)

        print("Registering shutdown hook for SIGTERM...")
        signal.signal(
            signal.SIGTERM,
            get_handle_sigterm(
                download_path, db_account_url, container_name, blob_name
            ),
        )
    else:
        print("No DB_ACCOUNT_URL found, skipping shutdown hook registration.")


def download_blob_to_file(
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
