import subprocess

subprocess.Popen(
    ["wsl.exe", "--", "bash", "-lc",
     "cd ~/QTLseqGUI && ./QTL-seq_GUI_ver1_02_windows"],
    creationflags=subprocess.CREATE_NO_WINDOW,
)
