import tkinter as tk
from tkinter import filedialog
import os
import sys
import glob
import shutil
import subprocess
from tkinter import messagebox, filedialog
import stat
from tkinterdnd2 import DND_FILES, TkinterDnD


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

    png_files = glob.glob(os.path.join(output_folder, '*.png'))
    for png_file in png_files:
        destination = os.path.join(result_folder, os.path.basename(png_file))
        if os.path.exists(destination):
            os.remove(destination)
        shutil.move(png_file, destination)

    bam_files = glob.glob(os.path.join(output_folder, '*.bam'))
    for bam_file in bam_files:
        destination = os.path.join(bam_folder, os.path.basename(bam_file))
        if os.path.exists(destination):
            os.remove(destination)
        shutil.move(bam_file, destination)

    bam_bai_files = glob.glob(os.path.join(output_folder, '*.bam.bai'))
    for bam_bai_file in bam_bai_files:
        destination = os.path.join(bam_folder, os.path.basename(bam_bai_file))
        if os.path.exists(destination):
            os.remove(destination)
        shutil.move(bam_bai_file, destination)

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS  
else:
    application_path = os.path.dirname(os.path.abspath(__file__)) 
file_paths = {
    'F1': ['F1_sim.txt'],
    'F2': [f'F2_{i}_sim.txt' for i in range(10, 51)],
    'BC1F1': [f'BC1F1_{i}_sim.txt' for i in range(10, 51)],
    'RIL': [f'RIL_{i}_sim.txt' for i in range(10, 51)]
}

for group, filenames in file_paths.items():
    for filename in filenames:
        var_name = f"{group}_{filename.split('_')[1]}_sim_path" if group != 'F1' else "F1_sim_path"
        globals()[var_name] = os.path.join(application_path, filename)

P_singele_snpindex=os.path.join(application_path, 'P_singele_snpindex.py')
P_snpindex=os.path.join(application_path, 'P_snpindex.py')
PF_singele_snpindex=os.path.join(application_path, 'PF_singele_snpindex.py')
PF_snpindex=os.path.join(application_path, 'PF_snpindex.py')
PP_singele_snpindex=os.path.join(application_path, 'PP_singele_snpindex.py')
PP_snpindex=os.path.join(application_path, 'PP_snpindex.py')
PPF_singele_snpindex=os.path.join(application_path, 'PPF_singele_snpindex.py')
PPF_snpindex=os.path.join(application_path, 'PPF_snpindex.py')

class DetailWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def select_folder(self):#output
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.out_entry.delete(0, tk.END)
            self.out_entry.insert(0, folder_path)
        else:
            desktop_path = os.path.expanduser("~/Desktop")
            self.out_entry.delete(0, tk.END)
            self.out_entry.insert(0, desktop_path)

    def browse_foldersamtools(self):#samtools
        file_path = filedialog.askopenfilename()
        if file_path:
            self.samtools_entry.delete(0, tk.END)
            self.samtools_entry.insert(0, file_path)
    
    def browse_folderbcftools(self):#bcftools
        file_path = filedialog.askopenfilename()
        if file_path:
            self.bcftools_entry.delete(0, tk.END)
            self.bcftools_entry.insert(0, file_path)
    
    def browse_folderfasta(self):#fasta
        file_path = filedialog.askopenfilename()
        if file_path:
            self.fasta_entry.delete(0, tk.END)
            self.fasta_entry.insert(0, file_path)
   
    def create_widgets(self):
        color0 =  "#FFFFFF"
        color1 =  "#8D9298"
        color2 =  "#97C2EE"
        color4 = "#7A41FF"

        canvas = tk.Canvas(self.master, width=1100, height=900, background=color0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.master, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = tk.Frame(canvas, bg=color0)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=1100)
        # コンテンツの高さに合わせてスクロール範囲を自動更新する
        # （固定値のままだと、項目が増えたときに下側（Nextボタンなど）へスクロールできなくなる）
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        self.title_frame = tk.Frame(scrollable_frame, bg=color4, relief="raised", borderwidth=8)
        self.title_frame.pack(fill="x", padx=20, pady=[10, 0])
        self.title_label = tk.Label(self.title_frame, text="QTL-seq_GUI", font=("Arial", 25), bg=color4, fg="black")
        self.title_label.pack(anchor="center")
######################################################################################################################################################################################################################################
        self.out_frame = tk.Frame(scrollable_frame, bg=color2)
        self.out_frame.pack(fill="x", padx=20, pady=[10, 0])

        self.path_label = tk.Label(self.out_frame, text="Enter the path to the file", font=("Arial", 20), fg='black', bg=color2)
        self.path_label.pack(side="left")

        self.out_frame = tk.Frame(scrollable_frame, bg=color1)
        self.out_frame.pack(fill="x", padx=20, pady=0)
        
        self.out_frame = tk.Frame(scrollable_frame, bg=color1)
        self.out_frame.pack(fill="x", padx=20, pady=0)
        self.out_label = tk.Label(self.out_frame, text="Output folder", bg=color1, fg="black", width=11)
        self.out_label.pack(side="left")
        self.out_entry = tk.Entry(self.out_frame, fg="black", bg=color0, width=60)  
        self.out_entry.insert(0, "/Users/XXXXX/Desktop")
        #self.out_entry.insert(0, "/Volumes/HD-PUSU3-D/sakemoto_data/ronbun_soybean/test")
        self.out_entry.pack(side="left", fill="x", expand=True, padx=10)  
        self.out_entry.configure(highlightbackground=color1)
        self.out_button = tk.Button(self.out_frame, text="Browse", command=self.select_folder, fg="black")
        self.out_button.pack(side="right")
        self.out_button.configure(highlightbackground=color1)
        def drop_out_file(event):
            file_path = self.tk.splitlist(event.data)[0]
            self.out_entry.delete(0, tk.END)
            self.out_entry.insert(0, file_path)

        self.out_entry.drop_target_register(DND_FILES)
        self.out_entry.dnd_bind('<<Drop>>', drop_out_file)

        self.bam_frame = tk.Frame(scrollable_frame, bg=color1)
        self.bam_frame.pack(fill="x", padx=20, pady=0)
        self.samtools_label = tk.Label(self.bam_frame, text="samtools", bg=color1, fg="black", width=11)
        self.samtools_label.pack(side="left")
        self.samtools_entry = tk.Entry(self.bam_frame, fg='black', bg=color0, width=60) 
        #self.samtools_entry.insert(0, "/Users/sakemoto/Desktop/tools/samtools-1.20/samtools")
        self.samtools_entry.insert(0, "/Users/XXXXX/Desktop/samtools")
        self.samtools_entry.pack(side="left", fill="x", expand=True, padx=10)
        self.samtools_entry.configure(highlightbackground=color1)
        self.samtools_button = tk.Button(self.bam_frame, text="Browse", command=self.browse_foldersamtools, fg="black")
        self.samtools_button.pack(side="right")
        self.samtools_button.configure(highlightbackground=color1)
        # samtools ドラッグ＆ドロップ処理
        def drop_samtools_file(event):
            file_path = self.tk.splitlist(event.data)[0]
            self.samtools_entry.delete(0, tk.END)
            self.samtools_entry.insert(0, file_path)
        self.samtools_entry.drop_target_register(DND_FILES)
        self.samtools_entry.dnd_bind('<<Drop>>', drop_samtools_file)


        self.bam_frame = tk.Frame(scrollable_frame, bg=color1)
        self.bam_frame.pack(fill="x", padx=20, pady=0)
        self.bcftools_label = tk.Label(self.bam_frame, text="bcftools", bg=color1, fg="black", width=11)
        self.bcftools_label.pack(side="left")
        self.bcftools_entry = tk.Entry(self.bam_frame, fg='black', bg=color0, width=60)  
        #self.bcftools_entry.insert(0, "/Users/sakemoto/Desktop/tools/bcftools-1.20/bcftools")
        self.bcftools_entry.insert(0, "/Users/XXXXX/Desktop/bcftools")
        self.bcftools_entry.pack(side="left", fill="x", expand=True, padx=10)
        self.bcftools_entry.configure(highlightbackground=color1)
        self.bcftools_button = tk.Button(self.bam_frame, text="Browse", command=self.browse_folderbcftools, fg="black")
        self.bcftools_button.pack(side="right")
        self.bcftools_button.configure(highlightbackground=color1)
        # bcftools ドラッグ＆ドロップ処理
        def drop_bcftools_file(event):
            file_path = self.tk.splitlist(event.data)[0]
            self.bcftools_entry.delete(0, tk.END)
            self.bcftools_entry.insert(0, file_path)
        self.bcftools_entry.drop_target_register(DND_FILES)
        self.bcftools_entry.dnd_bind('<<Drop>>', drop_bcftools_file)

        self.bam_frame = tk.Frame(scrollable_frame, bg=color1)
        self.bam_frame.pack(fill="x", padx=20, pady=0)
        self.fasta_label = tk.Label(self.bam_frame, text="fasta", bg=color1, fg="black", width=11)
        self.fasta_label.pack(side="left")
        self.fasta_entry = tk.Entry(self.bam_frame, fg='black', bg=color0, width=60) 
        self.fasta_entry.insert(0, "/Users/Desktop/XXXXX.fna")
        #self.fasta_entry.insert(0, "/Users/sakemoto/Desktop/alignment/test_data/test_refarence.fasta")
        self.fasta_entry.pack(side="left", fill="x", expand=True, padx=10)
        self.fasta_entry.configure(highlightbackground=color1)
        self.fasta_button = tk.Button(self.bam_frame, text="Browse", command=self.browse_folderfasta, fg="black")
        self.fasta_button.pack(side="right")
        self.fasta_button.configure(highlightbackground=color1)   
        # fasta ドラッグ＆ドロップ処理
        def drop_fasta_file(event):
            file_path = self.tk.splitlist(event.data)[0]
            self.fasta_entry.delete(0, tk.END)
            self.fasta_entry.insert(0, file_path)
        self.fasta_entry.drop_target_register(DND_FILES)
        self.fasta_entry.dnd_bind('<<Drop>>', drop_fasta_file)
        
        self.name = tk.Frame(scrollable_frame, bg=color2)
        self.name.pack(fill="x", padx=20, pady=[10,0])

        self.entry_label = tk.Label(self.name, text="Enter filtering values", font=("Arial", 20), fg='black', bg=color2)
        self.entry_label.pack(side="left")

        self.name = tk.Frame(scrollable_frame, bg=color1)
        self.name.pack(fill="x", padx=20, pady=0)

        self.depth_label = tk.Label(self.name, text="filter depth", bg=color1,fg="black", width=11)
        self.depth_label.pack(side="left")
        self.depth_entry = tk.Entry(self.name, width=8, fg="black",bg=color0)
        self.depth_entry.pack(side="left",padx=0)
        self.depth_entry.configure(highlightbackground=color1)
        self.depth_entry.insert(0, '10')

        self.windowsize_label = tk.Label(self.name, text="window size", bg=color1,fg="black", width=11)
        self.windowsize_label.pack(side="left")
        self.windowsize_entry = tk.Entry(self.name, width=8, fg="black",bg=color0)
        self.windowsize_entry.pack(side="left",padx=0)
        self.windowsize_entry.configure(highlightbackground=color1)
        self.windowsize_entry.insert(0, '2000000')

        self.stepsize_label = tk.Label(self.name, text="step size", bg=color1,fg="black", width=11)
        self.stepsize_label.pack(side="left")
        self.stepsize_entry = tk.Entry(self.name, width=8, fg="black",bg=color0)
        self.stepsize_entry.pack(side="left",padx=0)
        self.stepsize_entry.configure(highlightbackground=color1)
        self.stepsize_entry.insert(0, '50000')

        self.bulknumber_label = tk.Label(self.name, text="bulk number", bg=color1,fg="black", width=11)
        self.bulknumber_label.pack(side="left")
        self.bulknumber_entry = tk.Entry(self.name, width=8, fg="black",bg=color0)
        self.bulknumber_entry.pack(side="left",padx=0)
        self.bulknumber_entry.configure(highlightbackground=color1)
        self.bulknumber_entry.insert(0, '15')

        self.removal_label = tk.Label(self.name, text="Removal SNP-index value", bg=color1,fg="black", width=20)
        self.removal_label.pack(side="left")
        self.removal_entry = tk.Entry(self.name, width=8, fg="black",bg=color0)
        self.removal_entry.pack(side="left",padx=0)
        self.removal_entry.configure(highlightbackground=color1)
        self.removal_entry.insert(0, '0.3')

        self.name = tk.Frame(scrollable_frame, bg=color2)
        self.name.pack(fill="x", padx=20, pady=[10,0])

        self.entry_label = tk.Label(self.name, text="Graph options", font=("Arial", 20), fg='black', bg=color2)
        self.entry_label.pack(side="left")

        self.name = tk.Frame(scrollable_frame, bg=color1)
        self.name.pack(fill="x", padx=20, pady=0)


        # 代表的な色（色見本のラジオボタン選択肢）
        color_options = [
            ("Red", "red"),
            ("Blue", "blue"),
            ("Yellow", "yellow"),
            ("Green", "green"),
            ("Orange", "orange"),
            ("Purple", "purple"),
            ("Pink", "pink"),
            ("Brown", "brown"),
            ("Gray", "gray"),
            ("Black", "black"),
        ]

        def add_color_swatches(row, variable, options, size=20):
            """四角ではなく丸い色見本（Canvasの円）を並べる。
            クリックで variable に色名をセットし、選択中の円だけ枠を太くする。"""
            circles = {}  # color_value -> (canvas, item_id)
            pad = 2

            def refresh_look(*_):
                selected = variable.get()
                for color_value, (cv, item_id) in circles.items():
                    width = 3 if color_value == selected else 1
                    cv.itemconfig(item_id, width=width)

            def make_selector(color_value):
                def _select(event=None):
                    variable.set(color_value)
                return _select

            for label_text, color_value in options:
                cv = tk.Canvas(row, width=size, height=size, bg=color1, highlightthickness=0, cursor="hand2")
                item_id = cv.create_oval(pad, pad, size - pad, size - pad, fill=color_value, outline="black", width=1)
                cv.bind("<Button-1>", make_selector(color_value))
                cv.pack(side="left", padx=5)
                circles[color_value] = (cv, item_id)

            variable.trace_add("write", refresh_look)
            refresh_look()

        # Abulk color
        self.abulk_color_row = tk.Frame(self.name, bg=color1)
        self.abulk_color_row.pack(fill="x", pady=2)
        self.abulk_color_label = tk.Label(self.abulk_color_row, text="Abulk color", bg=color1, fg="black", width=11)
        self.abulk_color_label.pack(side="left", padx=(0, 5))
        self.abulk_color_var = tk.StringVar(value='green')
        add_color_swatches(self.abulk_color_row, self.abulk_color_var, color_options)
        self.abulk_color_name_label = tk.Label(self.abulk_color_row, textvariable=self.abulk_color_var, bg=color1, fg="black", width=13, anchor="w")
        self.abulk_color_name_label.pack(side="left", padx=(10, 0))

        # Bbulk color（デフォルトの gold も選択肢に含める）
        self.bbulk_color_row = tk.Frame(self.name, bg=color1)
        self.bbulk_color_row.pack(fill="x", pady=2)
        self.bbulk_color_label = tk.Label(self.bbulk_color_row, text="Bbulk color", bg=color1, fg="black", width=11)
        self.bbulk_color_label.pack(side="left", padx=(0, 5))
        self.bbulk_color_var = tk.StringVar(value='gold')
        add_color_swatches(self.bbulk_color_row, self.bbulk_color_var, color_options + [("Gold", "gold")])
        self.bbulk_color_name_label = tk.Label(self.bbulk_color_row, textvariable=self.bbulk_color_var, bg=color1, fg="black", width=13, anchor="w")
        self.bbulk_color_name_label.pack(side="left", padx=(10, 0))

        # Delta color（デフォルトの midnightblue も選択肢に含める）
        self.delta_color_row = tk.Frame(self.name, bg=color1)
        self.delta_color_row.pack(fill="x", pady=2)
        self.delta_color_label = tk.Label(self.delta_color_row, text="Delta color", bg=color1, fg="black", width=11)
        self.delta_color_label.pack(side="left", padx=(0, 5))
        self.delta_color_var = tk.StringVar(value='midnightblue')
        add_color_swatches(self.delta_color_row, self.delta_color_var, color_options + [("Midnight Blue", "midnightblue")])
        self.delta_color_name_label = tk.Label(self.delta_color_row, textvariable=self.delta_color_var, bg=color1, fg="black", width=13, anchor="w")
        self.delta_color_name_label.pack(side="left", padx=(10, 0))

        self.side_row = tk.Frame(self.name, bg=color1)
        self.side_row.pack(fill="x", pady=2)
        self.side_label = tk.Label(self.side_row, text="Number of row", bg=color1, fg="black")
        self.side_label.pack(side="left", padx=(0, 5))
        self.side_entry = tk.Entry(self.side_row, width=8, fg="black", bg=color0)
        self.side_entry.pack(side="left", padx=(0, 15))
        self.side_entry.configure(highlightbackground=color1)
        self.side_entry.insert(0, '2')

        
