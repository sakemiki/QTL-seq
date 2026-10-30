# coding: UTF-8
import sys
import os
import shutil
import pandas as pd
import numpy as np


def load_data(filepath, columns):
    data = pd.read_csv(filepath, sep='\t', header=None)
    data.columns = columns
    return data


def load_confidence_interval(output_folder):
    """confidence_interval.txt を読み込み、(Chr, start, end) をキーに
    95%信頼区間 (average_low_95, average_high_95) を引けるdictを返す。"""
    ci_path = os.path.join(output_folder, 'confidence_interval.txt')

    ci_columns = [
        'Chr', 'midpoint', 'start', 'end',
        'average_low_99', 'average_high_99',
        'average_low_95', 'average_high_95',
    ]

    ci_data = load_data(ci_path, ci_columns)

    ci_dict = {}
    for _, row in ci_data.iterrows():
        try:
            low_95 = float(row['average_low_95'])
            high_95 = float(row['average_high_95'])
        except (TypeError, ValueError):
            continue
        key = (row['Chr'], int(row['start']), int(row['end']))
        ci_dict[key] = (low_95, high_95)

    return ci_dict


def average_snpindex(output_folder, fai_file, filter_depth, window_size, step_size):
    snpindex_txt = os.path.join(output_folder, 'snpindex_merge.txt')

    snpindex_columns = [
        'Chr', 'Position', 'P1_SNP', 'P1_depth', 'P2_SNP', 'P2_depth',
        'Bulk_A_SNP', 'Bulk_A_depth'
    ]

    snpindex_data = load_data(snpindex_txt, snpindex_columns)
    ci_dict = load_confidence_interval(output_folder)

    # 染色体ごとの最大SNP位置
    chr_max_positions = snpindex_data.groupby('Chr')['Position'].max().to_dict()

    output_file_name = "average_snp_index_per_window.txt"
    output_path = os.path.join(output_folder, output_file_name)

    with open(output_path, 'w') as d:
        for chr_name, max_position in chr_max_positions.items():

            start = -window_size // 2

            while True:

                end = start + window_size
                midpoint = start + window_size // 2

                # =========================
                # ★ ここが今回の最重要修正
                # =========================
                if midpoint > max_position:
                    break

                # SNP抽出
                mask = (
                    (snpindex_data['Position'] >= max(0, start)) &
                    (snpindex_data['Position'] < end) &
                    (snpindex_data['Chr'] == chr_name)
                )

                filtered_data = snpindex_data.loc[mask]
                snp_count = filtered_data.shape[0]

                # SNP数チェック
                if snp_count >= filter_depth:
                    avgA = np.round(filtered_data['Bulk_A_SNP'].mean(), 3)
                elif snp_count > 0:
                    # SNP数がfilter_depth未満でも、そのwindowの
                    # 95%信頼区間を超えている場合は除外せず全SNPを対象にする
                    candidate_avgA = filtered_data['Bulk_A_SNP'].mean()
                    ci = ci_dict.get((chr_name, start, end))

                    if ci is not None:
                        low_95, high_95 = ci
                        if candidate_avgA < low_95 or candidate_avgA > high_95:
                            avgA = np.round(candidate_avgA, 3)
                        else:
                            avgA = 'N/A'
                    else:
                        avgA = 'N/A'
                else:
                    avgA = 'N/A'

                d.write(f"{chr_name}\t{midpoint}\t{start}\t{end}\t{avgA}\n")

                start += step_size

    shutil.move(output_path, output_path)


def main(output_folder, fai_file, filter_depth, window_size, step_size):
    average_snpindex(output_folder, fai_file, filter_depth, window_size, step_size)


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python script.py <output_folder> <fai_file> <filter_depth> <window_size> <step_size>")
    else:
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))