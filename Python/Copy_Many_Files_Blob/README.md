# Azure Blob Storage File Indexing, Upload, and Restoration

This repository contains Python scripts for indexing files, uploading them to Azure Blob Storage, and restoring them back to a local path.  
It is designed for large-scale file backup and retrieval workflows, with support for parallel operations and system metrics monitoring.

## 📋 Pre-reqs

- **Python 3.6 or later**  
  Verify installation:
  ```bash
  python3 --version
  ```
  
- **pip**  
  Verify installation:
  ```bash
  pip --version
  ```
  Install using apt:
  ```bash
  apt install python3-pip
  ```

- **Azure Storage Blob library for Python**  
```bash
pip install azure-storage-blob
```

- **psutil library for system monitoring**  
```bash
pip install psutil
```

## 📂 Scripts Overview

### 1. `config.py`
Central configuration file used by all other scripts.

- **`source_path`** — Local directory to index (`build_index.py`).
- **`guid_mapping_file`** — JSON file mapping GUIDs to file paths.
- **`skip_files`** — List of filenames to skip during upload.
- **`skip_path`** — List of paths to skip during upload (directory placeholders are still created).
- **`restore_root`** — Base directory for restored files.
- **`max_workers`** — Number of parallel workers for restoring files.
- **`metrics_log_file`** — Path to store system performance metrics during restore.
- **`connection_string`** — Azure Blob Storage connection string.
- **`container_name`** — Azure Blob Storage container name.

> **Security Note:** For production, store sensitive values like `connection_string` in environment variables.

---

### 2. `build_index.py`
Indexes all files in `source_path` and creates a GUID mapping JSON.

**Key Features:**
- Recursively scans `source_path`.
- Generates a server-wide GUID prefix and per-file GUIDs.
- Saves a JSON mapping of `{guid: file_path}`.
- Deletes any existing mapping file before recreating.

**Usage:**
```bash
python build_index.py
```
**Output:**
- Console log of GUID → file path mappings.
- JSON mapping file saved to `guid_mapping_file`.

---

### 3. `save_blob.py`
Uploads files to Azure Blob Storage using the GUIDs from `build_index.py`.

**Key Features:**
- Reads GUID-to-path mapping from `guid_mapping_file`.
- Skips files based on `skip_files` and `skip_path`.
- Creates empty blobs for skipped directories (placeholders).
- Uploads each file as a blob with the GUID as its name.

**Usage:**
```bash
python save_blob.py
```
**Output:**
- Console log of skipped/processed files.
- Upload progress and total file count.

---

### 4. `write-blob.py`
Restores files from Azure Blob Storage using the GUID mapping.

**Key Features:**
- Downloads files in parallel (`max_workers` threads).
- Restores to `restore_root` while preserving original directory structure.
- Monitors CPU, memory, and disk I/O usage every second (`psutil`).
- Saves performance metrics to `metrics_log_file`.

**Usage:**
```bash
python write-blob.py
```
**Output:**
- Console log for each restored file.
- Total restore time (seconds & minutes).
- Total files restored.
- System metrics JSON log.

---

## ⚙️ Installation

1. **Clone Repository**
```bash
git clone <repo_url>
cd <repo_directory>
```

2. **Install Dependencies**
```bash
pip install azure-storage-blob psutil
```

3. **Edit Configuration**
Open `config.py` and set:
- `source_path`
- `connection_string`
- `container_name`
- `restore_root`
- Any skip rules for uploads

---

## 🚀 Typical Workflow

1. **Index Files**
```bash
python build_index.py
```

2. **Upload to Azure**
```bash
python save_blob.py
```

3. **Restore Files**
```bash
python write-blob.py
```

---

## 📄 Example `config.py`
```python
source_path = "/mnt/data"
guid_mapping_file = "guid_file_mapping.json"

skip_files = ["temp.txt", "ignore.me"]
skip_path = ["/mnt/data/cache"]

restore_root = "/mnt/restore"
max_workers = 20
metrics_log_file = "system_metrics_log.json"

connection_string = "DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=core.windows.net"
container_name = "mycontainer"
```

---

## 🛡️ Security
- **Never commit `connection_string` to version control.**
- Use environment variables:
```python
import os
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
```

---

## 📌 Notes
- Ensure `source_path` exists before running `build_index.py`.
- Azure Blob container must exist before running `save_blob.py`.
- The GUID mapping must be consistent between upload and restore steps.
- `write-blob.py` assumes `guid_file_mapping.json` is present in the current directory.

