# coding: UTF-8
import sys
import os
import re
import math

def parse_size(size_str):
    size_str = size_str.strip().upper()
    if size_str.endswith('GB'):
        return float(size_str[:-2]) * 1000
    elif size_str.endswith('G'):
        return float(size_str[:-1]) * 1000
    elif size_str.endswith('MB'):
        return float(size_str[:-2])
    elif size_str.endswith('M'):
        return float(size_str[:-1])
    elif size_str.endswith('KB'):
        return float(size_str[:-2]) / 1000
    elif size_str.endswith('K'):
        return float(size_str[:-1]) / 1000
    elif size_str.endswith('B'):
        return float(size_str[:-1]) / (1024 * 1024)
    else:
        return float(size_str)

def main(output_folder, fai_file, samtools, P1_name, Abulk_name, Bbulk_name):
    split_script_path = os.path.join(output_folder, 'bam_fai_sequence.sh')
    index_script_path = os.path.join(output_folder, 'bam_fai_sequence_index.sh')
    bam_file_data_volume_txt = os.path.join(output_folder, "bam_file_data_volume.txt")
    chrom_lengths = {}

    with open(fai_file, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            chrom_lengths[parts[0]] = int(parts[1])

    fai_chr_names = list(chrom_lengths.keys())
    should_split_all = False
    files_to_split = []

    with open(bam_file_data_volume_txt, 'r') as file:
        for line in file:
            bam_name, size, bam_path = line.strip().split('\t')
            size_mb = parse_size(size)
            files_to_split.append((bam_name, bam_path, size_mb))
            if size_mb > 500:
                should_split_all = True

    if should_split_all:
        num_parts = math.ceil(max(size_mb for _, _, size_mb in files_to_split) / 500)
        num_parts_file = os.path.join(output_folder, 'num_parts.txt')
        with open(num_parts_file, 'w') as f:
            f.write(str(num_parts))

        with open(split_script_path, 'w') as split_script, open(index_script_path, 'w') as index_script:
            for bam_name, bam_path, _ in files_to_split:
                match = re.search(rf"^({P1_name}|{Abulk_name}|{Bbulk_name})_(.+?)\.bam$", bam_name)
                if match:
                    sample_name, candidate_chr = match.groups()
                    matched_chrs = [chr_name for chr_name in fai_chr_names if chr_name in candidate_chr]

                    if matched_chrs:
                        chromosome = max(matched_chrs, key=len)
                        length = chrom_lengths[chromosome]
                        part_size = length // num_parts

                        for part in range(num_parts):
                            start = part * part_size + 1
                            end = (part + 1) * part_size if part < num_parts - 1 else length
                            output_bam = f"{sample_name}_{chromosome}__part{part+1}.bam"
                            output_bam_path = os.path.join(output_folder, output_bam)

                            split_script.write(
                                f"{samtools} view -b {bam_path} {chromosome}:{start}-{end} -o {output_bam_path}\n"
                            )
                            index_script.write(
                                f"{samtools} index {output_bam_path}\n"
                            )
                    else:
                        print(f"⚠️ Warning: '{candidate_chr}' does not match any chromosome in {fai_file}")     
    else:
        print("No files over 500MB, no script generated.")
    os.remove(bam_file_data_volume_txt)

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: python script.py <output_folder> <fai_file> <samtools> <P1_name> <Abulk_name> <Bbulk_name>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
