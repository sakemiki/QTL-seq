import os
import sys

def main(output_folder, filter_depth, removal_SNPindex):

    vcf_files = [f for f in os.listdir(output_folder) if f.endswith('.vcf')]

    if not vcf_files:
        print(f"No VCF files found in the directory: {output_folder}")
        return

    script_file = os.path.join(output_folder, 'PPF_snpindex.sh')
    script_path = os.path.join(output_folder, 'PPF_snpindex.py')

    with open(script_file, 'w') as f:
        for vcf in vcf_files:
            vcf_path = os.path.join(output_folder, vcf)
            f.write(
                f"python3 {script_path} {output_folder} {vcf_path} {filter_depth} {removal_SNPindex}\n"
            )

    print(f"Commands written to {script_file}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py <output_folder> <filter_depth> <removal_SNPindex>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
