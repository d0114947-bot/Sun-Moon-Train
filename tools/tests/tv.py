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
    ev("closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.journeyCount=4;state.currentLocation='starIslands';state.visitedLocations=['dawnForest','starIslands'];state.completedEvents=['voyage_symbol','board_lumi','board_felinia','board_leviathaurora','board_sola','board_cinder','board_aelis','board_pyro'];state.discoveredLifeforms=['lumi','felinia','leviathaurora','sola','cinder','aelis','pyro'];"
       "for(const id of ['felinia','leviathaurora','cinder','aelis','pyro']) state.passengers[id]={stage:1,talks:1,records:[],aboard:true,left:false,boardedJourney:2};"
       "state.duty={scan:true,briefing:true,signal:true,doors:true,reported:true};state.spirit.equipment={tablet:true,compass:true,talisman:true};state.currentCarriage='cab';render();startDeparture()"); W(500)
    for _ in range(10):
        if not ev("!!document.querySelector('.cine')"): break
        pg.mouse.click(640,360); W(300)
    ev("state.voyage.progress=.78"); W(1500)
    for _ in range(12):
        if ev("!!document.querySelector('.cine')") and '苔葉' in pg.inner_text('.cine'): break
        if ev("!!document.querySelector('.cine')"): pg.mouse.click(640,360)
        W(600)
    ok('P1 voyage to 晨曦森林 → boarding cine', ev("state.voyage&&state.voyage.to")=='dawnForest' and '苔葉' in pg.inner_text('.cine'))
    pg.mouse.click(640,360); W(1600); ok('A2 boarding card portrait', img(ev,'.ov.board .portrait img')); pg.screenshot(path=S+'/v_board.png')
    pg.click('#hi'); W(500); drain(pg,ev,W)
    ok('P3 record says boarded during voyage', '航行途中' in ev("state.passengers.vandora.records[0].t"))
    ev("closeAll();state.currentCarriage='habitat';render()"); W(1800)
    ok('P4 six animated passengers shown', all(img(ev,f'[data-hs="hab-p-{i}"] img') for i in ['vandora','pyro','aelis','cinder','felinia','leviathaurora']))
    pg.screenshot(path=S+'/v_hab.png')
    body=ev("""(()=>{const sp=document.querySelector('[data-hs="hab-p-vandora"]');const r=sp.querySelector('img').getBoundingClientRect();
      for(let y=r.top+r.height*.35;y<r.bottom;y+=5) for(let x=r.left+r.width*.3;x<r.right;x+=5){ if(spriteHit(sp,x,y)&&document.elementFromPoint(x,y).closest('[data-hs]')===sp) return [x,y]; } return null})()""")
    pg.mouse.click(body[0],body[1]); W(700); ok('A5 click → dialogue with portrait', img(ev,'.dlg .who img')); pg.screenshot(path=S+'/v_dlg.png'); drain(pg,ev,W)
    ev("openBook('life','vandora')"); W(1500); ok('A6 codex detail', img(ev,'.plate.big img') and img(ev,'.studies img') and '虹彩折射與觸鬚感應' in pg.inner_text('.spread') and '雨林翡翠' in pg.inner_text('.spread')); pg.screenshot(path=S+'/v_book.png'); ev("closeAll()")
    ok('P7 codex 9 entries, 8 known', ev("CODEX_LIFE.length")==9 and ev("CODEX_LIFE.map(codexEntry).filter(e=>e.known).length")==8)
    ok('A8 no blocked resources / errors', not bad and not errs, (bad,errs))
    b.close()
os.remove(d+'/_c.html')
