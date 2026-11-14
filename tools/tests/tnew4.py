import sys,os
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad/nshot4'; os.makedirs(S,exist_ok=True)
VW=int(sys.argv[1]) if len(sys.argv)>1 else 1280; VH=int(sys.argv[2]) if len(sys.argv)>2 else 720
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':VW,'height':VH}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n,x if not c else '',flush=True)
    def shot(n): pg.screenshot(path=f'{S}/{n}_{VW}.png')
    pg.goto('http://127.0.0.1:8766/'); W(900); ev("startNew()"); W(300)
    ev("document.querySelector('#mainscreen')?.remove();closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.storyFlags.metDragon=1;state.currentPhase='docked';state.currentLocation='dawnForest';state.journeyCount=3;state.visitedLocations=['dawnForest','starIslands'];state.clues=['clue_wake','clue_ring'];state.spirit.equipment={tablet:true,compass:true,talisman:true};"
       "for(const id of ['felinia','pyro','frost']){state.discoveredLifeforms.push(id);state.passengers[id]={stage:2,talks:1,records:[],aboard:true,left:false,boardedJourney:2,zone:PASSENGERS[id].zone}};state.currentCarriage='cab';render()"); W(1500)
    shot('announce')
    ev("briefPanel()"); W(3600); shot('brief'); ok('B1 rows reveal by themselves', ev("document.querySelectorAll('.tl.open').length")==5); ev("closeAll()")
    ev("discPanel()"); W(500); shot('disc'); ev("closeAll()")
    ev("compassPanel()"); W(2500); shot('compass'); pg.click('.dlg'); W(300); pg.click('.dlg'); W(1500); shot('compass2'); ev("closeAll()")
    ev("state.currentCarriage='observation';render()"); W(1200)
    ev("scopePanel()"); W(800); shot('scope'); ev("document.querySelector('[data-sh] ')&&document.querySelector('[data-sh]').dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}))"); W(2500); shot('scope2'); ok('S1 shadow found', len(ev("state.scopeSeen||[]"))>=1); ev("closeAll()")
    ev("constPanel('deer')"); W(500); shot('const')
    ev("""(()=>{const c=CONSTS[0];const fire=i=>document.querySelector('[data-st="'+i+'"]').dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}));fire(0);fire(1);fire(2);fire(3);fire(4)})()"""); W(400); shot('const2'); ok('C1 chain connects', ev("document.querySelectorAll('.cs-round line[stroke=\"#ffe9a8\"]').length")>=4); ev("closeAll()")
    ev("openBook('lore')"); W(900); shot('lore'); ev("closeAll()")
    ev("state.currentCarriage='nature';render()"); W(1200); ev("seedPanel()"); W(2500); shot('vault'); ev("closeAll()")
    ev("vinePanel()"); W(800); pg.click('#vn'); W(400); shot('vine'); ok('V1 "no" keeps the vine open', ev("!!document.querySelector('.vine-stage')")); ev("closeAll()")
    ev("state.currentCarriage='habitat';render()"); W(1200); ev("zoneInfo('spring')"); W(700); shot('drawer'); ev("closeAll()")
    ev("state.currentPhase='voyage';state.voyage={from:'dawnForest',to:'starIslands',progress:.5,evt:true,sky:{type:'meteor',at:.4,started:true,ended:false,watched:false}};state.currentCarriage='observatory';render()"); W(1000)
    ev("skyWatch()"); W(2500); shot('sky'); ok('K1 sky watch is a dialogue', ev("!!document.querySelector('.dlg')") and not ev("!!document.querySelector('#layer .ov')")); ev("closeAll()")
    ev("state.voyage.progress=.99"); W(2500)
    for _ in range(6):
        if ev("!!document.querySelector('.cine')"): pg.click('.cine'); W(700)
    shot('senses');
    ok('Z no errors', not errs, errs)
    b.close()
