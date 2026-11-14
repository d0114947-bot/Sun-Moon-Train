from playwright.sync_api import sync_playwright
import sys
S='.'
cands=[(62,33,18),(57,24,17),(44,22,16)]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout
    pg.goto('http://127.0.0.1:8766/'); W(800); ev("startNew()"); W(200)
    ev("closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.journeyCount=8;state.currentLocation='dawnForest';state.discoveredLifeforms=['lumi','felinia','leviathaurora','sola','cinder','aelis','pyro','vandora','frost','sirenora','titan','lynx'];for(const id of ['felinia','leviathaurora','cinder','aelis','pyro','vandora','frost','sirenora','titan','lynx']) state.passengers[id]={stage:1,talks:1,records:[],aboard:true,left:false,boardedJourney:2};state.currentCarriage='habitat';render()"); W(1500)
    for i,(x,y,h) in enumerate(cands):
        ev(f"PASSENGERS.lynx.spot={{x:{x},y:{y}}};PASSENGERS.lynx.spriteH={h};closeAll();state.currentCarriage='habitat';render()"); W(1200)
        bad=set()
        for t in range(6):
            r=ev("""(()=>{const out=[];const sp=document.querySelector('[data-hs="hab-p-lynx"]');for(const el of document.querySelectorAll('[data-hs]')){ if(el===sp)continue; const r=el.getBoundingClientRect(); if(!r.width)continue;
             for(const [dx,dy] of [[0,0],[-6,0],[6,0],[0,-5],[0,5]]){const x=r.left+r.width/2+dx,y=r.top+r.height/2+dy; const s=sp.getBoundingClientRect(); if(x>s.left&&x<s.right&&y>s.top&&y<s.bottom&&spriteHit(sp,x,y)) {out.push(el.dataset.hs);break;}}} return out})()""")
            bad|=set(r); W(1100)
        print((x,y,h),sorted(bad),flush=True); pg.screenshot(path=f'{S}/lspot{i}.png')
    b.close()
