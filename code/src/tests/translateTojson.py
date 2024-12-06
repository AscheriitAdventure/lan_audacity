import os
import sys
import json

VAR_ORIGIN_FILE = "C:\\Users\\g.tronche\\Documents\\GitHub\\lan_audacity\\code\\data\\type_object.json"
VAR_DEST_FILE = "D:\\lan-audacity\\backup\\resources\\type_object.json"

VAR_ORIGIN_HEAD = ["_id", "_osi_protocol", "_name_type", "_dsc_type"]
VAR_NEW_HEAD = ["osi_layer", "name", "description", "pixmap_path"]

"""
    Table of correspondance between the old and new keys:
    _osi_protocol (str) -> osi_layer (int)
    _name_type (str) -> name (str)
    _dsc_type (str) -> description (str)
    "" -> pixmap_path (str)
"""

def map_keys(data):
    """
    Maps the old keys to the new keys based on the defined correspondence.
    """
    new_data = []
    for item in data:
        transformed_item = {
            "osi_layer": int(item.get("_osi_protocol", 0)) if "_osi_protocol" in item else 0,
            "name": item.get("_name_type", ""),
            "description": item.get("_dsc_type", ""),
            "pixmap_path": ""  # Assuming pixmap_path is not available in the source
        }
        new_data.append(transformed_item)
    return new_data

def main():
    # Ensure the source file exists
    if not os.path.exists(VAR_ORIGIN_FILE):
        print(f"Error: The file {VAR_ORIGIN_FILE} does not exist.", file=sys.stderr)
        sys.exit(1)

    # Read the source file
    with open(VAR_ORIGIN_FILE, "r", encoding="utf-8") as origin_file:
        try:
            data = json.load(origin_file)
        except json.JSONDecodeError as e:
            print(f"Error reading JSON file: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Transform the data
    transformed_data = map_keys(data)

    # Ensure the destination directory exists
    dest_dir = os.path.dirname(VAR_DEST_FILE)
    os.makedirs(dest_dir, exist_ok=True)

    # Write the transformed data to the destination file
    with open(VAR_DEST_FILE, "w", encoding="utf-8") as dest_file:
        json.dump(transformed_data, dest_file, ensure_ascii=False, indent=4)

    print(f"Transformed data has been written to {VAR_DEST_FILE}.")

if __name__ == "__main__":
    main()
