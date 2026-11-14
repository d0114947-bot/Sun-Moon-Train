from playwright.sync_api import sync_playwright
import sys
S=sys.argv[1]; d='/home/claude/game'
html=open(d+'/index.html').read()
open(d+'/_t.html','w').write('<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover">'+html)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    ev=pg.evaluate; W=pg.wait_for_timeout
    pg.goto('http://127.0.0.1:8765/_t.html'); W(800); ev("window.rollBoarders=()=>[]")
    pg.click('#ms-work'); W(1500); pg.click('#ms-new'); W(500)
    ev("closeAll();state.introDone=true;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.currentPhase='docked';state.currentLocation='dawnForest';state.journeyCount=3;state.visitedLocations=['dawnForest'];state.clues=CLUE_ORDER.slice(0,4);state.collectibles.push('seed_ancient_a');state.consts=['deer'];state.backlog=[{w:'菲莉妮雅',t:'你好呀',g:1,j:2,l:'dawnForest'},{w:'菲莉妮雅',t:'今天的風好舒服',g:1,j:2,l:'dawnForest'},{w:'列車廣播',t:'各位旅客',g:5,j:3,l:'starIslands'}];save()")
    def shot(n,js,w=900):
        ev("closeAll()"); W(300); ev(js); W(w); pg.screenshot(path=f'{S}/b2_{n}.png')
    shot('obsF',"state.currentCarriage='observation';state.oview=0;render()",1200)
    shot('obsB',"state.currentCarriage='observation';state.oview=1;render()",1200)
    shot('save',"savePanel('game')")
    shot('mem',"state.currentCarriage='memory';render();memoryPanel()")
    shot('items',"itemsPanel()")
    shot('globe',"orreryPanel()",1200)
    shot('lore',"openBook('lore')",1200)
    shot('clue',"clueBook()",1200)
    shot('const',"state.currentCarriage='observation';state.oview=0;render();constPanel()",1200)
    ev("document.querySelector('[data-face=\"1\"]').click()"); W(900); pg.screenshot(path=f'{S}/b2_const2.png')
    shot('vine',"state.currentCarriage='nature';render();vinePanel()",1500)
    shot('vault',"seedPanel()",900)
    ev("document.querySelector('[data-cs]') && document.querySelector('[data-cs]').click()"); W(800); pg.screenshot(path=f'{S}/b2_vault2.png')
    shot('engr',"state.currentCarriage='observatory';state.engr=[];render();engravePanel()",900)
    shot('mirror',"state.currentCarriage='habitat';render();spiritPanel()",900)
    print('errs',errs)
    b.close()
