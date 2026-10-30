"""QTL-seq CUI版

GUI版と同じ解析を、画面を使わずにコマンドラインから実行する。
通常は一つ上の階層の Run.sh から呼び出す。

例:
    python3 src/Run_CUI.py --output /path/out --samtools samtools --bcftools bcftools \
        --fasta ref.fna --pattern P1P2 --bulk double --bulk-type F2 \
        --p1-bam P1.bam --p2-bam P2.bam --abulk-bam A.bam --bbulk-bam B.bam
"""
import os
import sys
import glob
import shutil
import argparse
import importlib
import subprocess
import traceback


def organize_files(output_folder):
    txt_folder = os.path.join(output_folder, 'txt')
    result_folder = os.path.join(output_folder, 'result')
    bam_folder = os.path.join(output_folder, 'bam')

    os.makedirs(txt_folder, exist_ok=True)
    os.makedirs(result_folder, exist_ok=True)
    os.makedirs(bam_folder, exist_ok=True)

    sim_txt_files = glob.glob(os.path.join(output_folder, '*sim.txt'))
    sh_files = glob.glob(os.path.join(output_folder, '*.sh'))
    py_files = glob.glob(os.path.join(output_folder, '*.py'))
    for file in sim_txt_files + sh_files + py_files:
        os.remove(file)

    txt_files = glob.glob(os.path.join(output_folder, '*.txt'))
    for txt_file in txt_files:
        destination = os.path.join(txt_folder, os.path.basename(txt_file))
        if os.path.exists(destination):
            os.remove(destination)
        shutil.move(txt_file, txt_folder)

    for pattern_glob, folder in [('*.png', result_folder), ('*.bam', bam_folder), ('*.bam.bai', bam_folder)]:
        for src in glob.glob(os.path.join(output_folder, pattern_glob)):
            destination = os.path.join(folder, os.path.basename(src))
            if os.path.exists(destination):
                os.remove(destination)
            shutil.move(src, destination)


if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
# サブモジュールをどのカレントディレクトリからでも import できるようにする
if application_path not in sys.path:
    sys.path.insert(0, application_path)

# GUI のラジオボタンの値と同じ番号に変換する
PATTERN_CHOICES = {"P1": 1, "P1P2": 2, "P1P2F1": 3, "P1F1": 4}
PATTERN_PREFIX = {1: "P", 2: "PP", 3: "PPF", 4: "PF"}
PATTERN_STR = {1: "P1", 2: "P1 , P2", 3: "P1 , P2 , F1", 4: "P1 , F1"}
BULK_CHOICES = {"single": 1, "double": 2}
BULK_TYPE_CHOICES = {"RIL": 1, "F2": 2, "BC1F1": 3}

# double bulk の P1,P2,F1 パターンだけはプレフィックス無しのモジュールを使うが、
# 以下のステップは PPF_ のモジュールを使う
PPF_DOUBLE_STEPS = {"vcf_snpindex", "run_snpindex_commands_lib", "snpindex_marge", "average"}
# single bulk で "singele" ではなく "single" と綴られているモジュール
SINGLE_SPELLED_STEPS = {"vcf_snpindex", "run_snpindex_commands_lib", "average_selection_txt"}


def module_name(step, pattern, bulk):
    """GUI版の分岐で使っていたモジュール名を返す"""
    if step == "figure_legend":
        return "figure_legend" if bulk == 2 else "figure_legend_single"
    prefix = PATTERN_PREFIX[pattern]
    if bulk == 2:
        if pattern == 3:
            return f"PPF_{step}" if step in PPF_DOUBLE_STEPS else step
        return f"{prefix}_{step}"
    spelling = "single" if step in SINGLE_SPELLED_STEPS else "singele"
    return f"{prefix}_{spelling}_{step}"


def progress(pct, message):
    print(f"[{pct:3d}%] {message}", flush=True)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="QTL-seq (CUI version)")
    g = parser.add_argument_group("paths")
    g.add_argument("--output", required=True, help="Output folder")
    g.add_argument("--samtools", default="samtools", help="Path to samtools")
    g.add_argument("--bcftools", default="bcftools", help="Path to bcftools")
    g.add_argument("--fasta", required=True, help="Reference FASTA")

    g = parser.add_argument_group("processing details")
    g.add_argument("--pattern", required=True, choices=PATTERN_CHOICES.keys(),
                   help="Parent pattern: P1 / P1P2 / P1F1 / P1P2F1")
    g.add_argument("--bulk", required=True, choices=BULK_CHOICES.keys(), help="single / double")
    g.add_argument("--bulk-type", required=True, choices=BULK_TYPE_CHOICES.keys(), help="RIL / F2 / BC1F1")

    g = parser.add_argument_group("bam files and sample names")
    g.add_argument("--p1-bam", required=True)
    g.add_argument("--p1-name", default="P1")
    g.add_argument("--p2-bam", default="")
    g.add_argument("--p2-name", default="P2")
    g.add_argument("--f1-bam", default="")
    g.add_argument("--f1-name", default="F1")
    g.add_argument("--abulk-bam", required=True)
    g.add_argument("--abulk-name", default="Abulk")
    g.add_argument("--bbulk-bam", default="")
    g.add_argument("--bbulk-name", default="Bbulk")

    g = parser.add_argument_group("filtering values")
    g.add_argument("--filter-depth", type=int, default=10)
    g.add_argument("--window-size", type=int, default=2000000)
    g.add_argument("--step-size", type=int, default=50000)
    g.add_argument("--bulk-number", type=int, default=15)
    g.add_argument("--removal-snpindex", type=float, default=0.3)

    g = parser.add_argument_group("graph options")
    g.add_argument("--abulk-color", default="green")
    g.add_argument("--bbulk-color", default="gold")
    g.add_argument("--delta-color", default="midnightblue")
    g.add_argument("--side", type=int, default=2, help="Number of row")
    return parser.parse_args(argv)


