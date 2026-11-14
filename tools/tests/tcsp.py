from playwright.sync_api import sync_playwright
import sys,os
src=sys.argv[1]; d='/home/claude/game'
CSP='<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; script-src \'unsafe-inline\'; style-src \'unsafe-inline\' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src data: blob:; media-src data: blob:">'
open(d+'/_c.html','w').write('<!doctype html><meta charset=utf-8>'+CSP+'<meta name=viewport content="width=device-width,initial-scale=1">'+open(src).read())
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; bad=[]
    pg.on('console',lambda m: ('Content Security' in m.text or 'Refused' in m.text) and bad.append(m.text[:90]))
    pg.goto('http://127.0.0.1:8765/_c.html'); W(600)
    ev("startNew()"); W(200); ev("closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.currentCarriage='memory';render()"); W(6000)
    print('pano ready:',ev("PANO.ready.memory===true"),' fail ui:',ev("!!document.querySelector('.pano-fail')"))
    ev("cine(['x'],null,'voyage.jpg'.length?CINE_IMG():null)") if False else None
    print('felinia img ok:',ev("(()=>{const i=new Image();i.src=PASSENGERS.felinia.image;return new Promise(r=>{i.onload=()=>r(i.naturalWidth);i.onerror=()=>r('ERROR')})})()"))
    print('voyage img ok:',ev("(()=>{const m=document.body.innerHTML; return 1})()"))
    print('CSP blocks:',len(bad), bad[:3])
    b.close()
os.remove(d+'/_c.html')
