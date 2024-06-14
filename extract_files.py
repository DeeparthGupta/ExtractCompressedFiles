import argparse
import os

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


def extract_compressed_file(compressed_file, output_dir, fail_list):
    """
    Extracts a compressed file and logs any failures.

    Supports ZIP, 7z, and RAR formats. Files that fail to extract are added to fail_list.

    Args:
        compressed_file (str): Path to the compressed file.
        output_dir (str): Target directory for extraction.
        fail_list (list): Accumulates paths of failed extractions.
    """

    try:
        patoolib.extract_archive(compressed_file, outdir=output_dir)
        print(f"Successfully extracted {compressed_file}")
    except Exception as exception:  # pylint: disable = W0718
        handle_extraction_error(compressed_file, exception, fail_list)


def handle_extractions(path, output_dir, fail_list):
    """
    Extracts all supported files in a directory and logs failures. Alternatively, extract a single archive.

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
    # CLI arguments
    parser = argparse.ArgumentParser(description="Extract compressed archives.")
    parser.add_argument("source", help="Source file or directory containing archives.")
    parser.add_argument(
        "destination", help="Destination directory for extracted files."
    )
    args = parser.parse_args()

    # List of all failed extractions
    fail_list = []
    handle_extractions(args.source, args.destination, fail_list)

    if fail_list:
        print("The following files could not be extracted:")
        for item in fail_list:
            print(item)
    else:
        print(f"Extraction completed. Files saved in {args.destination}")


if __name__ == "__main__":
    main()
