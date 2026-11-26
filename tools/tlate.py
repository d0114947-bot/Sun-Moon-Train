# 五位後期乘客
from playwright.sync_api import sync_playwright
import json
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad'
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
BASE=open(S+'/tchap.py').read().split('BASE="')[1].split('"\n')[0]
IDS=['porcel','tidemane','pulsewyrm','rivertrunk','bloomeel']
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
    # 章節模式：第 3 章結束後，到逆生之境
    ev("state.chap.ended=[1,2,3];state.currentLocation='reverseRealm';state.journeyCount=12;state.boardQ=[];save()")
    got=set()
    for _ in range(5): got|=set(ev("rollBoarders()"))
    ok('B2 after chapter 3, at 逆生之境: 溯泉長吻獸 and 逆綻花鰻 come', {'board_rivertrunk','board_bloomeel'}<=got and not ({'board_porcel','board_tidemane','board_pulsewyrm'}&got), got)
    ev("state.currentLocation='boundlessCorridor';save()"); got=set()
    for _ in range(5): got|=set(ev("rollBoarders()"))
    ok('B3 at 無界迴廊: 瓷甲踱廊獸 and 脈光遊脊', {'board_porcel','board_pulsewyrm'}<=got and 'board_tidemane' not in got, got)
    ev("state.currentLocation='timeriftSea';save()"); got=set()
    for _ in range(5): got|=set(ev("rollBoarders()"))
    ok('B4 時隙之海 before chapters 4 and 5 are done: 霧鬃潮靈 not yet', 'board_tidemane' not in got, got)
    ev("state.chap.ended=[1,2,3,4,5];save()"); got=set()
    for _ in range(5): got|=set(ev("rollBoarders()"))
    ok('B5 時隙之海 after chapters 4 and 5: 霧鬃潮靈 comes', 'board_tidemane' in got, got)
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
    pg.screenshot(path=S+'/late_hab.png')
    ev("closeAll();state.passengers.rivertrunk.boardedJourney=state.journeyCount-1;"); 
    ok('C3 story beat is waiting (ARC)', ev("arcWait('rivertrunk')"))
    ev("talk('rivertrunk')"); W(400); txt=''
    for _ in range(30):
        if ev("!!document.querySelector('#layer .dlg')"): txt+=ev("document.querySelector('#layer .dlg').innerText")+'|'; ev("document.querySelector('#layer .dlg .box').click()"); W(80); ev("document.querySelector('#layer .dlg .box')?.click()"); W(120)
        else: break
    ok('C4 first beat plays', '嗆到一次' in txt and ev("arcAt('rivertrunk')")==1, txt[:120])
    ok('Z no page errors', not errs, errs[:3])
    b.close()
