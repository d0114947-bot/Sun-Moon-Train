# 三位新的一次性隱藏訪客（影片）
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad'
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
BASE=open(S+'/tchap.py').read().split('BASE="')[1].split('"\n')[0]
V={'thorneye':('boundlessCorridor','memory',0,'荊枝'),'wheeleye':('timeriftSea','observatory',0,'光點'),'shardwing':('reverseRealm','nature',0,'羽毛')}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(1000)
    for vid,(loc,car,view,end) in V.items():
        ev(BASE+f"state.currentPhase='voyage';state.voyage={{from:'dawnForest',to:'starIslands',progress:.3}};state.currentCarriage='{car}';state.mview=0;state.nview=0;state.visitors={{flicker:{{n:1,lastJ:0}},voidshape:{{n:1,lastJ:0}},elder:{{n:1,lastJ:0}}}};save();PANO.active=null;RUNNING=true;render()"); W(400)
        ok(f'{vid} V0 not before {loc}', ev(f"(visitorRoll(),!(state.visitorNow&&state.visitorNow.id==='{vid}'))"))
        ev(f"state.visitorNow=null;state.visitedLocations.push('{loc}');visitorRoll();render()"); W(600)
        ok(f'{vid} V1 comes after {loc}', ev("state.visitorNow&&state.visitorNow.id")==vid, ev("state.visitorNow"))
        ok(f'{vid} V2 shows up in {car}', ev(f"!!document.querySelector('#scene [data-hs=\"vis-{vid}\"]')"))
        ev("closeAll();visitorMeet()"); W(1200)
        ok(f'{vid} V3 video plays', ev(f"(()=>{{const v=document.querySelector('.xevvid.visvid video');return !!v&&v.src.includes('vis-{vid}')}})()"))
        pg.screenshot(path=f'{S}/vis_{vid}.png'); txt=''
        for _ in range(40):
            if ev("!!document.querySelector('#layer .dlg')"): txt+=ev("document.querySelector('#layer .dlg').innerText")+'|'; ev("document.querySelector('#layer .dlg .box').click()"); W(80); ev("document.querySelector('#layer .dlg .box')?.click()"); W(200)
            else: break
        W(1500)
        ok(f'{vid} V4 story, video fades', end in txt and not ev("!!document.querySelector('.xevvid.visvid')"), txt[-100:])
        ok(f'{vid} V5 only once', ev(f"state.visitors.{vid}&&state.visitors.{vid}.n")==1 and ev(f"(state.visitorNow=null,state.journeyCount+=5,visitorRoll(),!(state.visitorNow&&state.visitorNow.id==='{vid}'))"))
    ok('Z no page errors', not errs, errs[:3])
    b.close()
