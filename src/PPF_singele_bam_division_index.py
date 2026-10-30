# coding: UTF-8
import sys
import os

def main(output_folder, P1_name, P2_name, F1_name, Abulk_name, samtools, fai_file):
    chrom_names = []
    with open(fai_file, "r") as file:
        chrom_names = [line.split()[0] for line in file]

    output_index_script = os.path.join(output_folder, 'bam_division_index.sh')

    with open(output_index_script, 'w') as script:
        for chrom in chrom_names:
            # P1
            bam_p1 = os.path.join(output_folder, f"{P1_name}_{chrom}.bam")
            script.write(f"{samtools} index {bam_p1}\n")

            # P2
            bam_p2 = os.path.join(output_folder, f"{P2_name}_{chrom}.bam")
            script.write(f"{samtools} index {bam_p2}\n")

            # F1
            bam_F1 = os.path.join(output_folder, f"{F1_name}_{chrom}.bam")
            script.write(f"{samtools} index {bam_F1}\n")

            # Abulk
            bam_ab = os.path.join(output_folder, f"{Abulk_name}_{chrom}.bam")
            script.write(f"{samtools} index {bam_ab}\n")

if __name__ == "__main__":
    if len(sys.argv) != 8:
        print("Usage: python script.py <output_folder> <P1_name> <P2_name> <F1_name> <Abulk_name> <samtools> <fai_file>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
