# LiverTox

LiverTox is a clinical and research database maintained by the National Institute of Diabetes and Digestive and Kidney Diseases (NIDDK). It contains information about drug-induced liver injury (DILI) for over 1,000 medications, including prescription and over-the-counter drugs, herbals, and dietary supplements.

## Data Source

- **Source**: NCBI Bookshelf / NIDDK
- **URL**: https://www.ncbi.nlm.nih.gov/books/NBK547852/
- **FTP**: https://ftp.ncbi.nlm.nih.gov/pub/litarch/29/31/
- **License**: Public Domain (US Government Work)

## Contents

The database includes:
- Drug/compound names
- Hepatotoxicity information
- Likelihood scores for causing liver injury
- Mechanisms of hepatotoxicity
- Clinical outcomes and management
- Case reports
- References

## Output Files

| File | Description |
|------|-------------|
| `brick/livertox.parquet` | Main dataset with drug hepatotoxicity information |

## Usage

```r
# R
biobricks::install_brick("livertox")
biobricks::brick_pull("livertox")
livertox <- biobricks::brick_load("livertox")
```

```python
# Python
import biobricks as bb
bb.install("livertox")
livertox = bb.load("livertox")
```

## Schema

| Column | Description |
|--------|-------------|
| source_file | Original XML filename |
| drug_name | Name of the drug or compound |
| overview | General overview of the drug |
| hepatotoxicity | Description of hepatotoxic effects |
| likelihood_score | Likelihood of causing DILI (A-E scale) |
| mechanism | Mechanism of hepatotoxicity |
| outcome_and_management | Clinical outcomes and treatment |
| case_reports | Summary of case reports |
| references | Key references |

## Citation

LiverTox: Clinical and Research Information on Drug-Induced Liver Injury [Internet]. Bethesda (MD): National Institute of Diabetes and Digestive and Kidney Diseases; 2012-.
