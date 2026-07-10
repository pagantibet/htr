"""
Tibetan HTR postprocessing script

Description
-----------
This script applies rule-based postprocessing to Tibetan HTR output stored in CSV or Excel files. It cleans common OCR/HTR errors involving punctuation, decorative markers, and character misrecognition - based on PaganTibet's diplomatic transcription standards.

The script processes a single column in a dataset, applies deterministic regex corrections, and writes a corrected copy of the file. The original file is not modified.

Key features
------------
- Column selection by name or index (with fallback logic)
- Regex-based Tibetan text normalisation
- Batch processing of tabular datasets
- Automatic output file generation

Supported formats:
- CSV (.csv)
- Excel (.xlsx, .xls)

Requirements
------------
- Python 3.8+
- pandas
- openpyxl (for Excel support)

To Use
-----
Run from the command line:

    python Tibetan_HTR_postprocessing.py input_file.csv
    python Tibetan_HTR_postprocessing.py input_file.csv -o output.csv
    python Tibetan_HTR_postprocessing.py input_file.csv -c column_name
"""

import argparse
import pandas as pd
import os
import re

def postprocess_tibetan_transcript(text: str) -> str:
    """
    Apply Tibetan HTR postprocessing corrections.
    
    Rules applied:
    1. Replace ' ༧ ' with ' ༸ '
    2. Remove ྃ from punctuation/decorative marks
    3. Remove ཾ from decorative marks only in combination with ༄ or ༅
    4. Replace '༐' with '༴'
    """
    if not isinstance(text, str):
        return text

    # 1. Replace ༧ with ༸ - only when there's space around the ༧.
    text = re.sub(r"\s༧\s", " ༸ ", text)

    # 2. Remove ྃ from shad and yig mgo.
    text = re.sub(r"།ྃ+", "།", text)
    text = re.sub(r"༄ྃ*༅ྃ*", "༄༅", text)

    # 3. Remove ཾ from yig mgo.
    text = re.sub(r"༄ཾ*༅ཾ*", "༄༅", text)

    # 4. Replace ༅༅༅ with ༄༅༅ or ༅༅ with ༄༅.
    text = re.sub(r"༅{3}", "༄༅༅", text)
    text = re.sub(r"(?<!༄)༅{2}", "༄༅", text)

    # 5. Replace ༐ with ༴.
    text = re.sub(r"༐", "༴", text)

    # 6. Replace no-break tsheg ༌ with normal tsheg ་.
    text = re.sub(r"༌", "་", text)

    # 7. Replace ༎ nyis shad with two separate shads །།.
    text = re.sub(r"༎", "།།", text)

    # 8. Replace Khmer ៖ with Tibetan gter tsheg ༔ (in case of wrong copying).
    text = re.sub(r"៖", "༔", text)

    # 9. Replace ༝ with ྾.
    text = re.sub(r"༝", "྾", text)

    # 10. Replace double vowels in one char with two chars.
    text = re.sub(r"ཻ", "ེེ", text)
    text = re.sub(r"ཽ", "ོོ", text)

    # 11. Replace ཱུ with two separate chars.
    text = re.sub(r"ཱུ", "ྰུ", text)

    # 12. Replace ཿ with ༔.
    text = re.sub(r"ཿ", "༔", text)

    # 13. Replace tsa rtags that belong to characters.
    text = re.sub(r"ཅ༹", "ཙ", text)
    text = re.sub(r"ཆ༹", "ཚ", text)

    return text


def process_file(input_file: str, output_file: str = None, column="final_reviewed_transcript"):
    """
    Process a CSV or Excel file column with Tibetan HTR text and apply postprocessing.
    """
    ext = os.path.splitext(input_file)[1].lower()

    # Read file depending on extension
    if ext in [".csv"]:
        try:
            df = pd.read_csv(input_file, encoding="utf-8-sig")
        except UnicodeDecodeError:
            df = pd.read_csv(input_file, encoding="cp1252")
    elif ext in [".xlsx", ".xls"]:
        df = pd.read_excel(input_file)
    else:
        raise ValueError("Unsupported file type. Use CSV or Excel file.")

    # Resolve column name or index
    if isinstance(column, str):
        if column in df.columns:
            colname = column
        else:
            colname = df.columns[14] if len(df.columns) > 14 else df.columns[-1]
    else:
        colname = df.columns[int(column)]

    # Apply processing
    df[colname] = df[colname].apply(postprocess_tibetan_transcript)

    # Determine output file
    if not output_file:
        base, _ = os.path.splitext(input_file)
        output_ext = ext if ext in [".csv"] else ".xlsx"
        output_file = f"{base}_corrected{output_ext}"

    # Save file
    if output_file.endswith(".csv"):
        df.to_csv(output_file, index=False, encoding="utf-8-sig")
    else:
        df.to_excel(output_file, index=False)
    print(f"Processed file saved to {output_file}")
    return df


def main():
    parser = argparse.ArgumentParser(description="Tibetan HTR Postprocessing Script (regex version, CSV/XLSX)")
    parser.add_argument("input_file", help="Input CSV or Excel file")
    parser.add_argument("-o", "--output", help="Output file (default: input_corrected.csv/xlsx)")
    parser.add_argument(
        "-c",
        "--column",
        help="Column name or index (default: final_reviewed_transcript)",
        default="final_reviewed_transcript",
    )
    args = parser.parse_args()

    process_file(args.input_file, output_file=args.output, column=args.column)


if __name__ == "__main__":
    main()
