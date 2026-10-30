import subprocess
from concurrent.futures import ThreadPoolExecutor
import os

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed: {command}\nError: {e.stderr}")

def run_commands_from_file(output_folder, max_workers=4):
    script_file = os.path.join(output_folder, "PP_single_snpindex.sh")#######

    if not os.path.isfile(script_file):
        print(f"Error: {script_file} does not exist.")
        return

    with open(script_file, 'r') as f:
        commands = [line.strip() for line in f if line.strip()]

    if not commands:
        print(f"No commands found in {script_file}")
        return

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(run_command, commands)

def main(output_folder):
    run_commands_from_file(output_folder, max_workers=3)#####

if __name__ == "__main__":
    main()
