# 五位後期乘客
from playwright.sync_api import sync_playwright
import json
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad'
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
BASE=open(S+'/tchap.py').read().split('BASE="')[1].split('"\n')[0]
IDS=['voidroot','husk','jadewing','witherwalk','silvereye']
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:(errs.append(str(e)),print('STACK',e.stack[:700],flush=True)))
    pg.add_init_script("window.CHAP_TEST=true; window.ARC_TEST=true")
    pg.goto('http://127.0.0.1:8766/'); W(1000)
    T=['KEEPS','HOME_C','REQ','LEAVE_AT','OMEN','TRACE','SIGN','PERS','CARE','DECK_LINE','COMP_LINE','PREF','LOVE_LINE','HOME_NAME','MSG_SIG','GIFT2','GIFT3','CR_ABIL','CR_SOL','NOTES','REQ_SEED','ARC']
    miss=ev(f"(()=>{{const T={json.dumps(T)},I={json.dumps(IDS)},o=[];T.forEach(t=>{{const X=eval(t);I.forEach(i=>{{if(!X[i]) o.push(t+':'+i);}});}});I.forEach(i=>{{if(!PASSENGERS[i]) o.push('P:'+i); if(!VOICE.P[i]) o.push('VOICE:'+i); if(!skillOf(i)) o.push('skill:'+i); if(!COLLECTIBLES['keep_'+i]) o.push('keep:'+i); if(!MEMORIES.find(m=>m.id===i)) o.push('mem:'+i); if(!CODEX_LIFE.find(m=>m.id===i)) o.push('codex:'+i); if(!EVENTS['board_'+i]) o.push('ev:'+i); if(!HSDEF.find(h=>h.id==='hab-p-'+i)) o.push('hs:'+i);}});return o;}})()")
    ok('A1 every table has all five', not miss, miss)
    bad=ev(f"(()=>{{const o=[];{json.dumps(IDS)}.forEach(i=>{{const txt=PASSENGERS[i].talks.map(t=>t.lines.join('|')).join('|');NOTES[i].list.forEach(n=>{{if(!txt.includes(n.p)) o.push(i+':'+n.p);}});}});return o;}})()")
    ok('A2 every note phrase is actually said in a talk', not bad, bad)
    ok('A3 pictures load', ev("Promise.all("+json.dumps(IDS)+".flatMap(i=>[PASSENGERS[i].image,PASSENGERS[i].still,...PASSENGERS[i].studies]).map(s=>new Promise(r=>{const im=new Image();im.onload=()=>r(im.naturalWidth>0);im.onerror=()=>r(false);im.src=s;}))).then(a=>a.every(Boolean))"))
    # 不會提早出現
    ev(BASE+"chapS();state.chap.ended=[1,2];state.currentLocation='starIslands';state.journeyCount=8;save()")
    early=[]
    for _ in range(40): early+=ev("rollBoarders()")
    ok('B1 not in the random boarders early on', not any(x.replace('board_','') in IDS for x in early), set(early))
    ev("state.chap.ended=[1,2,3];state.currentLocation='reverseRealm';state.journeyCount=12;state.boardQ=[];save()"); got=set()
    for _ in range(6): got|=set(ev("rollBoarders()"))
    ok('B2 after chapter 3, at 逆生之境: 翠翅逆蜓 comes', 'board_jadewing' in got, got)
    ev("state.currentLocation='silentVoid';save()"); got=set()
    for _ in range(6): got|=set(ev("rollBoarders()"))
    ok('B3 寂滅虛空 before chapters 4-5: nobody new yet', not ({'board_voidroot','board_witherwalk'}&got), got)
    ev("state.chap.ended=[1,2,3,4,5];save()"); got=set()
    for _ in range(6): got|=set(ev("rollBoarders()"))
    ok('B4 寂滅虛空 after chapter 5: 寂絡垂靈 and 枯枝踽行者', {'board_voidroot','board_witherwalk'}<=got, got)
    ev("state.currentLocation='timeriftSea';save()"); got=set()
    for _ in range(6): got|=set(ev("rollBoarders()"))
    ok('B5 時隙之海 after chapter 5: 殼瞳守夜者 and 銀瞳長肢獸', {'board_husk','board_silvereye'}<=got, got)
    # 上車、說話、故事
    for i in IDS:
        ev(f"closeAll();EVENTS['board_{i}'].run(()=>{{}})"); W(400)
        for _ in range(30):
            if ev("!!document.querySelector('#layer .cine')"): ev("document.querySelector('#layer .cine').click()"); W(150)
            elif ev("!!document.querySelector('#layer .ov.board #hi')"): ev("document.querySelector('#layer .ov.board #hi').click()"); W(300)
            elif ev("!!document.querySelector('#layer .dlg')"): ev("document.querySelector('#layer .dlg .box').click()"); W(80); ev("document.querySelector('#layer .dlg .box')?.click()"); W(120)
            else: break
        ok(f'C1 {i} boards', ev(f"aboard('{i}')&&state.discoveredLifeforms.includes('{i}')"), ev(f"state.passengers['{i}']"))
    ev("closeAll();state.currentPhase='docked';state.currentCarriage='habitat';state.hview=0;render()"); W(800)
    shown=ev("[...document.querySelectorAll('#scene [data-hs^=\"hab-p-\"]')].map(e=>e.dataset.hs)")
    ok('C2 they appear in 棲息車廂', all('hab-p-'+i in shown for i in IDS), shown)
    pg.screenshot(path=S+'/late2_hab.png')
    ev("closeAll();state.passengers.jadewing.boardedJourney=state.journeyCount-1;"); 
    ok('C3 story beat is waiting (ARC)', ev("arcWait('jadewing')"))
    ev("talk('jadewing')"); W(400); txt=''
    for _ in range(30):
        if ev("!!document.querySelector('#layer .dlg')"): txt+=ev("document.querySelector('#layer .dlg').innerText")+'|'; ev("document.querySelector('#layer .dlg .box').click()"); W(80); ev("document.querySelector('#layer .dlg .box')?.click()"); W(120)
        else: break
    ok('C4 first beat plays', '撞到' in txt and ev("arcAt('jadewing')")==1, txt[:120])
    ev("closeAll();state.passengers.cinder={stage:2,talks:3,records:[],aboard:true,left:false,boardedJourney:1,zone:'crystal'};state.discoveredLifeforms.push('cinder');openBook&&0"); 
    ok('P1 燼風帆獸 has the new pose', ev("PASSENGERS.cinder.extra[0]").endswith('cinder-pose2.webp') and ev("bookLifeDetail('cinder').includes('cinder-pose2.webp')"))
    ok('Z no page errors', not errs, errs[:3])
    b.close()
