# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Run.py'],
    pathex=[],
    binaries=[],
    datas=[('/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/tkinterdnd2', 'tkinterdnd2'), ('F1_sim.txt', '.'), ('F2_10_sim.txt', '.'), ('F2_11_sim.txt', '.'), ('F2_12_sim.txt', '.'), ('F2_13_sim.txt', '.'), ('F2_14_sim.txt', '.'), ('F2_15_sim.txt', '.'), ('F2_16_sim.txt', '.'), ('F2_17_sim.txt', '.'), ('F2_18_sim.txt', '.'), ('F2_19_sim.txt', '.'), ('F2_20_sim.txt', '.'), ('F2_21_sim.txt', '.'), ('F2_22_sim.txt', '.'), ('F2_23_sim.txt', '.'), ('F2_24_sim.txt', '.'), ('F2_25_sim.txt', '.'), ('F2_26_sim.txt', '.'), ('F2_27_sim.txt', '.'), ('F2_28_sim.txt', '.'), ('F2_29_sim.txt', '.'), ('F2_30_sim.txt', '.'), ('F2_31_sim.txt', '.'), ('F2_32_sim.txt', '.'), ('F2_33_sim.txt', '.'), ('F2_34_sim.txt', '.'), ('F2_35_sim.txt', '.'), ('F2_36_sim.txt', '.'), ('F2_37_sim.txt', '.'), ('F2_38_sim.txt', '.'), ('F2_39_sim.txt', '.'), ('F2_40_sim.txt', '.'), ('F2_41_sim.txt', '.'), ('F2_42_sim.txt', '.'), ('F2_43_sim.txt', '.'), ('F2_44_sim.txt', '.'), ('F2_45_sim.txt', '.'), ('F2_46_sim.txt', '.'), ('F2_47_sim.txt', '.'), ('F2_48_sim.txt', '.'), ('F2_49_sim.txt', '.'), ('F2_50_sim.txt', '.'), ('BC1F1_10_sim.txt', '.'), ('BC1F1_11_sim.txt', '.'), ('BC1F1_12_sim.txt', '.'), ('BC1F1_13_sim.txt', '.'), ('BC1F1_14_sim.txt', '.'), ('BC1F1_15_sim.txt', '.'), ('BC1F1_16_sim.txt', '.'), ('BC1F1_17_sim.txt', '.'), ('BC1F1_18_sim.txt', '.'), ('BC1F1_19_sim.txt', '.'), ('BC1F1_20_sim.txt', '.'), ('BC1F1_21_sim.txt', '.'), ('BC1F1_22_sim.txt', '.'), ('BC1F1_23_sim.txt', '.'), ('BC1F1_24_sim.txt', '.'), ('BC1F1_25_sim.txt', '.'), ('BC1F1_26_sim.txt', '.'), ('BC1F1_27_sim.txt', '.'), ('BC1F1_28_sim.txt', '.'), ('BC1F1_29_sim.txt', '.'), ('BC1F1_30_sim.txt', '.'), ('BC1F1_31_sim.txt', '.'), ('BC1F1_32_sim.txt', '.'), ('BC1F1_33_sim.txt', '.'), ('BC1F1_34_sim.txt', '.'), ('BC1F1_35_sim.txt', '.'), ('BC1F1_36_sim.txt', '.'), ('BC1F1_37_sim.txt', '.'), ('BC1F1_38_sim.txt', '.'), ('BC1F1_39_sim.txt', '.'), ('BC1F1_40_sim.txt', '.'), ('BC1F1_41_sim.txt', '.'), ('BC1F1_42_sim.txt', '.'), ('BC1F1_43_sim.txt', '.'), ('BC1F1_44_sim.txt', '.'), ('BC1F1_45_sim.txt', '.'), ('BC1F1_46_sim.txt', '.'), ('BC1F1_47_sim.txt', '.'), ('BC1F1_48_sim.txt', '.'), ('BC1F1_49_sim.txt', '.'), ('BC1F1_50_sim.txt', '.'), ('RIL_10_sim.txt', '.'), ('RIL_11_sim.txt', '.'), ('RIL_12_sim.txt', '.'), ('RIL_13_sim.txt', '.'), ('RIL_14_sim.txt', '.'), ('RIL_15_sim.txt', '.'), ('RIL_16_sim.txt', '.'), ('RIL_17_sim.txt', '.'), ('RIL_18_sim.txt', '.'), ('RIL_19_sim.txt', '.'), ('RIL_20_sim.txt', '.'), ('RIL_21_sim.txt', '.'), ('RIL_22_sim.txt', '.'), ('RIL_23_sim.txt', '.'), ('RIL_24_sim.txt', '.'), ('RIL_25_sim.txt', '.'), ('RIL_26_sim.txt', '.'), ('RIL_27_sim.txt', '.'), ('RIL_28_sim.txt', '.'), ('RIL_29_sim.txt', '.'), ('RIL_30_sim.txt', '.'), ('RIL_31_sim.txt', '.'), ('RIL_32_sim.txt', '.'), ('RIL_33_sim.txt', '.'), ('RIL_34_sim.txt', '.'), ('RIL_35_sim.txt', '.'), ('RIL_36_sim.txt', '.'), ('RIL_37_sim.txt', '.'), ('RIL_38_sim.txt', '.'), ('RIL_39_sim.txt', '.'), ('RIL_40_sim.txt', '.'), ('RIL_41_sim.txt', '.'), ('RIL_42_sim.txt', '.'), ('RIL_43_sim.txt', '.'), ('RIL_44_sim.txt', '.'), ('RIL_45_sim.txt', '.'), ('RIL_46_sim.txt', '.'), ('RIL_47_sim.txt', '.'), ('RIL_48_sim.txt', '.'), ('RIL_49_sim.txt', '.'), ('RIL_50_sim.txt', '.'), ('P_singele_snpindex.py', '.'), ('P_snpindex.py', '.'), ('PF_singele_snpindex.py', '.'), ('PF_snpindex.py', '.'), ('PP_singele_snpindex.py', '.'), ('PP_snpindex.py', '.'), ('PPF_singele_snpindex.py', '.'), ('PPF_snpindex.py', '.')],
    hiddenimports=['tkinterdnd2', 'pandas', 'numpy'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='QTL-seq_GUI_ver1_02',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['QTL_seq_GUI.icns'],
)
app = BUNDLE(
    exe,
    name='QTL-seq_GUI_ver1_02.app',
    icon='QTL_seq_GUI.icns',
    bundle_identifier=None,
)
