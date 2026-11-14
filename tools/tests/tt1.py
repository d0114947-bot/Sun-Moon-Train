from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout
    pg.goto('http://127.0.0.1:8765/'); W(800); ev("startNew()"); W(200)
    ev("document.querySelector('#mainscreen')?.remove();closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.currentPhase='docked';state.voyage=null;state.currentLocation='dawnForest';state.currentCarriage='observatory';render()"); W(600)
    print(ev("[CARRIAGES.observatory.image.slice(0,40), !!document.querySelector('#scene img.bg'), !!document.querySelector('#streaks'), document.querySelector('#scene').innerHTML.slice(0,200)]"))
    b.close()
