# coding: UTF-8
import os
import sys
import math
import matplotlib.pyplot as plt
import numpy as np


def load_chromosomes(fai_file):
    with open(fai_file, 'r') as file:
        chr_names = [line.split('\t')[0] for line in file]
    return chr_names


def load_fai_max_length(fai_file):
    """faiファイルから全染色体の最大長(Mb)を返す"""
    max_len = 0
    with open(fai_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                length = int(line.split('\t')[1])
                if length > max_len:
                    max_len = length
    return max_len / 1e6




def load_fai_max_length_for_names(fai_file, name_list):
    """指定した名前リストの中で最大の染色体長(Mb)を返す"""
    name_set = set(name_list)
    max_len = 0
    with open(fai_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if parts[0] in name_set:
                length = int(parts[1])
                if length > max_len:
                    max_len = length
    return max_len / 1e6


def split_into_parts(name_list, max_per_part=20):
    """リストをmax_per_part個ずつのチャンクに分割して返す"""
    return [name_list[i:i + max_per_part] for i in range(0, len(name_list), max_per_part)]


def load_data(filepath):
    full_path = os.path.join(filepath)
    data = []
    with open(full_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                fields = line.split('\t')
                data.append(fields)
    return data


def calc_x_axis_max(max_mb):
    """
    最長染色体の長さ(Mb)から横軸の最大値を計算する。
    - 5の倍数に切り上げる
    - ただし、切り上げ後の値と実際の最大値の差が2Mb未満の場合は
      さらに+5Mbする（例: 73.49Mb → 75は近すぎる → 80Mb）
    """
    rounded = math.ceil(max_mb / 5) * 5
    if rounded - max_mb < 2:
        rounded += 5
    return rounded


def create_and_save_plots(data, average_list, sim99_low_list, sim99_high_list, sim95_low_list, sim95_high_list, file_name, color, y_axis_line=0.5, chr_names=None, num_rows=1, num_cols=2, output_folder="", x_axis_max=80, label=""):
    if chr_names is None:
        chr_names = []
    fig_width = 8
    fig_height = num_rows * 2
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(fig_width, fig_height), sharex=False, sharey=False)
    plt.subplots_adjust(wspace=0.5, hspace=0.8)
    axes = axes.flatten()

    # faiから渡された横軸最大値をそのまま使用
    all_max_position = x_axis_max

    if num_rows * num_cols > len(chr_names):
        for ax in axes[len(chr_names):]:
            ax.remove()
    axes = axes[:len(chr_names)]

    for i, chr_name in enumerate(chr_names):
        positions = [x[1] / 1e6 for x in data if x[0] == chr_name]
        values = [x[2] for x in data if x[0] == chr_name]
        midpoints = [float(x[1]) / 1e6 for x in average_list if x[0] == chr_name]
        avg_values = [x[2] for x in average_list if x[0] == chr_name]
        sim99_low = [x[2] for x in sim99_low_list if x[0] == chr_name]
        sim99_high = [x[2] for x in sim99_high_list if x[0] == chr_name]
        sim95_low = [x[2] for x in sim95_low_list if x[0] == chr_name]
        sim95_high = [x[2] for x in sim95_high_list if x[0] == chr_name]

        axes[i].plot(positions, values, '.', markersize=1, color=color)
        axes[i].plot(midpoints, avg_values, '-', color='red', linewidth=0.8)
        axes[i].plot(midpoints, sim99_low, '-', color='orange', linewidth=0.8)
        axes[i].plot(midpoints, sim99_high, '-', color='orange', linewidth=0.8)
        axes[i].plot(midpoints, sim95_low, '-', color='chartreuse', linewidth=0.8)
        axes[i].plot(midpoints, sim95_high, '-', color='chartreuse', linewidth=0.8)
        axes[i].set_title(f'{chr_name}', fontsize=9)
        axes[i].set_xlabel('chr position(Mb)', fontsize=9)
        axes[i].set_ylabel('SNP-index', fontsize=9)
        axes[i].set_yticks(np.arange(0, 1.1, 0.2))
        axes[i].set_xticks(np.arange(0, all_max_position + 1, 5))  # +1で最大値tickを確実に含める
        axes[i].set_xlim([0, all_max_position])
        axes[i].tick_params(axis='x', labelsize=4)
        axes[i].tick_params(axis='y', labelsize=4)
        axes[i].axhline(y=y_axis_line, color='cornflowerblue', linestyle='--', linewidth=0.7)
        axes[i].spines['top'].set_visible(False)
        axes[i].spines['right'].set_visible(False)

    fig.tight_layout()
    if label:
        fig.text(0.01, 0.99, label, fontsize=9, fontweight='bold',
                 va='top', ha='left', transform=fig.transFigure)
    plt.savefig(os.path.join(output_folder, file_name + '.png'), dpi=300)
    plt.close()


def plotting_main(output_folder, Abulk_name, fai_file, abulk_color, side):

    snpindex_txt = os.path.join(output_folder, 'snpindex_merge.txt')
    average_snp_index_per_window = os.path.join(output_folder, "average_snp_index_per_window.txt")
    confidence_interval = os.path.join(output_folder, 'confidence_interval.txt')

    # faiの全配列名をそのまま取得（分類なし）
    all_names = load_chromosomes(fai_file)
    num_cols = int(side)

    snpindex_data = load_data(snpindex_txt)
    average_snp_index_data = load_data(average_snp_index_per_window)
    PP_snpindex_F2_20_sim_data = load_data(confidence_interval)

    Abulk_snpindex = [[row[0], int(row[1]), float(row[6])] for row in snpindex_data]

    average_snp_index_Abulk_list = [
        [row[0], int(row[1]), float(row[4])]
        for row in average_snp_index_data if row[4] != 'N/A'
    ]

    average_99low = [
        [row[0], int(row[1]), float(row[4])]
        for row in PP_snpindex_F2_20_sim_data if row[4] != 'N/A'
    ]
    average_99high = [
        [row[0], int(row[1]), float(row[5])]
        for row in PP_snpindex_F2_20_sim_data if row[5] != 'N/A'
    ]
    average_95low = [
        [row[0], int(row[1]), float(row[6])]
        for row in PP_snpindex_F2_20_sim_data if row[6] != 'N/A'
    ]
    average_95high = [
        [row[0], int(row[1]), float(row[7])]
        for row in PP_snpindex_F2_20_sim_data if row[7] != 'N/A'
    ]

    # 全配列名を20個ずつのパートに分割して出力
    parts = split_into_parts(all_names, max_per_part=20)
    total_parts = len(parts)

    for part_idx, name_chunk in enumerate(parts, start=1):
        part_label = f"_part{part_idx}" if total_parts > 1 else ""
        chunk_max_mb = load_fai_max_length_for_names(fai_file, name_chunk)
        x_axis_max = calc_x_axis_max(chunk_max_mb)
        num_rows = math.ceil(len(name_chunk) / num_cols)

        create_and_save_plots(
            Abulk_snpindex, average_snp_index_Abulk_list,
            average_99low, average_99high, average_95low, average_95high,
            f"{Abulk_name}{part_label}", abulk_color,
            chr_names=name_chunk, num_rows=num_rows, num_cols=num_cols,
            output_folder=output_folder, x_axis_max=x_axis_max,
            label=Abulk_name
        )


def main(output_folder, Abulk_name, fai_file, abulk_color, side):
    plotting_main(output_folder, Abulk_name, fai_file, abulk_color, side)


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            "Usage: python script.py <output_folder> <Abulk_name> <fai_file> "
            "<abulk_color> <side>"
        )
    else:
        main(
            sys.argv[1], sys.argv[2], sys.argv[3],
            sys.argv[4], int(sys.argv[5])
        )