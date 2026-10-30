# coding: UTF-8
import sys
import os
import pandas as pd

COLUMN_NAMES = ['chromosome', 'position', 'P1_snp', 'P1_depth', 'P2_snp', 'P2_depth', 'Bulk_A_snp', 'Bulk_A_depth']
COLUMN_DTYPES = {
    'chromosome': str, 'position': int, 'P1_snp': float, 'P1_depth': int,
    'P2_snp': float, 'P2_depth': int, 'Bulk_A_snp': float, 'Bulk_A_depth': int,
}

SNPINDEX_SUFFIX = '_snpindex.txt'
NO_SELECT_SUFFIX = '_snpindex_no_select.txt'  # PP_singele_snpindex.py の出力名と一致させる


def read_fai_file(fai_file):
    with open(fai_file, 'r') as f:
        chromosomes = [line.split('\t')[0] for line in f if line.strip()]
    return chromosomes


def find_result_files(output_folder, suffix, exclude_suffix=None):
    """
    output_folder 内で suffix に一致するファイルを集める。
    exclude_suffix を指定すると、それに一致するファイルは除外する。
    """
    files = []
    for file in os.listdir(output_folder):
        if not file.endswith(suffix):
            continue
        if exclude_suffix is not None and file.endswith(exclude_suffix):
            continue
        files.append(os.path.join(output_folder, file))
    return files


def read_result_files(files):
    dataframes = []
    for file in files:
        df = pd.read_csv(
            file, sep='\t', header=None,
            names=COLUMN_NAMES,
            dtype=COLUMN_DTYPES,
        )
        dataframes.append(df)
    return pd.concat(dataframes, ignore_index=True)


def merge_and_sort(output_folder, chromosome_order, output_file, suffix, exclude_suffix=None):
    files = find_result_files(output_folder, suffix, exclude_suffix)

    if not files:
        print(f"WARNING: '{suffix}' に一致するファイルが見つからなかったため、{output_file} は作成しません。")
        return

    combined_df = read_result_files(files)

    combined_df['chromosome'] = pd.Categorical(combined_df['chromosome'], categories=chromosome_order, ordered=True)
    sorted_df = combined_df.sort_values(by=['chromosome', 'position']).reset_index(drop=True)

    sorted_df.to_csv(output_file, sep='\t', index=False, header=False)

    for file in files:
        try:
            os.remove(file)
            print(f"Deleted file: {file}")
        except OSError as e:
            print(f"Error deleting file {file}: {e}")


def main(output_folder, fai_file):
    chromosome_order = read_fai_file(fai_file)

    snpindex_output = os.path.join(output_folder, 'snpindex_merge.txt')
    no_select_output = os.path.join(output_folder, 'snpindex_no_select_merge.txt')

    # 選抜されたSNP (*_snpindex.txt, ただし *_snpindex_no_select.txt は除く) をマージ
    merge_and_sort(
        output_folder, chromosome_order, snpindex_output,
        suffix=SNPINDEX_SUFFIX, exclude_suffix=NO_SELECT_SUFFIX,
    )

    # 選抜されなかったSNP (*_snpindex_no_select.txt) をマージ
    merge_and_sort(
        output_folder, chromosome_order, no_select_output,
        suffix=NO_SELECT_SUFFIX,
    )


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 PP_singele_snpindex_marge.py <output_folder> <fai_file>")
        sys.exit(1)

    output_folder = sys.argv[1]
    fai_file = sys.argv[2]

    if not os.path.isdir(output_folder):
        print(f"Error: {output_folder} is not a valid directory.")
        sys.exit(1)

    if not os.path.isfile(fai_file):
        print(f"Error: {fai_file} is not a valid file.")
        sys.exit(1)

    main(output_folder, fai_file)