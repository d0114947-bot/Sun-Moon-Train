# 曦月渡：兩萬人模擬試玩（代理人模型）。參數是依照遊戲程式內容估的，不是真人資料。
import numpy as np, json
rng=np.random.default_rng(20261125)
N=20000
# 段落：名稱, 中位時間(分), 要點的對話句數, 引導清楚度g, 新鮮感nov, 操作/解謎難度diff, 劇情回報payoff
SEG=[
 ('開場：醒來、標題',            0.8,  2, .90,.85,.00,.4),
 ('飛行教學（三步）',              1.3,  2, .82,.70,.22,.1),
 ('秘器劇情（意識文字）',          1.6,  8, .70,.55,.10,.4),
 ('第一次異常與切換（V）',         0.9,  3, .85,.85,.10,.6),
 ('光痕（切過去就看見自己的路）',   0.6,  2, .90,.75,.05,.5),
 ('自動跟著星光飛、看見列車',      0.8,  2, .85,.75,.05,.6),
 ('晨曦森林、上車（觀察可略過）',    1.0,  3, .88,.80,.08,.6),
 ('銘文、聽見聲音、走到駕駛室',    1.3,  7, .80,.55,.10,.5),
 ('曦淵見面與車廂導覽',            1.3,  6, .90,.60,.00,.7),
 ('索拉漂進來、說出心願',           1.0,  7, .90,.75,.00,.8),
 ('晶盤甦醒、曦淵帶著做一次值勤',   2.3,  8, .85,.60,.15,.7),
 ('第一次航行（途中才教裝置）',     6.5, 22, .70,.75,.25,.6),
 ('第一章（停靠、主角上車、抉擇）', 11.0, 55, .63,.65,.38,.7),
 ('第二～三章（值勤循環第 2～4 次）',22.0,110, .62,.50,.42,.6),
 ('第四～七章與結局',              55.0,240, .57,.43,.48,.8),
]
P=[ # 族群, 比例, 耐心, 閱讀耐受, 迷路耐受, 操作熟練, 新鮮感權重, 劇情權重
 ('休閒',   .38, .85, .60, .50, .50,1.0, .6),
 ('劇情派', .24,1.20,1.60, .60, .50, .7,1.5),
 ('探索派', .18,1.00, .90, .90, .70,1.4, .7),
 ('效率派', .12, .80, .45, .80, .85, .8, .4),
 ('觸控',   .08, .75, .80, .50, .40,1.0, .7),
]
pi=rng.choice(len(P),N,p=[x[1] for x in P])
pat=np.array([P[i][2] for i in pi])*rng.lognormal(0,.25,N)
rd =np.array([P[i][3] for i in pi])*rng.lognormal(0,.25,N)
ct =np.array([P[i][4] for i in pi])*rng.lognormal(0,.2,N)
sk =np.clip(np.array([P[i][5] for i in pi])+rng.normal(0,.12,N),.05,1)
nw =np.array([P[i][6] for i in pi]); sw=np.array([P[i][7] for i in pi])
touch=(pi==4)
alive=np.ones(N,bool); B=np.zeros(N)            # 累積的膩
S=len(SEG); reach=np.zeros(S); quitB=np.zeros(S); quitC=np.zeros(S); conf=np.zeros(S); strug=np.zeros(S); mins=np.zeros(S)
confP=np.zeros((S,len(P))); quitP=np.zeros((S,len(P))); reachP=np.zeros((S,len(P)))
for k,(nm,dur,cl,g,nov,diff,pay) in enumerate(SEG):
    a=alive.copy(); reach[k]=a.sum()
    for j in range(len(P)): reachP[k,j]=(a&(pi==j)).sum()
    d=diff+(.25 if (touch.any() and k==1) else 0)*touch   # 觸控玩家：飛行操作更難
    # 卡關／迷路
    pc=np.clip((1-g)*(.55+diff)*(1.35-ct),0,.95); c=a&(rng.random(N)<pc)
    ps=np.clip(d*(1-sk)*1.2,0,.9); st=a&(rng.random(N)<ps)
    t=dur*rng.lognormal(0,.35,N)+c*rng.exponential(2.5,N)+st*rng.exponential(1.5,N)
    # 膩：時間 × 沒新鮮感 ＋ 要讀的字 ÷ 閱讀耐受；劇情回報會沖淡一點
    inc=t*(1-nov*nw*.8)*.11 + cl/(rd*38) + c*.5 + st*.3
    B=np.where(a, B*.92+inc - pay*sw*.12, B); B=np.maximum(B,0)
    hb=1/(1+np.exp(-(B-pat*3.9)/.6))*.28                    # 膩到不想玩
    hc=c*np.clip(.22*(1.2-ct),0,.5)                          # 迷路、不知道要做什麼而離開
    qb=a&(rng.random(N)<hb); qc=a&~qb&(rng.random(N)<hc)
    alive=a&~qb&~qc
    quitB[k]=qb.sum(); quitC[k]=qc.sum(); conf[k]=c.sum(); strug[k]=st.sum(); mins[k]=np.median(t[a])
    for j in range(len(P)): confP[k,j]=(c&(pi==j)).sum(); quitP[k,j]=((qb|qc)&(pi==j)).sum()
out={'seg':[s[0] for s in SEG],'reach':(reach/N).round(4).tolist(),'quitBored':(quitB/N).round(4).tolist(),'quitLost':(quitC/N).round(4).tolist(),
     'confused':(conf/np.maximum(reach,1)).round(3).tolist(),'struggle':(strug/np.maximum(reach,1)).round(3).tolist(),'median_min':mins.round(1).tolist(),
     'finish':float(alive.mean()),'persona':[p[0] for p in P],'personaShare':[float((pi==j).mean()) for j in range(len(P))],
     'finishP':[float((alive&(pi==j)).sum()/(pi==j).sum()) for j in range(len(P))],
     'confByP':(confP/np.maximum(reachP,1)).round(3).tolist(),'quitByP':(quitP/np.maximum(reachP,1)).round(3).tolist()}
json.dump(out,open('/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad/sim20k_v4.json','w'),ensure_ascii=False,indent=1)
print(f"完成全部：{out['finish']:.1%}")
for k,n in enumerate(out['seg']):
    print(f"{k+1:2d} {n:<22} 到達{out['reach'][k]:6.1%} 迷路{out['confused'][k]:5.1%} 卡操作{out['struggle'][k]:5.1%} 膩走{out['quitBored'][k]:5.1%} 迷走{out['quitLost'][k]:5.1%} {out['median_min'][k]}分")
import numpy as _n
cum=_n.cumsum(out['median_min']); print('累積（中位數，分）：',[round(x,1) for x in cum])
print('各族群完成率',dict(zip(out['persona'],[round(x,3) for x in out['finishP']])))
