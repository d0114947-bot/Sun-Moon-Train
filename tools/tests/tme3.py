from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout
    pg.goto('http://127.0.0.1:8766/'); W(800); ev("startNew()"); W(200)
    ev("document.querySelector('#mainscreen')?.remove();closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.currentCarriage='memory';render()"); W(1500)
    print(ev("['mem-mirror','mem-crystal','mem-save','mem-armillary'].map(i=>{const e=document.querySelector(`[data-hs=\"${i}\"]`);return [i,e&&e.outerHTML.slice(0,260)]})"))
    b.close()
