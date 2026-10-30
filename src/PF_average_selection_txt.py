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

def extract_simulation_data(output_folder, Abulk_name, Bbulk_name, fai_path):
    chr_lengths = load_chromosome_lengths(fai_path)

    position_average_sim_list = os.path.join(output_folder, 'position_average_sim_list.txt')
    sim_95_output = os.path.join(output_folder, f"{Abulk_name}-{Bbulk_name}_95_sim_snp.txt")
    sim_99_output = os.path.join(output_folder, f"{Abulk_name}-{Bbulk_name}_99_sim_snp.txt")

    with open(position_average_sim_list, 'r') as a, \
         open(sim_95_output, 'w') as b95, \
         open(sim_99_output, 'w') as b99:

        for line in a:
            line = line.strip()
            fields = line.split("\t")
            if 'N/A' not in fields:
                chr_name = fields[0]
                mind_position = int(fields[1])
                Abulk_snp_average = float(fields[2])
                Bbulk_snp_average = float(fields[3])
                delta_snp_average = float(fields[4])
                low_99 = float(fields[5])
                high_99 = float(fields[6])
                low_95 = float(fields[7])
                high_95 = float(fields[8])
                delta_low_99 = float(fields[9])
                delta_high_99 = float(fields[10])
                delta_low_95 = float(fields[11])
                delta_high_95 = float(fields[12])

                start_position = max(0, mind_position - 1000000)
                chr_max_length = chr_lengths.get(chr_name, mind_position + 1000000)
                end_position = min(chr_max_length, mind_position + 1000000)

                output_line = "\t".join([
                    chr_name, str(mind_position), str(start_position), str(end_position),
                    str(Abulk_snp_average), str(Bbulk_snp_average), str(delta_snp_average)
                ]) + "\n"

                if (delta_snp_average < delta_low_95) or (delta_snp_average > delta_high_95):
                    b95.write(output_line)

                if (delta_snp_average < delta_low_99) or (delta_snp_average > delta_high_99):
                    b99.write(output_line)
    os.remove(position_average_sim_list)

def main(output_folder=None, Abulk_name=None, Bbulk_name=None, fai_file=None):
    if output_folder is None:
        if len(sys.argv) != 5:
            print("Usage: python script.py <output_folder> <Abulk_name> <Bbulk_name> <fai_file>")
            return
        output_folder = sys.argv[1]
        Abulk_name = sys.argv[2]
        Bbulk_name = sys.argv[3]
        fai_file = sys.argv[4]

    extract_simulation_data(output_folder, Abulk_name, Bbulk_name, fai_file)

if __name__ == "__main__":
    main()

