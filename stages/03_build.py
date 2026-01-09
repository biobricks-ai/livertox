#!/usr/bin/env python3
"""
Build script to parse LiverTox XML files and convert to Parquet format.
LiverTox contains drug-induced liver injury (DILI) information for 1000+ medications.
"""

import os
import xml.etree.ElementTree as ET
from pathlib import Path
import pandas as pd
import re
from glob import glob

def extract_text(element):
    """Recursively extract text from an XML element."""
    if element is None:
        return ""
    text = element.text or ""
    for child in element:
        text += extract_text(child)
        if child.tail:
            text += child.tail
    return text.strip()

def parse_livertox_xml(xml_file):
    """Parse a single LiverTox XML file and extract key information."""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Extract metadata
        record = {
            'source_file': os.path.basename(xml_file),
            'drug_name': '',
            'overview': '',
            'hepatotoxicity': '',
            'likelihood_score': '',
            'mechanism': '',
            'outcome_and_management': '',
            'case_reports': '',
            'references': ''
        }

        # Find the book title/drug name
        title_elem = root.find('.//book-title')
        if title_elem is not None:
            record['drug_name'] = extract_text(title_elem)

        # Find article title if no book title
        if not record['drug_name']:
            art_title = root.find('.//article-title')
            if art_title is not None:
                record['drug_name'] = extract_text(art_title)

        # Extract sections by title
        for sec in root.findall('.//sec'):
            title_elem = sec.find('title')
            if title_elem is not None:
                title = extract_text(title_elem).lower()
                content = extract_text(sec)

                if 'overview' in title:
                    record['overview'] = content
                elif 'hepatotoxicity' in title:
                    record['hepatotoxicity'] = content
                elif 'likelihood' in title or 'score' in title:
                    record['likelihood_score'] = content
                elif 'mechanism' in title:
                    record['mechanism'] = content
                elif 'outcome' in title or 'management' in title:
                    record['outcome_and_management'] = content
                elif 'case' in title:
                    record['case_reports'] = content

        # Extract references
        refs = root.findall('.//ref')
        ref_texts = []
        for ref in refs:
            ref_texts.append(extract_text(ref))
        record['references'] = ' | '.join(ref_texts[:10])  # Limit to first 10

        return record
    except Exception as e:
        print(f"Error parsing {xml_file}: {e}")
        return None

def main():
    raw_path = Path("raw")
    brick_path = Path("brick")
    brick_path.mkdir(exist_ok=True)

    # Find all XML files
    xml_files = list(raw_path.rglob("*.xml"))
    print(f"Found {len(xml_files)} XML files")

    if not xml_files:
        print("No XML files found, looking for nxml files...")
        xml_files = list(raw_path.rglob("*.nxml"))
        print(f"Found {len(xml_files)} NXML files")

    # Parse all files
    records = []
    for xml_file in xml_files:
        record = parse_livertox_xml(xml_file)
        if record and record['drug_name']:
            records.append(record)

    print(f"Successfully parsed {len(records)} drug records")

    if records:
        # Create DataFrame and save as Parquet
        df = pd.DataFrame(records)
        output_file = brick_path / "livertox.parquet"
        df.to_parquet(output_file, index=False)
        print(f"Saved {len(df)} records to {output_file}")
        print(f"Columns: {list(df.columns)}")
        print(df.head())
    else:
        print("No records parsed - creating empty placeholder")
        df = pd.DataFrame(columns=['drug_name', 'hepatotoxicity', 'likelihood_score'])
        df.to_parquet(brick_path / "livertox.parquet", index=False)

if __name__ == "__main__":
    main()
