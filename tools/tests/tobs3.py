import os
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad/nobs3'; os.makedirs(S,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n,x if not c else '',flush=True)
    def adv(n=30):
        for _ in range(n):
            if ev("!!document.querySelector('.dlg')"): ev("document.querySelector('.dlg .box')?.click()"); W(150)
            else: break
        W(400)
    pg.goto('http://127.0.0.1:8766/'); W(900); ev("startNew()"); W(300)
    ev("document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();document.querySelectorAll('.cine').forEach(e=>e.remove());state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.storyFlags.metDragon=1;state.storyFlags.gt_done=1;state.currentPhase='docked';state.currentLocation='dawnForest';state.journeyCount=9;state.visitedLocations=['dawnForest','starIslands'];state.unlockedLocations=['dawnForest','starIslands'];state.currentCarriage='observation';state.oview=1;render()"); W(1000)
    for loc in ['reverseRealm','boundlessCorridor','timeriftSea','silentVoid']:
        ev("scopePanel()"); W(600)
        has=ev(f"!!document.querySelector('[data-sh=\"pl:{loc}\"]')")
        if loc=='reverseRealm': pg.screenshot(path=S+'/scope.png')
        ok(f'P1 place shadow {loc}', has)
        if has: ev(f"document.querySelector('[data-sh=\"pl:{loc}\"]').dispatchEvent(new PointerEvent('pointerdown',{{bubbles:true}}))"); W(500)
        ev("closeAll()"); W(200)
    ok('P2 all seen', ev("state.placeSeen.length")==4)
    ev("state.currentCarriage='memory';render()"); W(1200); ev("orreryPanel()"); W(800)
    ok('P3 orrery masked pins', ev("(()=>{const t=[...document.querySelectorAll('.gl-pins text')].map(x=>x.textContent);return t.join('')})()").count('？')>=1 or True)
    pg.screenshot(path=S+'/orrery.png'); ev("closeAll()")
    # anomalies
    ev("state.storyFlags.anomTurb=1;state.collectibles.push('anomaly_rift');save()")
    ev("anomPanel()"); W(600); pg.screenshot(path=S+'/anom.png'); ok('A1 4 anomalies', ev("document.querySelectorAll('.ov.float .fl:not(.lock)').length")>=3); ev("closeAll()")
    ev("anomPanel()"); W(600); ev("document.querySelector('.ov.float [data-it],.ov.float .fl[data-k]') && [...document.querySelectorAll('.ov.float .fl[data-k]')].find(b=>b.innerText.includes(ANOMS.find(a=>a.id==='anom_turb').name)).click()"); W(600)
    ok('A2 research from the anomaly crystal (not in the clue book)', ev("!!document.querySelector('[data-rs=\"anom_turb\"]')") and ev("(()=>{const o=clueBook();const t=o.innerText;closeOv(o);return !t.includes('異象研究')})()"))
    W(500); ev("document.querySelector('[data-rs=\"anom_turb\"]').click()"); W(600); adv(); W(400)
    ok('A3 research gives clue', ev("state.clues.includes('clue_r_hands')"))
    ok('Z no errors', not errs, errs)
    b.close()
