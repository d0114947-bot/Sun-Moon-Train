from playwright.sync_api import sync_playwright
import sys
S=sys.argv[1]
IDS=['treeling','sandwyrm','moonwyrm','skyfox','grinfox','dawnsail','scythe']
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n+(' '+str(x) if x!='' else ''),flush=True)
img=lambda ev,sel: ev(f"(()=>{{const i=document.querySelector('{sel}');return !!i&&i.complete&&i.naturalWidth>0}})()")
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]; bad=[]
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: 'violates' in m.text and bad.append(m.text[:90]))
    pg.goto('http://127.0.0.1:8766/'); W(800); ev("startNew()"); W(300)
    ev("document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();document.querySelectorAll('.cine,.dlg').forEach(e=>e.remove());state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.journeyCount=14;state.currentPhase='docked';state.currentLocation='dawnForest';state.visitedLocations=['dawnForest','starIslands'];state.currentCarriage='habitat';state.boardQ=[];render()"); W(600)
    for i in IDS:
        ev(f"closeAll();document.querySelectorAll('.dlg,.cine').forEach(e=>e.remove());boarding('{i}','test line',()=>{{}})"); W(500)
        for _ in range(4):
            if ev("!!document.querySelector('.cine')"): ev("document.querySelector('.cine')?.click()"); W(400)
        W(900); ok(f'{i} boarding card', img(ev,'.ov.board .portrait img')); pg.screenshot(path=f'{S}/six_{i}_card.png')
        ev("document.querySelector('#hi')?.click()"); W(500)
        for _ in range(20):
            if not ev("!!document.querySelector('.dlg')"): break
            if ev("!!document.querySelector('.dlg .chs button')"): ev("document.querySelector('.dlg .chs button').click()"); W(900)
            else: ev("(document.querySelector('.dlg .box')||document.querySelector('.dlg')).click()"); W(150)
        ok(f'{i} aboard', ev(f"aboard('{i}')"))
    ev("closeAll();state.currentCarriage='habitat';state.hview=0;render()"); W(2000)
    ok('all seven shown', all(img(ev,f'[data-hs="hab-p-{i}"] img') for i in IDS), [i for i in IDS if not img(ev,f'[data-hs="hab-p-{i}"] img')])
    pg.screenshot(path=f'{S}/six_hab.png')
    cov=ev("""(()=>{const out=[];for(const el of document.querySelectorAll('[data-hs]')){ if(el.dataset.hs.startsWith('hab-p-'))continue; if(el.style.visibility==='hidden')continue; const r=el.getBoundingClientRect(); if(!r.width)continue; const x=r.left+r.width/2,y=r.top+r.height/2; if(x<0||x>innerWidth||y<0||y>innerHeight)continue; const t=document.elementFromPoint(x,y); const h=t&&t.closest('[data-hs]'); if(h&&h!==el&&h.dataset.hs.startsWith('hab-p-')&&spriteHit(h,x,y)) out.push(el.dataset.hs+'->'+h.dataset.hs);} return out})()""")
    ok('no hotspot covered', not cov, cov)
    for i in IDS:
        ev(f"closeAll();state.filed=state.filed||{{}};openBook('life','{i}')"); W(1300); pg.screenshot(path=f'{S}/six_{i}_book.png')
        ok(f'{i} codex', img(ev,'.plate.big img') and PASS if False else img(ev,'.plate.big img'))
    ok('no errors', not errs and not bad, (errs,bad))
    b.close()