######################################################################################################################################################################################################################################
        self.selection_frame = tk.Frame(scrollable_frame, bg=color2)
        self.selection_frame.pack(fill="x", padx=20, pady=[10,0])

        self.option_label = tk.Label(self.selection_frame, text="Select processing details", font=("Arial", 20), fg='black', bg=color2)
        self.option_label.pack(side="left")

        self.selection_frame = tk.Frame(scrollable_frame, bg=color1)
        self.selection_frame.pack(fill="x", padx=20, pady=0)
        self.selection_frame = tk.Frame(scrollable_frame, bg=color1)
        self.selection_frame.pack(fill="x", padx=20, pady=0)
        self.selection_frame = tk.Frame(scrollable_frame, bg=color1)
        self.selection_frame.pack(fill="x", padx=20, pady=0)

        self.selection_frame = tk.Frame(scrollable_frame, bg=color1)
        self.selection_frame.pack(fill="x", padx=20, pady=0)
        self.pattern_label = tk.Label(self.selection_frame, text="pattern", font=("Arial", 15), fg='black', bg=color1, width=11)
        self.pattern_label.pack(side="left")
        self.filter_pattern_selection_var = tk.IntVar(value=0)
        self.P1_selection_radiobutton = tk.Radiobutton(self.selection_frame, text="P1", variable=self.filter_pattern_selection_var, value=1, fg='black', bg=color1, width=11)
        self.P1_selection_radiobutton.pack(side="left")
        self.P1P2_selection_radiobutton = tk.Radiobutton(self.selection_frame, text="P1 , P2", variable=self.filter_pattern_selection_var, value=2, fg='black', bg=color1, width=11)
        self.P1P2_selection_radiobutton.pack(side="left")
        self.P1F1_selection_radiobutton = tk.Radiobutton(self.selection_frame, text="P1 , F1", variable=self.filter_pattern_selection_var, value=4, fg='black', bg=color1, width=11)
        self.P1F1_selection_radiobutton.pack(side="left")
        self.P1P2F1_selection_radiobutton = tk.Radiobutton(self.selection_frame, text="P1 , P2 , F1", variable=self.filter_pattern_selection_var, value=3, fg='black', bg=color1, width=11)
        self.P1P2F1_selection_radiobutton.pack(side="left")
        
        self.selection_frame = tk.Frame(scrollable_frame, bg=color1)
        self.selection_frame.pack(fill="x", padx=20, pady=0)
        self.Bulk_single_double_ = tk.Label(self.selection_frame, text="Bulk", font=("Arial", 15), fg='black', bg=color1, width=11)
        self.Bulk_single_double_.pack(side="left")
        self.Bulk_single_double_selection_var = tk.IntVar(value=0)
        self.single_selection_radiobutton = tk.Radiobutton(self.selection_frame, text="single", variable=self.Bulk_single_double_selection_var, value=1, fg='black', bg=color1, width=11)
        self.single_selection_radiobutton.pack(side="left")
        self.double_selection_radiobutton = tk.Radiobutton(self.selection_frame, text="double", variable=self.Bulk_single_double_selection_var, value=2, fg='black', bg=color1, width=11)
        self.double_selection_radiobutton.pack(side="left")

        self.selection_frame = tk.Frame(scrollable_frame, bg=color1)
        self.selection_frame.pack(fill="x", padx=20, pady=0)
        self.bulktype_label = tk.Label(self.selection_frame, text="Bulk type", font=("Arial", 15), fg='black', bg=color1, width=11)
        self.bulktype_label.pack(side="left")
        self.selection_var = tk.IntVar(value=0)
        self.RIL_selection_radiobutton = tk.Radiobutton(self.selection_frame, text="RIL", variable=self.selection_var, value=1, fg='black', bg=color1, width=11)
        self.RIL_selection_radiobutton.pack(side="left")
        self.F2_selection_radiobutton = tk.Radiobutton(self.selection_frame, text="F2", variable=self.selection_var, value=2, fg='black', bg=color1, width=11)
        self.F2_selection_radiobutton.pack(side="left")
        self.BC1F1_selection_radiobutton = tk.Radiobutton(self.selection_frame, text="BC1F1", variable=self.selection_var, value=3, fg='black', bg=color1, width=11)
        self.BC1F1_selection_radiobutton.pack(side="left")



######################################################################################################################################################################################################################################
        self.run_frame = tk.Frame(scrollable_frame, bg=color0)
        self.run_frame.pack(fill="x", padx=20, pady=[10, 0])
        self.run_button = tk.Button(self.run_frame, text="Next", command=self.run_script, fg="black", width=5, height=2, font=("Arial", 16))
        self.run_button.pack(side="right", padx=20, pady=[0, 10])
######################################################################################################################################################################################################################################

