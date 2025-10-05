# Tibetan HTR Postprocessing Script

A Python script to clean Tibetan transcriptions in CSV or Excel files before creating Ground Truth. It automatically applies a set of corrections to normalise punctuation.

This was created as part of the PaganTibet project (pagantibet.com) at EPHE-PSL Paris, with funding from the European Union (ERC, Reconstructing the Pagan Religion of Tibet (2023-2028), 101097364). Please cite the associated article:

Griffiths, Rachael and Marieke Meelen. (forthc). Collaborative Workflows for Handwritten Text Recognition in
Under-resourced Manuscript Collections.

---

## Installation & Dependencies

Requires Python 3 and pandas. Install dependencies:

```bash
pip install pandas openpyxl
```

---

## Use

### 1. Open a Command Prompt (Windows) or Terminal (macOS/Linux), then run:
```bash
python tibetan_postprocessing.py input_HTRtranscriptions.csv
```
### 2. Optional
#### a. Specify an output file
```bash
python tibetan_postprocessing.py input_HTRtranscriptions.csv -o name_output_file.csv
```

If no `-o` is given, the processed transcripts will be saved as:

- `input_HTRtranscriptions_corrected.csv`

#### b. Process a specific column by index (0-based)
```bash
python tibetan_postprocessing.py input_HTRtranscriptions.csv -c 2
```

In the example above, the third column is selected. If a column isn't specified with `-c`, the script defaults to:

- The column named `final_reviewed_transcript`, **if it exists**.
- If that column doesn't exist:
  - **15th column**, if there are at least 15 columns
  - Otherwise, it uses the **last column**
    
## Features

The script applies the following transformations:

- Replace `༧ → ༸` only when there's space around the ༧ to avoid deleting numerals
- Remove stray  ` ྃ` and  ` ཾ` in punctuation
- Replace `༐ → ༴`
- Replace `༅༅༅ → ༄༅༅` and/or `༅༅ → ༄༅`

## Notes

- Syllables with ` ཾ` (e.g., `དཾ`) are preserved
- Works on both CSV and Excel files (`.csv`, `.xls`, `.xlsx`)

## Licence

MIT Licence
