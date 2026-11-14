from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(800); ev("startNew()"); W(200)
    ev("document.querySelector('#mainscreen')?.remove();closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.storyFlags.metDragon=1;state.storyFlags.panoHintDone=1;state.journeyCount=2;state.currentLocation='dawnForest';state.discoveredLifeforms=['lumi','vandora'];state.passengers.vandora={stage:1,talks:1,records:[],aboard:true,left:false,boardedJourney:2};state.currentCarriage='habitat';render()"); W(1800)
    r=ev("(()=>{const e=document.querySelector('[data-hs=\"hab-p-vandora\"]');const r=e.getBoundingClientRect();return [r.left,r.top,r.width,r.height,e.style.visibility]})()"); print(r)
    x,y=r[0]+r[2]/2,r[1]+r[3]*0.4
    print('at',ev(f"(()=>{{const e=document.elementFromPoint({x},{y});return e.outerHTML.slice(0,120)}})()"), ev("[HS_SCENE(), TRANS.busy, !!document.querySelector('#layer .cine,#layer .dlg,#layer .ov:not(.closing)'), document.querySelector('#layer').innerHTML.slice(0,200)]"))
    pg.mouse.click(x,y); W(1200); print('dlg',ev("!!document.querySelector('.dlg')"), ev("document.querySelector('.dlg .dsk')&&document.querySelector('.dlg .dsk').innerText"))
    pg.screenshot(path='ux_dlg.png')
    if ev("!!document.querySelector('.dlg .dsk')"):
        pg.click('.dlg .dsk'); W(900); print('sketch panel',ev("!!document.querySelector('.ov.sketch')"))
    print(errs); b.close()