######################################################################################################################################################################################################################################
    def run_script(self):

        Bulk_single_double = self.Bulk_single_double_selection_var.get()
        fasta = self.fasta_entry.get()
        output_folder = self.out_entry.get()
        samtools = self.samtools_entry.get()
        bcftools = self.bcftools_entry.get()
        filter_depth = int(self.depth_entry.get())
        window_size = int(self.windowsize_entry.get())
        step_size = int(self.stepsize_entry.get())
        bulk_number = int(self.bulknumber_entry.get()) if self.bulknumber_entry.get().isdigit() else 111111
        removal_SNPindex = float(self.removal_entry.get())
        abulk_color = self.abulk_color_var.get()
        bbulk_color = self.bbulk_color_var.get()
        delta_color = self.delta_color_var.get()
        side = int(self.side_entry.get())
        bulk_type = self.selection_var.get()
        pattern = self.filter_pattern_selection_var.get()


        if not bulk_type:
            messagebox.showerror("Error", "plese select bulk type option")
            return

        if not pattern:
            messagebox.showerror("Error", "plese select filter pattern option")
            return

        # 設定保存
        self.master.settings = {
            "Bulk_single_double": Bulk_single_double,
            "fasta": fasta,
            "output_folder": output_folder,
            "samtools": samtools,
            "bcftools": bcftools,
            "filter_depth": filter_depth,
            "window_size": window_size,
            "step_size": step_size,
            "bulk_number": bulk_number,
            "removal_SNPindex": removal_SNPindex,
            "abulk_color": abulk_color,
            "bbulk_color": bbulk_color,
            "delta_color": delta_color,
            "side": side,
            "bulk_type": bulk_type,
            "pattern": pattern,
        }

        # rootのwidgetを全部削除（これが重要）
        for widget in self.master.winfo_children():
            widget.destroy()

        # 次画面
        BamWindow(self.master, pattern, Bulk_single_double)
