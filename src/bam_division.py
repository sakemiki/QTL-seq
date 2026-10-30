# coding: UTF-8
import sys
import os

def main(output_folder, P1_bam, P1_name, P2_bam, P2_name, F1_bam, F1_name, Abulk_bam, Abulk_name, Bbulk_bam, Bbulk_name, samtools, fai_file):

    # 読み込む染色体名一覧（faiファイル）
    with open(fai_file, "r") as file:
        chr_name_list = [line.split()[0] for line in file if line.strip()]

    output_file_name = os.path.join(output_folder, "bam_division.sh")

    # 注: samtools view -b <bam> <chr_name> はリージョン指定のため、
    # 入力BAM（P1_bam, P2_bam, F1_bam, Abulk_bam, Bbulk_bam）が
    # 事前に samtools index 済み（.bai あり）である必要があります。

    with open(output_file_name, 'w') as script_file:
        for chr_name in chr_name_list:
            # P1
            output_p1 = os.path.join(output_folder, f"{P1_name}_{chr_name}.bam")
            script_file.write(f"{samtools} view -b {P1_bam} {chr_name} > {output_p1}\n")

            # P2
            output_p2 = os.path.join(output_folder, f"{P2_name}_{chr_name}.bam")
            script_file.write(f"{samtools} view -b {P2_bam} {chr_name} > {output_p2}\n")

            # F1
            output_F1 = os.path.join(output_folder, f"{F1_name}_{chr_name}.bam")
            script_file.write(f"{samtools} view -b {F1_bam} {chr_name} > {output_F1}\n")

            # Abulk
            output_ab = os.path.join(output_folder, f"{Abulk_name}_{chr_name}.bam")
            script_file.write(f"{samtools} view -b {Abulk_bam} {chr_name} > {output_ab}\n")

            # Bbulk
            output_bb = os.path.join(output_folder, f"{Bbulk_name}_{chr_name}.bam")
            script_file.write(f"{samtools} view -b {Bbulk_bam} {chr_name} > {output_bb}\n")

if __name__ == "__main__":
    # sys.argv[0] はスクリプト名、sys.argv[1]〜[13] が13個の引数なので長さは14
    if len(sys.argv) != 14:
        print("Usage: python script.py <output_folder> <P1_bam> <P1_name> <P2_bam> <P2_name> <F1_bam> <F1_name> <Abulk_bam> <Abulk_name> <Bbulk_bam> <Bbulk_name> <samtools> <fai_file>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13])