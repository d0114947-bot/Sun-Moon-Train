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
    ev("Math.random=()=>0.99;closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.journeyCount=6;state.currentLocation='starIslands';state.visitedLocations=['dawnForest','starIslands'];state.completedEvents=['voyage_symbol','board_lumi','board_felinia','board_leviathaurora','board_sola','board_cinder','board_aelis','board_pyro','board_vandora','board_frost'];state.discoveredLifeforms=['lumi','felinia','leviathaurora','sola','cinder','aelis','pyro','vandora','frost'];"
       "for(const id of ['felinia','leviathaurora','cinder','aelis','pyro','vandora','frost']) state.passengers[id]={stage:1,talks:1,records:[],aboard:true,left:false,boardedJourney:2};"
       "state.duty={scan:true,briefing:true,signal:true,doors:true,reported:true};state.spirit.equipment={tablet:true,compass:true,talisman:true};state.currentCarriage='cab';render();startDeparture();state.voyage.sky=null"); W(500)
    for _ in range(10):
        if not ev("!!document.querySelector('.cine')"): break
        pg.mouse.click(640,360); W(300)
    ev("rollBoarders=()=>['board_sirenora'];state.voyage.progress=.99;(function w(){ if(document.querySelector('#layer .dlg,#layer .cine')) return setTimeout(w,200); if(state.voyage) voyageArrive(); })()"); W(400)
    W(2500)
    print(ev("(()=>{const b=document.querySelector('.dlg .box');if(!b)return 'nobox';const r=b.getBoundingClientRect();const e=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return [e&&(e.id+'.'+e.className+'<'+e.parentElement.className),document.querySelectorAll('.dlg').length,[...document.querySelectorAll('#layer>*')].map(x=>x.className)]})()"))
    pg.screenshot(path='srs_dbg.png'); b.close()
