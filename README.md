# Patient Data Cleaning

A Python script that cleans a messy patient records table (inconsistent formats, placeholder text, impossible values, and duplicates), then reports how much data is missing and which patients need manual review.

## How it works
1. **Placeholders become real missing values:** whitespace is stripped, and text like `"N/A"`, `"unknown"`, and empty strings are converted to `NaN`
2. **Impossible values become missing:** weights outside 20-300 kg and heights outside 50-250 cm are blanked, not guessed
3. **Text is standardized:** names in title case, blood types in upper case, and gender variants (`"F"`, `"f"`, `"female"`) mapped to one value
4. **Dates are parsed from mixed formats:** `"1962/11/02"`, `"12 Jul 1993"`, and `"1985-03-12"` all become real dates, and dates in the future become missing
5. **Phone numbers are reduced to digits only**
6. **Duplicates are removed after standardizing,** so records that only match once cleaned are caught
7. **A quality report** shows rows before and after, the percentage missing in each column, and a `needs_review` flag for patients missing any critical field

## What gets fixed (sample data)
| Problem | Example | Result |
|---------|---------|--------|
| Extra spaces and odd casing | `"  maria SILVA "` | Maria Silva |
| Placeholder text | `"N/A"`, `"unknown"`, `""` | missing |
| Inconsistent categories | `"F"`, `"f"`, `"Female"` | Female |
| Mixed date formats | `"1962/11/02"`, `"12 Jul 1993"` | proper dates |
| Impossible values | weight 0 and -1, height 999 | missing |
| Date in the future | `2090-01-01` | missing |
| Messy phone formats | `"(11) 5550-1010"` | `1155501010` |
| Duplicate patient | John Carter appears twice (P002 and P005) | one kept |

**Result:** 8 rows become 7, and 5 patients are flagged for review (P003, P004, P006, P007, P008).

## How to run
```bash
python patient_cleaning.py
```
This creates `patients_clean.csv` in the same folder when run.

## What I learned
- Turning placeholder text into real missing values with `.replace(..., np.nan)`
- Using `.where(series.between(a, b))` to blank values outside a valid range
- Standardizing categories with `.str.lower().map(dictionary)`
- Parsing messy dates with `pd.to_datetime(..., format="mixed", errors="coerce")`
- Removing non-digits with a regular expression (`\D`)
- Why the order matters: deduplicating *after* standardizing catches duplicates that look different in the raw data
- Flagging incomplete records with `.isnull().any(axis=1)`
- Calculating percent missing per column with `.isnull().mean()`
- Treating bad values as missing and flagging them for review, not guessing replacements

## Limitations
- **Educational only.** All data is fictional. Real patient data is protected by privacy laws such as HIPAA and GDPR and must never be committed to a public repository.
- The valid ranges are illustrative, not clinical standards.
- Duplicates are matched on name, birth date, and gender. That can merge two different people when information is missing, and miss the same person if a name is misspelled.
- Ambiguous dates like `03/04/2024` are read as month-first by default.
- Phone numbers are reduced to digits but not checked for length or country code.

## Dependencies
Requires pandas 2.0 or newer (for `format="mixed"`) and NumPy:
```bash
pip install "pandas>=2.0" numpy
```
