# coding: UTF-8
import sys
import os

def snp_sim_main(output_folder, bulk_number, bulk_type):
    snpindex_txt = os.path.join(output_folder, 'snpindex_merge.txt')

    if bulk_type == 1:
        sim_txt = os.path.join(output_folder, f'RIL_{bulk_number}_sim.txt')
    elif bulk_type == 2:
        sim_txt = os.path.join(output_folder, f'F2_{bulk_number}_sim.txt')
    elif bulk_type == 3:
        sim_txt = os.path.join(output_folder, f'BC1F1_{bulk_number}_sim.txt')
    else:
        raise ValueError("Invalid bulk type. Please specify 1 for RIL, 2 for F2, or 3 for BC1F1.")

    snp_sim_txt = os.path.join(output_folder, 'sim_snp.txt')

    if not os.path.exists(snpindex_txt):
        print(f"Error: snpindex_merge.txtが存在しません: {snpindex_txt}")
        return
    if not os.path.exists(sim_txt):
        print(f"Error: シミュレーションファイルが存在しません: {sim_txt}")
        return

    with open(snpindex_txt, 'r') as a, open(sim_txt, 'r') as b, open(snp_sim_txt, 'w') as c:
        data_list = []
        depth_300_data = None

        for line in b:
            line = line.strip()
            if line:
                fields = line.split("\t")
                depth = fields[0]
                data_entry = {
                    'depth': depth,
                    'data': "\t".join(fields[1:])
                }
                data_list.append(data_entry)

                if depth == "300":
                    depth_300_data = data_entry

        for line_a in a:
            line_a = line_a.strip()
            if line_a:
                fields = line_a.split("\t")
                min_depth = min(int(fields[5]), int(fields[7]))

                if min_depth >= 300 and depth_300_data:
                    output_line = f"{line_a}\t{depth_300_data['depth']}\t{depth_300_data['data']}"
                else:
                    matched_items = [item for item in data_list if item['depth'] == str(min_depth)]
                    if matched_items:
                        for item in matched_items:
                            output_line = f"{line_a}\t{item['depth']}\t{item['data']}"
                    else:
                        output_line = line_a

                c.write(output_line + "\n")

def main(output_folder, bulk_number, bulk_type):
    snp_sim_main(output_folder, bulk_number, bulk_type)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <output_folder> <bulk_number> <bulk_type>")
    else:
        output_folder = sys.argv[1]
        bulk_number = int(sys.argv[2])
        bulk_type = int(sys.argv[3])
        main(output_folder, bulk_number, bulk_type)
