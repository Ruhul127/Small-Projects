import os
import shutil
import zipfile
import argparse
from pathlib import Path

# Function to rename files in bulk
def bulk_rename(directory, prefix=None, suffix=None):
    for count, filename in enumerate(os.listdir(directory), 1):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_extension = os.path.splitext(filename)[1]  # Get file extension
            new_filename = f"{prefix if prefix else ''}{count}{suffix if suffix else ''}{file_extension}"
            new_file_path = os.path.join(directory, new_filename)
            os.rename(file_path, new_file_path)
            print(f"Renamed: {filename} -> {new_filename}")

# Function to organise files by type into folders
def organize_by_type(directory):
    file_types = {
        "Images": [".jpg", ".jpeg", ".png", ".gif"],
        "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
        "Videos": [".mp4", ".mov", ".avi"],
        "Archives": [".zip", ".tar", ".gz"]
    }
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_extension = os.path.splitext(filename)[1]
            
            # Find matching file type folder
            moved = False
            for folder, extensions in file_types.items():
                if file_extension.lower() in extensions:
                    folder_path = os.path.join(directory, folder)
                    os.makedirs(folder_path, exist_ok=True)
                    shutil.move(file_path, os.path.join(folder_path, filename))
                    print(f"Moved: {filename} -> {folder}/")
                    moved = True
                    break
            
            if not moved:
                print(f"No folder for {filename} (extension {file_extension}), skipping.")

# Function to create a ZIP backup of a folder
def create_zip_backup(directory, output_filename):
    output_path = os.path.join(directory, output_filename)
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for foldername, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                if not filename.endswith('.zip'):  # Avoid including the output ZIP itself
                    zipf.write(file_path, os.path.relpath(file_path, directory))
    print(f"Backup created: {output_path}")

# Function to move specific files to a designated folder
def move_files(directory, destination_folder, pattern):
    destination_folder = Path(destination_folder)
    destination_folder.mkdir(parents=True, exist_ok=True)
    
    for filename in os.listdir(directory):
        if pattern in filename:
            source_path = os.path.join(directory, filename)
            if os.path.isfile(source_path):
                destination_path = destination_folder / filename
                shutil.move(source_path, destination_path)
                print(f"Moved: {filename} -> {destination_folder}/")

# Main function with command-line interface
def main():
    parser = argparse.ArgumentParser(description="Automate common system tasks")
    
    # Add subcommands
    subparsers = parser.add_subparsers(dest="command")
    
    # Subcommand: Rename files
    rename_parser = subparsers.add_parser('rename', help="Bulk rename files in a directory")
    rename_parser.add_argument('directory', help="Directory containing files to rename")
    rename_parser.add_argument('--prefix', help="Prefix for new filenames", default=None)
    rename_parser.add_argument('--suffix', help="Suffix for new filenames", default=None)
    
    # Subcommand: Organise files
    organise_parser = subparsers.add_parser('organise', help="Organise files by type into subfolders")
    organise_parser.add_argument('directory', help="Directory containing files to organise")
    
    # Subcommand: Create ZIP backup
    zip_parser = subparsers.add_parser('zip', help="Create a ZIP backup of a folder")
    zip_parser.add_argument('directory', help="Directory to backup")
    zip_parser.add_argument('--output', help="Name of the output ZIP file", default="backup.zip")
    
    # Subcommand: Move files based on pattern
    move_parser = subparsers.add_parser('move', help="Move files based on a pattern to a designated folder")
    move_parser.add_argument('directory', help="Directory containing files to move")
    move_parser.add_argument('destination', help="Destination folder to move files to")
    move_parser.add_argument('pattern', help="Pattern to match filenames")
    
    args = parser.parse_args()
    
    # Execute the appropriate function based on the command
    if args.command == "rename":
        bulk_rename(args.directory, args.prefix, args.suffix)
    elif args.command == "organise":
        organize_by_type(args.directory)
    elif args.command == "zip":
        create_zip_backup(args.directory, args.output)
    elif args.command == "move":
        move_files(args.directory, args.destination, args.pattern)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
