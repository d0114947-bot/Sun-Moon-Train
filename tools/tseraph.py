# 一次性的隱藏訪客：晶冠的守望者（影片）
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad'
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
BASE=open(S+'/tchap.py').read().split('BASE="')[1].split('"\n')[0]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(1000)
    ev(BASE+"state.currentPhase='voyage';state.voyage={from:'starIslands',to:'timeriftSea',progress:.3};state.currentCarriage='observation';state.oview=1;save();PANO.active=null;RUNNING=true;render()"); W(500)
    ok('V0 not before 寂滅虛空', ev("(visitorRoll(),!(state.visitorNow&&state.visitorNow.id==='seraph'))"))
    ev("state.visitorNow=null;state.visitors={flicker:{n:1,lastJ:0},voidshape:{n:1,lastJ:0},elder:{n:1,lastJ:0}};state.visitedLocations.push('silentVoid');visitorRoll();render()"); W(600)
    ok('V1 after 寂滅虛空 it comes (important visitor; after other important ones)', ev("state.visitorNow&&state.visitorNow.id")=='seraph')
    ok('V2 shows up in 觀星車廂', ev("!!document.querySelector('#scene [data-hs=\"vis-seraph\"]')"))
    ev("closeAll();visitorMeet()"); W(1500)
    ok('V3 the video plays', ev("(()=>{const v=document.querySelector('.xevvid.visvid video');return !!v&&v.src.includes('vis-seraph')})()"))
    pg.screenshot(path=S+'/seraph.png')
    txt=''
    for _ in range(40):
        if ev("!!document.querySelector('#layer .dlg')"): txt+=ev("document.querySelector('#layer .dlg').innerText")+'|'; ev("document.querySelector('#layer .dlg .box').click()"); W(80); ev("document.querySelector('#layer .dlg .box')?.click()"); W(200)
        else: break
    W(1500)
    ok('V4 story plays and the video fades away after', '白羽' in txt and not ev("!!document.querySelector('.xevvid.visvid')"), txt[-120:])
    ok('V5 recorded once, never again', ev("state.visitors.seraph&&state.visitors.seraph.n")==1 and ev("(state.visitorNow=null,state.journeyCount+=5,visitorRoll(),!(state.visitorNow&&state.visitorNow.id==='seraph'))"))
    ok('Z no page errors', not errs, errs[:3])
    b.close()
