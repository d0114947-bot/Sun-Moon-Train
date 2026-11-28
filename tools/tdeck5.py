# 展望台超過四位乘客（使用者回報：Cannot read properties of undefined (reading 'x') at hsBtn）
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad'
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
BASE=open(S+'/tchap.py').read().split('BASE="')[1].split('"\n')[0]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(1000)
    ids=['sola','felinia','cinder','aelis','porcel','husk']
    ev(BASE+"".join(f"state.passengers['{i}']={{stage:2,talks:3,records:[],aboard:true,left:false,boardedJourney:1,zone:PASSENGERS['{i}'].zone,place:'deck'}};state.discoveredLifeforms.push('{i}');" for i in ids)+"state.currentPhase='docked';state.currentCarriage='observation';state.oview=0;save();PANO.active=null;RUNNING=true;render()"); W(1200)
    ok('D1 six on the deck (old save): no error, page draws', not errs and ev("!!document.querySelector('#scene')"), errs[:2])
    ok('D2 at most four stay on the deck; the rest go back', ev("deckList().length")<=4 and ev("Object.values(state.passengers).filter(s=>s.place==='deck').length")<=4)
    ev("state.passengers.husk.place='deck';state.passengers.porcel.place='deck';deckSlot('husk');document.querySelectorAll('[data-hs^=\"ot-p-\"]').length"); 
    ok('D3 deckSlot never undefined', ev("['sola','felinia','cinder','aelis','porcel','husk'].every(i=>!!deckSlot(i))"))
    ev("render()"); W(500)
    ok('Z no page errors', not errs, errs[:3])
    b.close()
