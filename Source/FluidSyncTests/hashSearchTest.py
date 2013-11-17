__author__ = 'XXX'

import os
import subprocess
import time
import fnmatch

sox = "c:\\Program Files (x86)\\sox-14-4-1\\sox.exe"
hashBuild = "d:\\TestCodec\\FingerPrint\\FingerprintTest\\HashBuild.exe"
hbTool = "d:\\TestCodec\\FingerPrint\\FingerprintTest\\HBTool.exe"
hashSearch = "d:\\TestCodec\\FingerPrint\\FingerprintTest\\HashSearch.exe"

dirName = "d:\\TestCodec\\FingerPrint\\FingerprintTest\\"
baseName = dirName + "fpBase.hbs"
baseNameAdditional = dirName + "fpBase.nbs"


hashes = list()

os.chdir(dirName)


for dirname, dirnames, filenames in os.walk(dirName):
    for filename in filenames:
        if fnmatch.fnmatch(filename, '*.hash'):
            path = os.path.join(dirName, filename)
            hashes.append(path)




for hash in hashes:
    result = os.path.splitext(hash)[0] + "_result.txt"
    print(hash)
    subprocess.check_call([hashSearch, "-w", hash, baseName, result])
    #print(subprocess.check_output([hashSearch, "-w", peaceHashPath, baseName,result]))
