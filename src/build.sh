pyinstaller \
--onefile \
--windowed \
--icon=QTL_seq_GUI.icns \
--hidden-import=tkinterdnd2 \
--add-data "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/tkinterdnd2:tkinterdnd2" \
--add-data "F1_sim.txt:." \
$(for i in $(seq 10 50); do echo --add-data "F2_${i}_sim.txt:."; done) \
$(for i in $(seq 10 50); do echo --add-data "BC1F1_${i}_sim.txt:."; done) \
$(for i in $(seq 10 50); do echo --add-data "RIL_${i}_sim.txt:."; done) \
--add-data "P_singele_snpindex.py:." \
--add-data "P_snpindex.py:." \
--add-data "PF_singele_snpindex.py:." \
--add-data "PF_snpindex.py:." \
--add-data "PP_singele_snpindex.py:." \
--add-data "PP_snpindex.py:." \
--add-data "PPF_singele_snpindex.py:." \
--add-data "PPF_snpindex.py:." \
--hidden-import=pandas \
--hidden-import=numpy \
Run.py \
--name=QTL-seq_GUI_ver1_02

