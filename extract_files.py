import argparse
import os
import shutil
import zipfile

import py7zr
import patoolib


def extract_zip(input_file, output_dir):
    """
    Extracts files from a ZIP archive.

    Args:
        input_file (str): Path to the ZIP file.
        output_dir (str): Directory where extracted files will be saved.

    Example:
        extract_zip('myarchive.zip', '/path/to/output/directory')
    """
    with zipfile.ZipFile(input_file, "r") as file_ref:
        for file_info in file_ref.infolist():
            if not file_info.is_dir():
                with file_ref.open(file_info) as source, open(
                    os.path.join(output_dir, file_info.filename), "w+b"
                ) as target:
                    shutil.copyfileobj(source, target)
            else:
                subdir_path = os.path.join(output_dir, file_info.filename)
                os.makedirs(subdir_path, exist_ok=True)


def extract_7z(input_file, output_dir):
    """
    Extracts files from a 7-Zip (7z) archive.

    Args:
        input_file (str): Path to the 7z file.
        output_dir (str): Directory where extracted files will be saved.

    Example:
        extract_7z('myarchive.7z', '/path/to/output/directory')
    """
    with py7zr.SevenZipFile(input_file, mode="r") as archive:
        archive.extractall(output_dir)


def extract_rar(input_file, output_dir):
    """
    Extracts files from rar archives.

    Args:
        input_file (str): Path to the rar file
        output_dir (str): Directory where extracted files will be saved.

    Example:
        extract_rar('myarchive.7z', '/path/to/output/directory')
    """

    try:
        patoolib.extract_archive(input_file, outdir=output_dir)
        #print(f"RAR file '{input_file}' extracted to '{output_dir}")

    except Exception as error:
        print(f"Error extracting RAR file: '{error}'")


def extract_compressed_file(compressed_file, output_dir):
    if compressed_file.lower().endswith(".zip"):
        extract_zip(compressed_file, output_dir)
    elif compressed_file.lower().endswith(".7z"):
        extract_7z(compressed_file, output_dir)
    elif compressed_file.lower().endswith(".rar"):
        extract_rar(compressed_file, output_dir)
    else:
        print(f"Unsupported file format: {compressed_file}")


def extract_all_files_in_directory(path, output_dir):
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                full_path = os.path.join(root, file)
                extract_compressed_file(full_path, output_dir)

    elif os.path.isfile(path):
        extract_compressed_file(path,output_dir)

    else:
        print(f"{path} is not a valid path")


if __name__ == "__main__":

    # Take in command line parameters
    argument_parser = argparse.ArgumentParser(description="Extract some archives")
    argument_parser.add_argument(
        "-s", "--source", dest="source", nargs=1, required=True
    )
    argument_parser.add_argument(
        "-d", "--destination", dest="dest_dir", nargs=1, required=True
    )

    arguments = argument_parser.parse_args()

    INPUT_DIRECTORY = arguments.source[0]
    OUTPUT_DIRECTORY = arguments.dest_dir[0]

    # Extract all compressed files in the input directory
    extract_all_files_in_directory(INPUT_DIRECTORY, OUTPUT_DIRECTORY)

    print(f"Extraction completed. Files saved in {OUTPUT_DIRECTORY}")
