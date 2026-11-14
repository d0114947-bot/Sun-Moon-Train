from playwright.sync_api import sync_playwright
S='.'
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n,x if not c else '',flush=True)
    def face(i): ev(f"panoFace('{i}')"); W(350)
    pg.goto('http://127.0.0.1:8766/'); W(800); ev("startNew()"); W(200)
    ev("document.querySelector('#mainscreen')?.remove();closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.journeyCount=4;state.currentLocation='dawnForest';state.discoveredLifeforms=['lumi','vandora'];state.passengers.vandora={stage:2,talks:2,records:[],aboard:true,left:false,boardedJourney:2};state.currentCarriage='habitat';render()"); W(1000)
    ok('M1 no avatar in HUD', not ev("!!document.querySelector('#hud img')"))
    ev("dialogueScript([['dragon','……你醒了。'],['self','曦淵，值勤精靈前來報備。'],['dragon','嗯。']])"); W(400); pg.click('.dlg'); W(400)
    ok('M2 dialogue: no spirit art, no name tag', not ev("!!document.querySelector('.dlg .who.me, .dlg .mef, .dlg img[src*=\"spirit\"]')") and pg.inner_text('.dlg .nm').strip()=='')
    pg.click('.dlg'); W(300); pg.click('.dlg'); W(300)
    ev("dialogue('vandora',['……'],[{t:'你好',r:'嗯。'}])"); W(400); pg.click('.dlg .chs button'); W(300)
    ok('M3 reply: no name tag for the spirit', not ev("!!document.querySelector('.dlg .nm img')") and pg.inner_text('.dlg .nm').strip()==''); W(1200); pg.click('.dlg .box'); W(300); ev("closeAll()")
    for loc in ['dawnForest','starIslands']:
        ev(f"closeAll();state.currentLocation='{loc}';state.currentPhase='outside';state.companion='vandora';render()"); W(1000)
        ok(f'M4 {loc}: no spirit outside', not ev("!!document.querySelector('[data-hs^=\"out-me-\"], img[src*=\"spirit\"]')"))
    ev("closeAll();state.currentPhase='docked';state.currentLocation='dawnForest';state.companion=null;state.currentCarriage='memory';render()"); W(1800)
    face('mem-mirror')
    el=ev("(()=>{const e=document.querySelector('[data-hs=\"mem-mirror\"]'); if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2, e.innerText]})()")
    ok('M5 memory carriage has 映心鏡', el is not None and '映心鏡' in (el[2] or pg.inner_text('body')), el)
    pg.screenshot(path=S+'/me_mem.png')
    pg.mouse.click(el[0],el[1]); W(2500)
    t=pg.inner_text('.panel') if ev("!!document.querySelector('.panel')") else ''
    ok('M6 映心鏡 → mirror with taint + body only', '界染度' in t and '裝備' not in t and '足跡' not in t and ev("!!document.querySelector('.mir-glass .mir-ring')") and ev("(()=>{const i=document.querySelector('.panel .me-fig');return !!i&&i.naturalWidth>0})()"), t[:120])
    pg.screenshot(path=S+'/me_panel.png')
    pg.click('.panel .me-fig'); W(300); ok('M7 wings toggle', 'wings' in ev("document.querySelector('.panel .me-fig').src"))
    ev("TAINT.set(70)"); W(200); ok('M8 heavy taint dims spirit', ev("getComputedStyle(document.querySelector('.panel .me-fig')).filter").startswith('saturate') and '好重' in ev("spiritFeel()"))
    ok('M9 no errors', not errs, errs)
    b.close()
