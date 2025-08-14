"""
Restores files from Azure Blob Storage to the local filesystem, based on the GUID mapping file.

This script:
  - Reads `guid_mapping_file` to determine original file paths.
  - Downloads each blob in parallel (`max_workers` threads).
  - Reconstructs the original directory structure under `restore_root`.
  - Monitors system performance (CPU, memory, disk I/O) every second via psutil.
  - Saves metrics to `metrics_log_file` for performance review.

Run this script to restore all uploaded files from Azure to local storage.
Dependencies:
  - config.py must be configured with `restore_root`, `max_workers`, and Azure connection info.
  - `guid_mapping_file` must match the GUIDs in the Azure container.
"""
import json
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from azure.storage.blob import BlobServiceClient
import psutil
from config import *

# Load mapping
with open(guid_mapping_file, "r") as f:
    mapping = json.load(f)

# Azure client
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

restored_files = 0
restored_files_lock = threading.Lock()
system_metrics = []
monitoring = True

def monitor_system_metrics():
    """Monitor CPU, memory, and disk IOPS every second."""
    while monitoring:
        metrics = {
            "timestamp": time.time(),
            "cpu_percent": psutil.cpu_percent(interval=None),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_io": {
                "read_bytes": psutil.disk_io_counters().read_bytes,
                "write_bytes": psutil.disk_io_counters().write_bytes
            }
        }
        system_metrics.append(metrics)
        time.sleep(1)

def download_blob(guid, original_path):
    """Download a blob and save it to the restore path."""
    global restored_files
    try:
        restore_path = os.path.join(restore_root, original_path.lstrip("/mnt/windowsdisk/"))
        os.makedirs(os.path.dirname(restore_path), exist_ok=True)

        blob_client = container_client.get_blob_client(blob=guid)
        with open(restore_path, "wb") as f:
            # Use Azure SDK parallel chunk download
            data = blob_client.download_blob(max_concurrency=8)  # Increased concurrency
            f.write(data.readall())

        with restored_files_lock:
            restored_files += 1

        return f"Restored {guid} -> {restore_path}"
    except Exception as e:
        return f"Failed {guid}: {e}"

# Start monitoring thread
monitor_thread = threading.Thread(target=monitor_system_metrics)
monitor_thread.start()

# Start file restoration
start = time.perf_counter()
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = [executor.submit(download_blob, guid, path) for guid, path in mapping.items()]
    for future in as_completed(futures):
        print(future.result())
end = time.perf_counter()

# Stop monitoring and save metrics
monitoring = False
monitor_thread.join()

with open(metrics_log_file, "w") as f:
    json.dump(system_metrics, f, indent=2)

# Final output
print(f"Time taken: {end - start:.2f} seconds")
print(f"Time taken: {(end - start) / 60:.2f} minutes")
print(f"Total files restored: {restored_files}")
print(f"System metrics saved to {metrics_log_file}")
