# coding: UTF-8
import os
import sys
import re
from collections import defaultdict

def main(output_folder, fasta, bcftools, P1_name, P2_name, Abulk_name):
    output_script = os.path.join(output_folder, 'make_vcftxt_position.sh')
    bam_files = defaultdict(lambda: defaultdict(list))

    for filename in os.listdir(output_folder):
        match = re.match(rf"^({P1_name}|{P2_name}|{Abulk_name})_(.+?)__part(\d+)\.bam$", filename)
        if match:
            sample, chromosome, part = match.groups()
            part = int(part)
            bam_files[(chromosome, part)][sample].append(os.path.join(output_folder, filename))
        else:
            print(f"WARNING: {filename} の形式が不正です")

    def sort_bam_files(bam_files, chromosome, part):
        ordered_files = [
            bam_files[(chromosome, part)].get(P1_name, [""])[0],
            bam_files[(chromosome, part)].get(P2_name, [""])[0],
            bam_files[(chromosome, part)].get(Abulk_name, [""])[0]
        ]
        missing_files = [name for name, file in zip([P1_name, P2_name, Abulk_name], ordered_files) if not file]
        if missing_files:
            print(f"WARNING: {chromosome} part{part} の BAM ファイルが不足 ({', '.join(missing_files)})")
        return ordered_files

    with open(output_script, 'w') as a:
        for key in sorted(bam_files.keys()):
            chromosome, part = key
            files = sort_bam_files(bam_files, chromosome, part)

            if all(files): 
                output_vcf = os.path.join(output_folder, f"{P1_name}_{P2_name}_{Abulk_name}_{chromosome}_part{part}.vcf")

                a.write(
                    f"{bcftools} mpileup -a AD,DP -B -q 40 -Q 18 -Ou -f {fasta} {' '.join(files)} | "
                    f"{bcftools} call -m -Ou | "
                    f"{bcftools} view -v snps -i \"((FORMAT/GT[0] ~ \\\"0/0\\\" && FORMAT/GT[1] ~ \\\"1/1\\\") || "
                    f"(FORMAT/GT[0] ~ \\\"1/1\\\" && FORMAT/GT[1] ~ \\\"0/0\\\"))\" -Ov -o {output_vcf}\n"
                )

                for bam_file in files:
                    a.write(f"rm {bam_file}\n")
                    a.write(f"rm {bam_file}.bai\n")
            else:
                print(f"WARNING: {chromosome} part{part} の BAM ファイルが不足しているため VCF を作成できません")

    os.system(f"cat {output_script}")

if __name__ == "__main__":
    if len(sys.argv) < 8:
        print("エラー: 引数が不足しています。\n使用方法: python script.py <output_folder> <fasta> <bcftools> <P1_name> <P2_name> <Abulk_name>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
