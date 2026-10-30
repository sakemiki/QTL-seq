# coding: UTF-8
import sys
import os


def main(output_folder, vcf_file, filter_depth):
    F1_sim_txt = os.path.join(output_folder, 'F1_sim.txt')
    vcf_basename = os.path.basename(vcf_file).replace('.vcf', '')
    snpindex_txt = os.path.join(output_folder, f"{vcf_basename}_snpindex.txt")
    no_select_txt = os.path.join(output_folder, f"{vcf_basename}_snpindex_no_select.txt")

    hetero_sim = {}
    with open(F1_sim_txt, 'r') as a:
        for line in a:
            line = line.strip()
            if line:
                fields = line.split("\t")
                depth = int(fields[0])
                low_hetero = float(fields[1])
                high_hetero = float(fields[2])
                hetero_sim[depth] = (low_hetero, high_hetero)

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

                P2_data = fields[10].split(":")
                P2_array = P2_data[3].split(",")
                P2_ref = int(P2_array[0])
                P2_alt = int(P2_array[1])
                P2_depth = P2_ref + P2_alt
                P2_snp = round(P2_alt / P2_depth, 3) if P2_depth > 0 else 0

                F1_data = fields[11].split(":")
                F1_array = F1_data[3].split(",")
                F1_ref = int(F1_array[0])
                F1_alt = int(F1_array[1])
                F1_depth = F1_ref + F1_alt
                F1_snp = round(F1_alt / F1_depth, 3) if F1_depth > 0 else 0

                Bulk_A_data = fields[12].split(":")
                Bulk_A_array = Bulk_A_data[3].split(",")
                Bulk_A_ref = int(Bulk_A_array[0])
                Bulk_A_alt = int(Bulk_A_array[1])
                Bulk_A_depth = Bulk_A_ref + Bulk_A_alt

                if P1_snp == 1.0 and P2_snp == 0.0:
                    Bulk_A_snp = round(Bulk_A_ref / Bulk_A_depth, 3) if Bulk_A_depth > 0 else 0
                    direction_ok = True
                elif P1_snp == 0.0 and P2_snp == 1.0:
                    Bulk_A_snp = round(Bulk_A_alt / Bulk_A_depth, 3) if Bulk_A_depth > 0 else 0
                    direction_ok = True
                else:
                    Bulk_A_snp = round(Bulk_A_alt / Bulk_A_depth, 3) if Bulk_A_depth > 0 else 0
                    direction_ok = False

                depth_ok = (
                    P1_depth >= filter_depth
                    and P2_depth >= filter_depth
                    and F1_depth >= filter_depth
                    and Bulk_A_depth >= filter_depth
                )

                hetero_ok = False
                if depth_ok and F1_depth in hetero_sim:
                    low_hetero, high_hetero = hetero_sim[F1_depth]
                    hetero_ok = low_hetero <= F1_snp <= high_hetero

                bulk_ok = Bulk_A_snp != 0.0

                passed = depth_ok and direction_ok and hetero_ok and bulk_ok

                row = (
                    f"{chr_name}\t{position}\t{P1_snp}\t{P1_depth}\t{P2_snp}\t{P2_depth}\t"
                    f"{F1_snp}\t{F1_depth}\t{Bulk_A_snp}\t{Bulk_A_depth}\n"
                )

                if passed:
                    c.write(row)
                else:
                    d.write(row)


if __name__ == "__main__":
    if len(sys.argv) == 4:
        output_folder = sys.argv[1]
        vcf_file = sys.argv[2]
        filter_depth = int(sys.argv[3])
        main(output_folder, vcf_file, filter_depth)
    else:
        print("Usage: python3 PPF_singele_snpindex.py <output_folder> <vcf_file> <filter_depth>")