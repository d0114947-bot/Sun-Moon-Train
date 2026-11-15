# 序章尾聲：旅途的開始（抵達星河浮島、第一次下車、跟著索拉、回到車上進入自由旅程）
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
    POST6=POST5+"state.act3.canDepart=true;state.act6={woke:true,started:true,said:{go:1,taint:1,sign:1,id:1,mind:1,calmed:1,burst:1,after:1,pured:1},resolved:true,done:true};state.storyFlags.metDragon=1;state.currentLocation='starIslands';state.currentPhase='docked';state.journeyCount=1;state.visitedLocations=['dawnForest','starIslands'];state.feelSeen=['origin','dawnForest','starIslands'];"
    pg.goto('http://127.0.0.1:8766/'); W(900)
    # ---- 自己下車（沒帶索拉）
    ev("document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();"+POST6+"save();PANO.active=null;layout.centered=false;RUNNING=true;render()"); W(300)
    waitdlg(9000); W(2500); pg.screenshot(path='e_arrive.png'); s=talk(); ok('E1 arrival: 星河浮島; 索拉 wants to show a place', '星河浮島' in s and '想讓你看' in s, s)
    W(500); ok('E2 badge on the door: 下車看看', 'step' in ev("epiBadge(HSDEF.find(h=>h.id==='hab-exit'))"))
    ok('E3 door is open now', ev("HSDEF.find(h=>h.id==='hab-exit').lock()") in (None,''))
    hs('hab-exit'); W(900)
    W(600); pg.screenshot(path='e_choose.png'); ok('E4 can invite 索拉 to come along', ev("!!document.querySelector('#layer [data-comp=\"sola\"]')"))
    ev("document.querySelector('#layer [data-comp=\"\"]')?.click() || (closeAll(),state.companion=null,act('exit',''))"); until("state.currentPhase==='outside'",15000); W(800)
    if ev("!!document.querySelector('#layer .ov')"): ev("closeAll()")
    s=talk(); ok('A1 went out alone: she is the one who knows the place', '索拉還在車上' in s or ev("state.companion")=='sola', [s, ev("state.companion")])
    ev("act('back','')"); until("state.currentPhase==='docked'",15000); talk(2500,8000)
    ok('A2 not finished without her', not ev("state.epi.done"))
    # ---- 帶著索拉
    hs('hab-exit'); W(900); ev("document.querySelector('#layer [data-comp=\"sola\"]').click()"); until("state.currentPhase==='outside'",15000); W(800)
    if ev("!!document.querySelector('#layer .ov')"): ev("closeAll()")
    talk(2000,8000); W(400)
    ok('O1 outside with 索拉', ev("state.companion")=='sola' and ev("state.epi.out"))
    pg.screenshot(path='e_out.png'); ok('O2 badge on 浮島漂走的痕跡: 跟著索拉', any(x.startswith('out-drift') for x in badge()), badge())
    hs('out-drift'); W(1200)
    pg.screenshot(path='e_place.png'); ok('O3 her place: the trail where her island drifted away', '漂走' in ev("document.querySelector('#layer .ov').innerText"))
    ok('O4 recorded (journal, passenger record, clue)', ev("state.places.includes('sola')") and any('浮島漂走' in e['t'] for e in ev("state.log")))
    ev("closeAll();act('back','')"); until("state.currentPhase==='docked'",15000)
    until("((document.querySelector('#layer .dlg')||{}).innerText||'').includes('陪我去看')",15000); W(2000); pg.screenshot(path='e_end.png'); s=talk(); ok('F1 back aboard: explore, observe, record, be with passengers', '探索、觀察、記錄' in s and '你來決定' in s, s)
    ok('F2 prologue complete -> free journey', ev("state.epi.done") and ev("state.prologueDone"))
    ok('F3 no ending title card', '序章' not in s and not ev("!!document.querySelector('#layer .cine')"))
    ok('F4 索拉 stays aboard for now', ev("aboard('sola')"))
    ok('F5 no more prologue badges', not [x for x in badge() if '✦' in x])
    st=ev("JSON.stringify(state)"); ev(f"closeAll();loadGame(JSON.parse({json.dumps(st)}),'t')"); W(3000)
    ok('R1 reload: nothing of the prologue replays', not any(k in dlg() for k in ['星河浮島','探索、觀察','下一站']), [dlg(), ev("[...document.querySelectorAll('#layer > *')].map(e=>e.className+':'+e.innerText.slice(0,60))")])
    ev("closeAll();state=freshState();state.introDone=true;render()")
    ok('L1 legacy: no epilogue', not ev("epiOn()") and ev("epiBadge({id:'hab-exit'})")=='')
    ok('Z no page errors', not errs, errs)
    print('ALL PASS' if all(R) else 'SOME FAIL', len(R))
