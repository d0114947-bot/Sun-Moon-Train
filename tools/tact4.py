# 第四幕：探索列車（自然調節、星月觀測、記憶典藏、棲息；存檔與讀檔）＋序章期間列車沉睡
import json
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
POST3="state=freshState();state.chapter='act1';state.act1={stage:'free',ended:true};state.world={location:'sleeping_land',dimension:'unresolved'};state.act2={completed:true};state.act3={trainSeen:true,obs:['carving'],entered:true,introduced:true,canDepart:false};state.introDone=true;state.currentLocation='dawnForest';state.currentPhase='docked';state.currentCarriage='habitat';state.carSeen=['habitat'];state.feelSeen=['origin','dawnForest'];state.visitedLocations=['dawnForest'];state.clues=['clue_wake'];"
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
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
        out=''; idle=0; t=0
        while t<total and idle<quiet:
            if ev("!!document.querySelector('#layer .dlg,#layer .cine')"): out+=adv(); idle=0
            else: W(250); idle+=250; t+=250
        return out
    pg.goto('http://127.0.0.1:8766/'); W(900)
    ev("document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();"+POST3+"save();PANO.active=null;layout.centered=false;RUNNING=true;render()"); W(800)
    # ---- 棲息車廂
    ok('A1 act4 starts after act3 (state created)', ev("!!state.act4&&!state.act4.finished"))
    ok('A2 habitat guide thought', waitdlg() and '發光的區域' in adv())
    W(400); bd=badge(); ok('A3 badge on one zone: 調整結界', any(x.startswith('hab-') for x in bd), bd)
    hs(ev("ACT4_ZONE")); W(700)
    ok('A4 zone panel opens', ev("!!document.querySelector('#layer .ov')"))
    ok('A5 nothing said while the panel is open', not ev("!!document.querySelector('#layer .dlg')"))
    ev("closeAll();document.querySelectorAll('.hdw').forEach(d=>drawerClose(d))"); ok('A6 after closing: what the habitat is for', waitdlg() and '住得舒服' in adv())
    ok('A7 habitat done, badge gone', ev("state.act4.done.habitat===1") and not [x for x in badge() if x.startswith('hab-')])
    ok('A8 exit door stays shut during the prologue', ev("!!HSDEF.find(h=>h.id==='hab-exit').lock()"))
    # ---- 森羅溫室
    go('nature'); s=talk()
    ok('N1 carriage intro first, then guide', '溫室' in s and '晶石' in s, s)
    W(400); ok('N2 badge on 界域調節晶石', any('nat-crystal' in x for x in badge()), badge())
    hs('nat-crystal'); W(900)
    ev("const b=[...document.querySelectorAll('.hdw .hdw-it')].find(e=>/月輝|星輝/.test(e.innerText)); b&&b.click()"); W(600)
    ok('N3 light switched', ev("!!state.storyFlags.gt_light"))
    ev("closeAll();document.querySelectorAll('.hdw').forEach(d=>drawerClose(d))"); ok('N4 natural regulation explained', waitdlg() and '植物需要' in adv())
    # ---- 星月觀測
    go('observation'); s=talk()
    ok('O1 observation intro + guide', '望遠鏡' in s, s)
    W(400); ok('O2 badge on 星月望遠鏡', any('obs-scope' in x for x in badge()), badge())
    ok('O3 navigation does not respond while asleep', '導航裝置沒有反應' in (ev("HSDEF.find(h=>h.id==='obs-nav').lock()") or ''))
    hs('obs-scope'); W(1200); ev("closeAll()"); ok('O4 observation explained', waitdlg() and '星星' in adv())
    # ---- 駕駛室（列車沉睡）
    go('memory'); s=talk(); ok('M1 memory intro + guide (save)', '旅途紀錄' in s, s)
    go('cab'); s=talk()
    ok('C1 cab: crystal still asleep', '還在沉睡' in s, s)
    ok('C2 no dragon, no duty steps', not ev("dragonHere()") and not ev("dutyOn()") and not [x for x in badge() if x.startswith('cab-')])
    ok('C4 no station announcement while asleep', ev("questText()")=='')
    ok('C3 control disc does not respond', '還在沉睡' in (ev("HSDEF.find(h=>h.id==='cab-disc').lock()") or '') and '沉睡' in (ev("crBlockDepart()") or ''))
    # ---- 記憶典藏：存檔與讀檔
    go('memory'); W(400); ok('M2 badge on 旅途紀錄', 'step' in ev("act4Badge(HSDEF.find(h=>h.id==='mem-save'))"))
    ev("localStorage.removeItem('sunmoon_slots')"); hs('mem-save'); W(900)
    ev("document.querySelector('#layer [data-save]').click()"); until("/已存檔/.test(document.querySelector('#layer .ov').innerText)",8000)
    ok('M3 saved into a crystal', '已存檔' in ev("document.querySelector('#layer .ov').innerText"))
    ok('M4 load button available', ev("!!document.querySelector('#layer [data-load]')"))
    ev("closeAll()"); s=adv() if waitdlg() else ''
    ok('M5 save / load / continue explained', '讀檔' in s and '接續旅程' in s, s)
    # ---- 完成
    s5=s
    ok('F1 act4 finished', until("state.act4.finished",8000))
    f2=talk(); ok('F2 closing thought', '可以住下來' in s5+f2, [f2, ev("JSON.stringify(state.act4)"), ev("act4Busy()"), ev("[...document.querySelectorAll('#layer > *, .hdw')].map(e=>e.className)")])
    ok('F3 journal records it', any('四節車廂' in e['t'] for e in ev("state.log")))
    ok('F4 no more act4 badges', not [x for x in badge() if x.startswith('mem-save')])
    ok('F5 still asleep after act4 (departure is a later act)', ev("proHold()"))
    # ---- 一次性：重新載入不會重播
    st=ev("JSON.stringify(state)"); ev(f"closeAll();loadGame(JSON.parse({json.dumps(st)}),'t')"); W(2500)
    ok('R1 reload: act4 does not replay', not any(k in dlg() for k in ['可以住下來','發光的區域','晶石','望遠鏡','旅途紀錄']) and ev("state.act4.finished"), dlg())
    # ---- v84 的舊存檔：列車在「沉睡之地」→ 搬到晨曦森林
    ev("closeAll();"+POST3+"state.currentLocation='origin';state.log[0]={j:0,t:'精靈在沉睡之地邊緣的世界縫隙裡，發現了一列沉睡的列車。'};normalizeState()")
    ok('R2 old act3 save moved to the Dawn Forest', ev("state.currentLocation")=='dawnForest' and '晨曦森林' in ev("state.log[0].t"))
    # ---- 舊開場（legacy）不受影響
    ev("closeAll();state=freshState();state.introDone=true;state.currentCarriage='cab';render()"); W(600)
    ok('L1 legacy: dragon and duty work as before', ev("dragonHere()") and ev("dutyOn()") and not ev("proHold()"))
    ok('L2 legacy: no act4 badges or locks', ev("act4Badge({id:'mem-save'})")=='' and ev("HSDEF.find(h=>h.id==='cab-disc').lock()") in (None,''))
    ok('L3 legacy origin unchanged', ev("LOCATIONS.origin.name")=='沉睡之地')
    ok('Z no page errors', not errs, errs)
    print('ALL PASS' if all(R) else 'SOME FAIL', len(R))
