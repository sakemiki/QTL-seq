# coding: UTF-8
import sys
import os
def load_chromosome_lengths(fai_path):
    chr_lengths = {}
    with open(fai_path, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            chr_name = parts[0]
            chr_len = int(parts[1])
            chr_lengths[chr_name] = chr_len
    return chr_lengths

def extract_simulation_data(output_folder, Abulk_name, fai_path):
    chr_lengths = load_chromosome_lengths(fai_path)
    input_path = os.path.join(output_folder, 'position_average_sim_list.txt')

    output_95_path = os.path.join(output_folder, f"{Abulk_name}_95_sim_snp.txt")
    output_99_path = os.path.join(output_folder, f"{Abulk_name}_99_sim_snp.txt")

    with open(input_path, 'r') as infile, \
         open(output_95_path, 'w') as out_95, \
         open(output_99_path, 'w') as out_99:

        for line in infile:
            line = line.strip()
            fields = line.split("\t")
            if 'N/A' not in fields:
                chr_name = fields[0]
                mind_position = int(fields[1])
                Abulk_snp_average = float(fields[2])
                low_99 = float(fields[3])
                high_99 = float(fields[4])
                low_95 = float(fields[5])
                high_95 = float(fields[6])

                start_position = str(mind_position - 1000000)
                chr_max_length = chr_lengths.get(chr_name, mind_position + 1000000)
                end_position = min(chr_max_length, mind_position + 1000000)
                avg_str = str(Abulk_snp_average)
                pos_str = str(mind_position)
                output_line = f"{chr_name}\t{pos_str}\t{start_position}\t{end_position}\t{avg_str}\n"

                # 95%外の行を書き出し
                if (Abulk_snp_average < low_95) or (Abulk_snp_average > high_95):
                    out_95.write(output_line)

                # 99%外の行を書き出し
                if (Abulk_snp_average < low_99) or (Abulk_snp_average > high_99):
                    out_99.write(output_line)

    os.remove(input_path)

def main(output_folder, Abulk_name, fai_path):
    extract_simulation_data(output_folder, Abulk_name, fai_path)

if __name__ == "__main__":
    if len(sys.argv) == 4:
        output_folder = sys.argv[1]
        Abulk_name = sys.argv[2]
        fai_file=sys.argv[3]
        main(output_folder, Abulk_name, fai_file)
    else:
        print("Usage: python script.py <output_folder> <Abulk_name>")
