# QTL-seq GUI ver. 1.02

QTL-seq GUI is an application for QTL-seq analysis from BAM files. It is available for macOS and Windows (WSL). A command-line (CUI) version is also included.

This repository contains:

| Item | Location |
| --- | --- |
| macOS application | [Releases](https://github.com/sakemiki/QTL-seq/releases/latest) → `QTL-seq_GUI_ver1_02_mac.zip` |
| Windows (WSL) application | [Releases](https://github.com/sakemiki/QTL-seq/releases/latest) → `QTL-seq_GUI_ver1_02_windows.zip` |
| CUI version | `Run.sh` + `src/` |
| Source code | `src/` (Windows launcher and installer: `windows/`) |
| Test data | `test_data/` |
| User manual | `QTL-seq_GUI_Manual.pdf` |

## Contents

- [Requirements](#requirements)
- [macOS](#macos)
- [Windows (WSL)](#windows-wsl)
- [CUI version](#cui-version)
- [Test data](#test-data)
- [Source code](#source-code)
- [Usage and contact](#usage-and-contact)

---

## Requirements

All versions require [SAMtools](http://www.htslib.org/download/) and [BCFtools](http://www.htslib.org/download/). Their paths are entered in the GUI (or in `Run.sh` for the CUI version).

| Version | Additional requirements |
| --- | --- |
| macOS | None (Python is bundled in the application) |
| Windows (WSL) | Windows 10 (21H2 or later) or Windows 11 with WSL 2 and Ubuntu (SAMtools and BCFtools are installed by `install.sh`) |
| CUI / running from source | Python 3.12 and the packages in `requirements.txt` |

---

## macOS

1. Download **[QTL-seq_GUI_ver1_02_mac.zip](https://github.com/sakemiki/QTL-seq/releases/latest/download/QTL-seq_GUI_ver1_02_mac.zip)**.
2. Double-click the ZIP file to extract it.
3. Move `QTL-seq_GUI_ver1_02.app` to any folder you like (e.g., **Applications**).
4. Double-click `QTL-seq_GUI_ver1_02.app` to start it.

> [!NOTE]
> **If macOS blocks the app** ("the developer cannot be verified" or "the app is damaged"):
>
> - Go to **System Settings → Privacy & Security**, find the message about `QTL-seq_GUI_ver1_02`, and click **Open Anyway**.
> - If that does not work, run the following in **Terminal** in the folder containing the app, then open it again:
>
>   ```bash
>   xattr -cr QTL-seq_GUI_ver1_02.app
>   ```

---

## Windows (WSL)

On Windows, QTL-seq GUI runs on **WSL**, a feature built into Windows. WSL is required because SAMtools and BCFtools are not distributed as Windows applications. After installation, the application is started by double-clicking `QTL-seq_GUI.exe`.

`QTL-seq_GUI_ver1_02_windows.zip` contains:

| File | Description |
| --- | --- |
| `QTL-seq_GUI.exe` | Launcher. Double-click to start QTL-seq GUI. |
| `QTL-seq_GUI.vbs` | Alternative launcher (use only if the `.exe` is blocked). |
| `QTL-seq_GUI_ver1_02_windows` | QTL-seq GUI application (runs in WSL). |
| `install.sh` | Installer (installs SAMtools, BCFtools and QTL-seq GUI in WSL). |
| `README.md` | Instructions for the Windows version. |

### Step 1. Install WSL

1. Open **PowerShell** as administrator and run the following command, then restart your PC:

   ```powershell
   wsl --install
   ```

   If WSL is already installed, run `wsl --update` instead.

2. After restarting, **Ubuntu** opens automatically (or open it from the Start menu). Set a user name and password when prompted.

### Step 2. Install QTL-seq GUI

1. Download **[QTL-seq_GUI_ver1_02_windows.zip](https://github.com/sakemiki/QTL-seq/releases/latest/download/QTL-seq_GUI_ver1_02_windows.zip)**.
2. Before extracting the ZIP file, right-click it, select **Properties**, check **Unblock** at the bottom of the dialog, and click **OK**.
3. Extract the ZIP file (for example, to the Downloads folder).
4. Open **Ubuntu**, move to the extracted folder and run `install.sh`. Enter your Ubuntu password when asked. For example, if the folder was extracted to `C:\Users\<YourName>\Downloads\QTL-seq_GUI_ver1_02_windows`:

   ```bash
   cd /mnt/c/Users/<YourName>/Downloads/QTL-seq_GUI_ver1_02_windows
   bash install.sh
   ```

### Step 3. Launch

Double-click `QTL-seq_GUI.exe`. The launcher can be placed anywhere (for example, on the Desktop).

> [!NOTE]
> **If Windows shows "Windows protected your PC"** (the launcher is not digitally signed), click **More info** and then **Run anyway**.
> If `QTL-seq_GUI.exe` is blocked by the security policy of your organization, double-click `QTL-seq_GUI.vbs` instead.

### Specifying file paths

QTL-seq GUI runs inside WSL, so file paths are written in the Linux format. Files on the Windows drive `C:\` are under `/mnt/c/`. Files can also be selected with the **Browse** buttons.

| Item | Example |
| --- | --- |
| SAMtools | `/usr/bin/samtools` |
| BCFtools | `/usr/bin/bcftools` |
| BAM file (`C:\Users\<YourName>\Desktop\P1.bam`) | `/mnt/c/Users/<YourName>/Desktop/P1.bam` |
| Output folder (`C:\Users\<YourName>\Desktop`) | `/mnt/c/Users/<YourName>/Desktop` |

To uninstall, delete `QTL-seq_GUI.exe` and the extracted folder, and run `rm -r ~/QTLseqGUI` in Ubuntu.

---

## CUI version

The command-line version runs the same analysis without a graphical interface, which is useful on servers or for batch processing. On Linux, please use this version. It uses the same scripts in `src/` as the GUI and produces the same output.

1. Download this repository and install the required Python packages:

   ```bash
   git clone https://github.com/sakemiki/QTL-seq.git
   cd QTL-seq
   pip3 install -r requirements.txt
   ```

2. Open `Run.sh` in a text editor and edit the settings at the top (output folder, tool paths, FASTA file, BAM files, and parameters).
3. Run the analysis:

   ```bash
   bash Run.sh
   ```

Settings can also be overridden from the command line without editing the file:

```bash
bash Run.sh --output /path/to/output --window-size 1000000
```

> [!NOTE]
> Each BAM file must be sorted and have a corresponding `.bam.bai` index file in the same folder.
> The output folder must be different from the folder containing `Run.sh` and from `src/`.
> To see all available options, run `bash Run.sh --help`.

| Setting in `Run.sh` | Option | Description |
|---|---|---|
| `OUTPUT_FOLDER` | `--output` | Output folder |
| `SAMTOOLS` / `BCFTOOLS` | `--samtools` / `--bcftools` | Paths to SAMtools and BCFtools |
| `FASTA` | `--fasta` | Reference genome (FASTA) |
| `PATTERN` | `--pattern` | Parent pattern: `P1` / `P1P2` / `P1F1` / `P1P2F1` |
| `BULK` | `--bulk` | `single` / `double` |
| `BULK_TYPE` | `--bulk-type` | Population type: `RIL` / `F2` / `BC1F1` |
| `P1_BAM`, `P2_BAM`, `F1_BAM`, `ABULK_BAM`, `BBULK_BAM` | `--p1-bam` etc. | BAM files (unused ones are ignored) |
| `P1_NAME` … `BBULK_NAME` | `--p1-name` etc. | Sample names (must be unique) |
| `FILTER_DEPTH` | `--filter-depth` | Minimum depth for SNP filtering (default: 10) |
| `WINDOW_SIZE` / `STEP_SIZE` | `--window-size` / `--step-size` | Sliding window size and step (bp) |
| `BULK_NUMBER` | `--bulk-number` | Number of individuals per bulk (if different, the smaller value) |
| `REMOVAL_SNPINDEX` | `--removal-snpindex` | SNPs below this SNP-index in both bulks are removed |
| `ABULK_COLOR` / `BBULK_COLOR` / `DELTA_COLOR` | `--abulk-color` etc. | Plot colors (matplotlib color names; see `src/color.txt`) |
| `NUMBER_OF_ROW` | `--side` | Number of columns used to arrange the plots |

---

## Test data

`test_data/` contains a small dataset for checking that the software works.

| File | Description |
| --- | --- |
| `test_refarence.fasta`, `test_refarence.fasta.fai` | Reference sequence (3 chromosomes) and its index |
| `P1.sort.bam`, `P2.sort.bam`, `F1.sort.bam` | Parent 1, parent 2, and F1 |
| `Abulk.sort.bam`, `Bbulk.sort.bam` | Bulk A and bulk B |
| `*.bam.bai` | BAM index files |

To try it, select these files in the GUI (or set them in `Run.sh`) with pattern `P1P2F1` or `P1P2`, bulk `double`, and population type `F2`. With the CUI version, for example:

```bash
bash Run.sh --output ~/qtlseq_test_output \
    --samtools "$(which samtools)" --bcftools "$(which bcftools)" \
    --fasta test_data/test_refarence.fasta \
    --p1-bam test_data/P1.sort.bam --p2-bam test_data/P2.sort.bam \
    --f1-bam test_data/F1.sort.bam \
    --abulk-bam test_data/Abulk.sort.bam --bbulk-bam test_data/Bbulk.sort.bam
```

Plots are written to `result/` and tables (SNP-index, confidence intervals, peak regions) to `txt/` in the output folder.

---

## Source code

The source code corresponding to QTL-seq GUI ver. 1.02 is in `src/`. The distributed macOS and Windows (WSL) applications were built from these files. The Windows launcher, installer and build script are in `windows/`.

| File(s) | Description |
| --- | --- |
| `Run.py` | Main program of the GUI version. Start the GUI from this file. |
| `Run_CUI.py` | Main program of the CUI version (called from `Run.sh`). |
| `P_*.py`, `PP_*.py`, `PF_*.py`, `PPF_*.py` | Analysis modules for each parental/F1 sample combination (BAM splitting, VCF generation, SNP-index calculation, confidence intervals, peak detection, plotting). Files containing `singele` are used for single-bulk analysis. |
| `bam_*.py`, `make_vcf*.py`, `average*.py`, `confidence_interval.py`, `peak.py`, `plot.py`, `snp_sim.py`, `figure_legend*.py`, `move.py`, `Run_*.py` | Shared analysis and helper modules. |
| `F1_sim.txt`, `F2_*_sim.txt`, `BC1F1_*_sim.txt`, `RIL_*_sim.txt` | Simulated SNP-index tables used to calculate confidence intervals for each population type (F2, BC1F1, RIL) and bulk size (10–50 individuals). |
| `color.txt` | List of color names available for plots. |
| `QTL-seq_GUI_ver1_02.spec`, `build.sh`, `QTL_seq_GUI.icns` | PyInstaller build files and application icon. |

### Running the GUI from source

```bash
pip3 install -r requirements.txt
cd src
python3 Run.py
```

### Building the macOS application

The macOS application was built with Python 3.12 and PyInstaller 6.10.0 on macOS 15 (Apple silicon).

```bash
pip3 install -r requirements.txt
cd src
bash build.sh
```

The built application is written to `src/dist/`.
`build.sh` and `QTL-seq_GUI_ver1_02.spec` refer to the `tkinterdnd2` package at
`/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/tkinterdnd2`.
If your Python is installed elsewhere, change this path to the location shown by:

```bash
python3 -c "import tkinterdnd2, os; print(os.path.dirname(tkinterdnd2.__file__))"
```

### Windows version (`windows/`)

| File | Description |
| --- | --- |
| `Run_windows.patch` | Difference between `src/Run.py` and the `Run.py` used for the Windows version. Only the example paths shown in the input fields are changed (e.g., `/Users/XXXXX/Desktop` → `/mnt/c/Users/XXXXX/Desktop`); the analysis is identical. |
| `build_wsl.sh` | Builds the application (`QTL-seq_GUI_ver1_02_windows`) with Python 3.12 and PyInstaller inside WSL (Ubuntu, x86-64). |
| `launcher/launcher.py`, `launcher/QTL-seq_GUI.spec`, `launcher/QTL-seq_GUI.ico` | Source, PyInstaller build file and icon of the launcher `QTL-seq_GUI.exe` (built on Windows with Python 3.13). The launcher only starts the application in WSL. |
| `QTL-seq_GUI.vbs` | Alternative launcher. |
| `install.sh` | Installer included in the Windows ZIP file. |

To build the Windows application, copy `src/`, apply the patch, and run `build_wsl.sh` in WSL (edit the `SRC` path in the script to the folder containing the files):

```bash
cp -r src/ QTLseqGUI_windows_build/
cd QTLseqGUI_windows_build
patch -p0 Run.py < ../windows/Run_windows.patch
bash ../windows/build_wsl.sh
```

To build the launcher, run the following in the Command Prompt on Windows:

```bash
cd windows\launcher
pyinstaller QTL-seq_GUI.spec
```

---

## Usage and contact

See **`QTL-seq_GUI_Manual.pdf`** for how to use the tool and for details on the settings and output files.
For bug reports or requests, please use [Issues](https://github.com/sakemiki/QTL-seq/issues) or submit a Pull Request.
