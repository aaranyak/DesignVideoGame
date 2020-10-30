# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/home/aaranyak/Documents/School_Work_grade_7/Design/Unit1/Projects/DesignVideoGame'],
             binaries=[],
             datas=[('./sprites.py', '.'), ('./settings.py', '.'), ('pygame.zip', '.'), ('corona_radius.png', '.'), ('NaughtyNess.ogg', '.'), ('Em-Poms-.ogg', '.'), ('phaseJump2.wav', '.'), ('powerUp3.wav', '.'), ('coin.wav', '.'), ('zapThreeToneDown.wav', '.'), ('Chase.ogg', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='DayInLife-Blocked-v2',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='Build_Versions/blocked-v1/DayInLife_blocked_v1.ico')
