# 章節決定卡片的插圖（第 1～7 章）
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad'
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
BASE=open(S+'/tchap.py').read().split('BASE="')[1].split('"\n')[0]
HERO={1:'treeling',2:'skywhale',3:'sirenora',4:'titan',5:'grinfox',6:'mnemo',7:'yixi'}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(1000)
    for n,h in HERO.items():
        ev(BASE+f"state.discoveredLifeforms.push('{h}');state.passengers['{h}']={{stage:2,talks:3,records:[],aboard:true,left:false,boardedJourney:2,zone:PASSENGERS['{h}'].zone}};state.currentPhase='voyage';state.voyage={{from:'dawnForest',to:'starIslands',progress:.3,evt:true}};save();PANO.active=null;RUNNING=true;render()"); W(400)
        ev(f"closeAll();decideNow('ch{n}')"); W(1500)
        r=ev("[...document.querySelectorAll('.dec-card')].map(c=>{const i=c.querySelector('.dc-art img');return [c.dataset.dec,i?(i.naturalWidth>0):null]})")
        want={7:2}.get(n,3)
        ok(f'C{n} chapter {n}: {want} cards have their picture', sum(1 for k,v in r if v)==want and all(v!=False for k,v in r), r)
        pg.screenshot(path=f'{S}/decimg_ch{n}.png'); ev("closeAll()")
    ok('Z no page errors', not errs, errs[:3])
    b.close()
