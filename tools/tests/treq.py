import os
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad/nreq'; os.makedirs(S,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n,x if not c else '',flush=True)
    def adv(n=30):
        for _ in range(n):
            if ev("!!document.querySelector('.dlg')"):
                if ev("!!document.querySelector('.dlg .chs button')"): ev("document.querySelector('.dlg .chs button').click()"); W(1600)
                else: ev("document.querySelector('.dlg .box')?.click(); document.querySelector('.dlg:not(:has(.chs))')?.click()"); W(150)
            elif ev("!!document.querySelector('.cine')"): ev("document.querySelector('.cine').click()"); W(150)
            else: break
        W(500)
    pg.goto('http://127.0.0.1:8766/'); W(900); ev("startNew()"); W(300)
    ev("document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();document.querySelectorAll('.cine').forEach(e=>e.remove());state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.storyFlags.metDragon=1;state.currentPhase='docked';state.currentLocation='dawnForest';state.journeyCount=4;state.visitedLocations=['dawnForest','starIslands'];"
       "for(const id of ['felinia','pyro','frost']){state.discoveredLifeforms.push(id);state.passengers[id]={stage:2,talks:2,records:[],aboard:true,left:false,boardedJourney:2,zone:PASSENGERS[id].zone}};state.currentCarriage='habitat';state.hview=0;render()"); W(1000)
    pg.screenshot(path=S+'/tip_hab.png')
    ok('T1 no tip pills outside the cab', not ev("!!document.querySelector('#scene .step')"))
    
    
    ev("talk('felinia')"); W(500); pg.screenshot(path=S+'/ask.png')
    ok('R1 asks for request', '山谷' in ev("document.querySelector('.dlg').innerText"))
    ok('B1 backlog button in dialog', ev("!!document.querySelector('.dlg .bl-btn')"))
    ev("document.querySelector('.dlg .bl-btn').click()"); W(500); pg.screenshot(path=S+'/backlog.png')
    ok('B2 backlog panel', ev("!!document.querySelector('.ov.backlog li')")); ev("document.querySelector('.ov.backlog .close').click()"); W(400)
    ok('B3 dialog still there', ev("!!document.querySelector('.dlg')"))
    adv()
    ok('R2 request on', ev("reqOn('felinia')"))
    ok('T4 talk tip gone', not ev("tipDone('talk')") or not ev("!!document.querySelector('[data-hs^=\"hab-p-\"] .step.tip')"))
    ev("talk('pyro')"); adv(); ev("talk('frost')"); adv()
    ev("notebookPanel()"); W(900); pg.screenshot(path=S+'/notebook.png'); ok('R3 notebook lists requests', '乘客的請求' in ev("document.querySelector('.ov').innerText")); ev("closeAll()")
    # sky fulfil
    ev("for(const id of ['felinia']) state.passengers[id].place='deck'; state.currentPhase='voyage';state.voyage={from:'dawnForest',to:'starIslands',progress:.5,evt:true,sky:{type:'meteor',at:.4,started:true,ended:false,watched:false}};state.currentCarriage='observatory';render()"); W(800)
    ev("skyWatch()"); W(300); adv(); ok('R4 sky request done', ev("reqOf('felinia').st")=='done')
    # loc fulfil (pyro -> dawnForest)
    ev("state.currentPhase='docked';state.voyage=null;state.currentLocation='dawnForest';state.journeyCount=6;state.currentCarriage='habitat';render();arrivalChecks()"); W(400); adv()
    ok('R5 loc request done', ev("reqOf('pyro').st")=='done')
    ok('S1 autosave snapshot', ev("autosGet().length")>=1, ev("autosGet().map(a=>a.name)"))
    # out fulfil (frost -> starIslands)
    ev("state.currentLocation='starIslands';state.currentPhase='outside';state.companion='frost';render()"); W(600); ev("compTalk()"); adv()
    ok('R6 out request done', ev("reqOf('frost').st")=='done')
    ev("state.currentPhase='docked';state.companion=null;state.currentCarriage='memory';render()"); W(1500); pg.screenshot(path=S+'/mem_tip.png')
    ev("memoryPanel()"); W(600); ok('B4 「聽見的話」 removed from memory crystals (by request)', ev("document.querySelectorAll('.ov.float .fl.heard').length")==0 and '聽見的話' not in ev("document.querySelector('.ov.float').innerText")); pg.screenshot(path=S+'/backlog2.png'); ev("closeAll()")
    ev("savePanel('game')"); W(700); pg.screenshot(path=S+'/save.png'); ok('S2 autosave listed', '第 6 趟' in ev("document.querySelector('.ov').innerText") and '晨曦森林' in ev("document.querySelector('.ov').innerText")); ev("closeAll()")
    ok('Z no errors', not errs, errs)
    b.close()