#######################################################################################################################################################################################################################################
class BamWindow(tk.Frame):
    def __init__(self, master, pattern, bulk):
        super().__init__(master)
        self.master = master
        self.pattern = pattern
        self.bulk = bulk
        self.pack()
        self.create_widgets()

    def save_bam_settings(self):
        self.master.bam_settings = {
            "p1_bam": self.p1_bam_entry.get(),
            "p1_name": self.p1_name.get(),
            "p2_bam": self.p2_bam_entry.get() if hasattr(self, "p2_bam_entry") else "",
            "p2_name": self.p2_name.get() if hasattr(self, "p2_name") else "",
            "f1_bam": self.f1_bam_entry.get() if hasattr(self, "f1_bam_entry") else "",
            "f1_name": self.f1_name.get() if hasattr(self, "f1_name") else "",
            "abulk_bam": self.abulk_bam_entry.get(),
            "abulk_name": self.abulk_name.get(),
            "bbulk_bam": self.bbulk_bam_entry.get() if hasattr(self, "bbulk_bam_entry") else "",
            "bbulk_name": self.bbulk_name.get() if hasattr(self, "bbulk_name") else ""
        }

    def go_back(self):
        self.save_bam_settings()
        settings = self.master.settings

        # rootのwidget削除
        for widget in self.master.winfo_children():
            widget.destroy()
        # DetailWindow再生成
        detail = DetailWindow(master=self.master)

        # 設定復元
        detail.out_entry.delete(0, tk.END)
        detail.out_entry.insert(0, settings["output_folder"])

        detail.samtools_entry.delete(0, tk.END)
        detail.samtools_entry.insert(0, settings["samtools"])

        detail.bcftools_entry.delete(0, tk.END)
        detail.bcftools_entry.insert(0, settings["bcftools"])

        detail.fasta_entry.delete(0, tk.END)
        detail.fasta_entry.insert(0, settings["fasta"])

        detail.depth_entry.delete(0, tk.END)
        detail.depth_entry.insert(0, settings["filter_depth"])

        detail.windowsize_entry.delete(0, tk.END)
        detail.windowsize_entry.insert(0, settings["window_size"])

        detail.stepsize_entry.delete(0, tk.END)
        detail.stepsize_entry.insert(0, settings["step_size"])

        detail.bulknumber_entry.delete(0, tk.END)
        detail.bulknumber_entry.insert(0, settings["bulk_number"])

        detail.removal_entry.delete(0, tk.END)
        detail.removal_entry.insert(0, settings["removal_SNPindex"])

        detail.selection_var.set(settings["bulk_type"])
        detail.filter_pattern_selection_var.set(settings["pattern"])
        detail.Bulk_single_double_selection_var.set(settings["Bulk_single_double"])

        detail.abulk_color_var.set(settings["abulk_color"])
        detail.bbulk_color_var.set(settings["bbulk_color"])
        detail.delta_color_var.set(settings["delta_color"])
        detail.side_entry.delete(0, tk.END)
        detail.side_entry.insert(0, settings["side"])
    ############################################################
    # file browse
    ############################################################

    def browse_folderP1bam(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.p1_entry.delete(0, tk.END)
            self.p1_entry.insert(0, file_path)

    def browse_folderP2bam(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.p2_entry.delete(0, tk.END)
            self.p2_entry.insert(0, file_path)

    def browse_folderF1bam(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.f1_entry.delete(0, tk.END)
            self.f1_entry.insert(0, file_path)

    def browse_folderAbam(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.abulk_entry.delete(0, tk.END)
            self.abulk_entry.insert(0, file_path)

    def browse_folderBbam(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.bbulk_entry.delete(0, tk.END)
            self.bbulk_entry.insert(0, file_path)

    ############################################################
    # GUI
    ############################################################

    def create_widgets(self):

        color0 = "#FFFFFF"
        color1 = "#8D9298"
        color2 = "#97C2EE"
        color4 = "#7A41FF"

        canvas = tk.Canvas(self.master, width=1100, height=900, background=color0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(self.master, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        self.scrollable_frame = tk.Frame(canvas, bg=color0)
        scrollable_frame = self.scrollable_frame
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=1100)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        self.canvas = canvas
        # title
        title_frame = tk.Frame(scrollable_frame, bg=color4, relief="raised", borderwidth=8)
        title_frame.pack(fill="x", padx=20, pady=[10, 0])
        tk.Label(
            title_frame,
            text="QTL-seq_GUI",
            font=("Arial", 25),
            bg=color4,
            fg="black"
        ).pack()
        # header
        header = tk.Frame(scrollable_frame, bg=color2)
        header.pack(fill="x", padx=20, pady=10)
        tk.Label(header,text="Enter the path to the file",font=("Arial", 20),bg=color2,fg="black").pack(side="left")
        # P1 bam
        self.bam_frame = tk.Frame(scrollable_frame, bg=color1)
        self.bam_frame.pack(fill="x", padx=20, pady=0)
        self.p1_bam_label = tk.Label(self.bam_frame, text="P1 bam", bg=color1, fg="black", width=11)
        self.p1_bam_label.pack(side="left")
        self.p1_bam_entry = tk.Entry(self.bam_frame, fg='black', bg=color0, width=60)  
        self.p1_bam_entry.insert(0, "/Users/XXXXX/Desktop/P1.bam")
        #self.p1_bam_entry.insert(0, "/Users/sakemoto/Desktop/alignment/test_data/P1.sort.bam")
        #self.p1_bam_entry.insert(0, "/Volumes/HD-PUSU3-D/sakemoto_data/ronbun_soybean/Mig_seq_bam/Ref_v1/Misuzudaizu_merged.bam")
        self.p1_bam_entry.pack(side="left", fill="x", expand=True, padx=10)
        self.p1_bam_entry.configure(highlightbackground=color1)
        self.p1_bam_button = tk.Button(self.bam_frame, text="Browse", command=self.browse_folderP1bam, fg="black")
        self.p1_bam_button.pack(side="right")
        self.p1_bam_button.configure(highlightbackground=color1)
        def drop_p1bam_file(event):
            file_path = self.tk.splitlist(event.data)[0]
            self.p1_bam_entry.delete(0, tk.END)
            self.p1_bam_entry.insert(0, file_path)
        self.p1_bam_entry.drop_target_register(DND_FILES)
        self.p1_bam_entry.dnd_bind('<<Drop>>', drop_p1bam_file)
        # P2 bam
        if self.pattern in [2,3]:
            self.bam_frame = tk.Frame(scrollable_frame, bg=color1)
            self.bam_frame.pack(fill="x", padx=20, pady=0)
            self.p2_bam_label = tk.Label(self.bam_frame, text="P2 bam", bg=color1, fg="black", width=11)
            self.p2_bam_label.pack(side="left")
            self.p2_bam_entry = tk.Entry(self.bam_frame, fg='black', bg=color0, width=60)  
            #self.p2_bam_entry.insert(0, "/Volumes/HD-PUSU3-D/sakemoto_data/ronbun_soybean/Mig_seq_bam/Ref_v1/Moshidou_merged.bam")
            #self.p2_bam_entry.insert(0, "/Users/sakemoto/Desktop/alignment/test_data/P2.sort.bam")
            self.p2_bam_entry.insert(0, "/Users/XXXXX/Desktop/P2.bam")
            self.p2_bam_entry.pack(side="left", fill="x", expand=True, padx=10)
            self.p2_bam_entry.configure(highlightbackground=color1)
            self.p2_bam_button = tk.Button(self.bam_frame, text="Browse", command=self.browse_folderP2bam, fg="black")
            self.p2_bam_button.pack(side="right")
            self.p2_bam_button.configure(highlightbackground=color1)
            def drop_p2bam_file(event):
                file_path = self.tk.splitlist(event.data)[0]
                self.p2_bam_entry.delete(0, tk.END)
                self.p2_bam_entry.insert(0, file_path)
            self.p2_bam_entry.drop_target_register(DND_FILES)
            self.p2_bam_entry.dnd_bind('<<Drop>>', drop_p2bam_file)
        # F1 bam
        if self.pattern in [3,4]:
            self.bam_frame = tk.Frame(scrollable_frame, bg=color1)
            self.bam_frame.pack(fill="x", padx=20, pady=0)
            self.f1_bam_label = tk.Label(self.bam_frame, text="F1 bam", bg=color1, fg="black", width=11)
            self.f1_bam_label.pack(side="left")
            self.f1_bam_entry = tk.Entry(self.bam_frame, fg='black', bg=color0, width=60)  
            #self.f1_bam_entry.insert(0, "/Volumes/HD-PUSU3-D/sakemoto_data/ronbun_soybean/Mig_seq_bam/Ref_v1/F1.sort.bam")
            #self.f1_bam_entry.insert(0, "/Users/sakemoto/Desktop/alignment/test_data/F1.sort.bam")
            self.f1_bam_entry.insert(0, "/Users/XXXXX/Desktop/F1.bam")
            self.f1_bam_entry.pack(side="left", fill="x", expand=True, padx=10)
            self.f1_bam_entry.configure(highlightbackground=color1)
            self.p2_bam_button = tk.Button(self.bam_frame, text="Browse", command=self.browse_folderF1bam, fg="black")
            self.p2_bam_button.pack(side="right")
            self.p2_bam_button.configure(highlightbackground=color1)
            def drop_f1bam_file(event):
                file_path = self.tk.splitlist(event.data)[0]
                self.f1_bam_entry.delete(0, tk.END)
                self.f1_bam_entry.insert(0, file_path)
            self.f1_bam_entry.drop_target_register(DND_FILES)
            self.f1_bam_entry.dnd_bind('<<Drop>>', drop_f1bam_file)
        # Abulk bam
        self.bam_frame = tk.Frame(scrollable_frame, bg=color1)
        self.bam_frame.pack(fill="x", padx=20, pady=0)
        self.abulk_bam_label = tk.Label(self.bam_frame, text="Abulk bam", bg=color1, fg="black", width=11)
        self.abulk_bam_label.pack(side="left")
        self.abulk_bam_entry = tk.Entry(self.bam_frame, fg='black', bg=color0, width=60)  
        #self.abulk_bam_entry.insert(0, "/Volumes/HD-PUSU3-D/sakemoto_data/ronbun_soybean/Mig_seq_bam/Ref_v1/early_bulk.sort.bam")
        #self.abulk_bam_entry.insert(0, "/Users/sakemoto/Desktop/alignment/test_data/Abulk.sort.bam")
        self.abulk_bam_entry.insert(0, "/Users/XXXXX/Desktop/Abulk.bam")
        self.abulk_bam_entry.pack(side="left", fill="x", expand=True, padx=10)
        self.abulk_bam_entry.configure(highlightbackground=color1)
        self.p1_bam_button = tk.Button(self.bam_frame, text="Browse", command=self.browse_folderAbam, fg="black")
        self.p1_bam_button.pack(side="right")
        self.p1_bam_button.configure(highlightbackground=color1)
        def drop_abulkbam_file(event):
            file_path = self.tk.splitlist(event.data)[0]
            self.abulk_bam_entry.delete(0, tk.END)
            self.abulk_bam_entry.insert(0, file_path)
        self.abulk_bam_entry.drop_target_register(DND_FILES)
        self.abulk_bam_entry.dnd_bind('<<Drop>>', drop_abulkbam_file)
        # Bbulk bam
        if self.bulk == 2:
            self.bam_frame = tk.Frame(scrollable_frame, bg=color1)
            self.bam_frame.pack(fill="x", padx=20, pady=0)
            self.bbulk_bam_label = tk.Label(self.bam_frame, text="Bbulk bam", bg=color1, fg="black", width=11)
            self.bbulk_bam_label.pack(side="left")
            self.bbulk_bam_entry = tk.Entry(self.bam_frame, fg='black', bg=color0, width=60)  
            self.bbulk_bam_entry.insert(0, "/Users/XXXXX/Desktop/Bbulk.bam")
            #self.bbulk_bam_entry.insert(0, "/Volumes/HD-PUSU3-D/sakemoto_data/ronbun_soybean/Mig_seq_bam/Ref_v1/late_bulk.sort.bam")
            #self.bbulk_bam_entry.insert(0, "/Users/sakemoto/Desktop/alignment/test_data/Bbulk.sort.bam")
            self.bbulk_bam_entry.pack(side="left", fill="x", expand=True, padx=10)
            self.bbulk_bam_entry.configure(highlightbackground=color1)
            self.p1_bam_button = tk.Button(self.bam_frame, text="Browse", command=self.browse_folderBbam, fg="black")
            self.p1_bam_button.pack(side="right")
            self.p1_bam_button.configure(highlightbackground=color1)
            def drop_p1bam_file(event):
                file_path = self.tk.splitlist(event.data)[0]
                self.bbulk_bam_entry.delete(0, tk.END)
                self.bbulk_bam_entry.insert(0, file_path)
            self.bbulk_bam_entry.drop_target_register(DND_FILES)
            self.bbulk_bam_entry.dnd_bind('<<Drop>>', drop_p1bam_file)
        # sample name header
        name_title = tk.Frame(scrollable_frame, bg=color2)
        name_title.pack(fill="x", padx=20, pady=[10,0])
        tk.Label(name_title,text="Enter the name of sample",font=("Arial",20),bg=color2,fg="black").pack(side="left")
        # sample name input
        name_frame = tk.Frame(scrollable_frame, bg=color1)
        name_frame.pack(fill="x", padx=20)
        # P1
        row = tk.Frame(name_frame, bg=color1)
        row.pack(fill="x")
        tk.Label(row,text="P1 name",bg=color1,fg="black",width=11).pack(side="left")
        self.p1_name = tk.Entry(row,bg=color0,fg="black",width=20,borderwidth=0,highlightthickness=0,relief="flat")
        self.p1_name.insert(0,"P1")
        self.p1_name.pack(side="left",padx=10)
        # P2
        if self.pattern in [2,3]:
            row = tk.Frame(name_frame, bg=color1)
            row.pack(fill="x")
            tk.Label(row,text="P2 name",bg=color1,fg="black",width=11).pack(side="left")
            self.p2_name = tk.Entry(row,bg=color0,fg="black",width=20,borderwidth=0,highlightthickness=0,relief="flat")
            self.p2_name.insert(0,"P2")
            self.p2_name.pack(side="left",padx=10)
        # F1
        if self.pattern in [3,4]:
            row = tk.Frame(name_frame, bg=color1)
            row.pack(fill="x")
            tk.Label(row,text="F1 name",bg=color1,fg="black",width=11).pack(side="left")
            self.f1_name = tk.Entry(row,bg=color0,fg="black",width=20,borderwidth=0,highlightthickness=0,relief="flat")
            self.f1_name.insert(0,"F1")
            self.f1_name.pack(side="left",padx=10)
        # Abulk
        row = tk.Frame(name_frame, bg=color1)
        row.pack(fill="x")
        tk.Label(row,text="A-bulk name",bg=color1,fg="black",width=11).pack(side="left")
        self.abulk_name = tk.Entry(row,bg=color0,fg="black",width=20,borderwidth=0,highlightthickness=0,relief="flat")
        self.abulk_name.insert(0,"Abulk")
        self.abulk_name.pack(side="left",padx=10)
        # Bbulk
        if self.bulk == 2:
            row = tk.Frame(name_frame, bg=color1)
            row.pack(fill="x")
            tk.Label(row,text="B-bulk name",bg=color1,fg="black",width=11).pack(side="left")
            self.bbulk_name = tk.Entry(row,bg=color0,fg="black",width=20,borderwidth=0,highlightthickness=0,relief="flat")
            self.bbulk_name.insert(0,"Bbulk")
            self.bbulk_name.pack(side="left",padx=10)
        # Run
        self.run_frame = tk.Frame(scrollable_frame, bg=color0)
        self.run_frame.pack(fill="x", padx=20, pady=[10, 0])

        self.back_button = tk.Button(self.run_frame,text="Back",command=self.go_back,fg="black", width=5,height=2,font=("Arial", 16))
        self.back_button.pack(side="left", padx=20, pady=[0, 10])

        self.run_button = tk.Button(self.run_frame,text="Run",command=self.run_analysis,fg="black", width=5,  height=2,font=("Arial", 16))
        self.run_button.pack(side="right", padx=20, pady=[0, 10])

        # 画面作成後に復元
        if hasattr(self.master, "bam_settings"):
            bs = self.master.bam_settings

            self.p1_bam_entry.delete(0, tk.END)
            self.p1_bam_entry.insert(0, bs["p1_bam"])

            self.p1_name.delete(0, tk.END)
            self.p1_name.insert(0, bs["p1_name"])

            if hasattr(self, "p2_bam_entry"):
                self.p2_bam_entry.delete(0, tk.END)
                self.p2_bam_entry.insert(0, bs["p2_bam"])
                self.p2_name.delete(0, tk.END)
                self.p2_name.insert(0, bs["p2_name"])

            if hasattr(self, "f1_bam_entry"):
                self.f1_bam_entry.delete(0, tk.END)
                self.f1_bam_entry.insert(0, bs["f1_bam"])
                self.f1_name.delete(0, tk.END)
                self.f1_name.insert(0, bs["f1_name"])

            self.abulk_bam_entry.delete(0, tk.END)
            self.abulk_bam_entry.insert(0, bs["abulk_bam"])
            self.abulk_name.delete(0, tk.END)
            self.abulk_name.insert(0, bs["abulk_name"])

            if hasattr(self, "bbulk_bam_entry"):
                self.bbulk_bam_entry.delete(0, tk.END)
                self.bbulk_bam_entry.insert(0, bs["bbulk_bam"])
                self.bbulk_name.delete(0, tk.END)
                self.bbulk_name.insert(0, bs["bbulk_name"])
    ############################################################
    def show_inline_progress(self):
        import tkinter.ttk as ttk
        color0 = "#FFFFFF"

        # 進捗フレームをrun_frameの前（scrollable_frame内）に挿入
        self.progress_frame = tk.Frame(self.scrollable_frame, bg=color0)
        self.progress_frame.pack(fill="x", padx=20, pady=[5, 0], before=self.run_frame)

        self.progress_label = tk.Label(self.progress_frame, text="Analysis is starting...", font=("Arial", 13), bg=color0, fg="#333333")
        self.progress_label.pack(anchor="w", pady=[2, 0])

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill="x", pady=3)

        self.progress_pct_label = tk.Label(self.progress_frame, text="0%", font=("Arial", 11), bg=color0, fg="#555555")
        self.progress_pct_label.pack(anchor="e")

        # スクロール領域を更新して表示を確定させる
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_progress(self, pct, label_text):
        self.progress_var.set(pct)
        self.progress_label.config(text=label_text)
        self.progress_pct_label.config(text=f"{pct:.0f}%")
        self.master.update_idletasks()

    def run_analysis(self):
        import threading
        # Back ボタンを無効化（実行中に画面を切り替えさせない）
        self.back_button.config(state="disabled")
        self.run_button.config(state="disabled")
        # カーソルをぐるぐるに変更
        self.master.config(cursor="watch")
        self.master.update()
        # 進捗バーをインライン表示
        self.show_inline_progress()
        thread = threading.Thread(target=self._run_analysis_thread, daemon=True)
        thread.start()
    def _finish_analysis(self):
        # 進捗フレームを削除
        if hasattr(self, "progress_frame") and self.progress_frame.winfo_exists():
            self.progress_frame.destroy()
        # カーソルを元に戻す
        self.master.config(cursor="")
        # ボタンを再度有効化
        if self.back_button.winfo_exists():
            self.back_button.config(state="normal")
        if self.run_button.winfo_exists():
            self.run_button.config(state="normal")

    def _on_analysis_finished(self):
        self.update_progress(100, "It's all over!")
        self._finish_analysis()
        messagebox.showinfo("Message", "Analysis Completed")

    ############################################################
    def _run_analysis_thread(self):
        import matplotlib
        matplotlib.use('Agg')

        settings = self.master.settings
        # --- settings ---
        Bulk_single_double = settings["Bulk_single_double"]
        bulk_type = settings["bulk_type"]
        pattern = settings["pattern"]
        fasta = settings["fasta"]
        output_folder = settings["output_folder"]
        samtools = settings["samtools"]
        bcftools = settings["bcftools"]
        filter_depth = settings["filter_depth"]
        window_size = settings["window_size"]
        step_size = settings["step_size"]
        bulk_number = settings["bulk_number"]
        removal_SNPindex = settings["removal_SNPindex"]
        abulk_color = settings["abulk_color"]
        bbulk_color = settings["bbulk_color"]
        delta_color = settings["delta_color"]
        side = settings["side"]
        # --- BAM取得 ---
        P1_bam = self.p1_bam_entry.get()
        P1_name = (self.p1_name.get() or "P1").replace(" ", "_")
        if not os.path.exists(P1_bam):
            messagebox.showerror("Error", "P1 BAM not found")
            self.master.after(0, self._finish_analysis)
            return
        if pattern in [2, 3]:
            P2_bam = self.p2_bam_entry.get()
            P2_name = (self.p2_name.get() or "P2").replace(" ", "_")
            if not os.path.exists(P2_bam):
                messagebox.showerror("Error", "P2 BAM not found")
                self.master.after(0, self._finish_analysis)
                return
        else:
            P2_bam, P2_name = None, None
        if pattern in [3, 4]:
            F1_bam = self.f1_bam_entry.get()
            F1_name = (self.f1_name.get() or "F1").replace(" ", "_")
            if not os.path.exists(F1_bam):
                messagebox.showerror("Error", "F1 BAM not found")
                self.master.after(0, self._finish_analysis)
                return
        else:
            F1_bam, F1_name = None, None
        Abulk_bam = self.abulk_bam_entry.get()
        Abulk_name = (self.abulk_name.get() or "Abulk").replace(" ", "_")
        if not os.path.exists(Abulk_bam):
            messagebox.showerror("Error", "Abulk BAM not found")
            self.master.after(0, self._finish_analysis)
            return
        if self.bulk == 2:
            Bbulk_bam = self.bbulk_bam_entry.get()
            Bbulk_name = (self.bbulk_name.get() or "Bbulk").replace(" ", "_")
            if not os.path.exists(Bbulk_bam):
                messagebox.showerror("Error", "Bbulk BAM not found")
                self.master.after(0, self._finish_analysis)
                return
        else:
            Bbulk_bam, Bbulk_name = None, None

        # --- サンプル名重複チェック ---
        all_names = [n for n in [P1_name, P2_name, F1_name, Abulk_name, Bbulk_name] if n is not None]
        if len(all_names) != len(set(all_names)):
            messagebox.showerror("Error", "The sample name is already taken. Please enter it again.")
            self.master.after(0, self._finish_analysis)
            return
        # --- FASTAチェック ---
        if not os.path.exists(fasta):
            messagebox.showerror("Error", "FASTA file not found")
            return
        # --- FAI作成 ---
        fai_file = fasta + ".fai"
        try:
            if not os.path.exists(fai_file):
                subprocess.run(f"{samtools} faidx {fasta}", shell=True, check=True)
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "FAI creation failed")
            return
        # --- 出力フォルダ ---
        os.makedirs(output_folder, exist_ok=True)
        # --- application path（安全版）---
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        # --- file copy ---
        file_paths = []
        file_paths.append(os.path.join(application_path, 'F1_sim.txt'))
        file_paths.extend([
            os.path.join(application_path, f'F2_{i}_sim.txt') for i in range(10, 51)
        ])
        file_paths.extend([
            os.path.join(application_path, f'BC1F1_{i}_sim.txt') for i in range(10, 51)
        ])
        file_paths.extend([
            os.path.join(application_path, f'RIL_{i}_sim.txt') for i in range(10, 51)
        ])
        snp_files = [
            'P_singele_snpindex', 'PF_singele_snpindex', 'P_snpindex', 'PF_snpindex',
            'PP_singele_snpindex', 'PP_snpindex', 'PPF_singele_snpindex', 'PPF_snpindex'
        ]
        file_paths.extend([
            os.path.join(application_path, f"{fname}.py") for fname in snp_files
        ])
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
            bulk_type_str = {1: "RIL", 2: "F2", 3: "BC1F1"}.get(bulk_type, "Not selected")
            pattern_str = {
                1: "P1",
                2: "P1 , P2",
                3: "P1 , P2 , F1",
                4: "P1 , F1"
            }.get(pattern, "Not selected")
            log_file.write(f"Bulk Type: {bulk_type_str}\n")
            log_file.write(f"Filter Pattern: {pattern_str}\n")
#################################################################################################################
        error_log_path = os.path.join(output_folder, "QTLseq_error_log.txt")
        try:
            if Bulk_single_double == 2:
                if pattern == 3:         
                    from bam_division import main as bam_division_main
                    bam_division_main(output_folder, P1_bam, P1_name, P2_bam, P2_name, F1_bam, F1_name, Abulk_bam, Abulk_name, Bbulk_bam, Bbulk_name, samtools, fai_file)

                    from Run_bam_division import main as run_bam_division_main
                    self.master.after(0, self.update_progress, 25, "Splitting bam by chromosome...")
                    run_bam_division_main(output_folder)

                    from bam_division_index import main as bam_division_index_main
                    bam_division_index_main(output_folder, P1_name, P2_name, F1_name, Abulk_name, Bbulk_name, samtools, fai_file)

                    from Run_bam_division_index import main as run_bam_division_index_main
                    self.master.after(0, self.update_progress, 33, "Creating index...")
                    run_bam_division_index_main(output_folder)


                    from bam_file_data_volume import main as bam_file_data_volume_main
                    bam_file_data_volume_main(output_folder, P1_name, P2_name, F1_name, Abulk_name, Bbulk_name)

                    from bam_fai_sequence import main as bam_fai_sequence_main
                    bam_fai_sequence_main(output_folder, fai_file, samtools, P1_name, P2_name, F1_name, Abulk_name, Bbulk_name)

                    num_parts_path = os.path.join(output_folder, 'num_parts.txt')
                    if os.path.exists(num_parts_path):
                        from Run_bam_fai_sequence import main as run_bam_fai_sequence_main
                        self.master.after(0, self.update_progress, 41, "Splitting the BAM file by size...")
                        run_bam_fai_sequence_main(output_folder)

                        from Run_bam_fai_sequence_index import main as run_bam_fai_sequence_index_main
                        self.master.after(0, self.update_progress, 49, "Creating index...")
                        run_bam_fai_sequence_index_main(output_folder)

                        from make_vcftxt_position import main as make_vcftxt_position_main
                        make_vcftxt_position_main(output_folder, fasta, bcftools, P1_name, P2_name, F1_name, Abulk_name, Bbulk_name)

                        from Run_make_vcftxt_position import main as run_make_vcftxt_position_main
                        self.master.after(0, self.update_progress, 57, "Creating a VCF file...")
                        run_make_vcftxt_position_main(output_folder)

                    else:
                        from make_vcf import main as make_vcf_main
                        make_vcf_main(output_folder, fasta, bcftools, P1_name, P2_name, F1_name, Abulk_name, Bbulk_name, fai_file)

                        from Run_make_vcf import main as run_make_vcf_main
                        self.master.after(0, self.update_progress, 57, "Creating a VCF file...")
                        run_make_vcf_main(output_folder)

                    
                    from PPF_vcf_snpindex import main as PPF_vcf_snpindex_main
                    PPF_vcf_snpindex_main(output_folder, filter_depth, removal_SNPindex)

                    from PPF_run_snpindex_commands_lib import main as PPF_run_snpindex_commands_lib_main
                    self.master.after(0, self.update_progress, 65, "Calculating SNP index...")
                    PPF_run_snpindex_commands_lib_main(output_folder)

                    vcf_files = glob.glob(os.path.join(output_folder, '*.vcf'))
                    for file in vcf_files:
                        os.remove(file)
                    
                    from PPF_snpindex_marge import main as PPF_snpindex_marge_main
                    PPF_snpindex_marge_main(output_folder, fai_file)

                    from snp_sim import main as snp_sim
                    snp_sim(output_folder, bulk_number, bulk_type)

                    from confidence_interval import main as confidence_interval
                    self.master.after(0, self.update_progress, 81, "Setting confidence interval...")
                    confidence_interval(output_folder, fai_file, window_size, step_size, filter_depth)

                    from PPF_average import main as PPF_average_main
                    self.master.after(0, self.update_progress, 73, "Calculating the average SNP index...")
                    PPF_average_main(output_folder, fai_file, filter_depth, window_size, step_size)

                    from plot import main as plot
                    self.master.after(0, self.update_progress, 89, "Creating a plot...")
                    plot(output_folder, Abulk_name, Bbulk_name, fai_file, abulk_color, bbulk_color, delta_color, side)

                    from figure_legend import main as figure_legend
                    self.master.after(0, self.update_progress, 89, "Creating a figure legend...")
                    figure_legend(output_folder, abulk_color, bbulk_color, delta_color, window_size, step_size)

                    from average_selection import main as average_selection
                    average_selection(output_folder)

                    from average_selection_txt import main as average_selection_txt
                    average_selection_txt(output_folder, Abulk_name, Bbulk_name, fai_file)

                    from peak import main as peak
                    self.master.after(0, self.update_progress, 97, "Detecting peak regions...")
                    peak(output_folder, Abulk_name, Bbulk_name)

                    organize_files(output_folder)
                    self.master.after(0, self._on_analysis_finished)


                if pattern == 2:
                    from PP_bam_division import main as bam_division_main
                    bam_division_main(output_folder, P1_bam, P1_name, P2_bam, P2_name, Abulk_bam, Abulk_name, Bbulk_bam, Bbulk_name, samtools, fai_file)

                    from PP_Run_bam_division import main as run_bam_division_main
                    self.master.after(0, self.update_progress, 25, "Splitting bam by chromosome...")
                    run_bam_division_main(output_folder)

                    from PP_bam_division_index import main as bam_division_index_main
                    bam_division_index_main(output_folder, P1_name, P2_name, Abulk_name, Bbulk_name, samtools, fai_file)

                    from PP_Run_bam_division_index import main as run_bam_division_index_main
                    self.master.after(0, self.update_progress, 33, "Creating index...")
                    run_bam_division_index_main(output_folder)

                    from PP_bam_file_data_volume import main as bam_file_data_volume_main
                    bam_file_data_volume_main(output_folder, P1_name, P2_name, Abulk_name, Bbulk_name)

                    from PP_bam_fai_sequence import main as bam_fai_sequence_main
                    bam_fai_sequence_main(output_folder, fai_file, samtools, P1_name, P2_name, Abulk_name, Bbulk_name)


                    num_parts_path = os.path.join(output_folder, 'num_parts.txt')

                    if os.path.exists(num_parts_path):
                        from PP_Run_bam_fai_sequence import main as run_bam_fai_sequence_main
                        self.master.after(0, self.update_progress, 41, "Splitting the BAM file by size...")
                        run_bam_fai_sequence_main(output_folder)

                        from PP_Run_bam_fai_sequence_index import main as run_bam_fai_sequence_index_main
                        self.master.after(0, self.update_progress, 49, "Creating index...")
                        run_bam_fai_sequence_index_main(output_folder)

                        from PP_make_vcftxt_position import main as make_vcftxt_position_main
                        make_vcftxt_position_main(output_folder, fasta, bcftools, P1_name, P2_name, Abulk_name, Bbulk_name)

                        from PP_Run_make_vcftxt_position import main as run_make_vcftxt_position_main
                        self.master.after(0, self.update_progress, 57, "Creating a VCF file...")
                        run_make_vcftxt_position_main(output_folder)

                    else:
                        from PP_make_vcf import main as make_vcf_main
                        make_vcf_main(output_folder, fasta, bcftools, P1_name, P2_name, Abulk_name, Bbulk_name, fai_file)

                        from PP_Run_make_vcf import main as run_make_vcf_main
                        self.master.after(0, self.update_progress, 57, "Creating a VCF file...")
                        run_make_vcf_main(output_folder)

                    from PP_vcf_snpindex import main as PP_vcf_snpindex_main
                    PP_vcf_snpindex_main(output_folder, filter_depth, removal_SNPindex)

                    from PP_run_snpindex_commands_lib import main as PP_run_snpindex_commands_lib_main
                    self.master.after(0, self.update_progress, 65, "Calculating SNP index...")
                    PP_run_snpindex_commands_lib_main(output_folder)

                    vcf_files = glob.glob(os.path.join(output_folder, '*.vcf'))
                    for file in vcf_files:
                        os.remove(file)

                    from PP_snpindex_marge import main as PP_snpindex_marge_main
                    PP_snpindex_marge_main(output_folder, fai_file)

                    from PP_snp_sim import main as snp_sim
                    snp_sim(output_folder, bulk_number, bulk_type)

                    from PP_confidence_interval import main as confidence_interval
                    self.master.after(0, self.update_progress, 81, "Setting confidence interval...")
                    confidence_interval(output_folder, fai_file, window_size, step_size, filter_depth)

                    from PP_average import main as average
                    self.master.after(0, self.update_progress, 73, "Calculating the average SNP index...")
                    average(output_folder, fai_file, filter_depth, window_size, step_size)

                    from PP_plot import main as plot
                    self.master.after(0, self.update_progress, 89, "Creating a plot...")
                    plot(output_folder, Abulk_name, Bbulk_name, fai_file, abulk_color, bbulk_color, delta_color, side)

                    from figure_legend import main as figure_legend
                    self.master.after(0, self.update_progress, 89, "Creating a figure legend...")
                    figure_legend(output_folder, abulk_color, bbulk_color, delta_color, window_size, step_size)

                    from PP_average_selection import main as average_selection
                    average_selection(output_folder)

                    from PP_average_selection_txt import main as average_selection_txt
                    average_selection_txt(output_folder, Abulk_name, Bbulk_name, fai_file)

                    from PP_peak import main as peak
                    self.master.after(0, self.update_progress, 97, "Detecting peak regions...")
                    peak(output_folder, Abulk_name, Bbulk_name)

                    organize_files(output_folder)
                    self.master.after(0, self._on_analysis_finished)


                if pattern == 4:

                    from PF_bam_division import main as bam_division_main
                    bam_division_main(output_folder, P1_bam, P1_name, F1_bam, F1_name, Abulk_bam, Abulk_name, Bbulk_bam, Bbulk_name, samtools, fai_file)

                    from PF_Run_bam_division import main as run_bam_division_main
                    self.master.after(0, self.update_progress, 25, "Splitting bam by chromosome...")
                    run_bam_division_main(output_folder)

                    from PF_bam_division_index import main as bam_division_index_main
                    bam_division_index_main(output_folder, P1_name, F1_name, Abulk_name, Bbulk_name, samtools, fai_file)

                    from PF_Run_bam_division_index import main as run_bam_division_index_main
                    self.master.after(0, self.update_progress, 33, "Creating index...")
                    run_bam_division_index_main(output_folder)

                    from PF_bam_file_data_volume import main as bam_file_data_volume_main
                    bam_file_data_volume_main(output_folder, P1_name, F1_name, Abulk_name, Bbulk_name)

                    from PF_bam_fai_sequence import main as bam_fai_sequence_main
                    bam_fai_sequence_main(output_folder, fai_file, samtools, P1_name, F1_name, Abulk_name, Bbulk_name)
                

                    num_parts_path = os.path.join(output_folder, 'num_parts.txt')
                    if os.path.exists(num_parts_path):
                        from PF_Run_bam_fai_sequence import main as run_bam_fai_sequence_main
                        self.master.after(0, self.update_progress, 41, "Splitting the BAM file by size...")
                        run_bam_fai_sequence_main(output_folder)

                        from PF_Run_bam_fai_sequence_index import main as run_bam_fai_sequence_index_main
                        self.master.after(0, self.update_progress, 49, "Creating index...")
                        run_bam_fai_sequence_index_main(output_folder)

                        from PF_make_vcftxt_position import main as make_vcftxt_position_main
                        make_vcftxt_position_main(output_folder, fasta, bcftools, P1_name, F1_name, Abulk_name, Bbulk_name)

                        from PF_Run_make_vcftxt_position import main as run_make_vcftxt_position_main
                        self.master.after(0, self.update_progress, 57, "Creating a VCF file...")
                        run_make_vcftxt_position_main(output_folder)
                    else:
                        from PF_make_vcf import main as make_vcf_main
                        make_vcf_main(output_folder, fasta, bcftools, P1_name, F1_name, Abulk_name, Bbulk_name, fai_file)

                        from PF_Run_make_vcf import main as run_make_vcf_main
                        self.master.after(0, self.update_progress, 57, "Creating a VCF file...")
                        run_make_vcf_main(output_folder)

                    from PF_vcf_snpindex import main as PF_vcf_snpindex_main
                    PF_vcf_snpindex_main(output_folder, filter_depth, removal_SNPindex)

                    from PF_run_snpindex_commands_lib import main as PF_run_snpindex_commands_lib_main
                    self.master.after(0, self.update_progress, 65, "Calculating SNP index...")
                    PF_run_snpindex_commands_lib_main(output_folder)

                    vcf_files = glob.glob(os.path.join(output_folder, '*.vcf'))
                    for file in vcf_files:
                        os.remove(file)

                    from PF_snpindex_marge import main as PF_snpindex_marge_main
                    PF_snpindex_marge_main(output_folder, fai_file)

                    from PF_snp_sim import main as snp_sim
                    snp_sim(output_folder, bulk_number, bulk_type)

                    from PF_confidence_interval import main as confidence_interval
                    self.master.after(0, self.update_progress, 81, "Setting confidence interval...")
                    confidence_interval(output_folder, fai_file, window_size, step_size, filter_depth)

                    from PF_average import main as average
                    self.master.after(0, self.update_progress, 73, "Calculating the average SNP index...")
                    average(output_folder, fai_file, filter_depth, window_size, step_size)

                    from PF_plot import main as plot
                    self.master.after(0, self.update_progress, 89, "Creating a plot...")
                    plot(output_folder, Abulk_name, Bbulk_name, fai_file, abulk_color, bbulk_color, delta_color, side)

                    from figure_legend import main as figure_legend
                    self.master.after(0, self.update_progress, 89, "Creating a figure legend...")
                    figure_legend(output_folder, abulk_color, bbulk_color, delta_color, window_size, step_size)

                    from PF_average_selection import main as average_selection
                    average_selection(output_folder)

                    from PF_average_selection_txt import main as average_selection_txt
                    average_selection_txt(output_folder, Abulk_name, Bbulk_name, fai_file)

                    from PF_peak import main as peak
                    self.master.after(0, self.update_progress, 97, "Detecting peak regions...")
                    peak(output_folder, Abulk_name, Bbulk_name)

                    organize_files(output_folder)
                    self.master.after(0, self._on_analysis_finished)

                if pattern == 1:
                    from P_bam_division import main as bam_division_main
                    bam_division_main(output_folder, P1_bam, P1_name, Abulk_bam, Abulk_name, Bbulk_bam, Bbulk_name, samtools, fai_file)

                    from P_Run_bam_division import main as run_bam_division_main
                    self.master.after(0, self.update_progress, 25, "Splitting bam by chromosome...")
                    run_bam_division_main(output_folder)

                    from P_bam_division_index import main as bam_division_index_main
                    bam_division_index_main(output_folder, P1_name, Abulk_name, Bbulk_name, samtools, fai_file)

                    from P_Run_bam_division_index import main as run_bam_division_index_main
                    self.master.after(0, self.update_progress, 33, "Creating index...")
                    run_bam_division_index_main(output_folder)

                    from P_bam_file_data_volume import main as bam_file_data_volume_main
                    bam_file_data_volume_main(output_folder, P1_name, Abulk_name, Bbulk_name)

                    from P_bam_fai_sequence import main as bam_fai_sequence_main
                    bam_fai_sequence_main(output_folder, fai_file, samtools, P1_name, Abulk_name, Bbulk_name)

                    num_parts_path = os.path.join(output_folder, 'num_parts.txt')
                    if os.path.exists(num_parts_path):
                        from P_Run_bam_fai_sequence import main as run_bam_fai_sequence_main
                        self.master.after(0, self.update_progress, 41, "Splitting the BAM file by size...")
                        run_bam_fai_sequence_main(output_folder)

                        from P_Run_bam_fai_sequence_index import main as run_bam_fai_sequence_index_main
                        self.master.after(0, self.update_progress, 49, "Creating index...")
                        run_bam_fai_sequence_index_main(output_folder)

                        from P_make_vcftxt_position import main as make_vcftxt_position_main
                        make_vcftxt_position_main(output_folder, fasta, bcftools, P1_name, Abulk_name, Bbulk_name)

                        from P_Run_make_vcftxt_position import main as run_make_vcftxt_position_main
                        self.master.after(0, self.update_progress, 57, "Creating a VCF file...")
                        run_make_vcftxt_position_main(output_folder)
                    else:
                        from P_make_vcf import main as make_vcf_main
                        make_vcf_main(output_folder, fasta, bcftools, P1_name, Abulk_name, Bbulk_name, fai_file)

                        from P_Run_make_vcf import main as run_make_vcf_main
                        self.master.after(0, self.update_progress, 57, "Creating a VCF file...")
                        run_make_vcf_main(output_folder)

                    from P_vcf_snpindex import main as P_vcf_snpindex_main
                    P_vcf_snpindex_main(output_folder, filter_depth, removal_SNPindex)

                    from P_run_snpindex_commands_lib import main as P_run_snpindex_commands_lib_main
                    self.master.after(0, self.update_progress, 65, "Calculating SNP index...")
                    P_run_snpindex_commands_lib_main(output_folder)

                    vcf_files = glob.glob(os.path.join(output_folder, '*.vcf'))
                    for file in vcf_files:
                        os.remove(file)

                    from P_snpindex_marge import main as P_snpindex_marge_main
                    P_snpindex_marge_main(output_folder, fai_file)

                    from P_snp_sim import main as snp_sim
                    snp_sim(output_folder, bulk_number, bulk_type)

                    from P_confidence_interval import main as confidence_interval
                    self.master.after(0, self.update_progress, 81, "Setting confidence interval...")
                    confidence_interval(output_folder, fai_file, window_size, step_size, filter_depth)

                    from P_average import main as average
                    self.master.after(0, self.update_progress, 73, "Calculating the average SNP index...")
                    average(output_folder, fai_file, filter_depth, window_size, step_size)

                    from P_plot import main as plot
                    self.master.after(0, self.update_progress, 89, "Creating a plot...")
                    plot(output_folder, Abulk_name, Bbulk_name, fai_file, abulk_color, bbulk_color, delta_color, side)

                    from figure_legend import main as figure_legend
                    self.master.after(0, self.update_progress, 89, "Creating a figure legend...")
                    figure_legend(output_folder, abulk_color, bbulk_color, delta_color, window_size, step_size)

                    from P_average_selection import main as average_selection
                    average_selection(output_folder)

                    from P_average_selection_txt import main as average_selection_txt
                    average_selection_txt(output_folder, Abulk_name, Bbulk_name, fai_file)

                    from P_peak import main as peak
                    self.master.after(0, self.update_progress, 97, "Detecting peak regions...")
                    peak(output_folder, Abulk_name, Bbulk_name)

                    organize_files(output_folder)
                    self.master.after(0, self._on_analysis_finished)
                    



            elif Bulk_single_double == 1:
                if pattern == 3:

                    from PPF_singele_bam_division import main as PPF_singele_bam_division_main
                    PPF_singele_bam_division_main(output_folder, P1_bam, P1_name, P2_bam, P2_name, F1_bam, F1_name, Abulk_bam, Abulk_name, samtools, fai_file)

                    from PPF_singele_Run_bam_division import main as PPF_singele_Run_bam_division_main
                    self.master.after(0, self.update_progress, 25, "Splitting bam by chromosome...")
                    PPF_singele_Run_bam_division_main(output_folder)

                    from PPF_singele_bam_division_index import main as PPF_singele_bam_division_index_main
                    PPF_singele_bam_division_index_main(output_folder, P1_name, P2_name, F1_name, Abulk_name, samtools, fai_file)

                    from PPF_singele_Run_bam_division_index import main as PPF_singele_Run_bam_division_index_main
                    self.master.after(0, self.update_progress, 33, "Creating index...")
                    PPF_singele_Run_bam_division_index_main(output_folder)

                    from PPF_singele_bam_file_data_volume import main as PPF_singele_bam_file_data_volume_main
                    PPF_singele_bam_file_data_volume_main(output_folder, P1_name, P2_name, F1_name, Abulk_name)

                    from PPF_singele_bam_fai_sequence import main as PPF_singele_bam_fai_sequence_main
                    PPF_singele_bam_fai_sequence_main(output_folder, fai_file, samtools, P1_name, P2_name, F1_name, Abulk_name)

                    num_parts_path = os.path.join(output_folder, 'num_parts.txt')
                    if os.path.exists(num_parts_path):
                        from PPF_singele_Run_bam_fai_sequence import main as PPF_singele_Run_bam_fai_sequence_main
                        self.master.after(0, self.update_progress, 41, "Splitting the BAM file by size...")
                        PPF_singele_Run_bam_fai_sequence_main(output_folder)

                        from PPF_singele_Run_bam_fai_sequence_index import main as PPF_singele_Run_bam_fai_sequence_index_main
                        self.master.after(0, self.update_progress, 49, "Creating index...")
                        PPF_singele_Run_bam_fai_sequence_index_main(output_folder)

                        from PPF_singele_make_vcftxt_position import main as PPF_singele_make_vcftxt_position_main
                        PPF_singele_make_vcftxt_position_main(output_folder, fasta, bcftools, P1_name, P2_name, F1_name, Abulk_name)

                        from PPF_singele_Run_make_vcftxt_position import main as PPF_singele_Run_make_vcftxt_position_main
                        self.master.after(0, self.update_progress, 57, "Creating a VCF file...")
                        PPF_singele_Run_make_vcftxt_position_main(output_folder)
                    else:
                        from PPF_singele_make_vcf import main as PPF_singele_make_vcf_main
                        PPF_singele_make_vcf_main(output_folder, fasta, bcftools, P1_name, P2_name, F1_name, Abulk_name, fai_file)

                        from PPF_singele_Run_make_vcf import main as PPF_singele_Run_make_vcf_main
                        self.master.after(0, self.update_progress, 57, "Creating a VCF file...")
                        PPF_singele_Run_make_vcf_main(output_folder)

                    from PPF_single_vcf_snpindex import main as PPF_single_vcf_snpindex_main
                    PPF_single_vcf_snpindex_main(output_folder, filter_depth)

                    from PPF_single_run_snpindex_commands_lib import main as PPF_single_run_snpindex_commands_lib_main
                    self.master.after(0, self.update_progress, 65, "Calculating SNP index...")
                    PPF_single_run_snpindex_commands_lib_main(output_folder)

                    vcf_files = glob.glob(os.path.join(output_folder, '*.vcf'))
                    for file in vcf_files:
                        os.remove(file)

                    from PPF_singele_snpindex_marge import main as PPF_singele_snpindex_marge_main
                    PPF_singele_snpindex_marge_main(output_folder, fai_file)

                    from PPF_singele_snp_sim import main as PPF_singele_snp_sim_main
                    PPF_singele_snp_sim_main(output_folder, bulk_number, bulk_type)

                    from PPF_singele_confidence_interval import main as PPF_singele_confidence_interval_main
                    self.master.after(0, self.update_progress, 81, "Setting confidence interval...")
                    PPF_singele_confidence_interval_main(output_folder, fai_file, window_size, step_size, filter_depth)

                    from PPF_singele_average import main as PPF_singele_average_main
                    self.master.after(0, self.update_progress, 73, "Calculating the average SNP index...")
                    PPF_singele_average_main(output_folder, fai_file, filter_depth, window_size, step_size)

                    from PPF_singele_plot import main as PPF_singele_plot_main
                    self.master.after(0, self.update_progress, 89, "Creating a plot...")
                    PPF_singele_plot_main(output_folder, Abulk_name, fai_file, abulk_color, side)

                    from figure_legend_single import main as figure_legend_single
                    self.master.after(0, self.update_progress, 89, "Creating a figure legend...")
                    figure_legend_single(output_folder, abulk_color, window_size, step_size)
                    
                    from PPF_singele_average_selection import main as PPF_singele_average_selection_main
                    PPF_singele_average_selection_main(output_folder)

                    from PPF_single_average_selection_txt import main as PPF_single_average_selection_txt_main
                    PPF_single_average_selection_txt_main(output_folder, Abulk_name, fai_file)

                    from PPF_singele_peak import main as PPF_singele_peak_main
                    self.master.after(0, self.update_progress, 97, "Detecting peak regions...")
                    PPF_singele_peak_main(output_folder, Abulk_name)

                    organize_files(output_folder)
                    self.master.after(0, self._on_analysis_finished)

                if pattern == 4:
                
                    from PF_singele_bam_division import main as PF_singele_bam_division_main
                    PF_singele_bam_division_main(output_folder, P1_bam, P1_name, F1_bam, F1_name, Abulk_bam, Abulk_name, samtools, fai_file)

                    from PF_singele_Run_bam_division import main as PF_singele_Run_bam_division_main
                    self.master.after(0, self.update_progress, 25, "Splitting bam by chromosome...")
                    PF_singele_Run_bam_division_main(output_folder)

                    from PF_singele_bam_division_index import main as PF_singele_bam_division_index_main
                    PF_singele_bam_division_index_main(output_folder, P1_name, F1_name, Abulk_name, samtools, fai_file)

                    from PF_singele_Run_bam_division_index import main as PF_singele_Run_bam_division_index_main
                    self.master.after(0, self.update_progress, 33, "Creating index...")
                    PF_singele_Run_bam_division_index_main(output_folder)

                    from PF_singele_bam_file_data_volume import main as PF_singele_bam_file_data_volume_main
                    PF_singele_bam_file_data_volume_main(output_folder, P1_name, F1_name, Abulk_name)

                    from PF_singele_bam_fai_sequence import main as PF_singele_bam_fai_sequence_main
                    PF_singele_bam_fai_sequence_main(output_folder, fai_file, samtools, P1_name, F1_name, Abulk_name)

                    num_parts_path = os.path.join(output_folder, 'num_parts.txt')
                    if os.path.exists(num_parts_path):
                        from PF_singele_Run_bam_fai_sequence import main as PF_singele_Run_bam_fai_sequence_main
                        self.master.after(0, self.update_progress, 41, "Splitting the BAM file by size...")
                        PF_singele_Run_bam_fai_sequence_main(output_folder)

                        from PF_singele_Run_bam_fai_sequence_index import main as PF_singele_Run_bam_fai_sequence_index_main
                        self.master.after(0, self.update_progress, 49, "Creating index...")
                        PF_singele_Run_bam_fai_sequence_index_main(output_folder)

                        from PF_singele_make_vcftxt_position import main as PF_singele_make_vcftxt_position_main
                        PF_singele_make_vcftxt_position_main(output_folder, fasta, bcftools, P1_name, F1_name, Abulk_name)

                        from PF_singele_Run_make_vcftxt_position import main as PF_singele_Run_make_vcftxt_position_main
                        self.master.after(0, self.update_progress, 57, "Creating a VCF file...")
                        PF_singele_Run_make_vcftxt_position_main(output_folder)
                    else:
                        from PF_singele_make_vcf import main as PF_singele_make_vcf_main
                        PF_singele_make_vcf_main(output_folder, fasta, bcftools, P1_name, F1_name, Abulk_name, fai_file)

                        from PF_singele_Run_make_vcf import main as PF_singele_Run_make_vcf_main
                        self.master.after(0, self.update_progress, 57, "Creating a VCF file...")
                        PF_singele_Run_make_vcf_main(output_folder)

                    from PF_single_vcf_snpindex import main as PF_single_vcf_snpindex_main
                    PF_single_vcf_snpindex_main(output_folder, filter_depth)

                    from PF_single_run_snpindex_commands_lib import main as PF_single_run_snpindex_commands_lib_main
                    self.master.after(0, self.update_progress, 65, "Calculating SNP index...")
                    PF_single_run_snpindex_commands_lib_main(output_folder)

                    vcf_files = glob.glob(os.path.join(output_folder, '*.vcf'))
                    for file in vcf_files:
                        os.remove(file)

                    from PF_singele_snpindex_marge import main as PF_singele_snpindex_marge_main
                    PF_singele_snpindex_marge_main(output_folder, fai_file)

                    from PF_singele_snp_sim import main as PF_singele_snp_sim_main
                    PF_singele_snp_sim_main(output_folder, bulk_number, bulk_type)

                    from PF_singele_confidence_interval import main as PF_singele_confidence_interval_main
                    self.master.after(0, self.update_progress, 81, "Setting confidence interval...")
                    PF_singele_confidence_interval_main(output_folder, fai_file, window_size, step_size, filter_depth)

                    from PF_singele_average import main as PF_singele_average_main
                    self.master.after(0, self.update_progress, 73, "Calculating the average SNP index...")
                    PF_singele_average_main(output_folder, fai_file, filter_depth, window_size, step_size)

                    from PF_singele_plot import main as PF_singele_plot_main
                    self.master.after(0, self.update_progress, 89, "Creating a plot...")
                    PF_singele_plot_main(output_folder, Abulk_name, fai_file, abulk_color, side)

                    from figure_legend_single import main as figure_legend_single
                    self.master.after(0, self.update_progress, 89, "Creating a figure legend...")
                    figure_legend_single(output_folder, abulk_color, window_size, step_size)

                    from PF_singele_average_selection import main as PF_singele_average_selection_main
                    PF_singele_average_selection_main( output_folder)

                    from PF_single_average_selection_txt import main as PF_single_average_selection_txt_main
                    PF_single_average_selection_txt_main(output_folder, Abulk_name, fai_file)

                    from PF_singele_peak import main as PF_singele_peak_main
                    self.master.after(0, self.update_progress, 97, "Detecting peak regions...")
                    PF_singele_peak_main(output_folder, Abulk_name)

                    organize_files(output_folder)
                    self.master.after(0, self._on_analysis_finished)


                if pattern == 2:

                    from PP_singele_bam_division import main as PP_singele_bam_division_main
                    PP_singele_bam_division_main(output_folder, P1_bam, P1_name, P2_bam, P2_name, Abulk_bam, Abulk_name,samtools, fai_file)

                    from PP_singele_Run_bam_division import main as PP_singele_Run_bam_division_main
                    self.master.after(0, self.update_progress, 25, "Splitting bam by chromosome...")
                    PP_singele_Run_bam_division_main(output_folder)

                    from PP_singele_bam_division_index import main as PP_singele_bam_division_index_main
                    PP_singele_bam_division_index_main(output_folder, P1_name, P2_name, Abulk_name, samtools, fai_file)

                    from PP_singele_Run_bam_division_index import main as PP_singele_Run_bam_division_index_main
                    self.master.after(0, self.update_progress, 33, "Creating index...")
                    PP_singele_Run_bam_division_index_main(output_folder)

                    from PP_singele_bam_file_data_volume import main as PP_singele_bam_file_data_volume_main
                    PP_singele_bam_file_data_volume_main(output_folder, P1_name, P2_name, Abulk_name)

                    from PP_singele_bam_fai_sequence import main as PP_singele_bam_fai_sequence_main
                    PP_singele_bam_fai_sequence_main(output_folder, fai_file, samtools, P1_name, P2_name, Abulk_name)

                    num_parts_path = os.path.join(output_folder, 'num_parts.txt')
                    if os.path.exists(num_parts_path):
                        from PP_singele_Run_bam_fai_sequence import main as PP_singele_Run_bam_fai_sequence_main
                        self.master.after(0, self.update_progress, 41, "Splitting the BAM file by size...")
                        PP_singele_Run_bam_fai_sequence_main(output_folder)

                        from PP_singele_Run_bam_fai_sequence_index import main as PP_singele_Run_bam_fai_sequence_index_main
                        self.master.after(0, self.update_progress, 49, "Creating index...")
                        PP_singele_Run_bam_fai_sequence_index_main(output_folder)

                        from PP_singele_make_vcftxt_position import main as PP_singele_make_vcftxt_position_main
                        PP_singele_make_vcftxt_position_main(output_folder, fasta, bcftools, P1_name, P2_name, Abulk_name)

                        from PP_singele_Run_make_vcftxt_position import main as PP_singele_Run_make_vcftxt_position_main
                        self.master.after(0, self.update_progress, 57, "Creating a VCF file...")
                        PP_singele_Run_make_vcftxt_position_main(output_folder)
                    else:
                        from PP_singele_make_vcf import main as PP_singele_make_vcf_main
                        PP_singele_make_vcf_main(output_folder, fasta, bcftools, P1_name, P2_name, Abulk_name, fai_file)

                        from PP_singele_Run_make_vcf import main as PP_singele_Run_make_vcf_main
                        self.master.after(0, self.update_progress, 57, "Creating a VCF file...")
                        PP_singele_Run_make_vcf_main(output_folder)

                    from PP_single_vcf_snpindex import main as PP_single_vcf_snpindex_main
                    PP_single_vcf_snpindex_main(output_folder, filter_depth)

                    from PP_single_run_snpindex_commands_lib import main as PP_single_run_snpindex_commands_lib_main
                    self.master.after(0, self.update_progress, 65, "Calculating SNP index...")
                    PP_single_run_snpindex_commands_lib_main(output_folder)

                    vcf_files = glob.glob(os.path.join(output_folder, '*.vcf'))
                    for file in vcf_files:
                        os.remove(file)

                    from PP_singele_snpindex_marge import main as PP_singele_snpindex_marge_main
                    PP_singele_snpindex_marge_main(output_folder, fai_file)

                    from PP_singele_snp_sim import main as PP_singele_snp_sim_main
                    PP_singele_snp_sim_main(output_folder, bulk_number, bulk_type)

                    from PP_singele_confidence_interval import main as PP_singele_confidence_interval_main
                    self.master.after(0, self.update_progress, 81, "Setting confidence interval...")
                    PP_singele_confidence_interval_main(output_folder, fai_file, window_size, step_size, filter_depth)

                    from PP_singele_average import main as PP_singele_average_main
                    self.master.after(0, self.update_progress, 73, "Calculating the average SNP index...")
                    PP_singele_average_main(output_folder, fai_file, filter_depth, window_size, step_size)

                    from PP_singele_plot import main as PP_singele_plot_main
                    self.master.after(0, self.update_progress, 89, "Creating a plot...")
                    PP_singele_plot_main(output_folder, Abulk_name, fai_file, abulk_color, side)

                    from figure_legend_single import main as figure_legend_single
                    self.master.after(0, self.update_progress, 89, "Creating a figure legend...")
                    figure_legend_single(output_folder, abulk_color, window_size, step_size)

                    from PP_singele_average_selection import main as PP_singele_average_selection_main
                    PP_singele_average_selection_main(output_folder)

                    from PP_single_average_selection_txt import main as PP_single_average_selection_txt_main
                    PP_single_average_selection_txt_main(output_folder, Abulk_name, fai_file)

                    from PP_singele_peak import main as PP_singele_peak_main
                    self.master.after(0, self.update_progress, 97, "Detecting peak regions...")
                    PP_singele_peak_main(output_folder, Abulk_name)

                    organize_files(output_folder)
                    self.master.after(0, self._on_analysis_finished)

                if pattern == 1:
                    from P_singele_bam_division import main as P_singele_bam_division_main
                    P_singele_bam_division_main(output_folder, P1_bam, P1_name, Abulk_bam, Abulk_name, samtools, fai_file)

                    from P_singele_Run_bam_division import main as P_singele_Run_bam_division_main
                    self.master.after(0, self.update_progress, 25, "Splitting bam by chromosome...")
                    P_singele_Run_bam_division_main(output_folder)

                    from P_singele_bam_division_index import main as P_singele_bam_division_index_main
                    P_singele_bam_division_index_main(output_folder, P1_name, Abulk_name, samtools, fai_file)

                    from P_singele_Run_bam_division_index import main as P_singele_Run_bam_division_index_main
                    self.master.after(0, self.update_progress, 33, "Creating index...")
                    P_singele_Run_bam_division_index_main(output_folder)


                    from P_singele_bam_file_data_volume import main as P_singele_bam_file_data_volume_main
                    P_singele_bam_file_data_volume_main(output_folder, P1_name, Abulk_name)

                    from P_singele_bam_fai_sequence import main as P_singele_bam_fai_sequence_main
                    P_singele_bam_fai_sequence_main(output_folder, fai_file, samtools, P1_name, Abulk_name)

                    num_parts_path = os.path.join(output_folder, 'num_parts.txt')
                    if os.path.exists(num_parts_path):
                        from P_singele_Run_bam_fai_sequence import main as P_singele_Run_bam_fai_sequence_main
                        self.master.after(0, self.update_progress, 41, "Splitting the BAM file by size...")
                        P_singele_Run_bam_fai_sequence_main(output_folder)

                        from P_singele_Run_bam_fai_sequence_index import main as P_singele_Run_bam_fai_sequence_index_main
                        self.master.after(0, self.update_progress, 49, "Creating index...")
                        P_singele_Run_bam_fai_sequence_index_main(output_folder)

                        from P_singele_make_vcftxt_position import main as P_singele_make_vcftxt_position_main
                        P_singele_make_vcftxt_position_main(output_folder, fasta, bcftools, P1_name, Abulk_name)

                        from P_singele_Run_make_vcftxt_position import main as P_singele_Run_make_vcftxt_position_main
                        self.master.after(0, self.update_progress, 57, "Creating a VCF file...")
                        P_singele_Run_make_vcftxt_position_main(output_folder)
                    else:
                        from P_singele_make_vcf import main as P_singele_make_vcf_main
                        P_singele_make_vcf_main(output_folder, fasta, bcftools, P1_name, Abulk_name, fai_file)

                        from P_singele_Run_make_vcf import main as P_singele_Run_make_vcf_main
                        self.master.after(0, self.update_progress, 57, "Creating a VCF file...")
                        P_singele_Run_make_vcf_main(output_folder)

                    from P_single_vcf_snpindex import main as P_single_vcf_snpindex_main
                    P_single_vcf_snpindex_main(output_folder, filter_depth)

                    from P_single_run_snpindex_commands_lib import main as P_single_run_snpindex_commands_lib_main
                    self.master.after(0, self.update_progress, 65, "Calculating SNP index...")
                    P_single_run_snpindex_commands_lib_main(output_folder)

                    vcf_files = glob.glob(os.path.join(output_folder, '*.vcf'))
                    for file in vcf_files:
                        os.remove(file)

                    from P_singele_snpindex_marge import main as P_singele_snpindex_marge_main
                    P_singele_snpindex_marge_main(output_folder, fai_file)

                    from P_singele_snp_sim import main as P_singele_snp_sim_main
                    P_singele_snp_sim_main(output_folder, bulk_number, bulk_type)

                    from P_singele_confidence_interval import main as P_singele_confidence_interval_main
                    self.master.after(0, self.update_progress, 81, "Setting confidence interval...")
                    P_singele_confidence_interval_main(output_folder, fai_file, window_size, step_size, filter_depth)

                    from P_singele_average import main as P_singele_average_main
                    self.master.after(0, self.update_progress, 73, "Calculating the average SNP index...")
                    P_singele_average_main(output_folder, fai_file, filter_depth, window_size, step_size)

                    from P_singele_plot import main as P_singele_plot_main
                    self.master.after(0, self.update_progress, 89, "Creating a plot...")
                    P_singele_plot_main(output_folder, Abulk_name, fai_file, abulk_color, side)

                    from figure_legend_single import main as figure_legend_single
                    self.master.after(0, self.update_progress, 89, "Creating a figure legend...")
                    figure_legend_single(output_folder, abulk_color, window_size, step_size)

                    from P_singele_average_selection import main as P_singele_average_selection_main
                    P_singele_average_selection_main(output_folder)

                    from P_single_average_selection_txt import main as P_single_average_selection_txt_main
                    P_single_average_selection_txt_main(output_folder, Abulk_name, fai_file)

                    from P_singele_peak import main as P_singele_peak_main
                    self.master.after(0, self.update_progress, 97, "Detecting peak regions...")
                    P_singele_peak_main(output_folder, Abulk_name)

                    organize_files(output_folder)
                    self.master.after(0, self._on_analysis_finished)
        
            else:
                messagebox.showerror("error", f"plese select bulk option")
                return
        except Exception as e:
            import traceback
            with open(error_log_path, "w", encoding="utf-8") as ef:
                ef.write("=== Error log ===\n")
                ef.write(f"Error details: {e}\n\n")
                ef.write("=== Detailed traceback ===\n")
                ef.write(traceback.format_exc())
            self.master.after(0, self._finish_analysis)
            messagebox.showerror("Error", f"An error occurred during analysis\nPlease refer to the file below for further details:\n{error_log_path}")
#################################################################################################################
root = TkinterDnD.Tk()
root.title("QTL-seq_GUI")
root.geometry("1165x800")

# 設定保存
root.settings = {}

app = DetailWindow(master=root)

app.mainloop()