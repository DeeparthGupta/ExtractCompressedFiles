import argparse
import os
import shutil
import zipfile
from pathlib import Path

import py7zr
import patoolib


def handle_extraction_error(file, exception, fail_list):
    """
    Logs an extraction error and updates the failure list.

    This function is called when an extraction process encounters an error. It logs the error
    message and appends the file to the fail_list.

    Args:
        file (str): The file that failed to extract.
        exception (Exception): The exception that was raised during extraction.
        fail_list (list): The list tracking files that failed to extract.
    """

    print(f"Unable to extract {file} due to Error: {exception}")
    fail_list.append(file)


def extract_zip(input_file, output_dir, fail_list):
    """
    Extracts ZIP files and logs failures.

    Args:
        input_file (str): Path to the ZIP file.
        output_dir (str): Target directory for extraction.
        fail_list (list): Accumulates paths of failed extractions.
    """

    try:
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
        print(f"Successfully extracted file {input_file}")
    except Exception as exception: # pylint: disable = W0718
        handle_extraction_error(input_file, exception, fail_list)


def extract_7z(input_file, output_dir, fail_list):
    """
    Extracts 7z files and logs failures.

    Args:
        input_file (str): Path to the 7z file.
        output_dir (str): Target directory for extraction.
        fail_list (list): Accumulates paths of failed extractions.
    """

    try:
        with py7zr.SevenZipFile(input_file, mode="r") as archive:
            archive.extractall(output_dir)
        print(f"Successfully extracted file {input_file}")

    except Exception as exception: # pylint: disable = W0718
        handle_extraction_error(input_file, exception, fail_list)


def extract_rar(input_file, output_dir, fail_list):
    """
    Extracts RAR files and logs failures.

    Args:
        input_file (str): Path to the RAR file.
        output_dir (str): Target directory for extraction.
        fail_list (list): Accumulates paths of failed extractions.
    """

    try:
        patoolib.extract_archive(input_file, outdir=output_dir)

    except Exception as exception: # pylint: disable = W0718
        handle_extraction_error(input_file, exception, fail_list)


def extract_compressed_file(compressed_file, output_dir, fail_list):
    """
    Extracts a compressed file and logs any failures.

    Supports ZIP, 7z, and RAR formats. Files that fail to extract are added to fail_list.

    Args:
        compressed_file (str): Path to the compressed file.
        output_dir (str): Target directory for extraction.
        fail_list (list): Accumulates paths of failed extractions.
    """

    extractors = {".zip": extract_zip, ".7z": extract_7z, ".rar": extract_rar}

    file_extension = Path(compressed_file).suffix
    extractor = extractors.get(file_extension)

    if extractor:
        extractor(compressed_file, output_dir, fail_list)
    else:
        print(f"Unsupported file format:{file_extension}")
        fail_list.append(compressed_file)


def extract_all_files_in_directory(path, output_dir, fail_list):
    """
    Extracts all supported files in a directory and logs failures.

    Args:
        path (str): Source directory or file path.
        output_dir (str): Target directory for extraction.
        fail_list (list): Accumulates paths of failed extractions.
    """

    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                full_path = os.path.join(root, file)
                extract_compressed_file(full_path, output_dir, fail_list)

    elif os.path.isfile(path):
        extract_compressed_file(path, output_dir, fail_list)

    else:
        print(f"{path} is not a valid path")


def main():
    parser = argparse.ArgumentParser(description="Extract compressed archives.")
    parser.add_argument(
        "source", help="Source file or directory containing archives.", required=True
    )
    parser.add_argument(
        "destination", help="Destination directory for extracted files.", required=True
    )
    args = parser.parse_args()

    fail_list = []
    extract_all_files_in_directory(args.source, args.destination, fail_list)

    if fail_list:
        print("The following files could not be extracted:")
        for item in fail_list:
            print(item)
    else:
        print(f"Extraction completed. Files saved in {args.destination}")


if __name__ == "__main__":
    main()
