import os
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad/nobsv'; os.makedirs(S,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]
    for vw,vh in [(1280,720),(390,844)]:
        pg=b.new_page(viewport={'width':vw,'height':vh}); ev=pg.evaluate; W=pg.wait_for_timeout
        pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('http://127.0.0.1:8766/'); W(900); ev("startNew()"); W(300)
        ev("document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();document.querySelectorAll('.cine').forEach(e=>e.remove());state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.storyFlags.metDragon=1;state.currentPhase='docked';state.currentLocation='dawnForest';state.journeyCount=4;state.visitedLocations=['dawnForest','starIslands'];state.consts=['deer'];state.currentCarriage='habitat';render()"); W(800)
        ev("moveTo('observation')"); W(2500); pg.screenshot(path=f'{S}/front_{vw}.png')
        print(vw,'front',ev("[...document.querySelectorAll('#scene [data-hs]')].map(e=>e.dataset.hs)"))
        ev("turnView()"); W(1200); pg.screenshot(path=f'{S}/back_{vw}.png')
        print(vw,'back',ev("[...document.querySelectorAll('#scene [data-hs]')].map(e=>e.dataset.hs)"))
        ev("moveTo('observatory')"); W(2500); ev("moveTo('observation')"); W(2500); print('from deck view', ev("state.oview"))
        pg.close()
    print('errs',errs)
    b.close()
