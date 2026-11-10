#!/bin/bash
# QTL-seq GUI 本体（Linux版）を WSL 内でビルドするスクリプト
# 使い方（WSL の Ubuntu で）:
#   bash /mnt/c/Users/<YourName>/Desktop/QTLseqGUI_ver2_testvaersion/build_wsl.sh
set -e

SRC="/mnt/c/Users/<YourName>/Desktop/QTLseqGUI_ver2_testvaersion"   # Windows 側のスクリプト置き場
WORK="$HOME/QTLseqGUI_build"                                       # WSL 内の作業場所（高速・権限が保たれる）
NAME="QTL-seq_GUI_ver1_02_windows"                                 # 出来上がる本体の名前

echo "[1/3] スクリプトを WSL 内にコピー: $WORK"
rm -rf "$WORK"
mkdir -p "$WORK"
cp "$SRC"/*.py "$SRC"/*_sim.txt "$WORK"/
cd "$WORK"

echo "[2/3] Python 環境 (~/myenv) を有効化"
source "$HOME/myenv/bin/activate"
python --version
pyinstaller --version
DND=$(python -c 'import tkinterdnd2,os;print(os.path.dirname(tkinterdnd2.__file__))')

echo "[3/3] PyInstaller でビルド"
pyinstaller --onefile --windowed --noconfirm \
  --hidden-import=tkinterdnd2 \
  --hidden-import=pandas \
  --hidden-import=numpy \
  --add-data "$DND:tkinterdnd2" \
  --add-data "F1_sim.txt:." \
  $(for i in $(seq 10 50); do echo --add-data "F2_${i}_sim.txt:."; done) \
  $(for i in $(seq 10 50); do echo --add-data "BC1F1_${i}_sim.txt:."; done) \
  $(for i in $(seq 10 50); do echo --add-data "RIL_${i}_sim.txt:."; done) \
  --add-data "P_singele_snpindex.py:." \
  --add-data "P_snpindex.py:." \
  --add-data "PF_singele_snpindex.py:." \
  --add-data "PF_snpindex.py:." \
  --add-data "PP_singele_snpindex.py:." \
  --add-data "PP_snpindex.py:." \
  --add-data "PPF_singele_snpindex.py:." \
  --add-data "PPF_snpindex.py:." \
  --name="$NAME" \
  Run.py

echo "完了: $WORK/dist/$NAME"
ls -la "$WORK/dist/"
