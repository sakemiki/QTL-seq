import sys
import os
import shutil

def main(output_folder, file_paths):
    for file_path in file_paths:
        if not os.path.exists(file_path):
            continue
        filename = os.path.basename(file_path)
        destination = os.path.join(output_folder, filename)
        shutil.copy(file_path, destination)

if __name__ == "__main__":
    output_folder = sys.argv[1]  
    file_paths = sys.argv[2:]   
