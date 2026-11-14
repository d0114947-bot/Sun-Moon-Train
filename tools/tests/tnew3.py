import sys,os
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad/nshot3'; os.makedirs(S,exist_ok=True)
VW=int(sys.argv[1]) if len(sys.argv)>1 else 1280; VH=int(sys.argv[2]) if len(sys.argv)>2 else 720
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':VW,'height':VH}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n,x if not c else '',flush=True)
    def shot(n): pg.screenshot(path=f'{S}/{n}_{VW}.png')
    pg.goto('http://127.0.0.1:8766/'); W(1200)
    pg.click('#ms-work'); W(400); pg.click('#ms-new'); W(300); shot('fade'); W(900); ok('T1 one click starts with fade', not ev("!!document.querySelector('#mainscreen,#mainscreen-out')") and ev("!!document.querySelector('.cine')"))
    ev("closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.storyFlags.metDragon=1;state.currentPhase='docked';state.currentLocation='dawnForest';state.journeyCount=3;state.visitedLocations=['dawnForest','starIslands'];state.clues=['clue_wake','clue_ring'];state.spirit.equipment={tablet:true,compass:false,talisman:false};"
       "for(const id of ['felinia','pyro','frost','sirenora']){state.discoveredLifeforms.push(id);state.passengers[id]={stage:2,talks:1,records:[],aboard:true,left:false,boardedJourney:2,zone:PASSENGERS[id].zone}};state.currentCarriage='cab';render()"); W(1500)
    pg.mouse.click(5,400); W(300); shot('cab'); ok('D1 dragon away while duty not done', not ev("!!document.querySelector('[data-hs=\"cab-dragon\"]')"))
    ev("briefPanel()"); W(400); pg.click('.tl[data-i="0"]'); W(300); shot('brief'); pg.click('.tl[data-i="0"] .rn'); W(200); ok('B1 circle confirms', ev("document.querySelector('.tl[data-i=\"0\"]').classList.contains('ok')")); ev("closeAll()")
    ev("equipPanel()"); W(500); shot('equip'); ev("closeAll()")
    ev("cabSignal()"); W(400); shot('signal'); ok('S1 signal uses dialogue', ev("!!document.querySelector('.dlg')")); ev("closeAll()")
    ev("compassPanel()"); W(400); ok('S2 compass uses dialogue', ev("!!document.querySelector('.dlg')")); ev("closeAll()")
    ev("state.currentCarriage='memory';render()"); W(1500); shot('memory'); pg.click('.pano-turn.r'); W(1200); shot('memory2')
    ev("openBook('life')"); W(900); shot('life')
    box=ev("(()=>{const r=document.querySelector('.jr-pages').getBoundingClientRect();return [r.left,r.top,r.width,r.height]})()")
    pg.mouse.move(box[0]+box[2]*.9,box[1]+box[3]*.5); pg.mouse.down(); pg.mouse.move(box[0]+box[2]*.6,box[1]+box[3]*.5,steps=8); W(100); shot('life_drag')
    pg.mouse.move(box[0]+box[2]*.15,box[1]+box[3]*.5,steps=8); pg.mouse.up(); W(1300); ok('L1 drag flips', ev("document.querySelector('.ov.jr').dataset.page")!='0')
    ev("document.querySelector('.ov.jr').jump(0)"); W(300); ev("document.querySelector('.spec[data-life]').click()"); W(500); shot('life_detail'); ev("closeAll()")
    ev("openBook('lore')"); W(800); shot('lore'); ev("closeAll()")
    ev("orreryPanel()"); W(1500); shot('globe'); ev("closeAll()")
    ev("spiritPanel()"); W(800); shot('mirror'); ev("closeAll()")
    ev("savePanel('game')"); W(600); shot('save'); ev("closeAll()")
    ev("notebookPanel()"); W(800); shot('notebook'); ev("closeAll()")
    ev("state.currentCarriage='nature';render()"); W(1200)
    ev("seedPanel()"); W(600); shot('vault'); ev("closeAll()")
    ev("vinePanel()"); W(700); shot('vine'); ev("closeAll()")
    ok('Z no errors', not errs, errs)
    b.close()
