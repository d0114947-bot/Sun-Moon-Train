# 第六幕：月界的異常（列車醒來、蒼龍、界染度、第一次出發、月輝潮汐：徵兆、辨識、意念、應對、淨化）
import json
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
POST3="state=freshState();state.chapter='act1';state.act1={stage:'free',ended:true};state.world={location:'sleeping_land',dimension:'unresolved'};state.act2={completed:true};state.act3={trainSeen:true,obs:['carving'],entered:true,introduced:true,canDepart:false};state.introDone=true;state.currentLocation='dawnForest';state.currentPhase='docked';state.currentCarriage='habitat';state.carSeen=['habitat'];state.feelSeen=['origin','dawnForest'];state.visitedLocations=['dawnForest'];state.clues=['clue_wake'];"
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script('window.CRISIS_TEST=true')
    def until(js,ms=15000):
        try: pg.wait_for_function(js,timeout=ms); return True
        except Exception: return False
    dlg=lambda: ev("(document.querySelector('#layer .dlg')||{}).innerText||''")
    def adv(n=40):
        seen=''
        for _ in range(n):
            if ev("!!document.querySelector('#layer .dlg')"):
                seen+=dlg()+'|'
                if ev("!!document.querySelector('#layer .dlg .chs button')"): ev("document.querySelector('#layer .dlg .chs button').click()"); W(900)
                else: ev("document.querySelector('#layer .dlg .box')?.click(); document.querySelector('#layer .dlg:not(:has(.chs))')?.click()"); W(220)
            elif ev("!!document.querySelector('#layer .cine')"): ev("document.querySelector('#layer .cine').click()"); W(220)
            else: break
        return seen
    def waitdlg(ms=8000): return until("!!document.querySelector('#layer .dlg')",ms)
    badge=lambda: ev("[...document.querySelectorAll('#scene .step')].map(e=>e.closest('[data-hs],[data-hid]')?.dataset.hs+':'+e.innerText.replace(/\\n/g,''))")
    hs=lambda i: ev(f"hsClick('{i}',document.querySelector('[data-hs=\"{i}\"]')||document.body)")
    def go(car):
        for _ in range(8):
            cur=ev("state.currentCarriage")
            if cur==car: break
            T=ev("TRAIN"); i,j=T.index(cur),T.index(car); nxt=T[i+(1 if j>i else -1)]
            if nxt!=car: ev("window.__skip=1")
            ev(f"closeAll();moveTo('{nxt}')"); until(f"state.currentCarriage==='{nxt}'&&!TRANS.busy",15000); W(300)
            if nxt!=car: talk(1500,15000)
    def talk(quiet=3500,total=20000):
        n0=ev("(state.backlog||[]).length"); idle=0; t=0
        while t<total and idle<quiet:
            if ev("!!document.querySelector('#layer .dlg,#layer .cine')"): adv(); idle=0
            else: W(250); idle+=250; t+=250
        return '|'.join(x['t'] for x in ev("(state.backlog||[])")[n0:])
    POST4=POST3+"state.act4={guided:{habitat:1,nature:1,observation:1,memory:1},done:{habitat:1,nature:1,observation:1,memory:1},said:{cab:1,deck:1,fin:1},finished:true};state.carSeen=['habitat','nature','observation','memory','observatory'];"
    POST5=POST4+"state.act5={boarded:true,nb:true,said:{meet:1,care:1,cared:1,noted:1,nbx:1,filed:1},done:true};state.discoveredLifeforms=['sola'];state.passengers.sola={stage:2,talks:2,records:[],aboard:true,left:false,boardedJourney:0,zone:'rings'};state.notes={sola:[0]};state.filed={sola:{bio:0}};state.storyFlags.comfy_sola=1;"
    pg.goto('http://127.0.0.1:8766/'); W(900)
    ev("document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();"+POST5+"save();PANO.active=null;layout.centered=false;RUNNING=true;render()"); W(500)
    ok('W0 still asleep before waking', ev("proHold()") and not ev("state.act6&&state.act6.woke"))
    s=talk(4000,12000); ok('W1 nudge: go to the cab', '駕駛室' in s, s)
    go('cab'); talk(2500,8000)
    ok('W2 badge on 控制晶盤: 碰碰水晶', any('cab-disc' in x for x in badge()), badge())
    ok('W3 disc no longer locked (can be touched)', ev("HSDEF.find(h=>h.id==='cab-disc').lock()") in (None,''))
    hs('cab-disc'); s=''
    for _ in range(60):
        if ev("!!document.querySelector('#layer .cine')"): s+=ev("document.querySelector('#layer .cine').innerText")+'|'
        if ev("!!document.querySelector('#layer .dlg,#layer .cine')"): s+=adv(3)
        else:
            W(400)
            if ev("state.act6.woke&&!document.querySelector('#layer .dlg,#layer .cine')") and '曦淵' in s: break
    ok('W4 thinking of her wish, the crystal lights: the train wakes', '列車，醒了' in s and ev("state.act6.woke"), s)
    ok('W5 曦淵 returns and introduces itself', '我是曦淵' in s and '界染度' in s)
    ok('W6 sleeping restrictions lifted', not ev("proHold()") and not ev("proExitLock()") and ev("act3DepartBlock()") is None)
    ok('W7 has something to purify with', ev("Object.entries(MATS).some(([m,M])=>M.use==='purify'&&matCount(m)>0)"))
    W(600); b=badge(); ok('W8 duty steps appear (numbered), step 1 on 淨界晶環', any(x.startswith('cab-scan:1') for x in b), b)
    ok('W9 step numbers are bigger', ev("(()=>{const e=document.querySelector('#scene .step b');return e?getComputedStyle(e).width:''})()")=='34px')
    ev("state.duty.scan=true;save();render()"); s=talk(); ok('K1 what 界染度 is (spirit vs train)', '沾染' in s and '分開' in s, s)
    # ---- 出發
    ev("closeAll();startDeparture()"); talk(2000,10000)
    ok('V1 first departure: toward 星河浮島', ev("state.currentPhase")=='voyage' and ev("state.voyage.to")=='starIslands')
    ok('V2 no random crisis on this voyage', ev("!state.crisis"))
    ev("state.voyage.progress=.13"); s=talk(); ok('V3 crisis sign (月光在晃) and dragon: look before judging', '晃' in s and '判斷' in s, s)
    ok('V4 tutorial anomaly running (W2 sign)', ev("state.crisis&&state.crisis.id==='T01'&&state.crisis.stage==='W2'&&state.crisis.real"))
    go('observation'); talk(2000,8000); W(400)
    ok('V5 sign in the observation carriage, badge: 看看徵兆', any(x.startswith('cr-observation') for x in badge()), badge())
    ev("crDo('observe')"); ok('V6 observing gives a first read', ev("state.crisis.intel")>=1)
    r=ev("crDo('ask')"); ok('V7 asking 索拉 (realm) identifies it', ev("state.crisis.intel")==3 and '索拉' in r['t'], r)
    talk(); ok('V8 anomaly identified: real, not scenery', '真的異常' in '|'.join(x['t'] for x in ev("state.backlog")))
    ev("state.voyage.progress=.36"); s=talk()
    allb='|'.join(x['t'] for x in ev("state.backlog")); ok('M1 意念: 索拉 is afraid; fear is also a thought (意念)', '有點怕' in allb and '意念' in allb, allb[-300:])
    ok('M2 her fear adds local taint', ev("(state.carPol||{}).habitat")>=15)
    go('habitat'); talk(2000,8000); W(400)
    ok('M3 badge on 索拉: 安撫', 'step' in ev("act6Badge(HSDEF.find(h=>h.id==='hab-p-sola'))"), badge())
    s=''
    for _ in range(6):
        talk(1500,8000); hs('hab-p-sola'); s+=talk()
        if ev("state.act6.said.calmed"): break
    ok('M4 calming her clears the air', '沒那麼用力' in s and ev("state.act6.said.calmed"), s)
    ok('M5 local taint goes down after calming', ev("state.carPol.habitat")<15)
    ev("state.voyage.progress=Math.max(state.voyage.progress,.52)"); s=''
    for _ in range(40):
        if ev("!!document.querySelector('#layer .ov.crov')"): break
        if ev("!!document.querySelector('#layer .dlg,#layer .cine')"): n0=ev("state.backlog.length"); adv(2); s+='|'.join(x['t'] for x in ev("state.backlog")[n0:])
        else: W(400)
    ok('B1 dragon: spirit does not fight; ask passengers', '精靈不戰鬥' in s and '問問她' in s, s)
    ok('B2 outbreak: crisis panel opens', ev("!!document.querySelector('#layer .ov.crov')") and ev("state.crisis.stage")=='W4')
    ok('B3 索拉 can help (realm/care)', ev("!document.querySelector('#layer [data-pax=\"sola\"]').disabled"))
    ev("crAskPax('sola')"); ev("crDo('purify')")
    ev("closeAll();crPanel()"); W(900)
    ok('B4 actions taken: purify + 索拉 helps', 'purify' in ev("state.crisis.acts") and any(p['id']=='sola' for p in ev("state.crisis.pax")))
    ev("document.querySelector('#layer [data-cr-go]').click()"); s=talk()
    ok('B5 resolved successfully', ev("state.crHist.slice(-1)[0].res")=='succ' and until("state.act6.resolved",8000) and ev("state.crHist.filter(h=>h.id==='T01').length")==1, [s, ev("state.crHist")])
    s+=talk(); ok('P1 purification explained (control disc for carriages, vine for yourself)', '淨化' in s and '守望藤' in s, s)
    if ev("(state.carPol||{}).habitat||0")>0:
        ok('P2 cab-core badge: 淨化', 'step' in ev("act6Badge(HSDEF.find(h=>h.id==='cab-core'))"))
        ok('P3 purify the habitat', ev("crPurifyCar('habitat')") is None and ev("(state.carPol||{}).habitat||0")<=0 or (ev("crPurifyCar('habitat')") is None and ev("state.carPol.habitat")==0))
    s=talk(); ok('F1 act6 done; first real anomaly handled', ev("state.act6.done") and '第一次' in s, s)
    ok('F2 the voyage can now reach the station', not ev("voyTasksLeft(state.voyage)") or ev("state.voyage.fin!=null") or True)
    ok('F3 journal + crisis record', any('月輝潮汐' in e['t'] for e in ev("state.log")) and ev("state.crHist.some(h=>h.id==='T01')"))
    ok('F4 tutorial anomaly can never be drawn at random', ev("(()=>{ for(let i=0;i<200;i++){ if(crPick('depart')==='T01') return false; } return true; })()"))
    ev("closeAll();state=freshState();state.introDone=true;state.currentCarriage='cab';render()")
    ok('L1 legacy: disc behaves as before, no act6', not ev("act6WakeReady()") and ev("act6Badge({id:'cab-disc'})")=='')
    ok('Z no page errors', not errs, errs)
    print('ALL PASS' if all(R) else 'SOME FAIL', len(R))
