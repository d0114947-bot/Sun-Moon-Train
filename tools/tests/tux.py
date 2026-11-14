from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(800); ev("startNew()"); W(200)
    ev("document.querySelector('#mainscreen')?.remove();closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.storyFlags.metDragon=1;state.journeyCount=2;state.currentLocation='dawnForest';state.discoveredLifeforms=['lumi','vandora'];state.passengers.vandora={stage:1,talks:1,records:[],aboard:true,left:false,boardedJourney:2};state.notes={vandora:[0,1,3]};state.currentCarriage='cab';render()"); W(1500)
    pg.screenshot(path='ux_cab.png')
    ev("state.duty.scan=true;state.spirit.contamination={value:12,level:'純淨'};state.spirit.equipment={tablet:true,compass:true,talisman:true};render()"); W(5000); pg.screenshot(path='ux_cab2.png')
    pg.click('[data-hs="cab-scan"]',force=True); W(900); pg.screenshot(path='ux_scan.png'); ev("closeAll()"); W(300)
    ev("closeAll();state.currentCarriage='habitat';render()"); W(1800); pg.screenshot(path='ux_hab.png')
    pg.click('[data-hs="hab-p-vandora"]',force=True); W(900); pg.screenshot(path='ux_dlg.png')
    ev("document.querySelectorAll('.dlg').forEach(e=>e.remove());closeAll()"); W(200)
    pg.click('#hud .nbk'); W(900); pg.screenshot(path='ux_nb.png')
    print(errs); b.close()
