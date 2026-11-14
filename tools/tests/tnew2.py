import sys,os
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad/nshot2'; os.makedirs(S,exist_ok=True)
VW=int(sys.argv[1]) if len(sys.argv)>1 else 1280; VH=int(sys.argv[2]) if len(sys.argv)>2 else 720
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':VW,'height':VH}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n,x if not c else '',flush=True)
    def shot(n): pg.screenshot(path=f'{S}/{n}_{VW}.png')
    pg.goto('http://127.0.0.1:8766/'); W(800); ev("startNew()"); W(300)
    ev("document.querySelector('#mainscreen')?.remove();closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.storyFlags.metDragon=1;state.currentPhase='docked';state.currentLocation='dawnForest';state.journeyCount=3;state.visitedLocations=['dawnForest','starIslands'];"
       "for(const id of ['felinia','pyro','frost','sirenora']){state.discoveredLifeforms.push(id);state.passengers[id]={stage:2,talks:1,records:[],aboard:true,left:false,boardedJourney:2,zone:PASSENGERS[id].zone}};state.notes={felinia:[0,1,2]};state.currentCarriage='cab';render()"); W(1600)
    ok('Q1 announcement typed in the centre', ev("!!document.querySelector('#announce.on')") and len(ev("document.querySelector('#announce .an-t').textContent"))>5); shot('announce')
    pg.mouse.click(30,400); W(600); ok('Q2 click dismisses', not ev("!!document.querySelector('#announce.on')"))
    ok('Q3 no lumi', ev("!PASSENGERS.lumi&&!EVENTS.board_lumi"))
    ev("notebookPanel()"); W(800); shot('notebook'); ok('N1 notebook is a book with tabs', ev("!!document.querySelector('.ov.jr.notebook .jr-tab')"))
    pg.click('.jr-nav.next'); W(800); shot('notebook2'); ev("closeAll()")
    ev("skyBook()"); W(800); shot('skybook'); ev("closeAll()")
    ev("state.currentCarriage='habitat';render()"); W(1500); shot('habitat')
    ev("zoneInfo('rings')"); W(700); shot('drawer'); ok('H1 drawer has no zone tabs', not ev("!!document.querySelector('[data-z]')"))
    ev("document.querySelector('[data-ask]')&&document.querySelector('[data-ask]').click()"); W(500); shot('ask'); ok('H2 ask is a dialogue', ev("!!document.querySelector('.dlg')"))
    ev("closeAll()"); W(300)
    ev("talk('felinia')"); W(800); shot('talk'); ok('H3 talking passenger hidden in scene', ev("document.querySelector('[data-hs=\"hab-p-felinia\"]').classList.contains('talking')")); ev("closeAll()"); W(300)
    ev("state.currentCarriage='observation';render()"); W(1500); shot('obs')
    ev("navPanel()"); W(600); ev("document.querySelector('[data-st=\"starIslands\"]').dispatchEvent(new MouseEvent('click',{bubbles:true}))"); W(500); shot('nav')
    ev("document.querySelector('[data-route]')&&document.querySelector('[data-route]').click()"); W(400); ok('R1 route changed', ev("nextStop()")=='starIslands', ev("nextStop()")); ev("closeAll()")
    ev("anomPanel()"); W(800); shot('anom'); ev("closeAll()")
    ev("constPanel()"); W(600); shot('const'); pg.click('[data-cs="deer"]'); W(400); shot('const2'); ev("closeAll()")
    ev("state.currentCarriage='observatory';state.storyFlags.starLight=true;state.passengers.pyro.place='deck';state.passengers.frost.place='deck';render()"); W(1200); shot('deck')
    ev("engravePanel()"); W(500); shot('engrave')
    for k in range(5):
        ev(f"(()=>{{const E=engrEdges('dawnForest');const [a,b2]=E[{k}];[a,b2].forEach(i=>document.querySelector('[data-en=\"'+i+'\"]').dispatchEvent(new PointerEvent('pointerdown',{{bubbles:true}})))}})()"); W(150)
    W(400); shot('engrave2'); ok('D1 engraving done', ev("ENGR_OK('dawnForest')")); ev("closeAll()")
    ev("rubbingPanel()"); W(600); shot('rubbing'); ev("closeAll()")
    ev("state.currentPhase='outside';state.companion='pyro';render()"); W(9000); shot('outside'); ok('C1 companion talks first', ev("!!document.querySelector('.dlg')"))
    ok('Z no errors', not errs, errs)
    b.close()
