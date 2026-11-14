import os
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad/nobs'; os.makedirs(S,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n,x if not c else '',flush=True)
    def adv(n=30):
        for _ in range(n):
            if ev("!!document.querySelector('.dlg')"):
                if ev("!!document.querySelector('.dlg .chs button')"): ev("document.querySelector('.dlg .chs button').click()"); W(1600)
                else: ev("document.querySelector('.dlg .box')?.click(); document.querySelector('.dlg:not(:has(.chs))')?.click()"); W(150)
            else: break
        W(400)
    pg.goto('http://127.0.0.1:8766/'); W(900); ev("startNew()"); W(300)
    ev("document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();document.querySelectorAll('.cine').forEach(e=>e.remove());state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.storyFlags.metDragon=1;state.storyFlags.gt_done=1;state.currentPhase='docked';state.currentLocation='dawnForest';state.journeyCount=4;state.visitedLocations=['dawnForest','starIslands'];state.unlockedLocations=['dawnForest','starIslands'];"
       "for(const id of ['felinia','frost']){state.discoveredLifeforms.push(id);state.passengers[id]={stage:2,talks:9,records:[],aboard:true,left:false,boardedJourney:2,zone:PASSENGERS[id].zone}};state.req={felinia:{st:'on',j:1},frost:{st:'done'}};state.consts=['deer','jelly'];gardenSync();state.pods[0]={p:'stardaisy',st:0};state.currentCarriage='observation';state.oview=1;render()"); W(1200)
    ev("discPanel()"); W(600); ok('F1 cab disc shows forecast', '星象' in ev("document.querySelector('.disc-ring').textContent")); ev("closeAll()"); W(300); ev("navPanel()"); W(600)
    ev("document.querySelector('[data-st=\"starIslands\"]').dispatchEvent(new MouseEvent('click',{bubbles:true}))"); W(500); pg.screenshot(path=S+'/nav.png')
    t=ev("document.querySelector('#smi').innerText"); ok('F2 tip forecast', '星象預報' in t, t)
    ev("closeAll()")
    ev("state.currentCarriage='cab';render()"); W(800); ev("compassPanel()"); W(600); pg.screenshot(path=S+'/disc.png')
    ok('B1 compass bless', ev("document.querySelectorAll('[data-bless]:not([disabled])').length")==2)
    ev("document.querySelector('[data-bless=\"deer\"]').click()"); W(300); ok('B2 selected', ev("state.blessNext")=='deer'); ev("closeAll()")
    t0=ev("TAINT.val()"); cross=ev("TAINT_GAIN[realmKey(nextStop())].cross")
    ev("startDeparture()"); W(2500)
    for _ in range(20):
        if ev("state.currentPhase==='voyage'"): break
        if ev("!!document.querySelector('.cine')"): ev("document.querySelector('.cine').click()")
        W(300)
    d=ev('TAINT.val()')-t0; ok('B3 deer halves crossing taint (+4 when its sky does not match the route)', d in (round(cross/2),-(-cross//2),round(cross/2)+4,-(-cross//2)+4), (t0,ev('TAINT.val()'),cross))
    ok('B4 bless cleared after use', ev("state.blessNext===null&&state.storyFlags.voyBless==='deer'"))
    # deck home constellation
    ev("state.currentPhase='docked';state.voyage=null;state.passengers.felinia.place='deck';state.currentCarriage='observatory';render()"); W(800)
    ev("deckTalk('felinia')"); adv(); ok('H1 felinia points home const', ev("(state.homeConsts||[]).includes('felinia')"))
    ev("document.querySelectorAll('.cine').forEach(e=>e.remove());closeAll();state.currentCarriage='observation';state.oview=1;render()"); W(600); ev("constPanel()"); W(600); ev("document.querySelector('[data-face=\"2\"]').click()"); W(900); pg.screenshot(path=S+'/const.png')
    ok('H2 home const listed', ev("!!document.querySelector('[data-cs=\"h_felinia\"]')"))
    ev("document.querySelector('[data-cs=\"h_felinia\"]').click()"); W(400)
    ev("""(()=>{const c=HOME_C.felinia;const fire=i=>document.querySelector('[data-st="'+i+'"]').dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}));c.E.forEach(([a,b])=>{fire(a);fire(b);})})()"""); W(2200); pg.screenshot(path=S+'/const_done.png')
    ok('H3 traced', ev("constDone('h_felinia')"))
    ev("closeAll();state.currentCarriage='habitat';render()"); W(600); ev("talk('felinia')"); W(300)
    ok('H4 story', '風谷座' in ev("document.querySelector('.dlg').innerText")); adv(); ok('H5 told', ev("state.passengers.felinia.homeTold===1"))
    ok('Z no errors', not errs, errs)
    b.close()
