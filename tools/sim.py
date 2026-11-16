# 2 萬名玩家模擬：每一段的時間、卡住的原因、在哪裡放棄
# 輸入：遊戲實測（機器人計時、熱點數、台詞字數、等待秒數、主線需要的趟數）＋玩家類型的假設
# 輸出：sim_out.json
import numpy as np, json, sys
rng=np.random.default_rng(20261116)
N=20000
M=json.load(open('seg_inputs.json'))           # 段落參數（由 build_inputs.py 從實測數據產生）
SEG=M['segments']
# ---------- 玩家類型（比例與特質都是假設，報告裡會標明） ----------
TYPES={
 '目標導向':dict(share=.30,speed=(1.0,1.3),cps=(8,13),skim=.45,explore=.25,skill=(.6,.95),patience=(420,900),bore=(3,6),tol=(1.0,1.6),react=(3,8)),
 '探索型':  dict(share=.25,speed=(1.2,1.7),cps=(6,10),skim=.15,explore=.85,skill=(.5,.9),patience=(900,1800),bore=(5,10),tol=(1.4,2.2),react=(4,10)),
 '劇情休閒':dict(share=.30,speed=(1.3,2.0),cps=(4,8),skim=.05,explore=.5,skill=(.3,.7),patience=(600,1200),bore=(4,8),tol=(0.8,1.3),react=(6,14)),
 '手機零碎':dict(share=.15,speed=(1.1,1.6),cps=(7,12),skim=.6,explore=.2,skill=(.35,.75),patience=(240,600),bore=(2,4),tol=(0.6,1.0),react=(5,12)),
}
names=list(TYPES); share=np.array([TYPES[k]['share'] for k in names]); tix=rng.choice(len(names),N,p=share/share.sum())
def U(key): lo=np.array([TYPES[names[t]][key][0] for t in tix]); hi=np.array([TYPES[names[t]][key][1] for t in tix]); return lo+(hi-lo)*rng.random(N)
import os
speed,cps,skill,patience,bore,tol,react=U('speed'),U('cps'),U('skill'),U('patience'),U('bore'),U('tol'),U('react')
tol*=float(os.environ.get('TOLX',1)); bore*=float(os.environ.get('BOREX',1)); patience*=float(os.environ.get('PATX',1)); skill=np.clip(skill*float(os.environ.get('SKX',1)),.05,1)
skim=np.array([TYPES[names[t]]['skim'] for t in tix]); explore=np.array([TYPES[names[t]]['explore'] for t in tix])
CAUSES=['太難','沒有目標','標示不清楚','膩了','資訊太多','時間太短']
alive=np.ones(N,bool); frus=np.zeros(N); reps={}            # 累積的挫折感、每一種例行公事做了幾次
out=[]
for S in SEG:
    n=alive.sum(); idx=np.where(alive)[0]
    base=S['base']*speed[idx]                                            # 熟練玩家的操作時間 × 個人速度
    read=S['chars']/cps[idx]*(1-.6*skim[idx]*S.get('skippable',1))       # 讀台詞
    # 標示不清楚：沒有直接標在要點的地方 → 在一堆熱點裡找
    clar=S['clarity']; H=S['hotspots']
    search=(1-clar)*H*rng.uniform(3,7,n)/2*(1.2-.5*explore[idx])
    # 太難：需要自己想通的機關
    d=S['puzzle']; puzzle=np.where(d>0,rng.exponential(np.maximum(1,d*260/np.maximum(skill[idx],.15)),n),0)*(1-.35*clar)
    # 資訊太多：同一個畫面的熱點＋同時出現的台詞，超過個人能吸收的量
    load=H/8+S['burst']/6; over=np.maximum(0,load-tol[idx]); overload=over*S['base']*.6+over*S['chars']/cps[idx]*.4
    # 時間太短：有時間窗的事（天象、暗影航段），反應不及就要等下一趟
    win=S.get('window',0); pmiss=np.where(win>0,1-np.exp(-np.maximum(0,react[idx]+search*.1-win*.15)/max(win,1)),0)
    pmiss=np.where(win>0,np.clip(pmiss+(1-clar)*.25,0,.9),0); retry=(rng.random(n)<pmiss)*S.get('retry',0)
    # 沒有目標：要靠「跑幾趟」才會推進、這段時間沒有新的事可做
    gate=S.get('gate',0); nogoal=gate*(1-.55*explore[idx])
    # 膩了：同一套例行公事重複太多次（值勤 6 項、等號誌）
    k=S.get('routine'); bored=np.zeros(n)
    if k:
        reps[k]=reps.get(k,np.zeros(N)); reps[k][idx]+=S.get('reps',1); extra=np.maximum(0,reps[k][idx]-bore[idx])
        bored=extra*S.get('rep_cost',20)*(1+.5*(skim[idx]<.3))
    wait=S.get('wait',0); waitbore=np.maximum(0,wait-patience[idx]*.15)*.5     # 枯等也算膩
    comp=np.stack([puzzle,nogoal,search,bored+waitbore,overload,retry])       # 依 CAUSES 順序
    total=base+read+wait+comp.sum(0)
    # 挫折感：多花的時間佔原本時間的比例，越多越容易放棄
    exc=comp.sum(0); frus[idx]=frus[idx]*.85+exc/np.maximum(60,base+read+wait)*60
    quit_p=np.clip((frus[idx]/patience[idx]*3.2)**2*.10,0,.35)*S.get('quitw',1)
    q=rng.random(n)<quit_p; alive[idx[q]]=False
    dom=np.argmax(comp,0); sig=exc>.35*(base+read+wait)
    cause_cnt={c:int(((dom==i)&sig).sum()) for i,c in enumerate(CAUSES)}; cause_cnt['順利']=int((~sig).sum())
    by_type={names[t]:float(np.median(total[tix[idx]==t])) for t in range(len(names)) if (tix[idx]==t).any()}
    out.append(dict(key=S['key'],name=S['name'],part=S['part'],players=int(n),median=float(np.median(total)),p25=float(np.percentile(total,25)),p75=float(np.percentile(total,75)),p90=float(np.percentile(total,90)),
      comp={c:float(np.mean(comp[i])) for i,c in enumerate(CAUSES)},base=float(np.mean(base+read+wait)),causes=cause_cnt,quit=int(q.sum()),quit_types={names[t]:int((q&(tix[idx]==t)).sum()) for t in range(len(names))},by_type=by_type,why=S.get('why','')))
OUTF=os.environ.get('OUT','sim_out.json')
json.dump(dict(N=N,types={k:TYPES[k]['share'] for k in names},seg=out,finished=int(alive.sum())),open(OUTF,'w'),ensure_ascii=False,indent=1)
for o in out: print(f"{o['name'][:14]:<16}{o['players']:>6} 中位 {o['median']/60:5.1f} 分  p90 {o['p90']/60:5.1f}  放棄 {o['quit']:>5}  主因 {max((v,k) for k,v in o['causes'].items() if k!='順利')[1]}")
print('走完全程', alive.sum())
