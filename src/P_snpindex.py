# coding: UTF-8
import sys
import os


def main(output_folder, vcf_file, filter_depth, removal_SNPindex):
    vcf_basename = os.path.basename(vcf_file).replace('.vcf', '')
    snpindex_txt = os.path.join(output_folder, f"{vcf_basename}_snpindex.txt")
    no_select_txt = os.path.join(output_folder, f"{vcf_basename}_snpindex_no_select.txt")

    with open(vcf_file, 'r') as b, \
         open(snpindex_txt, 'w') as c, \
         open(no_select_txt, 'w') as d:
        for line_b in b:
            line_b = line_b.strip()
            if line_b and not line_b.startswith('#'):
                fields = line_b.split("\t")
                chr_name = fields[0]
                position = int(fields[1])

                P1_data = fields[9].split(":")
                P1_array = P1_data[3].split(",")
                P1_ref = int(P1_array[0])
                P1_alt = int(P1_array[1])
                P1_depth = P1_ref + P1_alt
                P1_snp = round(P1_alt / P1_depth, 3) if P1_depth > 0 else 0

                Bulk_A_data = fields[10].split(":")
                Bulk_A_array = Bulk_A_data[3].split(",")
                Bulk_A_ref = int(Bulk_A_array[0])
                Bulk_A_alt = int(Bulk_A_array[1])
                Bulk_A_depth = Bulk_A_ref + Bulk_A_alt

                Bulk_B_data = fields[11].split(":")
                Bulk_B_array = Bulk_B_data[3].split(",")
                Bulk_B_ref = int(Bulk_B_array[0])
                Bulk_B_alt = int(Bulk_B_array[1])
                Bulk_B_depth = Bulk_B_ref + Bulk_B_alt

                if P1_snp == 1.0:
                    Bulk_A_snp = round(Bulk_A_ref / Bulk_A_depth, 3) if Bulk_A_depth > 0 else 0
                    Bulk_B_snp = round(Bulk_B_ref / Bulk_B_depth, 3) if Bulk_B_depth > 0 else 0
                    direction_ok = True
                elif P1_snp == 0.0:
                    Bulk_A_snp = round(Bulk_A_alt / Bulk_A_depth, 3) if Bulk_A_depth > 0 else 0
                    Bulk_B_snp = round(Bulk_B_alt / Bulk_B_depth, 3) if Bulk_B_depth > 0 else 0
                    direction_ok = True
                else:
                    Bulk_A_snp = round(Bulk_A_alt / Bulk_A_depth, 3) if Bulk_A_depth > 0 else 0
                    Bulk_B_snp = round(Bulk_B_alt / Bulk_B_depth, 3) if Bulk_B_depth > 0 else 0
                    direction_ok = False

                delta_snp = round(Bulk_A_snp - Bulk_B_snp, 4)

                depth_ok = (
                    P1_depth >= filter_depth
                    and Bulk_A_depth >= filter_depth
                    and Bulk_B_depth >= filter_depth
                )

                bulk_ok = not (Bulk_A_snp == 0.0 and Bulk_B_snp == 0.0) and not (
                    Bulk_A_snp <= removal_SNPindex and Bulk_B_snp <= removal_SNPindex
                )

                passed = depth_ok and direction_ok and bulk_ok

                row = (
                    f"{chr_name}\t{position}\t{P1_snp}\t{P1_depth}\t"
                    f"{Bulk_A_snp}\t{Bulk_A_depth}\t{Bulk_B_snp}\t{Bulk_B_depth}\t{delta_snp}\n"
                )

                if passed:
                    c.write(row)
                else:
                    d.write(row)


if __name__ == "__main__":
    if len(sys.argv) == 5:
        output_folder = sys.argv[1]
        vcf_file = sys.argv[2]
        filter_depth = int(sys.argv[3])
        removal_SNPindex = float(sys.argv[4])
        main(output_folder, vcf_file, filter_depth, removal_SNPindex)
    else:
        print("Usage: python3 P_snpindex.py <output_folder> <vcf_file> <filter_depth> <removal_SNPindex>")