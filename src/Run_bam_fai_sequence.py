import subprocess
import os
import sys
from concurrent.futures import ThreadPoolExecutor

def run_command(cmd):
    subprocess.run(cmd, shell=True, check=True)

def main(output_folder):
    bam_filter_run = os.path.join(output_folder, "bam_fai_sequence.sh")

    with open(bam_filter_run, "r") as f:
        commands = [line.strip() for line in f if line.strip()]

    # 最大3並列
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(run_command, commands)
if __name__ == "__main__":
    main()

