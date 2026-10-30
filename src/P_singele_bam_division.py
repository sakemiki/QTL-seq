# coding: UTF-8
import sys
import os

def main(output_folder, P1_bam, P1_name, Abulk_bam, Abulk_name, samtools, fai_file):

    with open(fai_file, "r") as file:
        chr_name_list = [line.split()[0] for line in file if line.strip()]

    output_file_name = os.path.join(output_folder, "bam_division.sh")

    with open(output_file_name, 'w') as script_file:
        for chr_name in chr_name_list:
            # P1
            output_p1 = os.path.join(output_folder, f"{P1_name}_{chr_name}.bam")
            script_file.write(f"{samtools} view -b {P1_bam} {chr_name} > {output_p1}\n")

            # Abulk
            output_ab = os.path.join(output_folder, f"{Abulk_name}_{chr_name}.bam")
            script_file.write(f"{samtools} view -b {Abulk_bam} {chr_name} > {output_ab}\n")

if __name__ == "__main__":

    if len(sys.argv) != 8:
        print("Usage: python script.py <output_folder> <P1_bam> <P1_name> <Abulk_bam> <Abulk_name> <samtools> <fai_file>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])