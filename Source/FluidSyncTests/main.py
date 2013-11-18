import os
import subprocess
import time
import fnmatch
from track import Track

sox = "c:\\Program Files (x86)\\sox-14-4-1\\sox.exe"
hashBuild = "d:\\TestCodec\\FingerPrint\\FingerprintTest\\HashBuild.exe"
hbTool = "d:\\TestCodec\\FingerPrint\\FingerprintTest\\HBTool.exe"
hashSearch = "d:\\TestCodec\\FingerPrint\\FingerprintTest\\HashSearch.exe"

aifSetAll = "d:\\TestCodec\\FingerPrint\\FingerprintTest\\AifSetAll\\"
aifSet = "d:\\TestCodec\\FingerPrint\\FingerprintTest\\AifSet\\"
baseName = aifSet + "fpBase.hbs"
baseNameAdditional = aifSet + "fpBase.nbs"

maxLengthCheck = 100

tracks = list()

os.chdir(aifSet)


# Читаем файлы из директории
for dirname, dirnames, filenames in os.walk(aifSetAll):
    for filename in filenames:
        if fnmatch.fnmatch(filename, '*.aif'):
            path = os.path.join(aifSetAll, filename)
            track = Track()
            track.path = path
            tracks.append(track)


# Преобразование aif to wav
#for track in tracks:
#    wavFileName = os.path.splitext(track.path)[0] + ".wav"
#    subprocess.call([sox, track.path, wavFileName])
#    track.path = wavFileName



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
    print()
    print(track.hashPath)
    print("FP_ID = " + str(track.fingerPrintId))
    #print(track.hashPath)

tracks = list()

# Читаем файлы из директории для резки
for dirname, dirnames, filenames in os.walk(aifSet):
    for filename in filenames:
        if fnmatch.fnmatch(filename, '*.aif'):
            path = os.path.join(aifSet, filename)
            track = Track()
            track.path = path
            tracks.append(track)

# Определям длины файлов

for track in tracks:
    track.audioLength = int(float(subprocess.check_output([sox, "--i", "-D", track.path]).strip()))
    #print(track.path + " - " + str(track.audioLength))

# Режем файлы на куски по 5с с интервалом 0.1с
for track in tracks:
    i = 0
    while i < 10 * min(maxLengthCheck, track.audioLength - 5):
        i += 1
        cutFragmentName = os.path.splitext(track.path)[0] + "_" + str(i*100) + ".aif"
        subprocess.check_output([sox, track.path, cutFragmentName, "trim", str(i/10), "5"])

        cutHashName = os.path.splitext(cutFragmentName)[0] + ".hash"
        subprocess.check_output([hashBuild, cutFragmentName, cutHashName])
        os.remove(cutFragmentName)

        #track.peacesHashes.append(cutHashName)
        track.peacesHashes[cutHashName] = i*100
        #print(track.peacesHashes[track.peacesHashes.count - 1])




time.sleep(1)
# Запись результатов в файл
resultFile = open("result.txt", 'w')

#Делаем поиск по маленьким хешам в базе
for track in tracks:
    for peaceHashPath in track.peacesHashes:

        result = str(subprocess.check_output([hashSearch, "-w", peaceHashPath, baseName]))
        print("result = " + result)
        #idIndex = int(out.find("contains id = "))
        os.remove(peaceHashPath)
        print()
        print("Searching " + peaceHashPath)
        print(result)
        idIndex = int(result.find("->"))
        if(idIndex>0):
            fpId = result[idIndex+6:].split(':')[0]
            print(fpId)
            fpId = int(fpId.lstrip('0'),16)

            print("FP_ID = " + str(fpId))

            shiftIndex = int(result.find("shift = "))
            shift = int(result[shiftIndex+8:].split(' ')[0])
            print("Shift = " + str(shift))
            resultFile.write(peaceHashPath+ "," + str(fpId) + "," + str(shift) + "," + str(track.peacesHashes[peaceHashPath])+"\n")
        else:
            print("Search failed")
            resultFile.write(peaceHashPath+ "," + "Failed" + "," + "Failed" + "," + track.peacesHashes[peaceHashPath]+"\n")

    # print(subprocess.check_output([hashSearch, "-w", peaceHashPath, baseName,result]))

resultFile.close()

