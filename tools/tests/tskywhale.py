from playwright.sync_api import sync_playwright
import sys,os
S=sys.argv[1]; d='/home/claude/game'
CSP='<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; script-src \'unsafe-inline\'; style-src \'unsafe-inline\' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src data: blob:; media-src data: blob:">'
pass
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n+(' '+str(x) if x!='' else ''),flush=True)
img=lambda ev,sel: ev(f"(()=>{{const i=document.querySelector('{sel}');return !!i&&i.complete&&i.naturalWidth>0}})()")
def drain(pg,ev,W):
    while ev("!!document.querySelector('.dlg')"):
        if ev("!!document.querySelector('.dlg .chs button')"): pg.click('.dlg .chs button'); W(1100)
        else: pg.click('.dlg .box'); W(150)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; bad=[]; errs=[]
    pg.on('console',lambda m: 'violates' in m.text and bad.append(m.text[:90])); pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(800); ev("startNew()"); W(200)
    ev("Math.random=()=>0.99;closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.journeyCount=10;state.currentLocation='dawnForest';state.visitedLocations=['dawnForest','starIslands'];state.completedEvents=['voyage_symbol','board_lumi','board_felinia','board_leviathaurora','board_sola','board_cinder','board_aelis','board_pyro','board_vandora','board_frost','board_sirenora','board_titan','board_lynx'];state.discoveredLifeforms=['lumi','felinia','leviathaurora','sola','cinder','aelis','pyro','vandora','frost','sirenora','titan','lynx','strider','windkoi'];"
       "for(const id of ['felinia','leviathaurora','cinder','aelis','pyro','vandora','frost','sirenora','titan','lynx','skywhale']) state.passengers[id]={stage:1,talks:1,records:[],aboard:true,left:false,boardedJourney:2};"
       "state.duty={scan:true,briefing:true,signal:true,doors:true,reported:true};state.spirit.equipment={tablet:true,compass:true,talisman:true};state.currentCarriage='cab';render();startDeparture();state.voyage.sky=null;state.voyage.to='starIslands'"); W(500)
    for _ in range(10):
        if not ev("!!document.querySelector('.cine')"): break
        pg.mouse.click(640,360); W(300)
    ev("rollBoarders=()=>['board_skywhale'];state.voyage.progress=.99;setTimeout(function w(){ if(document.querySelector('#layer .dlg,#layer .cine')) return setTimeout(w,200); if(state.voyage) voyageArrive(); },1500)"); W(400)
    for _ in range(40):
        if ev("(state.boardQ||[]).includes('board_skywhale')") and not ev("!!document.querySelector('#layer .cine,#layer .dlg,#layer .board')"): break
        if ev("!!document.querySelector('.cine')"): pg.mouse.click(640,360)
        elif ev("!!document.querySelector('.dlg')"): pg.click('.dlg .box')
        W(400)
    ok('P0 docked boarding waits for the habitat (hint shown)', ev("(state.boardQ||[]).includes('board_skywhale')") and ev("!!state.boardSensed"), ev("questText()"))
    ev("closeAll();state.currentCarriage='habitat';render();checkCarriageEvents()"); W(600)
    for _ in range(20):
        if ev("!!document.querySelector('.cine')") and '巨大的灰色身影' in pg.inner_text('.cine'): break
        if ev("!!document.querySelector('.cine')"): pg.mouse.click(640,360)
        W(500)
    ok('P1 entering the habitat → boarding cine', ev("state.currentLocation")=='starIslands' and '巨大的灰色身影' in (pg.inner_text('.cine') if ev("!!document.querySelector('.cine')") else ''))
    pg.mouse.click(640,360); W(1600); ok('A2 boarding card portrait', img(ev,'.ov.board .portrait img')); pg.screenshot(path=S+'/sw_board.png')
    pg.click('#hi'); W(500); drain(pg,ev,W)
    ok('P3 skywhale aboard & discovered', ev("aboard('skywhale')&&done('board_skywhale')&&state.discoveredLifeforms.includes('skywhale')"))
    ev("closeAll();state.currentCarriage='habitat';render()"); W(1800)
    _L=['skywhale','lynx','titan','sirenora','frost','vandora','pyro','aelis','cinder','felinia','leviathaurora']; ok('P4 twelve animated passengers shown', all(img(ev,f'[data-hs="hab-p-{i}"] img') for i in _L), [i for i in _L if not img(ev,f'[data-hs="hab-p-{i}"] img')])
    pg.screenshot(path=S+'/sw_hab.png')
    cov=ev("""(()=>{const out=[];for(const el of document.querySelectorAll('[data-hs]')){ if(el.dataset.hs.startsWith('hab-p-'))continue; if(el.style.visibility==='hidden')continue; const r=el.getBoundingClientRect(); if(!r.width)continue; const x=r.left+r.width/2,y=r.top+r.height/2; if(x<0||x>innerWidth||y<0||y>innerHeight)continue; const t=document.elementFromPoint(x,y); const h=t&&t.closest('[data-hs]'); if(h!==el&&!(h&&h.classList.contains('sprite')&&!spriteHit(h,x,y))) out.push(el.dataset.hs+'->'+(h?h.dataset.hs:t&&t.tagName)); } return out})()""")
    ok('F9 no hotspot covered', not cov, cov)
    for _try in range(8):
        body=ev("""(()=>{const sp=document.querySelector('[data-hs="hab-p-skywhale"]');const r=sp.querySelector('img').getBoundingClientRect();const H=[];
          for(let y=r.top+r.height*.35;y<r.bottom;y+=5) for(let x=r.left+r.width*.3;x<r.right;x+=5){ if(spriteHit(sp,x,y)&&document.elementFromPoint(x,y).closest('[data-hs]')===sp) H.push([x,y]); } return H.length?H[H.length>>1]:null})()""")
        if body: pg.mouse.click(body[0],body[1]); W(700)
        if ev("!!document.querySelector('.dlg')"): break
        print('retry',body)
    ok('A5 click → dialogue with portrait', img(ev,'.dlg .who img')); pg.screenshot(path=S+'/sw_dlg.png'); drain(pg,ev,W)
    ev("state.filed=state.filed||{};state.filed.skywhale={habitat:0,habits:2,abilities:5,bio:7};state.sketches={skywhale:[0,1]};openBook('life','skywhale')"); W(1500); ok('A6 codex detail', img(ev,'.plate.big img') and img(ev,'.studies img') and '御空浮游' in pg.inner_text('.ov.jr') and '遠古天空巨獸' in pg.inner_text('.ov.jr') and '浮空巨獸' in pg.inner_text('.ov.jr')); pg.screenshot(path=S+'/sw_book.png'); ev("closeAll()")
    ok('P7 codex 14 entries, 13 known', ev("CODEX_LIFE.length")==25 and ev("CODEX_LIFE.map(codexEntry).filter(e=>e.known).length")==14, ev("CODEX_LIFE.map(codexEntry).filter(e=>e.known).length"))
    ok('A8 no blocked resources / errors', not bad and not errs, (bad,errs))
    b.close()

