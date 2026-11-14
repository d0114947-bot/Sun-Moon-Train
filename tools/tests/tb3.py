from playwright.sync_api import sync_playwright
import sys
S=sys.argv[1]; d='/home/claude/game'
html=open(d+'/index.html').read()
open(d+'/_t.html','w').write('<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover">'+html)
R=[]
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n+' '+str(x)[:200],flush=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    ev=pg.evaluate; W=pg.wait_for_timeout
    pg.goto('http://127.0.0.1:8765/_t.html'); W(800); ev("window.rollBoarders=()=>[]")
    pg.click('#ms-work'); W(1500); pg.click('#ms-new'); W(500)
    ev("closeAll();state.introDone=true;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.currentPhase='docked';state.currentLocation='dawnForest';state.currentCarriage='nature';state.labels={};render()")
    p0=ev("Object.keys(PLANTS).find(p=>!PLANTS[p].rare)"); ev(f"seedAdd('{p0}',2);seedPanel()"); W(800)
    pg.click(f'[data-cs="{p0}"]'); W(900)
    ok('L1 unlabeled jar has blank tag + label sheet', ev(f"document.querySelector('[data-cs=\"{p0}\"] .tag.blank')!==null") and ev("document.querySelectorAll('.lbl').length")>=2)
    pg.screenshot(path=S+'/b3_lbl.png')
    name=ev(f"PLANTS['{p0}'].seed"); bx=ev(f"(()=>{{const b=[...document.querySelectorAll('.lbl')].find(x=>x.dataset.lbl==='{name}').getBoundingClientRect();const t=document.querySelector('.lbl-jar').getBoundingClientRect();return [b.x+b.width/2,b.y+b.height/2,t.x+t.width/2,t.y+t.height/2]}})()")
    pg.mouse.move(bx[0],bx[1]); pg.mouse.down(); pg.mouse.move(bx[0]+20,bx[1]+10,steps=3); pg.mouse.move(bx[2],bx[3],steps=8); W(200); pg.screenshot(path=S+'/b3_drag.png'); pg.mouse.up(); W(500)
    ok('L2 sticker dragged onto the jar labels it', ev(f"state.labels['{p0}']===1") and ev(f"document.querySelector('[data-cs=\"{p0}\"] .tag').textContent")==name)
    pg.screenshot(path=S+'/b3_lbl2.png')
    ev("closeAll()"); W(300); ev("savePanel('game')"); W(900); pg.screenshot(path=S+'/b3_save.png')
    ok('S1 three crystals per face', ev("document.querySelector('.c3-face.front').querySelectorAll('.svc').length")==3)
    st=ev("(()=>{const r=document.querySelector('.sv3 .c3-stage').getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()")
    pg.mouse.move(st[0]+st[2]*.7,st[1]+st[3]/2); pg.mouse.down(); pg.mouse.move(st[0]+st[2]*.2,st[1]+st[3]/2,steps=10); pg.mouse.up(); W(900)
    ok('S2 drag rotates to next three', ev("[...document.querySelectorAll('.sv3 .c3-face')].findIndex(f=>f.classList.contains('front'))")==1)
    pg.screenshot(path=S+'/b3_save2.png')
    ok('no errors',not errs,errs)
    b.close()
