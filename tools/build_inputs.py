# 把實測數據組成模擬用的段落參數（seg_inputs.json）
import json
M=json.load(open('metrics.json')); T=M['text']
BOT={'P1':242,'P2':186,'P3':169,'P4':67,'P5':58,'P6':195,'P7':93}   # 機器人實測（秒，不含閱讀）
mid=M['mid']; HAB=mid['habitat0']; CAB=mid['cab0']
sig=T['sigCycle']; voy=T['voyMs']/1000; skywin=T['skyWin']*voy
lore_ch=sum(x['chars'] for x in T['lore'])/len(T['lore']); talk_ch=sum(x['chars'] for x in T['talks'])/len(T['talks'])/3
S=[]
def seg(**k): k.setdefault('hotspots',4); k.setdefault('burst',2); k.setdefault('puzzle',0); k.setdefault('clarity',.8); S.append(k)
P='序章'
seg(key='P1',part=P,name='第一幕 甦醒與飛行',base=BOT['P1'],chars=620,clarity=.7,hotspots=1,burst=2,puzzle=.35,why='要自己發現「停下來等，秘器才會亮」')
seg(key='P2',part=P,name='第二幕 日月切換',base=BOT['P2'],chars=520,clarity=.65,hotspots=1,burst=2,puzzle=.3,why='光痕只有切換日月界才看得到')
seg(key='P3',part=P,name='第三幕 縫隙與列車',base=BOT['P3'],chars=480,clarity=.7,hotspots=3,burst=2,puzzle=.25,why='要找到「變密的星光」')
seg(key='P4',part=P,name='第四幕 認識車廂',base=BOT['P4'],chars=950,clarity=.95,hotspots=7,burst=4,why='四節車廂各一段介紹')
seg(key='P5',part=P,name='第五幕 索拉上車',base=BOT['P5'],chars=720,clarity=.9,hotspots=8,burst=4)
seg(key='P6',part=P,name='第六幕 出發與月輝潮汐',base=BOT['P6'],chars=1550,clarity=.85,hotspots=CAB['hs']+1,burst=6,puzzle=.2,wait=10,why='值勤 7 步＋危機，台詞和廣播常常同時出現')
seg(key='P7',part=P,name='尾聲 星河浮島',base=BOT['P7'],chars=600,clarity=.9,hotspots=4,burst=3)
def journey(j,extra_chars=0,gate=0,wait_add=0,name=None,why='',window=0,retry=0,clar=.6):
    seg(key=f'J{j}',part='旅程',name=name or f'第 {j} 趟旅程',base=55+voy+15,chars=170+extra_chars+(talk_ch*2 if j>=3 else 0),clarity=clar,hotspots=max(CAB['hs'],HAB['hs']) if j>=4 else CAB['hs'],
        burst=HAB['imp'] if j>=5 else 3,routine='duty',reps=1,rep_cost=26,wait=sig[j%6]+wait_add,gate=gate,window=window,retry=retry,why=why)
Q='主線'
journey(1,name='第 1 趟（序章後第一趟）',why='值勤 6 步之後不再有提示')
seg(key='Q1',part=Q,name='主線① 看看封存的種子',base=40,chars=160,clarity=.85,hotspots=6,burst=2)
for j in range(2,7): journey(j,extra_chars=(250 if j>=3 else 0)+(lore_ch if j in (3,5) else 0),gate=150,why='主線卡在「旅程 7/7」，中間沒有新的主線目標')
seg(key='Q2',part=Q,name='主線② 聽曦淵說列車的故事',base=60,chars=lore_ch*4,clarity=.45,hotspots=CAB['hs'],burst=3,puzzle=.35,why='要在「航行中」到駕駛室找曦淵，目標沒寫；有幾趟曦淵還會飛出去')
journey(7,extra_chars=250+lore_ch)
seg(key='Q3n',part=Q,name='主線③ 改航道去逆生之境',base=50,chars=200,clarity=.6,hotspots=6,burst=3,puzzle=.25,why='要找到觀測車廂的導航裝置')
journey(8,name='第 8 趟 逆生之境',extra_chars=88)
seg(key='Q3',part=Q,name='主線③ 晨種（讀刻紋→看窗外→晨光）',base=120,chars=420,clarity=.75,hotspots=8,burst=3,puzzle=.2)
journey(9,name='第 9 趟 無界迴廊（暗影航段）',extra_chars=78,wait_add=50,window=.25*voy,retry=90,why='暗影航段只有約 37 秒，要及時切月界')
seg(key='Q4',part=Q,name='主線④ 潮種（月界＋天窗）',base=90,chars=360,clarity=.75,hotspots=5,burst=3,puzzle=.25)
journey(10,name='第 10 趟 時隙之海',extra_chars=92,window=.25*voy,retry=60)
seg(key='Q5',part=Q,name='主線⑤ 暮種（晶石＋切換）',base=80,chars=320,clarity=.75,hotspots=5,burst=3,puzzle=.3)
seg(key='SK',part='支線',name='天象（只出現約 33 秒）',base=40,chars=150,clarity=.7,hotspots=3,burst=3,window=skywin,retry=150,why='天象窗口短，又在火車最尾端')
for j in range(11,15): journey(j,extra_chars=250,gate=200,why='要湊滿 8 件紀念品，只能一直跑')
seg(key='Q6',part=Q,name='主線⑥ 前往寂滅虛空（結局）',base=voy+60,chars=900,clarity=.8,hotspots=6,burst=4,routine='duty',reps=1,rep_cost=26)
json.dump({'segments':S},open('seg_inputs.json','w'),ensure_ascii=False,indent=1); print(len(S),'segments')
