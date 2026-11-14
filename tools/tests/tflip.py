from playwright.sync_api import sync_playwright
import sys
S=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    for tag,vp in [('d',{'width':1280,'height':720}),('m',{'width':390,'height':780})]:
        pg=b.new_page(viewport=vp); ev=pg.evaluate; W=pg.wait_for_timeout
        pg.goto('http://127.0.0.1:8765/_t.html'); W(800)
        pg.click('#ms-work'); W(1200); pg.click('#ms-new'); W(500)
        ev("closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.currentPhase='docked';state.currentCarriage='memory';render();openBook('lore')"); W(1200)
        bx=ev("(()=>{const r=document.querySelector('.jr-pages').getBoundingClientRect();return [r.left,r.top,r.width,r.height]})()")
        x0=bx[0]+bx[2]*.85; y=bx[1]+bx[3]*.5
        pg.mouse.move(x0,y); pg.mouse.down()
        for k in range(1,6):
            pg.mouse.move(x0-k*bx[2]*.14,y,steps=4); W(60); pg.screenshot(path=f'{S}/fl_{tag}_{k}.png')
        pg.mouse.up()
        for k,t in enumerate([300,600,900,1000,1150]):
            W(t if k==0 else t-[300,600,900,1000,1150][k-1]); pg.screenshot(path=f'{S}/fl_{tag}_r{k}.png')
        pg.close()
    b.close()
