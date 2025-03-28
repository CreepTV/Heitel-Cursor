# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['HeitelCursorInstaller.py'],
    pathex=[],
    binaries=[],
    datas=[],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='HeitelCursorInstaller',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='C:\\Users\\MaRe\\HeitelCursors\\Heitel-Cursors\\recources\\HeitelCursorsInstallerIcon.ico',
    manifest='C:\\Users\\MaRe\\HeitelCursors\\Heitel-Cursors\\Heitel Cursor Installer\\HeitelCursorInstaller.manifest'
)
