"""
Central configuration file for all backup and restore scripts.

Defines:
  - Source file directory (`source_path`).
  - Mapping file location (`guid_mapping_file`).
  - Skip rules (`skip_files` and `skip_path`) for uploads.
  - Restore location (`restore_root`) and concurrency (`max_workers`).
  - Azure connection details (`connection_string`, `container_name`).
  - System metrics log file (`metrics_log_file`).

Edit this file before running any other scripts.
Security Note:
  - Move sensitive values like `connection_string` to environment variables for production.
"""

#  Path where the source files will be copied from (used in build_index.py)
source_path = ''
# JSON file to store GUID to file path mappings (used in build_index.py, save_blob.py, write-blob.py)
guid_mapping_file = 'guid_file_mapping.json'

# comma separated file names listed will be ignored (used in save_blob.py)
skip_files = []
# any paths listed will save the path name, but exclude any files within those paths (used in save_blob.py)
skip_path = []

# write-blob.py Configuration 
restore_root = "<path_where_files_will_be_restored>"
max_workers = 20  # parallel workers
metrics_log_file = "system_metrics_log.json"

# Azure Blob Storage details (used in save_blob.py, write-blob.py)
# note, these should be moved to env variables for security
connection_string = "<connection_string>"
container_name = "<container>"



