import sys
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad/hab'
VW=int(sys.argv[1]) if len(sys.argv)>1 else 1280; VH=int(sys.argv[2]) if len(sys.argv)>2 else 720
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':VW,'height':VH}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(900); ev("startNew()"); W(300)
    ev("document.querySelector('#mainscreen')?.remove();closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.storyFlags.metDragon=1;state.currentPhase='docked';state.currentLocation='dawnForest';state.journeyCount=3;state.annSeen='x';"
       "for(const id of Object.keys(PASSENGERS)){state.discoveredLifeforms.push(id);state.passengers[id]={stage:2,talks:1,records:[],aboard:true,left:false,boardedJourney:2,zone:PASSENGERS[id].zone}};state.currentCarriage='habitat';state.hview=0;render()"); W(2000)
    ev("annHide()"); W(300); pg.screenshot(path=f'{S}/front_{VW}.png')
    pg.click('.pano-turn.r'); W(900); pg.screenshot(path=f'{S}/back_{VW}.png')
    print([e.dataset if False else e for e in ev("[...document.querySelectorAll('#scene [data-hs]')].map(e=>e.dataset.hs)")])
    print(errs)
    b.close()
