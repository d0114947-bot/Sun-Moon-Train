# 第五幕：不期而遇（第一位乘客索拉：對話、互動、筆記本、乘客資料）
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
    POST4=POST3+"state.act4={guided:{habitat:1,nature:1,observation:1,memory:1},done:{habitat:1,nature:1,observation:1,memory:1},said:{cab:1,deck:1,fin:1},finished:true};state.carSeen=['habitat','nature','observation','memory','observatory'];"
    pg.goto('http://127.0.0.1:8766/'); W(900)
    ev("document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();"+POST4+"save();PANO.active=null;layout.centered=false;RUNNING=true;render()"); W(500)
    ok('B0 nothing happens immediately', not ev("!!document.querySelector('#layer .dlg,#layer .cine')") and ev("!state.act5.boarded"))
    b1=waitdlg(9000); t1=''
    for _ in range(12):
        if ev("!!document.querySelector('#layer .cine')"): break
        t1+=dlg(); ev("document.querySelector('#layer .dlg .box')?.click()"); W(300)
    ok('B1 something glows outside (after a quiet moment)', b1 and '縫隙' in t1, t1)
    ok('B2 she drifts in from the rift (boarding cine)', until("!!document.querySelector('#layer .cine')",8000) and '世界縫隙' in ev("document.querySelector('#layer .cine').innerText"))
    ev("document.querySelector('#layer .cine').click()"); ok('B3 new passenger card: 索拉', until("!!document.querySelector('#layer .ov.board')",8000) and '索拉' in ev("document.querySelector('#layer .ov.board').innerText"))
    ok('B4 she is aboard, living in the habitat', ev("aboard('sola')") and ev("state.discoveredLifeforms.includes('sola')"))
    ev("document.querySelector('#hi').click()"); waitdlg()
    ok('T1 first line fits a sleeping train', '好大的車' in dlg() and '好亮' not in dlg(), dlg())
    ok('T2 the phrase in it can be noted (glowing)', ev("!!document.querySelector('#layer .dlg mark.hl')"))
    # 第一次聊天：記下「我的島漂走了」
    for _ in range(30):
        if ev("!!document.querySelector('#layer .dlg mark.hl[data-nk=\"0\"]:not(.got)')"): ev("document.querySelector('#layer .dlg mark.hl[data-nk=\"0\"]').click()"); W(400)
        if not ev("!!document.querySelector('#layer .dlg')") or ev("state.passengers.sola.talks")>=1: break
        if ev("!!document.querySelector('#layer .dlg .chs button')"): ev("document.querySelector('#layer .dlg .chs button').click()"); W(900)
        else: ev("document.querySelector('#layer .dlg .box')?.click()"); W(260)
    ok('T3 talked once; relationship started', ev("state.passengers.sola.talks")>=1)
    ok('T4 the note was taken', ev("notesOf('sola').includes(0)"))
    s=talk(); ok('T5 spirit: who she is; then that the note was kept', '水母' in s and '記下來了' in s, s)
    ok('I1 interaction: she is not comfortable yet', not ev("careOk('sola')"))
    ok('I2 badge on her zone', any(x.startswith('hab-'+ev("zoneOf('sola')")) for x in badge()), badge())
    ev("state.zoneEnv=Object.assign(state.zoneEnv||{},{[zoneOf('sola')]:Object.assign({},zoneEnv(zoneOf('sola')),{l:0,h:2})});save();render()")
    s=talk(); ok('I3 she relaxes; each life likes a different place', '最舒服' in s and '不一樣' in s, s)
    ok('N1 notebook button glows after noting', ev("document.querySelector('[data-act=\"notes:open\"]').classList.contains('a5-cur')"))
    ev("document.querySelector('[data-act=\"notes:open\"]').click()"); W(900)
    ok('N2 notebook shows the note about her', '浮島漂離星河' in ev("document.querySelector('#layer .ov').innerText"))
    ev("closeAll()"); s=talk(); ok('N3 notes go into the encyclopedia (passenger profile)', '世界與生物圖鑑' in s, s)
    ok('N4 button no longer glows', not ev("document.querySelector('[data-act=\"notes:open\"]').classList.contains('a5-cur')"))
    go('memory'); talk(); W(400)
    ok('P1 badge on 世界與生物圖鑑', 'step' in ev("act5Badge(HSDEF.find(h=>h.id==='mem-book'))"))
    hs('mem-book'); W(1200); ok('P2 encyclopedia opens', ev("!!document.querySelector('#layer .ov.lifebook')"))
    ev("closeAll();state.filed=Object.assign(state.filed||{},{sola:{bio:0}});save();render()")
    s=talk(); ok('P3 not a task to finish: she has her own home', '想去的地方' in s, s)
    s5=s; s=talk(); s5+=s
    ok('D1 she wants to go home (leads to act 6)', '回去看看' in s5 and ev("state.act5.done"), s5)
    ok('D2 journal records the first passenger', any('第一位乘客' in e['t'] for e in ev("state.log")))
    ok('D3 train still asleep (wakes in act 6)', ev("proHold()"))
    st=ev("JSON.stringify(state)"); ev(f"closeAll();loadGame(JSON.parse({json.dumps(st)}),'t')"); W(5000)
    ok('R1 reload: nothing replays', not ev("!!document.querySelector('#layer .dlg,#layer .cine')"))
    ev("closeAll();state=freshState();state.introDone=true;render()")
    ok('L1 legacy: original first line and note', PASSENGERS_LINE()=='哇，好亮的車！我還以為是一顆走錯路的彗星。' if False else ev("PASSENGERS.sola.talks[0].lines[0]")=='哇，好亮的車！我還以為是一顆走錯路的彗星。' and ev("NOTES.sola.list[1].p")=='我還以為是一顆走錯路的彗星')
    ok('L2 legacy: no act5', not ev("act5On()") and ev("act5Badge({id:'mem-book'})")=='')
    ok('Z no page errors', not errs, errs)
    print('ALL PASS' if all(R) else 'SOME FAIL', len(R))
