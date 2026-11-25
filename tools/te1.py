# 開玩 10 分鐘就到第一次值勤：教學三步、自動跟星光、導覽完索拉馬上來、說完心願就碰晶盤
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad'
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("window.ACT1_TEST=true; window.XY_FAST=true")
    def until(js,ms=20000):
        try: pg.wait_for_function(js,timeout=ms); return True
        except Exception: return False
    def adv(n=60):
        seen=''
        for _ in range(n):
            if ev("!!document.querySelector('#layer .dlg')"):
                seen+=ev("document.querySelector('#layer .dlg').innerText")+'|'
                if ev("!!document.querySelector('#layer .dlg .chs button')"): ev("document.querySelector('#layer .dlg .chs button').click()"); W(700)
                else: ev("document.querySelector('#layer .dlg .box')?.click()"); W(90); ev("document.querySelector('#layer .dlg .box')?.click()"); W(150)
            elif ev("!!document.querySelector('#layer .cine')"): ev("document.querySelector('#layer .cine').click()"); W(200)
            elif ev("!!document.querySelector('#layer .ov.board #hi')"): ev("document.querySelector('#layer .ov.board #hi').click()"); W(300)
            else: break
        return seen
    def talk(quiet=3000,total=30000):
        out=''; idle=0; t=0
        while t<total and idle<quiet:
            if ev("!!document.querySelector('#layer .dlg,#layer .cine,#layer .ov.board')"): out+=adv(); idle=0
            else: W(250); idle+=250; t+=250
        return out
    pg.goto('http://127.0.0.1:8766/'); W(900)
    # ---- 曦淵導覽 → 索拉 → 晶盤 → 值勤
    ev("ACT1.active()&&ACT1.exit();closeAll();document.querySelector('#mainscreen')?.remove();state=freshState();normalizeState();state.chapter='act1';state.act1={stage:'free',ended:true,tut:6};state.world={location:'sleeping_land',dimension:'unresolved'};state.act2={completed:true};state.act3={trainSeen:true,obs:['carving'],entered:true,introduced:false,canDepart:false,inForest:true,xyCall:1};state.currentCarriage='cab';state.currentPhase='docked';state.currentLocation='dawnForest';state.visitedLocations=['dawnForest'];state.introDone=true;save();RUNNING=true;render()")
    s=''
    for _ in range(120):
        s+=talk(1200,6000)
        if ev("state.act3.introduced"): break
    ok('E1 tour ends with the wish line, 曦淵 does not leave', '心願' in s and '龍已經不見' not in s and '我去外面' not in s, s[-200:])
    ok('E2 train lesson (act 4) is no longer a gate', ev("state.act4.finished&&state.act4.said.fin&&state.act4.quick"))
    s=talk(4000,40000)
    ok('E3 索拉 drifts in right away and the first talk follows straight on', ev("state.act5&&state.act5.boarded") and ev("A5.talked()"), [ev("state.act5"),s[-200:]])
    s+=talk(3000,30000); s+='|'.join(x['t'] for x in ev("state.backlog||[]"))
    ok('E4 her wish, then 曦淵: put your hand on the disc', '回去看看' in s and '晶盤' in s and ev("state.act5.done"), s[-300:])
    ok('E5 still in the cab (no walking needed)', ev("state.currentCarriage")=='cab')
    ok('E6 care/notes/lifebook not required now', not ev("A5.filed()"))
    ev("hsClick('cab-disc',document.querySelector('[data-hs=\"cab-disc\"]')||document.body)"); s=''
    for _ in range(80):
        s+=talk(1500,6000)
        if ev("state.act6.woke&&!document.querySelector('#layer .dlg,#layer .cine')"): break
    ok('E7 crystal wakes, 曦淵 was already here (no "我回來了")', ev("state.act6.woke") and '我回來了' not in s and '界染度' in s, s[-300:])
    W(800); ok('E8 duty begins (界染 step badge)', ev("!!document.querySelector('#scene [data-hs=\"cab-scan\"] .step')"))
    # ---- 裝置：之後第一次用到時，說原本的那句
    ev("closeAll();state.currentCarriage='observation';render()"); W(600)
    ev("hsClick('obs-scope',document.querySelector('[data-hs=\"obs-scope\"]')||document.body)"); W(400); ev("closeAll()")
    s=talk(2500,8000); ok('J1 first time using the telescope: its line plays', '很遠的地方' in s and ev("state.act4.done.observation"), s)
    ev("closeAll();hsClick('obs-scope',document.querySelector('[data-hs=\"obs-scope\"]')||document.body)"); W(400); ev("closeAll()")
    s=talk(2000,5000); ok('J2 only once', '很遠的地方' not in s, s)
    # ---- 舊存檔：見過曦淵、卡在第四幕
    ev("state.act4={guided:{},done:{nature:1},said:{cab:1,deck:1},finished:false};state.act5=null;state.act6=null;state.act3.introduced=true;state.act3.xyMet=1;save();render()"); W(2500)
    ok('L1 old save mid act 4 (met 曦淵): moves on', ev("state.act4.finished&&state.act4.quick"))
    ev("state.act3.xyMet=0;state.act4={guided:{},done:{},said:{},finished:false};state.act5=null;save();render()"); W(2500)
    ok('L2 old save that never met 曦淵 keeps the old act 4', not ev("state.act4.finished"))
    ok('Z no page errors', not errs, errs[:3])
    b.close()
