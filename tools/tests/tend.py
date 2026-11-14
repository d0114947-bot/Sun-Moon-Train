import sys,os
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad/nend'; os.makedirs(S,exist_ok=True)
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
    def clickall(n=40):
        for _ in range(n):
            if ev("!!document.querySelector('.cine')"): ev("document.querySelector('.cine')?.click()"); W(120)
            else: break
        W(600)
    pg.goto('http://127.0.0.1:8766/'); W(900); ev("startNew()"); W(300)
    ev("document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();document.querySelectorAll('.cine').forEach(e=>e.remove());state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.storyFlags.metDragon=1;state.currentPhase='docked';state.currentLocation='dawnForest';state.journeyCount=8;state.visitedLocations=['dawnForest','starIslands'];"
       "for(const id of ['felinia','pyro','frost']){state.discoveredLifeforms.push(id);state.passengers[id]={stage:2,talks:1,records:[],aboard:true,left:false,boardedJourney:2,zone:PASSENGERS[id].zone}};state.currentCarriage='habitat';render()"); W(800)
    ev("farewell('felinia',()=>window._fw=1)"); W(300)
    for _ in range(30):
        if ev("!!window._fw"): break
        if ev("!!document.querySelector('.cine')"): pg.screenshot(path=S+'/fw.png'); ev("document.querySelector('.cine')?.click()")
        elif ev("!!document.querySelector('.dlg')"): ev("document.querySelector('.dlg .box').click()")
        W(250)
    ok('K1 farewell gives keepsake', ev("state.collectibles.includes('keep_felinia')"))
    ev("state.passengers.pyro.left=true;state.passengers.pyro.aboard=false;render()"); W(300)
    ok('K2 sync for old saves', ev("state.collectibles.includes('keep_pyro')"))
    ev("state.currentCarriage='memory';render()"); W(1200); ev("itemsPanel()"); W(600); pg.screenshot(path=S+'/items.png')
    ev("document.querySelector('[data-box=keep]')?.click()"); W(400); ok('K3 keepsakes in cabinet (紀念品 tab)', ev("document.querySelectorAll('.ov.float .fl:not(.lock)').length")>=2)
    ev("document.querySelector('[data-it=\"keep_felinia\"]').click()"); W(500); pg.screenshot(path=S+'/item_view.png'); ev("closeAll()")
    ok('S1 sealed by default', ev("COLLECTIBLES.seed_ancient_a.sealed===true"))
    ev("unlockSeed('seed_ancient_a',()=>window._sd=1)"); clickall()
    ok('S2 seed opened', ev("!COLLECTIBLES.seed_ancient_a.sealed&&COLLECTIBLES.seed_ancient_a.name==='古種・晨種'&&window._sd===1"))
    ev("state.currentCarriage='nature';render()"); W(1200); ev("seedPanel()"); W(600); ev("document.querySelector('[data-seed=\"seed_ancient_a\"]').click()"); W(2500); pg.screenshot(path=S+'/seed.png')
    ok('S3 panel text', '等一個沒有光' in sayall()+ev("document.querySelector('#sv')?.innerText||''")); ev("closeAll()")
    ev("culturePanel()"); W(500); ok('S4 ancient seed not in pod', not ev("!!document.querySelector('[data-p=\"seed_ancient_a\"]')")); ev("closeAll()")
    # acts
    ok('A1 not unlocked while location not ready', not ev("state.unlockedLocations.includes('reverseRealm')"))
    ev("state.clues.push('clue_dragon');LOCATIONS.reverseRealm.ready=true;LOCATIONS.boundlessCorridor.ready=true;render()"); W(400)
    ok('A2 act two opens both', ev("state.unlockedLocations.includes('reverseRealm')&&state.unlockedLocations.includes('boundlessCorridor')"))
    ev("annHide&&annHide()")
    # endings
    for t,k,exp in [(40,9,'night'),(10,9,'dawn'),(10,3,'return'),(25,10,'return')]:
        r=ev(f"(()=>{{state.storyFlags.departTaint={t};state.collectibles=state.collectibles.filter(x=>!x.startsWith('keep_'));Object.keys(KEEPS).slice(0,{k}).forEach(p=>state.collectibles.push('keep_'+p));return endingType()}})()")
        ok(f'E taint{t} keeps{k} -> {exp}', r==exp, r)
    ev("state.passengers={};state.storyFlags.departTaint=40;playFinale(()=>window._fn='night')"); clickall()
    ok('E1 night returns, can retry', ev("window._fn==='night'&&!state.ending&&!done('finale')"))
    ev("state.storyFlags.departTaint=10;state.collectibles=state.collectibles.filter(x=>!x.startsWith('keep_'));Object.keys(KEEPS).forEach(p=>state.collectibles.push('keep_'+p));playFinale(()=>window._fn='dawn')"); clickall()
    for _ in range(4):
        if ev("!!document.querySelector('#hi')"): ev("document.querySelector('#hi').click()"); W(800)
        clickall(); 
        for _ in range(12):
            if ev("!!document.querySelector('.dlg')"): ev("document.querySelector('.dlg .chs button')?document.querySelector('.dlg .chs button').click():document.querySelector('.dlg .box').click()"); W(300)
    pg.screenshot(path=S+'/yixi_after.png')
    ok('E2 dawn ending', ev("window._fn==='dawn'&&state.ending==='dawn'"))
    ok('E2b 遺曦 boards after the dawn ending', ev("aboard('yixi')&&state.discoveredLifeforms.includes('yixi')"), ev("Object.keys(state.passengers)"))
    ev("state.ending=null;state.completedEvents=[];state.storyFlags.departTaint=25;playFinale()"); clickall(); pg.screenshot(path=S+'/return.png')
    ok('E3 return ending panel', ev("state.ending==='return'&&!!document.querySelector('#ngp')"))
    ev("document.querySelector('#ngp').click()"); W(500)
    ok('E4 new game plus', ev("state.ngPlus===1&&state.journeyCount===0"))
    t=''
    for _ in range(10):
        t+=ev("document.querySelector('.cine .txt')?.innerText||''")
        if '見過' in t: pg.screenshot(path=S+'/ng.png'); break
        ev("document.querySelector('.cine')?.click()"); W(700)
    ok('E5 extra line after intro', '見過' in t, t)
    ok('Z no errors', not errs, errs)
    b.close()
