"""
Indexes all files under the configured `source_path` and generates a mapping
between each file and a unique GUID.

This script:
  - Recursively scans the `source_path` directory from config.py.
  - Generates a unique `server_guid` and appends a per-file UUID to form the blob ID.
  - Deletes any existing mapping file before creating a new one.
  - Saves the mapping to `guid_mapping_file` (JSON format) for later use by upload/restore scripts.

Run this script first in the workflow to prepare files for Azure Blob upload.
Dependencies:
  - config.py must be properly configured with `source_path` and `guid_mapping_file`.
"""
import os
import uuid
import json
import time
from config import *

# Start time
start = int(time.time())

# counter
count = 0

# Delete the JSON file if it exists
if os.path.exists(guid_mapping_file):
    os.remove(guid_mapping_file)
    print(f"{guid_mapping_file} has been deleted")

# Create a server GUID
server_guid = str(uuid.uuid4())

# Dictionary to hold the mappings
guid_mapping = {}

# Walk through the mounted directory and process each file
for root, dirs, files in os.walk(source_path):
    for file in files:
        file_path = os.path.join(root, file)
        file_guid = f"{server_guid}_{str(uuid.uuid4())}"
        guid_mapping[file_guid] = file_path
        print(f"{file_guid} -> {file_path}")
        count += 1

# Save the mapping to a JSON file
with open(guid_mapping_file, 'w') as f:
    json.dump(guid_mapping, f, indent=2)

# End time
end = int(time.time())
print(f"Script duration: {end - start} seconds")
print(f"Total files processed: {count}")
print(f"GUID to file path mappings have been saved in {guid_mapping_file}.")