from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad'
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n+(' '+str(x) if x!='' else ''),flush=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(900)
    ok('C0 every passenger has care needs', ev("Object.keys(PASSENGERS).every(id=>CARE[id]&&careWant(id).length===2)"))
    ids=['frost','pyro','cinder','sirenora','felinia','leviathaurora']
    ev("document.querySelector('#mainscreen')?.remove();RUNNING=true;state=freshState();normalizeState();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.storyFlags.metDragon=1;state.storyFlags.noteTip=1;state.currentPhase='docked';state.currentLocation='dawnForest';state.journeyCount=3;state.visitedLocations=['dawnForest'];"
       f"state.discoveredLifeforms={ids};for(const id of {ids}) state.passengers[id]={{stage:1,talks:id==='frost'?2:0,records:[],aboard:true,left:false,boardedJourney:2,zone:PASSENGERS[id].zone}};state.currentCarriage='habitat';render()"); W(800)
    def drain():
        for _ in range(30):
            if not ev("!!document.querySelector('.dlg')"): return
            if ev("!!document.querySelector('.dlg .chs button')"): pg.locator('.dlg .chs button').first.click(); W(1100)
            else: pg.locator('.dlg .box').last.click(); W(160)
    ev("talk('frost')"); W(400); t=pg.locator('.dlg .tx').last.inner_text(); pg.locator('.dlg .box').last.click(); W(200); t2=pg.locator('.dlg .tx').last.inner_text(); drain()
    ok('C1 last story held back until comfortable', '不太自在' in t and ev("state.passengers.frost.talks")==2, t)
    ok('C2 reaction hints the direction', '太熱' in t2, t2)
    c=ev("(()=>{const r=document.querySelector('[data-hs=\"hab-crystal\"]').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()"); pg.mouse.click(c[0],c[1]); W(800)
    print('DBG',c,ev("(()=>{const e=document.querySelector('[data-hs=\"hab-crystal\"]');return e?e.outerHTML.slice(0,200)+JSON.stringify(e.getBoundingClientRect()):'none'})()"),ev('PANO.raf+" "+PANO.active+" "+PANO.list.length'),ev(f"(()=>{{const t=document.elementFromPoint({c[0]},{c[1]});return t&&t.outerHTML.slice(0,100)}})()"),ev("document.querySelector('#layer').innerText.slice(0,200)"))
    ok('C3 zone panel: dials + passengers here + ask others', ev("document.querySelectorAll('.care-dials .dial').length")==3 and ev("document.querySelectorAll('.zlist li').length")==3 and ev("document.querySelectorAll('[data-ask]').length")>=3)
    pg.click('[data-dk="t"][data-dv="3"]'); W(500)
    ok('C4 one zone setting serves everyone there (炎熱 → cinder & pyro comfortable)', ev("careOk('cinder')&&careOk('pyro')") and not ev("careOk('frost')"))
    pg.screenshot(path=S+'/zone1.png')
    # frost needs 寒冷+明亮: set rings to that, then ask frost to come
    pg.click('[data-z="rings"]'); W(300); pg.click('[data-dk="t"][data-dv="0"]'); W(300); pg.click('[data-dk="l"][data-dv="2"]'); W(600)
    ok('C5 auto passenger leaves a zone that no longer suits it (felinia)', ev("zoneOf('felinia')")!='rings', ev("zoneOf('felinia')"))
    pg.click('[data-z="spring"]'); W(300); pg.click('[data-ask="pyro"]'); W(500)
    ok('C6 asking an unsuitable passenger: polite no with a reason', ev("zoneOf('pyro')")=='crystal' and ('太' in pg.inner_text('.ask-bubble') or '擠' in pg.inner_text('.ask-bubble')), repr(pg.inner_text('.ask-bubble')))
    pg.click('[data-z="rings"]'); W(300); pg.click('[data-ask="frost"]'); W(2000)
    ok('C7 asking a suitable passenger: it moves and is comfortable', ev("zoneOf('frost')")=='rings' and ev("careOk('frost')") and ev("state.passengers.frost.stage")==2)
    ev("closeAll()"); W(400)
    pos=ev("(()=>{const r=document.querySelector('[data-hs=\"hab-p-frost\"]').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()")
    ok('C8 the sprite really moved to the rings', pos[1]<330, pos)
    pg.screenshot(path=S+'/zone2.png')
    ev("talk('frost')"); W(400); first=pg.locator('.dlg .tx').last.inner_text(); drain()
    ok('C9 comfortable → tells the last story', '獵人說' in first and ev("state.passengers.frost.talks")==3, first)
    ok('C10 guest seat limit: zone hosts at most one guest', ev("Object.keys(ZONES).every(z=>guestIn(z).length<=1)"))
    ok('C11 🌡️ outside the habitat → hint only', (ev("closeAll();state.currentCarriage='cab';render()") or True) and (pg.click('[data-act="care:open"]') or True) and not ev("!!document.querySelector('.ov.care')"))
    ok('C12 no errors', not errs, errs)
    b.close()
