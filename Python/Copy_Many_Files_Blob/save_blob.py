"""
Uploads local files to Azure Blob Storage using the GUID-to-file mapping created by build_index.py.

This script:
  - Reads `guid_mapping_file` (JSON) created by build_index.py.
  - Skips files whose names are in `skip_files` (exact match).
  - Skips file content (but creates placeholders) for paths in `skip_path`.
  - Uploads each file as a blob, using the GUID as the blob name.
  - Prints progress for each file and a summary of total files uploaded.

Run this script after build_index.py to back up files to Azure.
Dependencies:
  - config.py must be configured with Azure `connection_string` and `container_name`.
  - Container must exist in Azure Blob Storage.
"""

import json
from azure.storage.blob import BlobServiceClient
import os
import time
from config import *

start = int(time.time())
files = 0

# read guid_mapping_file json file
with open(guid_mapping_file, "r") as json_file:
    data = json.load(json_file)

# Create BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

# Loop through JSON and upload files
for guid, file_path in data.items():
    print(f"Processing {guid} :: {file_path}")
    # check to see if any part of the file_path is in skip_files
    if any(skip_file in file_path for skip_file in skip_files):
        print(f"Skipping {guid} :: {file_path}")
        continue

    
    # Check if path should be treated as directory placeholder
    if any(file_path.startswith(path) for path in skip_path):
        print(f"Creating placeholder for directory {file_path}")
        blob_client = container_client.get_blob_client(blob=guid + "/")  # optional slash
        blob_client.upload_blob(b"", overwrite=True)  # empty content
        continue

    # upload file
    if os.path.exists(file_path):
        blob_client = container_client.get_blob_client(blob=guid)
        with open(file_path, "rb") as data_file:
            blob_client.upload_blob(data_file, overwrite=True)
        print(f"Uploaded {file_path} as {guid}")
        files += 1
    else:
        print(f"File not found: {file_path}")

end = int(time.time())
print(f"Time taken: {end - start} seconds")
print(f"Total files uploaded: {files}")
