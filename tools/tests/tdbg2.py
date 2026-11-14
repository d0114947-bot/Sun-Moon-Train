from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout
    pg.goto('http://127.0.0.1:8765/_t.html'); W(800); pg.click('#ms-work'); W(1200); pg.click('#ms-new'); W(500)
    ev("closeAll();state.introDone=true;state.storyFlags.noFeel=1;savePanel('game')"); W(1500)
    print(ev("(()=>{const e=document.querySelector('.svc');const c=getComputedStyle(e);return [e.parentElement.className,c.gridColumnStart,c.gridColumnEnd,c.gridRowStart,c.width, e.parentElement.parentElement.className, document.querySelectorAll('.c3-grid')[0].children.length]})()"))
    b.close()
