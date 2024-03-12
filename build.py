import base64
import hashlib
import sys

os = sys.argv[1]

files = [
    'CADD/Raccoon2/BoincClient.py',
    'CADD/Raccoon2/gui/AA_setup.py',
    'CADD/Raccoon2/gui/BB_ligand.py',
    'CADD/Raccoon2/gui/CC_receptor.py',
    'CADD/Raccoon2/gui/EE_jobmanager.py',
    'CADD/Raccoon2/gui/FF_anaylsis.py',
    'CADD/Raccoon2/gui/Raccoon2GUI.py',
    'CADD/Raccoon2/gui/RaccoonEngine.py',
    'CADD/Raccoon2/gui/icons/boinc.png'
]

def get_file_hash(file):
    with open(file, 'rb') as f:
        return hashlib.sha512(f.read()).hexdigest()
    
def get_file_content(file):
    with open(file, 'rb') as f:
        return base64.b64encode(f.read())

def build_installer_py():
    with open('raccoon2_boinc_installer.py', 'w') as f:
        f.write('# IMPORTANT: Do not run this file directly.\n')
        f.write('# Please read README.md first for usage instructions.\n')
        f.write('import base64\n')
        f.write('import hashlib\n')
        f.write('import os\n')
        f.write('import shutil\n')
        f.write('import sys\n')
        f.write('curdir = os.getcwd()\n')
        f.write('if len(sys.argv) > 1 and sys.argv[1] == \'install\':\n')
        for file in files:
            hash = get_file_hash(file)
            content = get_file_content(file)
            if os == 'linux' or os == 'macos':
                f.write('   file = curdir+\'/MGLToolsPckgs/%s\'\n' % file)
            elif os == 'windows':
                f.write('   file = curdir+\'/Lib/site-packages/%s\'\n' % file)
            f.write('   content = %s\n' % content)
            f.write('   if os.path.exists(file):\n')
            f.write('      with open(file, \'rb\') as f:\n')
            f.write('          hash = hashlib.sha512(f.read()).hexdigest()\n')
            f.write('      if hash != \'%s\':\n' % hash)
            f.write('          shutil.copy(file, file+\'.orig\')\n')
            f.write('          with open(file, \'wb\') as f:\n')
            f.write('              f.write(base64.b64decode(content))\n')
            f.write('      else:\n')
            f.write('          print(\'already updated: \' + file)\n')
            f.write('   else:\n')
            f.write('      with open(file, \'wb\') as f:\n')
            f.write('          f.write(base64.b64decode(content))\n')
        f.write('   print (\'Done\')\n')
        f.write('elif len(sys.argv) > 1 and sys.argv[1] == \'uninstall\':\n')
        for file in files:
            if os == 'linux' or os == 'macos':
                f.write('   file = curdir+\'/MGLToolsPckgs/%s\'\n' % file)
            elif os == 'windows':
                f.write('   file = curdir+\'/Lib/site-packages/%s\'\n' % file)
            f.write('   if os.path.exists(file+\'.orig\'):\n')
            f.write('       shutil.copy(file+\'.orig\', file)\n')
            f.write('       os.remove(file+\'.orig\')\n')
        f.write('   print (\'Done\')\n')
        f.write('else:\n')
        f.write('   print (\'Please read README.md for usage instructions.\')\n')

if __name__ == "__main__":
    build_installer_py()
