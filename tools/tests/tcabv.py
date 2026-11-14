from playwright.sync_api import sync_playwright
import sys
S=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--autoplay-policy=no-user-gesture-required'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(800); ev("startNew()"); W(300)
    ev("document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();document.querySelectorAll('.cine,.dlg').forEach(e=>e.remove());state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.currentPhase='voyage';state.voyage={from:'dawnForest',to:'starIslands',progress:.3,evt:true,sky:null};state.currentCarriage='cab';render()"); W(2500)
    print(ev("(()=>{const v=document.querySelector('video.cabvid');return v?[v.readyState,v.paused,v.currentTime,v.videoWidth]:null})()"))
    pg.screenshot(path=S+'/cabv_voy.png')
    ev("closeAll();CAB.reset();render()"); W(600); print(ev("!!document.querySelector('video.cabvid')"))
    print('errs',errs); b.close()
