import os
import shutil
import zipfile

import py7zr


def extract_zip(input_file, output_dir):
    with zipfile.ZipFile(input_file, "r") as zip_ref:
        for file_info in zip_ref.infolist():
            with zip_ref.open(file_info) as source, open(
                os.path.join(output_dir, file_info.filename), "wb"
            ) as target:
                shutil.copyfileobj(source, target)


def extract_7z(input_file, output_dir):
    with py7zr.SevenZipFile(input_file, mode="r") as archive:
        for file_info in archive.getnames():
            with archive.read(file_info) as source, open(
                os.path.join(output_dir, file_info), "wb"
            ) as target:
                shutil.copyfileobj(source, target)

def extract_rar(input_file, output_dir):
    


def extract_compressed_files(compressed_file, output_dir):
    if compressed_file.lower().endswith(".zip"):
        extract_zip(compressed_file, output_dir)
    elif compressed_file.lower().endswith(".7z"):
        extract_7z(compressed_file, output_dir)
    else:
        print(f"Unsupported file format: {compressed_file}")


def extract_all_files_in_directory(directory, output_dir):
    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            extract_compressed_files(full_path, output_dir)


if __name__ == "__main__":
    INPUT_DIRECTORY = "path/to/compressed/files"
    OUTPUT_DIRECTORY = "path/to/extracted/files"

    # Extract all compressed files in the input directory
    extract_all_files_in_directory(INPUT_DIRECTORY, OUTPUT_DIRECTORY)

    print(f"Extraction completed. Files saved in {OUTPUT_DIRECTORY}")
