from playwright.sync_api import sync_playwright
import sys
S=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader'])
    for tag,vp in [('d',{'width':1280,'height':720}),('m',{'width':390,'height':844})]:
        pg=b.new_page(viewport=vp); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('http://127.0.0.1:8766/'); W(800); ev("startNew()"); W(300)
        ev("document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();document.querySelectorAll('.cine,.dlg').forEach(e=>e.remove());state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.currentPhase='docked';state.currentLocation='dawnForest';state.currentCarriage='observatory';render()"); W(1500)
        pg.screenshot(path=f'{S}/os_{tag}1.png')
        x0=vp['width']*.6; y=vp['height']*.3
        pg.mouse.move(x0,y); pg.mouse.down(); pg.mouse.move(x0-vp['width']*.5,y,steps=8); pg.mouse.up(); W(400)
        pg.screenshot(path=f'{S}/os_{tag}2.png'); print(tag,'f',ev("OSKY.f"))
        ev("state.currentLocation='starIslands';render()"); W(1200); pg.screenshot(path=f'{S}/os_{tag}3.png')
        ev("state.currentPhase='voyage';state.voyage={from:'starIslands',to:'dawnForest',progress:.5,evt:true,sky:null};render()"); W(1500); pg.screenshot(path=f'{S}/os_{tag}4.png')
        print('errs',errs); pg.close()
    b.close()
