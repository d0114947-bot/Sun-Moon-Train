from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout
    pg.goto('http://127.0.0.1:8766/'); W(800); ev("startNew()"); W(200)
    ev("document.querySelector('#mainscreen')?.remove();closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.currentCarriage='cab';render()"); W(800)
    ev("dialogueScript([['dragon','……你醒了。'],['self','領頭，值勤精靈前來報備。'],['dragon','嗯。']])"); W(1500)
    print(ev("[...document.querySelectorAll('.dlg .who')].map(e=>{const r=e.getBoundingClientRect();const i=e.querySelector('img,svg');return [e.className,Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height),getComputedStyle(e).opacity,i&&i.tagName,i&&i.naturalWidth]})"))
    pg.screenshot(path='me_d1.png'); pg.click('.dlg'); W(1500); pg.screenshot(path='me_d2.png')
    print(ev("[...document.querySelectorAll('.dlg .who')].map(e=>{const r=e.getBoundingClientRect();return [e.className,Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]})"))
    b.close()
