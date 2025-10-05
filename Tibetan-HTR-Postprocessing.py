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
