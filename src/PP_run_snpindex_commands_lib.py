import subprocess
import os
import sys

def main(output_folder):
    bam_filter_run = os.path.join(output_folder, "PP_snpindex.sh")

    try:
        result = subprocess.run(['bash', bam_filter_run], check=True, text=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        # ログファイルにエラー情報を出力
        log_path = os.path.join(output_folder, "PP_snpindex_error.log")
        with open(log_path, "w") as log_file:
            log_file.write("An error occurred during script execution.\n")
            log_file.write(f"Command: {e.cmd}\n")
            log_file.write(f"Return code: {e.returncode}\n")
            log_file.write(f"Standard output:\n{e.stdout}\n")
            log_file.write(f"Error message:\n{e.stderr}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <output_folder>")
        sys.exit(1)
    
    output_folder = sys.argv[1]
    main(output_folder)
