import os

def get_chromosomes_from_fai(fai_file_path):
    chromosomes = []
    with open(fai_file_path, 'r') as fai_file:
        for line in fai_file:
            chrom_name = line.split()[0]
            chromosomes.append(chrom_name)
    return chromosomes

def create_vcf_script(output_folder, fasta, bcftools, P1_name, F1_name, Abulk_name, fai_file):
    script_content = ""
    chromosomes = get_chromosomes_from_fai(fai_file)

    for chromosome in chromosomes:
        vcf_output = os.path.join(output_folder, f"{P1_name}_{F1_name}_{Abulk_name}_{chromosome}.vcf")

        command = (
            f"{bcftools} mpileup -a AD,DP -B -q 40 -Q 18 -Ou -f {fasta} "
            f"{os.path.join(output_folder, P1_name)}_{chromosome}.bam "
            f"{os.path.join(output_folder, F1_name)}_{chromosome}.bam "
            f"{os.path.join(output_folder, Abulk_name)}_{chromosome}.bam | "
            f"{bcftools} call -m -Ou | "
            f"{bcftools} view -v snps -i \"(FORMAT/GT[0] ~ \\\"0/0\\\" || FORMAT/GT[0] ~ \\\"1/1\\\")\" -Ov -o {vcf_output}\n"
        )

        script_content += command

    script_file_path = os.path.join(output_folder, "make_vcf.sh")
    with open(script_file_path, "w") as script_file:
        script_file.write(script_content)

def main(output_folder, fasta, bcftools, P1_name, F1_name, Abulk_name, fai_file):
    create_vcf_script(output_folder, fasta, bcftools, P1_name, F1_name, Abulk_name, fai_file)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 8:
        print("Usage: python script.py <output_folder> <fasta> <bcftools> <P1_name> <F1_name> <Abulk_name> <fai_file>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
