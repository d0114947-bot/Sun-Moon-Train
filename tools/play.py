# 序章試跑：像玩家一樣只用畫面上的東西（按鍵、點擊看得到的按鈕與 ✦ 徽章），從新遊戲玩到序章尾聲
# 紀錄：每一段花的時間、每一句台詞、每個畫面同時出現的資訊量（熱點數、提示、toast、廣播）
import json, math, time, sys, os
from playwright.sync_api import sync_playwright
OUT='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad/play'; os.makedirs(OUT,exist_ok=True)
LOG=open(OUT+'/log.txt','w')
T0=time.time()
def log(*a):
    s='[%6.1fs] '%(time.time()-T0)+' '.join(str(x) for x in a); print(s,flush=True); LOG.write(s+'\n'); LOG.flush()
STOP=sys.argv[1] if len(sys.argv)>1 else 'epi'
FROM=sys.argv[2] if len(sys.argv)>2 else ''
CK='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad/play_ck_'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--disable-blink-features=AutomationControlled']); pg=b.new_page(viewport={'width':1280,'height':720}); pg.add_init_script("Object.defineProperty(Navigator.prototype,'webdriver',{get:()=>false})"); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:(errs.append(str(e)),log('PAGEERROR',e)))
    kb=pg.keyboard
    shotn=[0]
    def shot(name):
        shotn[0]+=1; f='%s/%02d_%s.png'%(OUT,shotn[0],name); pg.screenshot(path=f); log('SHOT',f)
    seen=set()
    def watch():
        # 記錄新出現的台詞（第一幕的 a1-say、念頭、tip；列車的 dlg、cine、toast、廣播）
        txt=ev("""(()=>{const q=s=>[...document.querySelectorAll(s)].map(e=>e.innerText.trim()).filter(Boolean);
          return {say:q('.a1-say'),th:q('.a1-th .fr'),tip:q('.a1-tip.on'),a2:q('.a2-tip'),dlg:q('#layer .dlg .tx'),who:q('#layer .dlg .nm'),cine:q('#layer .cine'),toast:q('.toast'),ann:q('#announce.on .an-t')}})()""")
        for k,v in txt.items():
            for t in v:
                key=k+':'+t
                if key not in seen and len(t)>0:
                    seen.add(key); log('  '+k.upper()+':',t.replace('\n',' ')[:140])
    pg.goto('http://127.0.0.1:8766/'); W(1500)
    shot('menu')
    ev("localStorage.clear()")
    pg.click('#ms-work'); W(1800); shot('menu2'); pg.click('#ms-new'); W(1500); watch(); shot('newgame')
    for _ in range(10):
        if ev("ACT1.active()"): break
        b2=ev("[...document.querySelectorAll('#layer button, .ov button')].map(b=>b.innerText.trim()).filter(Boolean)"); log('buttons',b2)
        if ev("!!document.querySelector('#layer .ov button.btn:not(.ghost)')"): ev("document.querySelector('#layer .ov button.btn:not(.ghost)').click()")
        W(1500); watch()
    D=lambda: ev("ACT1.active()?ACT1._dbg():null")
    def hold(keys,ms):
        for k in keys: kb.down(k)
        t=0
        while t<ms: W(250); t+=250; watch()
        for k in keys: kb.up(k)
    def wait_free(ms=60000):
        t=0
        while t<ms:
            d=D()
            if d and not d['lock'] and not d['busy'] and not d['saying']: return True
            W(300); t+=300; watch()
        return False
    def face(tx,tz,tol=.12):
        for _ in range(80):
            d=D(); P=d['P']; ang=math.atan2(tx-P['x'],tz-P['z']); dy=math.atan2(math.sin(ang-P['yaw']),math.cos(ang-P['yaw']))
            if abs(dy)<tol: return
            k='e' if dy>0 else 'q'; kb.down(k); W(int(min(600,max(80,abs(dy)*500)))); kb.up(k); watch()
    def fly_to(tx,tz,stop=40,maxs=400,y=None,cond=None):
        t0=time.time()
        while time.time()-t0<maxs:
            if cond and cond(): return True
            d=D()
            if not d: return False
            if d['lock'] or d['busy']: W(400); watch(); continue
            P=d['P']; dist=math.hypot(tx-P['x'],tz-P['z'])
            if dist<stop: return True
            face(tx,tz)
            ks=['w']
            if y is not None and P['y']<y-3: ks.append('Space')
            if y is not None and P['y']>y+3: ks.append('Shift')
            hold(ks,1500)
        return False
    def ckpt(n): open(CK+n+'.json','w').write(ev("JSON.stringify(state)")); log('checkpoint',n)
    def resume(n):
        st=open(CK+n+'.json').read(); ev("ACT1.active()&&ACT1.exit()"); ev(f"loadGame(JSON.parse({json.dumps(st)}),'ck')"); W(3000); log('resumed',n)
    if FROM: resume(FROM)
    if FROM in ('a4','a5','a6','epi'): FROM='a3'
    # ================= 第一幕 =================
    if not FROM:
        A1=time.time(); log('=== 第一幕開始')
        wait_free(90000); shot('a1_awake')
        # 依畫面下方的提示操作
        for _ in range(200):
            d=D()
            if d['stage']!='tut': break
            tip=ev("(document.querySelector('.a1-tip.on')||{}).innerText||''")
            if 'W' in tip and 'S' in tip: hold(['w'],900); hold(['s'],900)
            elif 'A' in tip and 'D' in tip: hold(['a'],900); hold(['d'],900)
            elif '空白' in tip: hold(['Space'],1200)
            elif 'Shift' in tip: hold(['Shift'],1200)
            elif '放開' in tip: W(2500)
            else: W(500)
            watch()
        log('tutorial done; stage',D()['stage']); shot('a1_tutdone')
        # 自由探索：往前飛、看看四周、往上飛……直到秘器出現
        k=0
        while D()['stage']=='explore' and k<60:
            hold(['w'],2000); hold(['e'],800); k+=1
            if k%4==0: hold(['Space'],1500)
        wait_free(60000); log('stage',D()['stage']); shot('a1_held')
        # 秘器在右下角：點它
        for _ in range(40):
            st=D()['stage']
            if st in ('again','free'): break
            if not D()['lock'] and not D()['busy']: pg.click('.a1-icon')
            W(1500); watch()
        wait_free(90000); shot('a1_first_thought')
        # 「……再碰一次看看。」
        pg.click('.a1-icon'); W(2500); watch()
        wait_free(60000)
        # 等待：自然停下來，讓秘器自己亮（被動接收）
        t=0
        while D()['stage']!='ending' and not ev("state.act1.ended") and t<240:
            W(2000); t+=2; watch()
            if t%30==0: pg.click('.a1-icon'); W(2000); watch()
        log('stage',D()['stage'],'passN',ev("state.act1.passN"),'againN',ev("state.act1.againN"))
        for _ in range(200):
            if ev("state.act1.ended") and not D()['lock']: break
            W(500); watch()
            if ev("!!document.querySelector('.a1-title.on')") and not os.path.exists(OUT+'/t1'): open(OUT+'/t1','w'); shot('a1_title')
        log('=== 第一幕結束 %.0fs'%(time.time()-A1)); shot('a1_end')
        ckpt('a1')
        if STOP=='a1': sys.exit()
    # ================= 第二幕 =================
    if FROM in ('','a1'):
        A2=time.time(); log('=== 第二幕開始'); W(3000); shot('a2_start_view')
        d=D(); log('pos',d['P'])
        # 看看星點路徑：轉一圈找光點（玩家會先環顧）
        for i in range(8): hold(['e'],700);
        shot('a2_look')
        fly_to(0,1700,stop=60,y=60,maxs=400,cond=lambda: ev("state.act2&&state.act2.firstAnomalySeen"))
        # 穿過水幕中段
        t=0
        while not ev("state.act2.firstAnomalySeen") and t<120:
            d=D();
            if d['lock'] or d['busy']: W(500); watch(); t+=.5; continue
            face(0,2100); hold(['w'],1500); t+=1.5
            if D()['P']['y']>500: hold(['Shift'],1500)
        log('anomaly seen',ev("state.act2.firstAnomalySeen"))
        for _ in range(120):
            if ev("!!document.querySelector('.a2-moon.call,.a2-moon.on')") and not D()['busy']: break
            W(500); watch()
        shot('a2_prompt')
        kb.press('KeyV'); W(4000); watch(); wait_free(30000); shot('a2_moon')
        # 自由切換：切回、再切過去
        W(6000); watch(); kb.press('KeyV'); W(3000); watch()
        # 光痕：往前飛一段，再切回月界看
        hold(['w'],6000); hold(['e'],3000); kb.press('KeyV'); W(3000); watch()
        for k in range(40):
            if ev("state.act2.completed"): break
            hold(['q'],1200); W(800); watch()
            if k%6==5:
                kb.press('KeyV'); W(2500); hold(['w'],4000); kb.press('KeyV'); W(2500); watch()
        log('act2 trailSeen',ev("state.act2.trailSeen"),'completed',ev("state.act2.completed"))
        shot('a2_end'); log('=== 第二幕結束 %.0fs'%(time.time()-A2))
        ckpt('a2')
        if STOP=='a2': sys.exit()
    # ================= 第三幕 =================
    if FROM in ('','a1','a2'):
        A3=time.time(); log('=== 第三幕開始'); wait_free(60000); W(8000); shot('a3_start_view')
        # 玩家先環顧，找變密的星光
        for i in range(10): hold(['e'],700); W(300);
        shot('a3_look')
        fly_to(-460,-460,stop=330,y=22,maxs=500,cond=lambda: ev("state.act3&&state.act3.trainSeen"))
        for _ in range(80):
            if ev("state.act3.trainSeen") and not D()['lock'] and not D()['saying']: break
            W(500); watch()
        shot('a3_seen')
        # 飛進縫隙：森林畫面左側的列車上有標記（車頂、車身、車門）
        fly_to(-460+40*0.7071,-460+40*0.7071,stop=12,y=10,maxs=200)
        face(-460,-460); W(1500); shot('a3_forest')
        for k in ['carving','struct']:
            if ev(f"!!document.querySelector('.a3-tsp.on[data-k={k}]')"): pg.click(f'.a3-tsp[data-k={k}]'); W(3000); watch(); wait_free(30000)
            log('obs',ev("state.act3.obs"))
        shot('a3_obs')
        for _ in range(20):
            if ev("!!document.querySelector('.a3-tsp.on[data-k=door]:not(.lock)')"): break
            W(500)
        shot('a3_door'); pg.click('.a3-tsp[data-k=door]')
        for _ in range(60):
            if not ev("ACT1.active()"): break
            W(500); watch()
        log('=== 第三幕進入列車 %.0fs'%(time.time()-A3))
        ev("window.__a3t=1")
        ckpt('a3')
        if STOP=='a3': sys.exit()
    # ================= 列車（第三幕後半～尾聲）：只點看得到的東西 =================
    exec(open('/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad/play_train.py').read())
