import os
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad/nobs2'; os.makedirs(S,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n,x if not c else '',flush=True)
    pg.goto('http://127.0.0.1:8766/'); W(900); ev("startNew()"); W(300)
    ev("document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();document.querySelectorAll('.cine').forEach(e=>e.remove());state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.storyFlags.metDragon=1;state.storyFlags.gt_done=1;state.currentPhase='docked';state.currentLocation='dawnForest';state.journeyCount=4;state.visitedLocations=['dawnForest','starIslands'];state.unlockedLocations=['dawnForest','starIslands'];state.currentCarriage='observation';state.oview=1;render()"); W(1000)
    ev("navPanel()"); W(500); ok('R1 obs button', ev("!!document.querySelector('#nv-obs')")); ev("document.querySelector('#nv-obs').dispatchEvent(new MouseEvent('click',{bubbles:true}))"); W(400); pg.screenshot(path=S+'/nav_obs.png')
    lv=ev("state.duty.obs.lv"); ok('R2 obs recorded', lv in ('平穩','微擾','亂流'), lv); ev("closeAll()")
    # report to dragon & depart
    ev("state.duty={signal:1,doors:1,scan:1,briefing:1,mic:1,obs:state.duty.obs};state.spirit.equipment={tablet:true,compass:true,talisman:true};state.spirit.contamination={value:10,level:'純淨'};state.spirit.taint=10;state.currentCarriage='cab';render()"); W(800)
    base=ev("TAINT_GAIN[realmKey(nextStop())].cross"); t0=ev("TAINT.val()")
    ev("INTERACT['cab:dragon']?INTERACT['cab:dragon']():0"); W(300)
    txt=''
    for _ in range(25):
        txt+=ev("document.querySelector('.dlg .tx')?.innerText||''")
        if ev("!!document.querySelector('.dlg')"): ev("document.querySelector('.dlg .box')?.click()"); W(200)
        elif ev("!!document.querySelector('.cine')"): ev("document.querySelector('.cine').click()"); W(300)
        elif ev("state.currentPhase==='voyage'"): break
        elif ev("state.duty.reported&&!document.querySelector('.ov')"): ev("discPanel()"); W(500); ev("document.querySelector('#dgo').click()"); W(7000)
        else: W(300)
    ok('R3 told dragon', '觀測車廂也看過了' in txt, txt[-300:])
    ok('R4 crossing reduced', ev("state.currentPhase")=='voyage' and ev("TAINT.val()")-t0==max(0,base-{'平穩':1,'微擾':2,'亂流':4}[lv]), (t0,ev("TAINT.val()"),base,lv))
    # lure
    ev("closeAll();document.querySelectorAll('.cine,.dlg').forEach(e=>e.remove());state.storyFlags.starLight=true;state.voyage.light=1;state.voyage.progress=.6;lureTick(state.voyage);state.currentCarriage='observatory';render()"); W(800); pg.screenshot(path=S+'/stray.png')
    ok('L1 stray light shown', ev("!!document.querySelector('.stray')"))
    LC=ev("(()=>{state.storyFlags.lightLure=true;state.currentPhase='docked';state.currentLocation='starIslands';let c=0;for(let i=0;i<60;i++){state.storyFlags.lightLure=true;const r=rollBoarders();if(r.includes('board_sola'))c++;}state.currentPhase='voyage';return c})()"); print('LC',LC); ok('L2 lure weights lost', LC>12, LC)
    # dust
    ev("state.currentLocation='dawnForest';state.voyage.sky={type:'meteor',at:.4,started:true,ended:false,watched:true};render()"); W(600)
    ok('D1 dust hotspot', ev("!!document.querySelector('[data-hs=\"ot-dust\"]')"))
    ev("dustGame()"); W(1500)
    for i in range(14):
        ev("[...document.querySelectorAll('.dg-mote:not([data-c])')].slice(0,1).forEach(d=>d.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true})))"); W(500)
    pg.screenshot(path=S+'/dust.png'); W(2500)
    ok('D2 stardust caught', ev("matCount('stardust')")>=3, ev("matCount('stardust')"))
    ok('D3 once per event', not ev("!!document.querySelector('[data-hs=\"ot-dust\"]')"))
    ok('Z no errors', not errs, errs)
    b.close()
