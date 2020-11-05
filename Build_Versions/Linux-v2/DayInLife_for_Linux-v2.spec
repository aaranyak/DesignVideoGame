# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/home/aaranyak/Documents/School_Work_grade_7/Design/Unit1/Projects/DesignVideoGame'],
             binaries=[],
             datas=[('sprites.py', '.'), ('settings.py', '.'), ('./Music/*', './Music'), ('./Pictures/*', './Pictures/'), ('./Pictures/Cars/*', './Pictures/Cars/'), ('pygame.zip', '.'), ('./topper.py', '.'), ('credentials.json', '.'), ('token.pickle', '.'), ('google-api-python-client-1.12.5.zip', '.'), ('google-auth-httplib2.zip', '.'), ('google-auth-oauthlib-0.4.2.zip', '.')],
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
          name='DayInLife_for_Linux-v2',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
