# coding: UTF-8
import sys
import os

def measure_bam_sizes(output_folder, P1_name, P2_name, F1_name, Abulk_name, Bbulk_name):
    sample_names = [P1_name, P2_name, F1_name, Abulk_name, Bbulk_name]

    bam_files = []
    for file in os.listdir(output_folder):
        if not file.endswith('.bam'):
            continue
        if file.endswith('_filter.bam'):
            # 染色体分割前のフィルタ後BAM本体は対象外
            continue
        if any(file.startswith(f"{name}_") for name in sample_names):
            # P1/P2/F1/Abulk/Bbulk 由来の、染色体分割後のBAMのみを対象にする
            bam_files.append(os.path.join(output_folder, file))

    output_index_script = os.path.join(output_folder, 'bam_file_data_volume.txt')

    with open(output_index_script, 'w') as file:
        for bam_path in bam_files:
            size_bytes = os.path.getsize(bam_path)
            size_mb = size_bytes / (1024 * 1024)
            size_str = f"{size_mb:.1f}MB"
            bam_name = os.path.basename(bam_path)
            file.write(f"{bam_name}\t{size_str}\t{bam_path}\n")

def main(output_folder, P1_name, P2_name, F1_name, Abulk_name, Bbulk_name):
    measure_bam_sizes(output_folder, P1_name, P2_name, F1_name, Abulk_name, Bbulk_name)

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: python script.py <output_folder> <P1_name> <P2_name> <F1_name> <Abulk_name> <Bbulk_name>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])