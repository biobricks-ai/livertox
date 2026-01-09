#!/usr/bin/env bash

# Script to download LiverTox data from NCBI FTP
# Source: https://www.ncbi.nlm.nih.gov/books/NBK547852/

set -euo pipefail

localpath=$(pwd)
echo "Local path: $localpath"

# Create download directory
downloadpath="$localpath/download"
mkdir -p "$downloadpath"

# LiverTox FTP URL
LIVERTOX_URL="https://ftp.ncbi.nlm.nih.gov/pub/litarch/29/31/livertox_NBK547852.tar.gz"

echo "Downloading LiverTox database..."
wget -nv -O "$downloadpath/livertox_NBK547852.tar.gz" "$LIVERTOX_URL"

echo "Download complete."
ls -lh "$downloadpath"
