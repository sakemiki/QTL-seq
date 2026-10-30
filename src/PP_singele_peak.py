# coding: UTF-8
import sys
import os

def extract_peak(input_path, output_path):
    current_chr = None
    current_start = None
    current_end = None
    current_max_a_bulk = None
    current_mind_pos = None

    with open(input_path, 'r') as file, open(output_path, 'w') as out_file:
        for line in file:
            fields = line.strip().split('\t')
            chr_name = fields[0]
            mind_position = int(fields[1])
            start_position = int(fields[2])
            end_position = int(fields[3])
            a_bulk = float(fields[4])

            if chr_name != current_chr:
                if current_chr is not None:
                    adjusted_start = max(0, current_start)
                    out_file.write(f"{current_chr}\t{adjusted_start}\t{current_end}\t{current_mind_pos}\t{current_max_a_bulk}\n")
                current_chr = chr_name
                current_start = start_position
                current_end = end_position
                current_max_a_bulk = a_bulk
                current_mind_pos = min(max(mind_position, start_position), end_position)
            else:
                if start_position <= current_end:
                    if a_bulk > current_max_a_bulk:
                        current_max_a_bulk = a_bulk
                        current_mind_pos = min(max(mind_position, start_position), end_position)
                    current_start = min(current_start, start_position)
                    current_end = max(current_end, end_position)
                else:
                    adjusted_start = max(0, current_start)
                    out_file.write(f"{chr_name}\t{adjusted_start}\t{current_end}\t{current_mind_pos}\t{current_max_a_bulk}\n")
                    current_start = start_position
                    current_end = end_position
                    current_max_a_bulk = a_bulk
                    current_mind_pos = min(max(mind_position, start_position), end_position)

        # 最終行の出力
        if current_chr is not None:
            adjusted_start = max(0, current_start)
            out_file.write(f"{current_chr}\t{adjusted_start}\t{current_end}\t{current_mind_pos}\t{current_max_a_bulk}\n")

    os.remove(input_path)


def main(output_folder, Abulk_name):
    # 95%データ処理
    input_95 = os.path.join(output_folder, f"{Abulk_name}_95_sim_snp.txt")
    output_95 = os.path.join(output_folder, f"{Abulk_name}_95_peak.txt")
    extract_peak(input_95, output_95)

    # 99%データ処理
    input_99 = os.path.join(output_folder, f"{Abulk_name}_99_sim_snp.txt")
    output_99 = os.path.join(output_folder, f"{Abulk_name}_99_peak.txt")
    extract_peak(input_99, output_99)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        output_folder = sys.argv[1]
        Abulk_name = sys.argv[2]
        main(output_folder, Abulk_name)
    else:
        print("Usage: python script.py <output_folder> <Abulk_name>")
