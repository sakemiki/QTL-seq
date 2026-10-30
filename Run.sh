#!/bin/bash
# =============================================================================
# QTL-seq CUI版 実行スクリプト
#
# 使い方:
#   1. 下の「設定」欄を編集する（GUI の入力欄と同じ項目）
#   2. bash Run.sh で実行する
#
#   設定はコマンドライン引数で上書きすることもできる:
#     bash Run.sh --output /path/to/out --window-size 1000000
#   引数の一覧: bash Run.sh --help
# =============================================================================

# ----------------------------------------------------------------------------
# 設定: Enter the path to the file
# ----------------------------------------------------------------------------
OUTPUT_FOLDER="/Users/Desktop/output_folder"
SAMTOOLS="/Users/Desktop/samtools-1.XX/samtools"
BCFTOOLS="/Users/Desktop/bcftools-1.XX/bcftools"
FASTA="/Users/Desktop/test_refarence.fasta"

# ----------------------------------------------------------------------------
# 設定: Select processing details
# ----------------------------------------------------------------------------
PATTERN="P1P2"        # P1 / P1P2 / P1F1 / P1P2F1
BULK="double"         # single / double
BULK_TYPE="F2"        # RIL / F2 / BC1F1

# ----------------------------------------------------------------------------
# 設定: BAM ファイルとサンプル名
#   PATTERN / BULK で使わないもの（例: P1 のみなら P2・F1）は無視される
# ----------------------------------------------------------------------------
P1_BAM="/Users/Desktop/test_data/P1.sort.bam"
P1_NAME="P1"
P2_BAM="/Users/Desktop/test_data/P2.sort.bam"
P2_NAME="P2"
F1_BAM="/Users/Desktop/test_data/F1.sort.bam"
F1_NAME="F1"
ABULK_BAM="/Users/Desktop/test_data/Abulk.sort.bam"
ABULK_NAME="Abulk"
BBULK_BAM="/Users/Desktop/test_data/Bbulk.sort.bam"
BBULK_NAME="Bbulk"

# ----------------------------------------------------------------------------
# 設定: Enter filtering values
# ----------------------------------------------------------------------------
FILTER_DEPTH=10
WINDOW_SIZE=2000000
STEP_SIZE=50000
BULK_NUMBER=15
REMOVAL_SNPINDEX=0.3

# ----------------------------------------------------------------------------
# 設定: Graph options
#   red / blue / yellow / green / orange / purple / pink / brown / gray / black
#   など matplotlib の色名（一覧: src/color.txt）
# ----------------------------------------------------------------------------
ABULK_COLOR="green"
BBULK_COLOR="gold"
DELTA_COLOR="midnightblue"
NUMBER_OF_ROW=2

# 使用する Python（環境変数 PYTHON で変更可）
PYTHON="${PYTHON:-python3}"

# =============================================================================
# ここから下は編集不要
# =============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$PYTHON" "$SCRIPT_DIR/src/Run_CUI.py" \
    --output "$OUTPUT_FOLDER" \
    --samtools "$SAMTOOLS" \
    --bcftools "$BCFTOOLS" \
    --fasta "$FASTA" \
    --pattern "$PATTERN" \
    --bulk "$BULK" \
    --bulk-type "$BULK_TYPE" \
    --p1-bam "$P1_BAM" --p1-name "$P1_NAME" \
    --p2-bam "$P2_BAM" --p2-name "$P2_NAME" \
    --f1-bam "$F1_BAM" --f1-name "$F1_NAME" \
    --abulk-bam "$ABULK_BAM" --abulk-name "$ABULK_NAME" \
    --bbulk-bam "$BBULK_BAM" --bbulk-name "$BBULK_NAME" \
    --filter-depth "$FILTER_DEPTH" \
    --window-size "$WINDOW_SIZE" \
    --step-size "$STEP_SIZE" \
    --bulk-number "$BULK_NUMBER" \
    --removal-snpindex "$REMOVAL_SNPINDEX" \
    --abulk-color "$ABULK_COLOR" \
    --bbulk-color "$BBULK_COLOR" \
    --delta-color "$DELTA_COLOR" \
    --side "$NUMBER_OF_ROW" \
    "$@"
