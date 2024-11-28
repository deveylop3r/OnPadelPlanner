# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.building.build_main import Analysis, PYZ, EXE

block_cipher = None

added_files = [
    ('ui/*.ui', 'ui'),
    ('ui/ressources/icons/*', 'ui/ressources/icons'),
    ('ui/ressources/images/*', 'ui/ressources/images'),
    ('onpadelPlanner.db', '.')
]

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'pandas',
        'openpyxl'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='onPadelPlanner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='ui/ressources/icons/logo_smalltrans.png'
)