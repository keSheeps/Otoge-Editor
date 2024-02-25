import const
import pickle
START_SEC=1
#note([beginX,EndX,BeginY,noteKind,MPM])
#chart[note,note,note,....]
with open('chart.pickle', mode='br') as fi:
        allChart = pickle.load(fi)
print("""/title:曲名
title:
/composer:作曲者名
composer:
/designer:譜面作者名
designer:
/wav:音声ファイルのパス
wav:
/offset:ノートのタイミングを -:早くする +:遅くする (単位[s])
offset:""")

print("""/MPM変化位置
#MPM""")
chartNo=0
for charts in allChart:
    chartSec=START_SEC
    for chart in charts:
        for note in chart:
            if(const.NOTE_KINDS[note[3]][0]!="MPMChange"):
                 continue
            print(note[2]+chartSec,end=",")
            print(note[4])
        chartSec=chartSec+1
    chartNo=chartNo+1

print("""/ノート位置
#NOTE""")
chartNo=0
for charts in allChart:
    chartSec=START_SEC
    for chart in charts:
        for note in chart:
            if(const.NOTE_KINDS[note[3]][0]=="MPMChange"):
                 continue
            print(note[2]+chartSec,end=",")
            print(const.NOTE_KINDS[note[3]][0],end=",")
            print(note[0]+chartNo,end=",")
            print(note[1]+chartNo)
        chartSec=chartSec+1
    chartNo=chartNo+1