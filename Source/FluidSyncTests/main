import os
import subprocess
import time
import fnmatch
from track import Track

sox = "c:\\Program Files (x86)\\sox-14-4-1\\sox.exe"
hashBuild = "d:\\TestCodec\\FingerPrint\\FingerprintTest\\HashBuild.exe"
hbTool = "d:\\TestCodec\\FingerPrint\\FingerprintTest\\HBTool.exe"
hashSearch = "d:\\TestCodec\\FingerPrint\\FingerprintTest\\HashSearch.exe"

dirName = "d:\\TestCodec\\FingerPrint\\FingerprintTest\\"
aifSet =  "d:\\TestCodec\\FingerPrint\\FingerprintTest\\AifSet\\"
baseName = aifSet + "fpBase.hbs"
baseNameAdditional = aifSet + "fpBase.nbs"

maxLengthCheck = 100

tracks = list()

os.chdir(dirName)


# Читаем файлы из директории
for dirname, dirnames, filenames in os.walk(aifSet):
    for filename in filenames:
        if fnmatch.fnmatch(filename, '*.aif'):
            path = os.path.join(dirName, filename)
            track = Track()
            track.path = path
            tracks.append(track)


# Преобразование aif to wav
#for track in tracks:
#    wavFileName = os.path.splitext(track.path)[0] + ".wav"
#    subprocess.call([sox, track.path, wavFileName])
#    track.path = wavFileName

# Определям длины файлов

for track in tracks:
    track.audioLength = int(float(subprocess.check_output([sox, "--i", "-D", track.path]).strip()))
    #print(track.path + " - " + str(track.audioLength))

#Делаем хеши полных файлов
for track in tracks:
    track.hashPath = os.path.splitext(track.path)[0] + ".hash"
    subprocess.check_output([hashBuild, track.path, track.hashPath])


# Удаляем базу перед началом добавления
if os.path.exists(baseName):
    os.remove(baseName)
if os.path.exists(baseNameAdditional):
    os.remove(baseNameAdditional)


# Добавляем хэш в базу, определям fingerPrintId из вывода утилиты
for track in tracks:
    out = subprocess.check_output([hbTool, "-add", track.hashPath, baseName, "The Comment"])
    out = str(out).replace(os.linesep, ' ') # тут черная магия


    idIndex = int(out.find("contains id = "))
    track.fingerPrintId = int(out[idIndex+14:].split('\\')[0]) # 14 - длина строки "contains id = "
    print(track.hashPath)
    #print(track.hashPath)


# Режем файлы на куски по 5с с интервалом 0.1с
for track in tracks:
    i = 10
    while i < 10 * min(maxLengthCheck, track.audioLength - 5):
        i += 1
        cutFragmentName = os.path.splitext(track.path)[0] + "_" + str(i) + ".aif"
        subprocess.check_output([sox, track.path, cutFragmentName, "trim", str(i/10), "5"])

        cutHashName = os.path.splitext(cutFragmentName)[0] + ".hash"
        subprocess.check_output([hashBuild, cutFragmentName, cutHashName])

        track.peacesHashes.append(cutHashName)
        #print(track.peacesHashes[track.peacesHashes.count - 1])
        break



time.sleep(1)
#Делаем поиск по маленьким хешам в базе
for track in tracks:
    for peaceHashPath in track.peacesHashes:

        result = os.path.splitext(peaceHashPath)[0] + "_result.txt"

        code = subprocess.check_call([hashSearch, "-w", peaceHashPath, baseName, result])

        #print("hashSearch exit code = "+ str(code))
        #print(subprocess.check_output([hashSearch, "-w", peaceHashPath, baseName,result]))



