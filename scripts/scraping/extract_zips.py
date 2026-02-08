import os
import zipfile

# ---------- Project Root ----------
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

raw_path = os.path.join(project_root, "data", "raw_json")

print("Raw ZIP folder:", raw_path)

# ---------- Extract Each ZIP ----------
for file in os.listdir(raw_path):

    if file.endswith(".zip"):

        zip_path = os.path.join(raw_path, file)

        # Folder name = zip name without extension
        extract_folder = os.path.join(raw_path, file.replace(".zip", ""))

        os.makedirs(extract_folder, exist_ok=True)

        print(f"\nExtracting {file}...")

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)

print("\nAll ZIP files extracted ✅")
