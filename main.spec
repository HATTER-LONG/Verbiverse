# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_all
from PyInstaller.utils.hooks import copy_metadata
datas = [('./PDF_js', './PDF_js')]
binaries = []
hiddenimports = []
need_collect_all = ['langchain', 'chromadb', 'onnxruntime']
for item in need_collect_all:
    tmp_ret = collect_all(item)
    datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

a = Analysis(
    ['main.py'],
    pathex=['./verbiverse',
            './verbiverse/CustomWidgets',
            './verbiverse/UI',
            './verbiverse/Functions',
            './verbiverse/LLM',
            './verbiverse/resources'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
a.datas += [('ic_launcher_round.png','.\\icons\\android\\mipmap-xxxhdpi\\ic_launcher_round.png','DATA')]
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Verbiverse',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    contents_directory='__depend__',
    icon='.\\icons\\android\\mipmap-xxxhdpi\\ic_launcher_round.png',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Verbiverse',
)
app = BUNDLE(
    coll,
    name='Verbiverse.app',
    bundle_identifier=None,
)
