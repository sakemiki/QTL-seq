import subprocess
import os
import sys

def main(output_folder):
    bam_filter_run = os.path.join(output_folder, "bam_division_index.sh")
    
    try:
        result = subprocess.run(['bash', bam_filter_run], check=True, text=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        # スクリプトの実行中にエラーが発生した場合
        print("An error occurred during script execution.")
        print("Error message:", e.stderr)

if __name__ == "__main__":
    main()