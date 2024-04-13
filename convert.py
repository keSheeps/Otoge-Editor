import const
import pickle
START_SEC=1
#note([beginX,EndX,BeginY,noteKind,MPM])
#chart[note,note,note,....]
def compile(dir,offset):
    with open(dir+r'\test.cht',mode='w') as dest:
        with open('chart.pickle', mode='br') as fi:
            data = pickle.load(fi)
        allChart = [data[0],data[1]]
        dest.write("""/title:曲名
title:
/composer:作曲者名
composer:
/designer:譜面作者名
designer:
/level:レベル(数値)
level:1
/wav:音声ファイルのパス
wav:test.wav
/jacket:絵のファイルのパス
jacket:test.png
/offset:ノートのタイミングを -:早くする +:遅くする (単位[s])
offset:""")
        dest.write(offset)
        dest.write("\n")

        dest.write("""/MPM変化位置
#MPM
""")
        chartNo=0
        for charts in allChart:
            chartSec=START_SEC
            for chart in charts:
                for note in chart:
                    if(const.NOTE_KINDS[note[3]][0]!="MPMChange"):
                        continue
                    dest.write(str(note[2]+chartSec)+","+str(note[4])+"\n")
                chartSec=chartSec+1
            chartNo=chartNo+1

        dest.write("""/ノート位置
#NOTE
""")
        chartNo=0
        for charts in allChart:
            chartSec=START_SEC
            for chart in charts:
                for note in chart:
                    if(const.NOTE_KINDS[note[3]][0]=="MPMChange"):
                        continue
                    dest.write(str(note[2]+chartSec)+","+str(const.NOTE_KINDS[note[3]][0])+","+str(note[0]+chartNo)+","+str(note[1]+chartNo)+"\n")
                chartSec=chartSec+1
            chartNo=chartNo+1
