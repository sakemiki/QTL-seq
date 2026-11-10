#!/bin/bash
# QTL-seq GUI for Windows (WSL) - installer
# Usage (in the Ubuntu terminal, inside the extracted folder):
#     bash install.sh
set -e

# Move to the folder that contains this script
cd "$(dirname "$0")"

APP="QTL-seq_GUI_ver1_02_windows"
DEST="$HOME/QTLseqGUI"

if [ ! -f "./$APP" ]; then
    echo "Error: $APP was not found in this folder."
    echo "Please run this script inside the extracted folder."
    exit 1
fi

echo "[1/2] Installing SAMtools and BCFtools..."
sudo apt-get update
sudo apt-get install -y samtools bcftools

echo "[2/2] Installing QTL-seq GUI to $DEST ..."
mkdir -p "$DEST"
cp "./$APP" "$DEST/"
chmod +x "$DEST/$APP"

echo ""
echo "Installation completed."
echo "  SAMtools : $(command -v samtools)"
echo "  BCFtools : $(command -v bcftools)"
echo "  QTL-seq GUI : $DEST/$APP"
echo ""
echo "You can now start QTL-seq GUI by double-clicking QTL-seq_GUI.exe."
