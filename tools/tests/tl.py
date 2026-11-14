from playwright.sync_api import sync_playwright
import sys,os
S=sys.argv[1]; d='/home/claude/game'
CSP='<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; script-src \'unsafe-inline\'; style-src \'unsafe-inline\' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src data: blob:; media-src data: blob:">'
open(d+'/_c.html','w').write('<!doctype html><meta charset=utf-8>'+CSP+'<meta name=viewport content="width=device-width,initial-scale=1">'+open(d+'/index.html').read())
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n+(' '+str(x) if x!='' else ''),flush=True)
img=lambda ev,sel: ev(f"(()=>{{const i=document.querySelector('{sel}');return !!i&&i.complete&&i.naturalWidth>0}})()")
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; bad=[]; errs=[]
    pg.on('console',lambda m: 'violates' in m.text and bad.append(m.text[:90])); pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8765/_c.html'); W(800)
    ev("startNew()"); W(200)
    ev("closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.journeyCount=1;state.currentLocation='dawnForest';state.visitedLocations=['dawnForest'];state.completedEvents=['voyage_symbol','board_lumi','board_felinia'];state.discoveredLifeforms=['lumi','felinia'];"
       "state.passengers.lumi={stage:1,talks:1,records:[],aboard:true,left:false,boardedJourney:1};state.passengers.felinia={stage:1,talks:1,records:[],aboard:true,left:false,boardedJourney:0};"
       "state.duty={scan:true,briefing:true,signal:true,doors:true,reported:true};state.spirit.equipment={tablet:true,compass:true,talisman:true};state.currentCarriage='cab';render();startDeparture()"); W(500)
    while ev("!!document.querySelector('.cine')"): pg.click('.cine'); W(300)
    ok('L0 heading to 星河浮島', ev("state.voyage.to")=='starIslands')
    ev("state.voyage.progress=.59"); W(1500)
    ok('L1 whale boarding cine', ev("!!document.querySelector('.cine')") and '靈泉' in pg.inner_text('.cine'))
    pg.click('.cine'); W(1600); ok('L2 boarding card portrait', img(ev,'.ov.board .portrait img')); pg.screenshot(path=S+'/l_board.png')
    pg.click('#hi'); W(500)
    while ev("!!document.querySelector('.dlg')"):
        if ev("!!document.querySelector('.dlg .chs button')"): pg.click('.dlg .chs button'); W(1100)
        else: pg.click('.dlg .box'); W(150)
    ev("state.currentCarriage='habitat';render()"); W(1600)
    ok('L3 whale + winged cat both visible', img(ev,'[data-hs="hab-p-leviathaurora"] img') and img(ev,'[data-hs="hab-p-felinia"] img'))
    r=ev("['hab-p-leviathaurora','hab-p-felinia','hab-p-lumi','hab-door','hab-spring','hab-moss','hab-rest'].map(id=>{const e=document.querySelector(`[data-hs=\"${id}\"]`);const b=e.getBoundingClientRect();return [id,Math.round(b.left),Math.round(b.top),Math.round(b.right),Math.round(b.bottom)]})")
    print(r)
    pg.screenshot(path=S+'/l_hab.png')
    pg.click('[data-hs="hab-p-leviathaurora"]',force=True); W(700); ok('L4 dialogue portrait', img(ev,'.dlg .who img')); pg.screenshot(path=S+'/l_dlg.png')
    while ev("!!document.querySelector('.dlg')"):
        if ev("!!document.querySelector('.dlg .chs button')"): pg.click('.dlg .chs button'); W(1100)
        else: pg.click('.dlg .box'); W(150)
    ev("openBook('life','leviathaurora')"); W(1500); ok('L5 codex still + studies', img(ev,'.plate.big img') and img(ev,'.studies img') and '生物冷光共鳴' in pg.inner_text('.spread')); pg.screenshot(path=S+'/l_book.png'); ev("closeAll()")
    ev("openBook('life')"); W(800); ok('L6 index: 4 known, 2 reserved', ev("CODEX_LIFE.map(codexEntry).filter(e=>e.known).length")==4 and ev("CODEX_LIFE.length")==6); ev("closeAll()")
    ok('L7 no blocked resources / errors', not bad and not errs, (bad,errs))
    b.close()
os.remove(d+'/_c.html')
