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
    ev("Math.random=()=>0.99;closeAll();state.introDone=true;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.journeyCount=8;state.currentLocation='dawnForest';state.visitedLocations=['dawnForest','starIslands'];state.completedEvents=['voyage_symbol','board_lumi','board_felinia','board_leviathaurora','board_sola','board_cinder','board_aelis','board_pyro','board_vandora','board_frost','board_sirenora','board_titan'];state.discoveredLifeforms=['lumi','felinia','leviathaurora','sola','cinder','aelis','pyro','vandora','frost','sirenora','titan'];"
       "for(const id of ['felinia','leviathaurora','cinder','aelis','pyro','vandora','frost','sirenora','titan']) state.passengers[id]={stage:1,talks:1,records:[],aboard:true,left:false,boardedJourney:2};"
       "state.duty={scan:true,briefing:true,signal:true,doors:true,reported:true};state.spirit.equipment={tablet:true,compass:true,talisman:true};state.currentCarriage='cab';render();startDeparture();state.voyage.sky=null"); W(500)
    for _ in range(10):
        if not ev("!!document.querySelector('.cine')"): break
        pg.mouse.click(640,360); W(300)
    ev("state.voyage.progress=.45"); W(1500)
    for _ in range(50):
        if ev("!!document.querySelector('.cine')") and '銀白的影子' in pg.inner_text('.cine'): break
        if ev("!!document.querySelector('.cine')"): pg.mouse.click(640,360)
        elif ev("!!document.querySelector('.dlg')"): pg.click('.dlg .box')
        W(500)
    W(1500); ok('P1 voyage to 星河浮島 → lynx boarding cine', ev("state.voyage&&state.voyage.to")=='starIslands' and '銀白的影子' in (pg.inner_text('.cine') if ev("!!document.querySelector('.cine')") else ''))
    pg.mouse.click(640,360); W(1600); ok('A2 boarding card portrait', img(ev,'.ov.board .portrait img')); pg.screenshot(path=S+'/ly_board.png')
    pg.click('#hi'); W(500); drain(pg,ev,W)
    ok('P3 lynx aboard & discovered', ev("aboard('lynx')&&done('board_lynx')&&state.discoveredLifeforms.includes('lynx')"))
    ev("closeAll();state.currentCarriage='habitat';render()"); W(1800)
    ok('P4 ten animated passengers shown', all(img(ev,f'[data-hs="hab-p-{i}"] img') for i in ['lynx','titan','sirenora','frost','vandora','pyro','aelis','cinder','felinia','leviathaurora']))
    pg.screenshot(path=S+'/ly_hab.png')
    cov=ev("""(()=>{const out=[];for(const el of document.querySelectorAll('[data-hs]')){ if(el.dataset.hs.startsWith('hab-p-'))continue; if(el.style.visibility==='hidden')continue; const r=el.getBoundingClientRect(); if(!r.width)continue; const x=r.left+r.width/2,y=r.top+r.height/2; if(x<0||x>innerWidth||y<0||y>innerHeight)continue; const t=document.elementFromPoint(x,y); const h=t&&t.closest('[data-hs]'); if(h!==el&&!(h&&h.classList.contains('sprite')&&!spriteHit(h,x,y))) out.push(el.dataset.hs+'->'+(h?h.dataset.hs:t&&t.tagName)); } return out})()""")
    ok('F9 no hotspot covered', not cov, cov)
    for _try in range(8):
        body=ev("""(()=>{const sp=document.querySelector('[data-hs="hab-p-lynx"]');const r=sp.querySelector('img').getBoundingClientRect();const H=[];
          for(let y=r.top+r.height*.35;y<r.bottom;y+=5) for(let x=r.left+r.width*.3;x<r.right;x+=5){ if(spriteHit(sp,x,y)&&document.elementFromPoint(x,y).closest('[data-hs]')===sp) H.push([x,y]); } return H.length?H[H.length>>1]:null})()""")
        if body: pg.mouse.click(body[0],body[1]); W(700)
        if ev("!!document.querySelector('.dlg')"): break
        print('retry',body)
    ok('A5 click → dialogue with portrait', img(ev,'.dlg .who img')); pg.screenshot(path=S+'/ly_dlg.png'); drain(pg,ev,W)
    ev("state.filed=state.filed||{};state.filed.lynx={habitat:0,habits:1,abilities:4,bio:6};state.sketches={lynx:[0,1]};openBook('life','lynx')"); W(1500); ok('A6 codex detail', img(ev,'.plate.big img') and img(ev,'.studies img') and '踏雪無痕' in pg.inner_text('.spread') and '極地奇幻獸類' in pg.inner_text('.spread') and '冰脊靈貓' in pg.inner_text('.spread')); pg.screenshot(path=S+'/ly_book.png'); ev("closeAll()")
    ok('P7 codex 14 entries, 12 known', ev("CODEX_LIFE.length")==14 and ev("CODEX_LIFE.map(codexEntry).filter(e=>e.known).length")==12)
    ok('A8 no blocked resources / errors', not bad and not errs, (bad,errs))
    b.close()

