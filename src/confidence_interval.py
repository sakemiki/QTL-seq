# coding: UTF-8
import sys
import os
import pandas as pd
import numpy as np


def load_data(filepath, columns):
    data = pd.read_csv(filepath, sep='\t', header=None)
    data.columns = columns
    return data


def confidence_interval_main(output_folder, fai_file, window_size, step_size, filter_depth): 

    snpindex_columns = [
        'Chr', 'Position', 'P1_SNP', 'P1_depth', 'P2_SNP', 'P2_depth', 'F1_SNP', 'F1_depth',
        'Bulk_A_SNP', 'Bulk_A_depth', 'Bulk_B_SNP', 'Bulk_B_depth', 'Delta_SNP',
        'depth', 'low_99', 'high_99', 'low_95', 'high_95', 'delta_99low', 'delta_99high', 
        'delta_95low', 'delta_95high'
    ]

    snpindex_txt = os.path.join(output_folder, 'sim_snp.txt')
    confidence_interval = os.path.join(output_folder, 'confidence_interval.txt')

    snpindex_data = load_data(snpindex_txt, snpindex_columns)

    # 染色体ごとの最大SNP位置
    chr_max_positions = snpindex_data.groupby('Chr')['Position'].max().to_dict()

    with open(confidence_interval, 'w') as d:
        for chr_name, max_position in chr_max_positions.items():

            start = -window_size // 2

            while True:

                end = start + window_size
                midpoint = start + window_size // 2

                # =========================
                # ★ 最重要修正
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

                # 値取得
                window_low_99 = filtered_data['low_99']
                window_high_99 = filtered_data['high_99']
                window_low_95 = filtered_data['low_95']
                window_high_95 = filtered_data['high_95']
                window_delta_99low = filtered_data['delta_99low']
                window_delta_99high = filtered_data['delta_99high']
                window_delta_95low = filtered_data['delta_95low']
                window_delta_95high = filtered_data['delta_95high']

                # フィルタ
                if len(filtered_data) >= filter_depth:
                    average_low_99 = np.round(window_low_99.mean(), 3)
                    average_high_99 = np.round(window_high_99.mean(), 3)
                    average_low_95 = np.round(window_low_95.mean(), 3)
                    average_high_95 = np.round(window_high_95.mean(), 3)
                    average_delta_99low = np.round(window_delta_99low.mean(), 3)
                    average_delta_99high = np.round(window_delta_99high.mean(), 3)
                    average_delta_95low = np.round(window_delta_95low.mean(), 3)
                    average_delta_95high = np.round(window_delta_95high.mean(), 3)
                else:
                    average_low_99 = 'N/A'
                    average_high_99 = 'N/A'
                    average_low_95 = 'N/A'
                    average_high_95 = 'N/A'
                    average_delta_99low = 'N/A'
                    average_delta_99high = 'N/A'
                    average_delta_95low = 'N/A'
                    average_delta_95high = 'N/A'

                d.write(
                    f"{chr_name}\t{midpoint}\t{start}\t{end}\t"
                    f"{average_low_99}\t{average_high_99}\t"
                    f"{average_low_95}\t{average_high_95}\t"
                    f"{average_delta_99low}\t{average_delta_99high}\t"
                    f"{average_delta_95low}\t{average_delta_95high}\n"
                )

                start += step_size

    os.remove(snpindex_txt)


def main(output_folder, fai_file, window_size, step_size, filter_depth):
    confidence_interval_main(output_folder, fai_file, window_size, step_size, filter_depth)


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python script.py <output_folder> <fai_file> <window_size> <step_size> <filter_depth>")
        sys.exit(1)

    output_folder = sys.argv[1]
    fai_file = sys.argv[2]
    window_size = int(sys.argv[3])
    step_size = int(sys.argv[4])
    filter_depth = int(sys.argv[5])

    main(output_folder, fai_file, window_size, step_size, filter_depth)