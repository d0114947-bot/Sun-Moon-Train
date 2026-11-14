from playwright.sync_api import sync_playwright
import json,sys
COV="""(()=>{const out=[];const W=innerWidth,H=innerHeight;for(const el of document.querySelectorAll('#scene [data-hs]')){ if(el.dataset.hs.startsWith('hab-p-'))continue; if(el.style.visibility==='hidden')continue; const r=el.getBoundingClientRect(); if(!r.width)continue; const x=r.left+r.width/2,y=r.top+r.height/2; if(x<0||x>W||y<0||y>H) continue; const t=document.elementFromPoint(x,y); const h=t&&t.closest('[data-hs]'); if(h!==el&&!(h&&h.classList.contains('sprite')&&!spriteHit(h,x,y))) out.push(el.dataset.hs+'->'+(h?h.dataset.hs:t&&t.tagName)); } return out})()"""
LB="""(()=>{const out=[];for(const el of document.querySelectorAll('#scene [data-hs^="hab-p-"]')){ if(el.style.visibility==='hidden')continue; const lb=el.querySelector('.lb'); const r=lb.getBoundingClientRect(); const x=r.left+r.width/2,y=r.top+r.height/2; if(x<0||x>innerWidth||y>innerHeight) {out.push(el.dataset.hs+' label offscreen');continue;} const t=document.elementFromPoint(x,y); if(!t||!el.contains(t)) out.push(el.dataset.hs+' label under '+(t&&t.closest('[data-hs]')?t.closest('[data-hs]').dataset.hs:t&&t.tagName)); } return out})()"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    vp=json.loads(sys.argv[1]) if len(sys.argv)>1 else {'width':1280,'height':720}
    pg=b.new_page(viewport=vp); ev=pg.evaluate; W=pg.wait_for_timeout
    pg.goto('http://127.0.0.1:8766/'); W(800); ev("startNew()"); W(200)
    ids=['lumi','sola','felinia','leviathaurora','cinder','aelis','pyro','vandora','frost','sirenora','titan','lynx','strider']
    ev("document.querySelector('#mainscreen')?.remove();closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.journeyCount=9;state.currentLocation='dawnForest';state.storyFlags.panoHintDone=1;state.discoveredLifeforms=%s;for(const id of %s) state.passengers[id]={stage:1,talks:1,records:[],aboard:true,left:false,boardedJourney:2};state.currentCarriage='habitat';render()"%(ids,ids)); W(2500)
    rng=ev("[panoClamp(0),panoClamp(359)]"); lons=sorted(set([rng[0],180,rng[1]]))
    for lon in lons:
        ev(f"PANO.tLon=PANO.lon={lon};PANO.need=true"); W(600)
        print(round(lon),'cover',ev(COV),'labels',ev(LB))
    pg.screenshot(path='cov.png')
    b.close()
