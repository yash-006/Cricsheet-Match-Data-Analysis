import os

base_path = "data/raw_json"

for folder in os.listdir(base_path):
    folder_path = os.path.join(base_path, folder)

    if os.path.isdir(folder_path):
        file_count = len(os.listdir(folder_path))
        print(f"{folder} → {file_count} files")
