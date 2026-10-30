# coding: UTF-8
import sys
import os

def extract_peak(input_file, output_file):
    current_chr = None
    current_start = None
    current_end = None
    current_max_delta = None
    current_mind_pos = None
    current_a_bulk = None
    current_b_bulk = None

    with open(input_file, 'r') as file, open(output_file, 'w') as out_file:
        for line in file:
            fields = line.strip().split('\t')
            chr_name = fields[0]
            mind_position = int(fields[1])
            start_position = int(fields[2])
            end_position = int(fields[3])
            a_bulk = float(fields[4])
            b_bulk = float(fields[5])
            delta_snp_average = float(fields[6])

            if chr_name != current_chr:
                if current_chr is not None:
                    adjusted_start = max(0, current_start)
                    out_file.write(f"{current_chr}\t{adjusted_start}\t{current_end}\t{current_mind_pos}\t{current_a_bulk}\t{current_b_bulk}\t{current_max_delta}\n")

                current_chr = chr_name
                current_start = start_position
                current_end = end_position
                current_max_delta = delta_snp_average
                # mind_position を start～end の範囲に制限
                current_mind_pos = min(max(mind_position, start_position), end_position)
                current_a_bulk = a_bulk
                current_b_bulk = b_bulk
            else:
                if start_position <= current_end:
                    if delta_snp_average > current_max_delta:
                        current_max_delta = delta_snp_average
                        # mind_position を start～end の範囲に制限
                        current_mind_pos = min(max(mind_position, start_position), end_position)
                        current_a_bulk = a_bulk
                        current_b_bulk = b_bulk
                    current_start = min(current_start, start_position)
                    current_end = max(current_end, end_position)
                else:
                    adjusted_start = max(0, current_start)
                    out_file.write(f"{current_chr}\t{adjusted_start}\t{current_end}\t{current_mind_pos}\t{current_a_bulk}\t{current_b_bulk}\t{current_max_delta}\n")

                    current_start = start_position
                    current_end = end_position
                    current_max_delta = delta_snp_average
                    # mind_position を start～end の範囲に制限
                    current_mind_pos = min(max(mind_position, start_position), end_position)
                    current_a_bulk = a_bulk
                    current_b_bulk = b_bulk

        if current_chr is not None:
            adjusted_start = max(0, current_start)
            out_file.write(f"{current_chr}\t{adjusted_start}\t{current_end}\t{current_mind_pos}\t{current_a_bulk}\t{current_b_bulk}\t{current_max_delta}\n")

    os.remove(input_file)

def extract_peak_region(output_folder, Abulk_name, Bbulk_name):
    input_95 = os.path.join(output_folder, f"{Abulk_name}-{Bbulk_name}_95_sim_snp.txt")
    output_95 = os.path.join(output_folder, f"{Abulk_name}-{Bbulk_name}_95_peak.txt")
    extract_peak(input_95, output_95)

    input_99 = os.path.join(output_folder, f"{Abulk_name}-{Bbulk_name}_99_sim_snp.txt")
    output_99 = os.path.join(output_folder, f"{Abulk_name}-{Bbulk_name}_99_peak.txt")
    extract_peak(input_99, output_99)

def main(output_folder, Abulk_name, Bbulk_name):
    extract_peak_region(output_folder, Abulk_name, Bbulk_name)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <output_folder> <Abulk_name> <Bbulk_name>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
