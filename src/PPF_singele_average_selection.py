# coding: UTF-8
import sys
import os


def merge_snp_and_confidence(output_folder):
    average_snp_index_per_window = os.path.join(output_folder, 'average_snp_index_per_window.txt')
    a = open(average_snp_index_per_window, 'r')

    confidence_interval = os.path.join(output_folder, 'confidence_interval.txt')
    b = open(confidence_interval, 'r')

    position_average_sim_list = os.path.join(output_folder, 'position_average_sim_list.txt')
    c = open(position_average_sim_list, 'w')

    snp_average_list = []
    for line in a:
        line = line.strip()
        if line:
            fields = line.split("\t")
            chr_name = fields[0]
            mind_position = fields[1]
            Abulk_snp_average = fields[4] if fields[4] != 'N/A' else None
            snp_average_list.append([chr_name, mind_position, Abulk_snp_average])

    for line in b:
        line = line.strip()
        if line:
            fields = line.split("\t")
            chr_name_b = fields[0]
            mind_position_b = fields[1]
            low_99 = fields[4] if fields[4] != 'N/A' else None
            high_99 = fields[5] if fields[5] != 'N/A' else None
            low_95 = fields[6] if fields[6] != 'N/A' else None
            high_95 = fields[7] if fields[7] != 'N/A' else None

            found = False
            for snp_data in snp_average_list:
                if snp_data[0] == chr_name_b and snp_data[1] == mind_position_b:
                    output_data = snp_data + [low_99, high_99, low_95, high_95]
                    output_line = "\t".join([x if x is not None else 'N/A' for x in output_data])
                    c.write(output_line + "\n")
                    found = True
                    break

            if not found:
                output_line = "\t".join([chr_name_b, mind_position_b, 'N/A', low_99 or 'N/A', high_99 or 'N/A', low_95 or 'N/A', high_95 or 'N/A'])
                c.write(output_line + "\n")

    a.close()
    b.close()
    c.close()

def main(output_folder):
    merge_snp_and_confidence(output_folder)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <output_folder>")
    else:
        main(sys.argv[1])