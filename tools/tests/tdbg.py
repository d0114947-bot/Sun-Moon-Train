from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout
    pg.goto('http://127.0.0.1:8765/_t.html'); W(800); pg.click('#ms-work'); W(1200); pg.click('#ms-new'); W(500)
    ev("closeAll();state.introDone=true;state.storyFlags.noFeel=1;savePanel('game')"); W(800)
    W(1500); pg.screenshot(path='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad/dbg_save.png'); print(ev("[...document.querySelectorAll('.svc')].slice(0,4).map(e=>{const r=e.getBoundingClientRect();return [Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height),getComputedStyle(e).position,getComputedStyle(e).animationName]})")); print(ev("(()=>{const g=document.querySelector('.sv3 .c3-grid'),st=document.querySelector('.sv3 .c3-stage'),pn=document.querySelector('.savep .panel');const c=getComputedStyle(g);return [[...document.querySelectorAll('.sv3 .c3-face')].map(f=>f.style.transform+'|'+f.className).join(' ; '),c.display,c.gridTemplateColumns,g.style.cssText,st.getBoundingClientRect().width,st.getBoundingClientRect().height,pn.getBoundingClientRect().width,getComputedStyle(pn).display]})()"))
    b.close()
