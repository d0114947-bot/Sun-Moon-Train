from playwright.sync_api import sync_playwright
import sys,os
S=sys.argv[1]; d='/home/claude/game'
CSP='<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; script-src \'unsafe-inline\'; style-src \'unsafe-inline\' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src data: blob:; media-src data: blob:">'
open(d+'/_c.html','w').write('<!doctype html><meta charset=utf-8>'+CSP+'<meta name=viewport content="width=device-width,initial-scale=1">'+open(d+'/index.html').read())
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
    pg.goto('http://127.0.0.1:8765/_c.html'); W(800); ev("startNew()"); W(200)
    ev("closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.journeyCount=2;state.currentLocation='starIslands';state.visitedLocations=['dawnForest','starIslands'];state.completedEvents=['voyage_symbol','board_lumi','board_felinia','board_leviathaurora','board_sola'];state.discoveredLifeforms=['lumi','felinia','leviathaurora','sola'];"
       "for(const id of ['felinia','leviathaurora']) state.passengers[id]={stage:1,talks:1,records:[],aboard:true,left:false,boardedJourney:2};"
       "state.duty={scan:true,briefing:true,signal:true,doors:true,reported:true};state.spirit.equipment={tablet:true,compass:true,talisman:true};state.currentCarriage='cab';render();startDeparture()"); W(500)
    while ev("!!document.querySelector('.cine')"): pg.click('.cine'); W(300)
    ok('D0 third voyage heads to 晨曦森林', ev("state.voyage.to")=='dawnForest')
    ev("state.voyage.progress=.5"); W(1000)
    for _ in range(20):
        if ev("!!document.querySelector('.cine')"): break
        W(300)
    ok('D1 boarding cine', ev("!!document.querySelector('.cine')") and '帆影' in pg.inner_text('.cine'))
    pg.click('.cine'); W(1600); ok('D2 boarding card portrait', img(ev,'.ov.board .portrait img')); pg.screenshot(path=S+'/d_board.png')
    pg.click('#hi'); W(500); drain(pg,ev,W)
    ev("state.currentCarriage='habitat';render()"); W(1800)
    ok('D3 three animated passengers shown', all(img(ev,f'[data-hs="hab-p-{i}"] img') for i in ['cinder','felinia','leviathaurora']))
    ok('D4 crystal platform powered', '供能中' in ev("(zoneInfo('crystal'),document.querySelector('#layer').innerText)")); ev("closeAll()"); W(300)
    pg.screenshot(path=S+'/d_hab.png')
    # click-through: find a transparent point inside the cinder box that sits on another hotspot
    pt=ev("""(()=>{const sp=document.querySelector('[data-hs="hab-p-cinder"]');
      for(const id of ['hab-veil','hab-crystal']){ const m=document.querySelector(`[data-hs="${id}"] .mk`); if(!m) continue; const r=m.getBoundingClientRect(); const x=r.left+r.width/2,y=r.top+r.height/2;
        const top=document.elementFromPoint(x,y).closest('[data-hs]'); if(top===sp && !spriteHit(sp,x,y)) return [id,x,y]; }
      return null})()""")
    print('click-through point',pt)
    if pt:
        pg.mouse.click(pt[1],pt[2]); W(500); ok('D5 transparent area passes click to zone below', '棲息車廂' in pg.inner_text('#layer') and ev("!document.querySelector('.dlg')")); ev("closeAll()"); W(300)
    body=ev("""(()=>{const sp=document.querySelector('[data-hs="hab-p-cinder"]');const r=sp.querySelector('img').getBoundingClientRect();
      for(let y=r.top+r.height*.3;y<r.bottom;y+=6) for(let x=r.left;x<r.right;x+=6){ if(spriteHit(sp,x,y)&&document.elementFromPoint(x,y).closest('[data-hs]')===sp) return [x,y]; } return null})()""")
    pg.mouse.click(body[0],body[1]); W(700); ok('D6 clicking the creature opens dialogue', img(ev,'.dlg .who img')); pg.screenshot(path=S+'/d_dlg.png'); drain(pg,ev,W)
    ev("openBook('life','cinder')"); W(1500); ok('D7 codex: still, studies, name origin, notes', img(ev,'.plate.big img') and img(ev,'.studies img') and '名稱由來' in pg.inner_text('.spread') and '太陽能航行' in pg.inner_text('.spread')); pg.screenshot(path=S+'/d_book.png')
    ev("document.querySelector('.spread .page.r').scrollTop=520"); W(300); pg.screenshot(path=S+'/d_book2.png'); ev("closeAll()")
    ok('D8 no blocked resources / errors', not bad and not errs, (bad,errs))
    b.close()
os.remove(d+'/_c.html')
