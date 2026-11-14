from playwright.sync_api import sync_playwright
import sys,os
S=sys.argv[1]; d='/home/claude/game'
open(d+'/_t.html','w').write('<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">'+open(d+'/index.html').read())
R=[]
def ok(n,c,x=''): R.append(('PASS ' if c else 'FAIL ')+n+(' '+str(x) if x!='' else '')); print(R[-1],flush=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8765/_t.html'); W(600)
    ev("startNew()"); W(300); ev("closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.duty={scan:true,briefing:true,signal:true,doors:true,reported:true};state.spirit.equipment={tablet:true,compass:true,talisman:true};state.storyFlags.metDragon=1;state.currentCarriage='cab';render();startDeparture()"); W(600)
    while ev("!!document.querySelector('.cine')"): pg.click('.cine'); W(300)
    ev("state.voyage.progress=.5"); W(900)
    while ev("!!document.querySelector('.cine')"): pg.click('.cine'); W(300)   # voyage symbol (default event)
    ok('F0 symbol event still runs first', ev("done('voyage_symbol')"))
    ev("state.voyage.progress=.71"); W(1500)
    ok('F1 boarding cine during voyage', ev("!!document.querySelector('.cine')") and '橫風' in pg.inner_text('.cine'))
    pg.click('.cine'); W(1600); pg.screenshot(path=S+'/f_board.png')
    p0=ev("state.voyage.progress"); W(1200); ok('F2 voyage pauses during boarding card', ev("state.voyage.progress")==p0)
    pg.click('#hi'); W(500); pg.screenshot(path=S+'/f_dlg.png')
    while ev("!!document.querySelector('.dlg')"):
        if ev("!!document.querySelector('.dlg .chs button')"): pg.click('.dlg .chs button'); W(1100)
        else: pg.click('.dlg .box'); W(150)
    ok('F3 aboard with record', ev("aboard('felinia')") and '航行途中' in ev("state.passengers.felinia.records[0].t"))
    ev("state.currentCarriage='habitat';render()"); W(1500)
    ok('F4 sprite in habitat', ev("!!document.querySelector('[data-hs=\"hab-p-felinia\"] .spr img')"))
    pg.screenshot(path=S+'/f_hab.png')
    pg.click('[data-hs="hab-p-felinia"]',force=True); W(500); ok('F5 click sprite → dialogue', ev("!!document.querySelector('.dlg .who img.land')"))
    while ev("!!document.querySelector('.dlg')"):
        if ev("!!document.querySelector('.dlg .chs button')"): pg.click('.dlg .chs button'); W(1100)
        else: pg.click('.dlg .box'); W(150)
    ev("openBook('life')"); W(1500); pg.screenshot(path=S+'/f_book1.png')
    pg.click('.spec[data-life="felinia"]'); W(1500); pg.screenshot(path=S+'/f_book2.png')
    ok('F6 book detail with field data', '御風滑翔' in pg.inner_text('.spread') and ev("document.querySelectorAll('.studies img').length")==2)
    ev("document.querySelector('.spread .page.r').scrollTop=600"); W(300); pg.screenshot(path=S+'/f_book3.png')
    ev("closeAll();memoryPanel()"); W(400); ok('F7 memory shard', ev("!!document.querySelector('[data-m=\"felinia\"]')")); ev("closeAll()")
    ev("if(state.voyage) state.voyage.progress=.99"); W(1200)
    while ev("!!document.querySelector('.cine')"): pg.click('.cine'); W(400)
    ok('F8 arrival continues after event', ev("state.currentPhase==='docked'&&state.journeyCount===1"))
    ok('F9 errors', not errs, errs)
    b.close()
os.remove(d+'/_t.html')
