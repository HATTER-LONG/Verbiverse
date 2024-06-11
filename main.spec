# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=['./verbiverse',
            './verbiverse/CustomWidgets',
            './verbiverse/UI',
            './verbiverse/Functions',
            './verbiverse/LLM',
            './verbiverse/resources'],
    binaries=[],
    datas=[('./PDF_js', './PDF_js')],
    hiddenimports=[],
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
    contents_directory='.',
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
    icon=None,
    bundle_identifier=None,
)
