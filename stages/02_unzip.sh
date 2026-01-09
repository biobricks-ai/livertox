#!/usr/bin/env bash

# Script to extract LiverTox archive

set -euo pipefail

localpath=$(pwd)
downloadpath="$localpath/download"
rawpath="$localpath/raw"

mkdir -p "$rawpath"

echo "Extracting LiverTox archive..."
tar -xzf "$downloadpath/livertox_NBK547852.tar.gz" -C "$rawpath"

echo "Extraction complete."
find "$rawpath" -type f | head -20 || true
