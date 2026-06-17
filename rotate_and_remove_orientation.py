"""
Rotate images and remove EXIF orientation metadata

Description
-----------
This script rotates image files by a specified angle, saves the rotated images to an output directory, and removes the EXIF Orientation tag.

It permanently applies the rotation to the image pixels and then removes the Orientation tag so that image viewers, OCR software, and HTR pipelines no longer rely on EXIF metadata for display.


Requirements
------------
- Python 3.8+
- Pillow
- ExifTool

Install Pillow:
    pip install pillow

Download ExifTool:
    https://exiftool.org/


Configuration
-------------
Update the following variables before running:

    EXIFTOOL_PATH
    INPUT_DIR
    OUTPUT_DIR
    ROTATION_ANGLE

Supported image formats:
    .jpg
    .jpeg
    .png
    .tif
    .tiff


To Use
-----
python rotate_and_remove_orientation.py


Notes
-----
- ExifTool will create backup files unless the '-overwrite_original' option is used
- The original images ARE NOT modified
- Rotated images are written to OUTPUT_DIR
"""

import os
import subprocess
from pathlib import Path

from PIL import Image

# Path to ExifTool
EXIFTOOL_PATH = r"path/to/exiftool"

# Directory containing your images
INPUT_DIR = r"path/to/input/images"

# Directory to save rotated images
OUTPUT_DIR = r"path/to/output/images"

# Common values:
# 90   = clockwise quarter turn
# 180  = upside down
# 270  = anticlockwise quarter turn
ROTATION_ANGLE = 270

def rotate_image(image_path, output_path, rotation_angle):
    """
    Rotate an image and preserve its EXIF metadata
    """
    try:
        with Image.open(image_path) as img:
            rotated = img.rotate(rotation_angle, expand=True)

            exif_data = img.info.get("exif", b"")

            rotated.save(output_path, exif=exif_data)

        print(f"Rotated: {output_path}")

    except Exception as error:
        print(f"Failed to rotate {image_path}: {error}")


def remove_orientation_tag(image_path, exiftool_path):
    """
    Remove the EXIF Orientation tag from an image
    """
    try:
        subprocess.run(
            [
                exiftool_path,
                "-overwrite_original",
                "-Orientation=",
                str(image_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        print(f"Removed Orientation tag: {image_path}")

    except subprocess.CalledProcessError as error:
        print(f"Failed to update EXIF for {image_path}")
        print(error.stderr)


def main():
    """
    Process all supported image files in INPUT_DIR
    """
    input_dir = Path(INPUT_DIR)
    output_dir = Path(OUTPUT_DIR)

    output_dir.mkdir(parents=True, exist_ok=True)

    supported_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".tif",
        ".tiff",
    }

    for image_file in input_dir.iterdir():

        if image_file.suffix.lower() not in supported_extensions:
            continue

        output_file = output_dir / image_file.name

        rotate_image(
            image_file,
            output_file,
            ROTATION_ANGLE,
        )

        remove_orientation_tag(
            output_file,
            EXIFTOOL_PATH,
        )

    print("\nProcessing complete.")


if __name__ == "__main__":
    main()