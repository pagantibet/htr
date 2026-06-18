# HTR

This repo contains preprocessing and postprocessing utility scripts for the Handwritten Text Recognition (HTR) pipeline of [PaganTibet](https://www.pagantibet.com/) described in Meelen & Griffiths (2025). Please cite the repo and the following article when using any part of this code:

Meelen, M. and Griffiths, R.M. (2025) ‘Collaborative Workflows for Handwritten Text Recognition in Under-Resourced Manuscript Collections’, _Journal of Open Humanities Data_, 11(1), p. 54. https://doi.org/10.5334/johd.388.

**Abstract.** This article addresses important questions that arise when trying to transcribe large and diverse historical manuscript collections, with a focus on under-resourced languages and scripts. Using a pilot study of challenging Tibetan manuscripts, we propose an efficient collaborative workflow that leverages existing layout recognition and HTR models and tools, including Transkribus, with iterative model training, and quantitative and qualitative error analysis. We show how this approach not only improves transcription accuracy but also provides a flexible framework adaptable to other under-resourced manuscript collections, supporting scalable text digitisation projects.

---
## Table of Contents

- [Requirements \& Installation](#requirements--installation)
- [Preprocessing: Image Rotation & EXIF Orientation Removal](#preprocessing-image-rotation--exif-orientation-removal)
  - [Configuration](#configuration)
  - [Usage](#usage)
- [Postprocessing: Transcript Correction](#postprocessing-transcript-correction)
  - [Correction Rules Applied](#correction-rules-applied)
  - [Usage](#usage-1)

---

# Requirements \& Installation

All scripts in this repo have been tested with **Python 3.8+**

## Image Preprocessing

The script `rotate_and_remove_orientation.py` requires:

- Python 3.8+
- Pillow
- ExifTool

Install Pillow:

```bash
pip install pillow
```

Install ExifTool separately from: https://exiftool.org/

## Transcript Postprocessing

The script `postprocess_tibetan_transcript.py` requires:

- Python 3.8+
- pandas

Install pandas:

```bash
pip install pandas
```

To process Excel files (`.xlsx` or `.xls`), install `openpyxl`:

```bash
pip install openpyxl
```

## Install All Dependencies

To install all optional dependencies used across the repository:

```bash
pip install pillow pandas openpyxl
```

---

# Preprocessing: Image Rotation & EXIF Orientation Removal

Many OCR and HTR systems do not consistently interpret EXIF orientation metadata. As a result, images that appear correctly oriented in image viewers may be processed incorrectly during recognition.

The script `rotate_and_remove_orientation.py` permanently applies a pixel-level rotation to manuscript images while preserving existing EXIF metadata. It then removes the EXIF Orientation tag so that image viewers, OCR software, and HTR pipelines no longer rely on metadata-based rotation.

### Configuration

Before running the script, update the following variables in `rotate_and_remove_orientation.py`:

| Variable | Description |
|-----------|-------------|
| `EXIFTOOL_PATH` | Path to the local ExifTool executable |
| `INPUT_DIR` | Directory containing source images |
| `OUTPUT_DIR` | Directory where rotated images will be written |
| `ROTATION_ANGLE` | Rotation angle in degrees |

Common rotation values:

| Value | Result |
|---------|---------|
| `90` | Clockwise quarter turn |
| `180` | Upside down |
| `270` | Anticlockwise quarter turn |

Supported formats:

- `.jpg`
- `.jpeg`
- `.png`
- `.tif`
- `.tiff`

### Usage

```bash
python rotate_and_remove_orientation.py
```

### Notes

- Original images are **not modified**
- Rotated images are written to `OUTPUT_DIR`
- Existing EXIF metadata is preserved
- The EXIF Orientation tag is removed using ExifTool
- The script uses the `-overwrite_original` option to prevent ExifTool from creating backup files

---

# Postprocessing: Transcript Correction

The script `postprocess_tibetan_transcript.py` applies a deterministic, regex-based correction layer to Tibetan HTR outputs stored in CSV or Excel files.

The script processes a specified column and writes a corrected copy of the file while preserving the original.

### Correction Rules Applied

The following transformations are applied sequentially:

1. Replaces `༧` with `༸` when surrounded by whitespace to avoid deleting numerals

2. Removes stray `ྃ` and `ཾ` attached to punctuation marks (`།`) and decorative markers (`༄༅`). Syllables with `ཾ` (e.g., `དཾ`) are preserved

4. Converts:
     - `༅༅༅` → `༄༅༅`
     - `༅༅` → `༄༅`

5. Replaces `༐` with `༴` - in keeping with PaganTibet's transcription standards (see, Meelen, M., & Griffiths, R. M. (2025). HTR Input & Correction Manual. Zenodo. https://doi.org/10.5281/zenodo.17257009).

### Input Formats

Supported input formats:

- `.csv`
- `.xlsx`
- `.xls`

### Column Selection

By default, the script looks for a column named:

```text
final_reviewed_transcript
```

If that column is not found, the script automatically falls back to:

1. Column 15 (index 14), if present
2. Otherwise, the final column in the spreadsheet

A different column can be specified by name or index using the `-c` option.

### Usage

Basic usage:

```bash
python postprocess_tibetan_transcript.py transcripts.xlsx
```

Specify an output file:

```bash
python postprocess_tibetan_transcript.py transcripts.xlsx \
  -o transcripts_corrected.xlsx
```

Specify a column name:

```bash
python postprocess_tibetan_transcript.py transcripts.xlsx \
  -c final_reviewed_transcript
```

Specify a column index:

```bash
python postprocess_tibetan_transcript.py transcripts.xlsx \
  -c 14
```

### Output

If no output filename is supplied, the script automatically creates one by appending `_corrected` to the original filename.

Examples:

| Input | Output |
|---------|---------|
| `transcripts.csv` | `transcripts_corrected.csv` |
| `transcripts.xlsx` | `transcripts_corrected.xlsx` |

---
## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/pagantibet/HTR/blob/main/LICENSE) file for details.

---
<table>
  <tr>
    <td width="47%">
      <sub>This work was partially funded by the European Union (ERC, Pagan Tibet, 101097364). 
      Views and opinions expressed are however those of the author(s) only and do not 
      necessarily reflect those of the European Union or the European Research Council 
      Executive Agency. Neither the European Union nor the granting authority can be 
      held responsible for them.</sub>
    </td>
    <td width="53%" align="center" valign="middle">
      <img src="https://erc.europa.eu/sites/default/files/2025-08/LOGO_ERC-FLAG_EU.png" alt="ERC" height="60">
      &nbsp;&nbsp;
      <img src="https://www.crcao.fr/assets/images/logo-crcao.png" alt="CRACO" height="60">
      &nbsp;&nbsp;
      <img src="https://www.crcao.fr/uploads/2026/06/logo_ephe_psl_rvb_blanc_cadre-421x500.png" alt="EPHE" height="60">
      &nbsp;&nbsp;
      <img src="https://www.cam.ac.uk/sites/default/files/secondary-logo-stacked.png" alt="Cambridge University" height="65">
    </td>
  </tr>
</table>

