import os
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad/ngar2'; os.makedirs(S,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    def sayall():
        t=''
        for _ in range(10):
            t+=ev("document.querySelector('.say-box')?.innerText||''")
            ev("const b=document.querySelector('.say-box');if(b){b.click();b.click();}"); W(250)
        return t

    def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n,x if not c else '',flush=True)
    def adv(n=30):
        for _ in range(n):
            if ev("!!document.querySelector('.dlg')"):
                if ev("!!document.querySelector('.dlg .chs button')"): ev("document.querySelector('.dlg .chs button').click()"); W(1600)
                else: ev("document.querySelector('.dlg .box')?.click(); document.querySelector('.dlg:not(:has(.chs))')?.click()"); W(150)
            else: break
        W(400)
    pg.goto('http://127.0.0.1:8766/'); W(900); ev("startNew()"); W(300)
    ev("document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();document.querySelectorAll('.cine').forEach(e=>e.remove());state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.storyFlags.metDragon=1;state.storyFlags.gt_done=1;state.currentPhase='docked';state.currentLocation='dawnForest';state.journeyCount=4;state.visitedLocations=['dawnForest','starIslands'];"
       "for(const id of ['felinia']){state.discoveredLifeforms.push(id);state.passengers[id]={stage:2,talks:9,records:[],aboard:true,left:false,boardedJourney:2,zone:PASSENGERS[id].zone}};state.req={felinia:{st:'done'}};state.currentCarriage='nature';render()"); W(2000)
    # hybrid
    ev("gardenSync();state.pods[0]={p:'bell',st:2};state.pods[1]={p:'stardaisy',st:2};state.hybridSeen=[];gardenPanel(0)"); W(500); ev("document.querySelector('#g-harvest').click()"); W(800); pg.screenshot(path=S+'/hybrid.png')
    ok('H1 hybrid seed', ev("seedN('starbell')")==1, ev("state.seedBag"))
    ev("closeAll()"); ev("seedPanel()"); W(800); ok('H2 vault shows hybrid row', '變種種子' in ev("document.querySelector('.ov').innerText")); pg.screenshot(path=S+'/vault.png'); ev("closeAll()")
    # sky bloom
    ev("state.pods[2]={p:'tidebloom',st:0};state.currentPhase='voyage';state.voyage={from:'dawnForest',to:'starIslands',progress:.5,evt:true,sky:{type:'tide',at:.4,started:true,ended:false,watched:false}};render()"); W(1200)
    ok('K1 skylight hotspot', ev("!!document.querySelector('[data-hs=\"nat-skylight\"]')")); pg.screenshot(path=S+'/skylight.png')
    ev("skylight()"); W(300); adv(); ok('K2 tidebloom bloomed by sky', ev("state.pods[2].st")==2)
    # home name gift
    ev("state.currentPhase='docked';state.voyage=null;plantAdd('goldreed',1);state.currentCarriage='habitat';render()"); W(800)
    ev("giveGift('felinia','goldreed')"); W(400); t=''
    for _ in range(6):
        t+=ev("document.querySelector('.dlg .tx')?.innerText||''"); ev("document.querySelector('.dlg .box')?.click()"); W(250)
    ok('L1 home name said', '山谷的風穗' in t, t)
    ev("state.grown=['goldreed','bell'];state.currentCarriage='nature';render()"); W(800); ev("samplePanel()"); W(400); ev("document.querySelector('[data-sp=\"goldreed\"]').click()"); W(3000); pg.screenshot(path=S+'/sample.png')
    tx=sayall()+ev("document.querySelector('#spd')?.innerText||''"); ok('L2 sample shows 花語 + home name', '花語' in tx and '山谷的風穗' in tx, tx[-200:])
    ok('Z no errors', not errs, errs)
    b.close()
