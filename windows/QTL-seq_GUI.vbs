Set sh = CreateObject("WScript.Shell")
sh.Run "wsl.exe -- bash -lc ""cd ~/QTLseqGUI && ./QTL-seq_GUI_ver1_02_windows""", 0, False