def error(message):
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def main(argv=None):
    args = parse_args(argv)

    pattern = PATTERN_CHOICES[args.pattern]
    Bulk_single_double = BULK_CHOICES[args.bulk]
    bulk_type = BULK_TYPE_CHOICES[args.bulk_type]
    fasta = args.fasta
    output_folder = os.path.abspath(os.path.expanduser(args.output))
    samtools = args.samtools
    bcftools = args.bcftools
    filter_depth = args.filter_depth
    window_size = args.window_size
    step_size = args.step_size
    bulk_number = args.bulk_number
    removal_SNPindex = args.removal_snpindex
    abulk_color = args.abulk_color
    bbulk_color = args.bbulk_color
    delta_color = args.delta_color
    side = args.side

    # 最後の整理で出力フォルダ内の *.py / *.sh を削除するため、script フォルダと Run.sh のフォルダは不可
    if os.path.realpath(output_folder) in (os.path.realpath(application_path),
                                           os.path.realpath(os.path.dirname(application_path))):
        error("Output folder must be different from the script folder")

    # --- BAM取得 ---
    def sample(bam, name, label):
        if not os.path.exists(bam):
            error(f"{label} BAM not found: {bam}")
        return bam, (name or label).replace(" ", "_")

    P1_bam, P1_name = sample(args.p1_bam, args.p1_name, "P1")
    P2_bam, P2_name = sample(args.p2_bam, args.p2_name, "P2") if pattern in [2, 3] else (None, None)
    F1_bam, F1_name = sample(args.f1_bam, args.f1_name, "F1") if pattern in [3, 4] else (None, None)
    Abulk_bam, Abulk_name = sample(args.abulk_bam, args.abulk_name, "Abulk")
    Bbulk_bam, Bbulk_name = sample(args.bbulk_bam, args.bbulk_name, "Bbulk") if Bulk_single_double == 2 else (None, None)

    # --- サンプル名重複チェック ---
    all_names = [n for n in [P1_name, P2_name, F1_name, Abulk_name, Bbulk_name] if n is not None]
    if len(all_names) != len(set(all_names)):
        error("The sample name is already taken. Please enter it again.")
    all_bams = [b for b in [P1_bam, P2_bam, F1_bam, Abulk_bam, Bbulk_bam] if b is not None]

    # --- FASTAチェック ---
    if not os.path.exists(fasta):
        error(f"FASTA file not found: {fasta}")
    # --- FAI作成 ---
    fai_file = fasta + ".fai"
    try:
        if not os.path.exists(fai_file):
            subprocess.run(f"{samtools} faidx {fasta}", shell=True, check=True)
    except subprocess.CalledProcessError:
        error("FAI creation failed")

    # --- 出力フォルダ ---
    os.makedirs(output_folder, exist_ok=True)
    # --- file copy ---
    file_paths = [os.path.join(application_path, 'F1_sim.txt')]
    for group in ['F2', 'BC1F1', 'RIL']:
        file_paths.extend(os.path.join(application_path, f'{group}_{i}_sim.txt') for i in range(10, 51))
    snp_files = [
        'P_singele_snpindex', 'PF_singele_snpindex', 'P_snpindex', 'PF_snpindex',
        'PP_singele_snpindex', 'PP_snpindex', 'PPF_singele_snpindex', 'PPF_snpindex'
    ]
    file_paths.extend(os.path.join(application_path, f"{fname}.py") for fname in snp_files)
    from move import main as move
    move(output_folder, file_paths)

    # --- log ---
    param_log_path = os.path.join(output_folder, "QTLseq_input_log.txt")
    with open(param_log_path, "w", encoding="utf-8") as log_file:
        log_file.write("=== QTL-seq run parameters ===\n")
        log_file.write(f"Output folder: {output_folder}\n")
        log_file.write(f"samtools: {samtools}\n")
        log_file.write(f"bcftools: {bcftools}\n")
        log_file.write(f"FASTA: {fasta}\n")
        log_file.write(f"P1 BAM: {P1_bam} ({P1_name})\n")
        log_file.write(f"P2 BAM: {P2_bam} ({P2_name})\n")
        log_file.write(f"F1 BAM: {F1_bam} ({F1_name})\n")
        log_file.write(f"Abulk BAM: {Abulk_bam} ({Abulk_name})\n")
        log_file.write(f"Bbulk BAM: {Bbulk_bam} ({Bbulk_name})\n")
        log_file.write(f"Filter Depth: {filter_depth}\n")
        log_file.write(f"Window Size: {window_size}\n")
        log_file.write(f"Step Size: {step_size}\n")
        log_file.write(f"Bulk Number: {bulk_number}\n")
        log_file.write(f"Abulk Color: {abulk_color}\n")
        log_file.write(f"Bbulk Color: {bbulk_color}\n")
        log_file.write(f"Delta Color: {delta_color}\n")
        log_file.write(f"Side: {side}\n")
        log_file.write(f"Bulk: {'Single' if Bulk_single_double == 1 else 'Double'}\n")
        log_file.write(f"Bulk Type: {args.bulk_type}\n")
        log_file.write(f"Filter Pattern: {PATTERN_STR[pattern]}\n")

    import matplotlib
    matplotlib.use('Agg')

    def run(step, *step_args):
        importlib.import_module(module_name(step, pattern, Bulk_single_double)).main(*step_args)

    # GUI版の各分岐と同じ引数の並び:
    #   bam_division には (bam, name) のペア、それ以外のステップには name のみを順に渡す
    bam_name_pairs = [x for bam, name in zip(all_bams, all_names) for x in (bam, name)]
    bulk_names = [Abulk_name, Bbulk_name] if Bulk_single_double == 2 else [Abulk_name]

    error_log_path = os.path.join(output_folder, "QTLseq_error_log.txt")
    try:
        run("bam_division", output_folder, *bam_name_pairs, samtools, fai_file)
        progress(25, "Splitting bam by chromosome...")
        run("Run_bam_division", output_folder)

        run("bam_division_index", output_folder, *all_names, samtools, fai_file)
        progress(33, "Creating index...")
        run("Run_bam_division_index", output_folder)

        run("bam_file_data_volume", output_folder, *all_names)
        run("bam_fai_sequence", output_folder, fai_file, samtools, *all_names)

        if os.path.exists(os.path.join(output_folder, 'num_parts.txt')):
            progress(41, "Splitting the BAM file by size...")
            run("Run_bam_fai_sequence", output_folder)
            progress(49, "Creating index...")
            run("Run_bam_fai_sequence_index", output_folder)
            run("make_vcftxt_position", output_folder, fasta, bcftools, *all_names)
            progress(57, "Creating a VCF file...")
            run("Run_make_vcftxt_position", output_folder)
        else:
            run("make_vcf", output_folder, fasta, bcftools, *all_names, fai_file)
            progress(57, "Creating a VCF file...")
            run("Run_make_vcf", output_folder)

        if Bulk_single_double == 2:
            run("vcf_snpindex", output_folder, filter_depth, removal_SNPindex)
        else:
            run("vcf_snpindex", output_folder, filter_depth)
        progress(65, "Calculating SNP index...")
        run("run_snpindex_commands_lib", output_folder)

        for file in glob.glob(os.path.join(output_folder, '*.vcf')):
            os.remove(file)

        run("snpindex_marge", output_folder, fai_file)
        run("snp_sim", output_folder, bulk_number, bulk_type)

        progress(73, "Setting confidence interval...")
        run("confidence_interval", output_folder, fai_file, window_size, step_size, filter_depth)
        progress(81, "Calculating the average SNP index...")
        run("average", output_folder, fai_file, filter_depth, window_size, step_size)

        progress(89, "Creating a plot...")
        if Bulk_single_double == 2:
            run("plot", output_folder, Abulk_name, Bbulk_name, fai_file, abulk_color, bbulk_color, delta_color, side)
            run("figure_legend", output_folder, abulk_color, bbulk_color, delta_color, window_size, step_size)
        else:
            run("plot", output_folder, Abulk_name, fai_file, abulk_color, side)
            run("figure_legend", output_folder, abulk_color, window_size, step_size)

        run("average_selection", output_folder)
        run("average_selection_txt", output_folder, *bulk_names, fai_file)

        progress(97, "Detecting peak regions...")
        run("peak", output_folder, *bulk_names)

        organize_files(output_folder)
        progress(100, "It's all over!")
        print("Analysis Completed")
    except Exception as e:
        with open(error_log_path, "w", encoding="utf-8") as ef:
            ef.write("=== Error log ===\n")
            ef.write(f"Error details: {e}\n\n")
            ef.write("=== Detailed traceback ===\n")
            ef.write(traceback.format_exc())
        traceback.print_exc()
        error(f"An error occurred during analysis\nPlease refer to the file below for further details:\n{error_log_path}")


if __name__ == "__main__":
    main()
