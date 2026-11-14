from playwright.sync_api import sync_playwright
import sys
S=sys.argv[1]; d='/home/claude/game'
html=open(d+'/index.html').read()
open(d+'/_t.html','w').write('<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover">'+html)
R=[]
def ok(n,c,x=''): R.append(('PASS ' if c else 'FAIL ')+n+' '+str(x)[:200]); print(R[-1],flush=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    ev=pg.evaluate; W=pg.wait_for_timeout
    pg.goto('http://127.0.0.1:8765/_t.html'); W(800); ev("window.rollBoarders=()=>[]")
    pg.click('#ms-work'); W(1500); pg.click('#ms-new'); W(600)
    for i in range(6): pg.click('.cine'); W(260)
    W(1000); pg.screenshot(path=S+'/b1_origin.png')
    pg.click('[data-hs="out-board-origin"]',force=True); W(1800); pg.screenshot(path=S+'/b1_cab.png')
    ev("panelFor('prep:scan')") if ev("typeof panelFor==='function'") else None
    ev("document.querySelector('[data-hs=\"cab-scan\"]').click()"); W(700); pg.screenshot(path=S+'/b1_scan.png')
    pg.click('#sb'); W(2900); pg.screenshot(path=S+'/b1_scan2.png'); ev("closeAll()"); W(400)
    ev("document.querySelector('[data-hs=\"cab-equip\"]').click()"); W(700); pg.screenshot(path=S+'/b1_equip.png')
    for k in ['tablet','compass','talisman']: pg.click(f'[data-eq="{k}"]'); W(120)
    ev("closeAll()"); W(400); ev("document.querySelector('[data-hs=\"cab-brief\"]').click()"); W(4500); pg.screenshot(path=S+'/b1_brief.png')
    for i in range(5): pg.click(f'.tl[data-i="{i}"]'); W(400); pg.click(f'.tl[data-i="{i}"] .rn'); W(90)
    W(400); pg.screenshot(path=S+'/b1_brief2.png'); ev("closeAll()"); W(400)
    ev("document.querySelector('[data-hs=\"cab-mic\"]').click()"); W(700); pg.screenshot(path=S+'/b1_mic.png'); ev("closeAll()")
    ev("discPanel()"); W(700); pg.screenshot(path=S+'/b1_disc.png')
    ev("closeAll();state.currentCarriage='observation';render()"); W(800); ev("navPanel()"); W(900); pg.screenshot(path=S+'/b1_nav.png')
    ok('no errors',not errs,errs)
    b.close()
